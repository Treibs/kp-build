"""kp-build CLI — turn an orchestrator's research JSON into a verified wikillm package.

    kp-build build    --input research.json --out <dir> [--no-verify]
    kp-build verify   --input research.json            # citation check only, report
    kp-build validate <package_dir>                    # lint an assembled package

The research JSON is what the /kp-build skill (Claude + subagents) produces; this engine does the
mechanical, deterministic part: verify every citation, assemble, and lint.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

from .schema import (Package, Paper, Claim, OpenProblem, Debate, Position, Benchmark, Verification,
                     GoalMetric, Relation, goal_metric_from_dict,
                     CLAIM_TYPES, CONFIDENCE, PROBLEM_STATUS, DIRECTIONS, ORACLE_KINDS, RELATION_TYPES)
from .citations import verify_all
from .assemble import assemble
from .validate import validate


class ResearchInputError(ValueError):
    """Malformed research JSON — reported with all problems aggregated, not a raw traceback."""


def _coerce_year(v, where, errs):
    if v is None:
        return None
    if isinstance(v, bool):                       # bool is an int subclass — reject explicitly
        errs.append(f"{where}: year {v!r} is a boolean, not a year")
        return None
    if isinstance(v, int):
        return v
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        errs.append(f"{where}: year {v!r} is not an integer")
        return None


def _strlist(v, where, errs):
    """A list-of-strings field. A bare string becomes a single element (never iterated char-by-char);
    a non-list/non-string is an error rather than a silent corruption."""
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    if isinstance(v, list):
        return [str(x) for x in v]
    errs.append(f"{where}: expected a list, got {type(v).__name__}")
    return []


def _section(d, key, errs):
    """Return d[key] as a list of dict elements; aggregate type errors instead of crashing."""
    raw = d.get(key) or []
    if not isinstance(raw, list):
        errs.append(f"'{key}' must be a list, got {type(raw).__name__}")
        return []
    out = []
    for i, el in enumerate(raw):
        if not isinstance(el, dict):
            errs.append(f"{key}[{i}]: must be an object, got {type(el).__name__}")
        else:
            out.append((i, el))
    return out


def _load(path: str) -> Package:
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ResearchInputError(f"{path}: not valid JSON — {e}") from None
    if not isinstance(d, dict):
        raise ResearchInputError(f"{path}: top level must be a JSON object")

    errs: list[str] = []
    if not d.get("topic"):
        errs.append("missing required 'topic'")

    node_ids: set = set()    # all node ids across kinds must be unique (chunk files share a namespace)

    def _uid(nid, kind, i):
        if not nid:
            return
        # every node id is used verbatim as a filename (claims/<id>.md, relations/<id>.md, ...) —
        # path-validate it like cite_key, or a crafted id writes OUTSIDE --out.
        if nid in (".", "..") or not re.fullmatch(r"[A-Za-z0-9_.-]+", nid):
            errs.append(f"{kind}[{i}]: id {nid!r} has unsafe characters (used as a filename; "
                        f"allowed: letters, digits, '_', '.', '-')")
        if nid in node_ids:
            errs.append(f"{kind}[{i}]: duplicate node id {nid!r}")
        node_ids.add(nid)

    # papers: required hashable cite_key, no duplicates, coerced year
    seen: dict[str, int] = {}
    papers = []
    for i, p in _section(d, "papers", errs):
        ck = p.get("cite_key")
        if not ck:
            errs.append(f"papers[{i}]: missing cite_key"); continue
        if not isinstance(ck, str):
            errs.append(f"papers[{i}]: cite_key must be a string, got {type(ck).__name__}"); continue
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", ck):
            # cite_key is used verbatim as a filename and a [[papers/<key>]] wikilink target — keep the
            # mapping bijective and path-safe (a slash would escape the papers/ dir and abort the build)
            errs.append(f"papers[{i}]: cite_key {ck!r} has unsafe characters (allowed: letters, digits, '_', '.', '-')"); continue
        if ck in seen:
            errs.append(f"duplicate cite_key {ck!r} (papers[{seen[ck]}] and papers[{i}])"); continue
        seen[ck] = i
        papers.append(Paper(
            cite_key=ck, title=str(p.get("title", "")), authors=_strlist(p.get("authors"), f"papers[{i}].authors", errs),
            year=_coerce_year(p.get("year"), f"papers[{i}] ({ck})", errs), venue=str(p.get("venue", "")),
            arxiv_id=str(p.get("arxiv_id", "")), arxiv_version=str(p.get("arxiv_version", "")),
            doi=str(p.get("doi", "")), url=str(p.get("url", "")),
            key_contributions=_strlist(p.get("key_contributions"), f"papers[{i}].key_contributions", errs),
            verified=Verification()))
    keys = set(seen)

    def _ref(k, where):
        if k and k not in keys:
            errs.append(f"{where}: references undefined cite_key {k!r}")

    claims = []
    for i, c in _section(d, "claims", errs):
        _uid(c.get("id"), "claims", i)
        for fld in ("id", "statement"):
            if not c.get(fld):
                errs.append(f"claims[{i}]: missing {fld}")
        exec_d = c.get("execution") or {}
        if exec_d and not exec_d.get("aesthetic"):   # V2-a execution directive (instead of a citation paper)
            if exec_d.get("tool") not in ("lint", "inspect", "validate"):
                errs.append(f"claims[{i}].execution: tool must be lint|inspect|validate")
            if not exec_d.get("gate_code"):
                errs.append(f"claims[{i}].execution: needs a gate_code (or aesthetic:true)")
            art = exec_d.get("artifact", "")
            if not art:
                errs.append(f"claims[{i}].execution: needs an artifact")
            elif art.startswith(("/", "\\")) or "://" in art or ".." in re.split(r"[\\/]", art):
                # the artifact is handed to a subprocess that reads files — must be a relative path
                # inside the pack; reject absolute paths, '..' traversal, and URL schemes.
                errs.append(f"claims[{i}].execution.artifact {art!r} must be a relative path inside the "
                            f"pack (no absolute path, '..', or URL)")
        grnd = c.get("grounding") or {}              # V2-a grounding directive (instead of a citation paper)
        if grnd:
            src = grnd.get("source", "")
            if not src:
                errs.append(f"claims[{i}].grounding: needs a 'source' (the pinned source the passage is quoted from)")
            elif src in (".", "..") or not re.fullmatch(r"[A-Za-z0-9_.-]+", src):
                # the source keys the corpus file (corpus/<source>.txt) — same filename-safety rule as cite_key
                errs.append(f"claims[{i}].grounding.source {src!r} has unsafe characters "
                            f"(used as a corpus filename; allowed: letters, digits, '_', '.', '-')")
            if not grnd.get("supporting_passage"):
                errs.append(f"claims[{i}].grounding: needs a 'supporting_passage' (the verbatim quote to ground)")
        judg = c.get("judgment") or {}               # V2-b judgment directive (a recorded blind-panel)
        if judg:
            for fld in ("task", "answer", "baseline"):
                if not judg.get(fld):
                    errs.append(f"claims[{i}].judgment: needs a non-empty '{fld}'")
            rounds = judg.get("rounds")
            if not isinstance(rounds, list) or not rounds:
                errs.append(f"claims[{i}].judgment: needs 'rounds' — the recorded blind-panel slot winners "
                            f"(a non-empty list of 'a'/'b'/'tie')")
            elif any(r not in ("a", "b", "tie") for r in rounds):
                errs.append(f"claims[{i}].judgment.rounds: each entry must be 'a', 'b', or 'tie'")
            elif len(rounds) < 2 or len(rounds) % 2 != 0:
                # the anti-position-bias guarantee REQUIRES an EVEN panel (>=2) so the answer sits in slot a
                # and slot b equally; an odd / length-1 panel lets a one-sided vote launder into a verdict.
                errs.append(f"claims[{i}].judgment.rounds must be an EVEN number of comparisons (>=2) — the "
                            f"answer must occupy slot a and slot b equally for position-bias cancellation")
        oracles = [bool(c.get("paper")), bool(exec_d), bool(grnd), bool(judg)]   # paper XOR exec XOR ground XOR judge
        if not any(oracles):
            errs.append(f"claims[{i}] ({c.get('id', '?')}): needs a 'paper', an 'execution', a 'grounding', "
                        f"or a 'judgment' directive")
        elif sum(oracles) > 1:                       # exactly one verification basis per node
            errs.append(f"claims[{i}] ({c.get('id', '?')}): has more than one verification basis "
                        f"(a claim is verified by exactly one of paper / execution / grounding / judgment — a "
                        f"mechanical, grounding, or panel verdict must not be overridable by a citation)")
        if c.get("paper"):
            _ref(c.get("paper"), f"claims[{i}] ({c.get('id', '?')})")
        if c.get("claim_type") and c["claim_type"] not in CLAIM_TYPES:
            errs.append(f"claims[{i}]: claim_type {c['claim_type']!r} not in {CLAIM_TYPES}")
        if c.get("confidence") and c["confidence"] not in CONFIDENCE:
            errs.append(f"claims[{i}]: confidence {c['confidence']!r} not in {CONFIDENCE}")
        corr = _strlist(c.get("corroborated_by"), f"claims[{i}].corroborated_by", errs)
        for k in corr:
            _ref(k, f"claims[{i}] corroborated_by")
        claims.append(Claim(id=str(c.get("id", "")), statement=str(c.get("statement", "")),
                            paper=str(c.get("paper", "")), supporting_passage=str(c.get("supporting_passage", "")),
                            claim_type=c.get("claim_type") or "finding", confidence=c.get("confidence") or "medium",
                            corroborated_by=corr,
                            survived_refuter=c.get("survived_refuter") is not False,  # absent/null -> True
                            execution={k: exec_d[k] for k in ("tool", "gate_code", "artifact", "aesthetic")
                                       if k in exec_d},
                            grounding={k: grnd[k] for k in ("source", "supporting_passage")
                                       if k in grnd},
                            judgment={k: judg[k] for k in ("task", "answer", "baseline", "rounds")
                                      if k in judg}))

    problems = []
    for i, o in _section(d, "open_problems", errs):
        _uid(o.get("id"), "open_problems", i)
        if not o.get("id") or not o.get("statement"):
            errs.append(f"open_problems[{i}]: missing id/statement")
        flags = _strlist(o.get("flagged_by"), f"open_problems[{i}].flagged_by", errs)
        if not flags:
            errs.append(f"open_problems[{i}] ({o.get('id', '?')}): flagged_by is empty")
        for k in flags:
            _ref(k, f"open_problems[{i}]")
        if o.get("status") and o["status"] not in PROBLEM_STATUS:
            errs.append(f"open_problems[{i}]: status {o['status']!r} not in {PROBLEM_STATUS}")
        problems.append(OpenProblem(id=str(o.get("id", "")), statement=str(o.get("statement", "")),
                                    flagged_by=flags, status=o.get("status") or "open",
                                    why_it_matters=str(o.get("why_it_matters", ""))))

    debates = []
    for i, db in _section(d, "debates", errs):
        _uid(db.get("id"), "debates", i)
        positions = []
        for j, p in _section(db, "positions", errs):
            papers_k = _strlist(p.get("papers"), f"debates[{i}].positions[{j}].papers", errs)
            for k in papers_k:
                _ref(k, f"debates[{i}].positions[{j}]")
            positions.append(Position(stance=str(p.get("stance", "")), papers=papers_k,
                                      summary=str(p.get("summary", ""))))
        debates.append(Debate(id=str(db.get("id", "")), question=str(db.get("question", "")),
                              positions=positions, resolved=bool(db.get("resolved", False))))

    benchmarks = []
    for i, b in _section(d, "benchmarks", errs):
        _uid(b.get("id"), "benchmarks", i)
        if not b.get("id") or not b.get("name"):
            errs.append(f"benchmarks[{i}]: missing id/name")
        _ref(b.get("paper"), f"benchmarks[{i}]")
        benchmarks.append(Benchmark(id=str(b.get("id", "")), name=str(b.get("name", "")),
                                    dataset=str(b.get("dataset", "")), metric=str(b.get("metric", "")),
                                    value=str(b.get("value", "")), method=str(b.get("method", "")),
                                    paper=str(b.get("paper", ""))))

    cov = d.get("coverage") or {}
    if not isinstance(cov, dict):
        errs.append(f"'coverage' must be an object, got {type(cov).__name__}"); cov = {}

    # ── V2-a KP-model spine (all optional — academic packs omit these and stay valid) ──
    goals = d.get("goals") or {}
    if not isinstance(goals, dict):
        errs.append(f"'goals' must be an object, got {type(goals).__name__}"); goals = {}

    goal_metrics = []
    for i, gm in _section(d, "goal_metrics", errs):
        if not gm.get("name"):
            errs.append(f"goal_metrics[{i}]: missing name")
        if gm.get("direction") and gm["direction"] not in DIRECTIONS:
            errs.append(f"goal_metrics[{i}]: direction {gm['direction']!r} not in {DIRECTIONS}")
        if gm.get("oracle_kind") and gm["oracle_kind"] not in ORACLE_KINDS:
            errs.append(f"goal_metrics[{i}]: oracle_kind {gm['oracle_kind']!r} not in {ORACLE_KINDS}")
        goal_metrics.append(goal_metric_from_dict(gm))
    metric_names = {gm.name for gm in goal_metrics if gm.name}

    all_nodes = node_ids | keys          # any node (claim/problem/debate/benchmark id or cite_key)
    relations = []
    for i, r in _section(d, "relations", errs):
        _uid(r.get("id"), "relations", i)
        for fld in ("id", "source", "target"):
            if not r.get(fld):
                errs.append(f"relations[{i}]: missing {fld}")
        for end in ("source", "target"):
            ev = r.get(end)
            if ev and ev not in all_nodes:
                errs.append(f"relations[{i}] ({r.get('id', '?')}): {end} {ev!r} resolves to no node")
        if r.get("type") and r["type"] not in RELATION_TYPES:
            errs.append(f"relations[{i}]: type {r['type']!r} not in {RELATION_TYPES}")
        kpis = _strlist(r.get("kpis"), f"relations[{i}].kpis", errs)
        if len(kpis) < 2:
            errs.append(f"relations[{i}] ({r.get('id', '?')}): a connection must span ≥2 KPIs, got {len(kpis)}")
        if metric_names:        # if KPIs are formally declared, edges must reference them
            for k in kpis:
                if k not in metric_names:
                    errs.append(f"relations[{i}]: kpi {k!r} is not a declared goal_metric")
        relations.append(Relation(
            id=str(r.get("id", "")), source=str(r.get("source", "")), target=str(r.get("target", "")),
            type=r.get("type") or "related", description=str(r.get("description", "")),
            confidence=r.get("confidence") or "medium", kpis=kpis, verification=Verification()))

    if errs:
        raise ResearchInputError("invalid research input:\n  - " + "\n  - ".join(errs))

    return Package(topic=d["topic"], scope=str(d.get("scope", "")), papers=papers, claims=claims,
                   open_problems=problems, debates=debates, benchmarks=benchmarks,
                   coverage=cov, goals=goals, goal_metrics=goal_metrics, relations=relations)


def _cmd_build(args) -> int:
    from .validate import _NAME_RE, _VERSION_RE
    if args.name and not _NAME_RE.match(args.name):                 # fail fast, before the slow verify+assemble
        print(f"error: --name {args.name!r} is not a valid kpm package name "
              f"(lowercase, optional @scope/, e.g. @kp/my-topic)", file=sys.stderr)
        return 2
    if not _VERSION_RE.match(args.version):
        print(f"error: --version {args.version!r} is not an exact semver (e.g. 0.1.0)", file=sys.stderr)
        return 2
    pkg = _load(args.input)
    today = args.built or datetime.date.today().isoformat()
    if args.no_verify:
        for p in pkg.papers:
            p.verified = Verification(exists=True, status="verified", via="(unchecked)", checked=today)
        # do NOT trust an inbound claim verdict. Reset citation claims (they ship via their stamped
        # paper); stamp execution/grounding (no-paper) claims as (unchecked) so a claim-spine pack under
        # --no-verify isn't silently EMPTY (and an inbound exists:true can't ship unchecked).
        for c in pkg.claims:
            if c.paper:
                c.verified = Verification()
            else:                                   # ship under --no-verify, but NEVER say 'verified': it
                kind = ("grounding" if c.grounding else "judgment" if c.judgment   # wasn't checked — an
                        else "execution")                                          # honest, kind-aware stamp
                c.verified = Verification(exists=True, status="unverified", kind=kind,
                                          via="(unchecked)", checked=today)
        summary = {"total": len(pkg.papers), "verified": len(pkg.papers),
                   "rejected": [], "unconfirmed": [], "errored": []}
    else:
        reused = 0
        if args.reuse_verification:                 # cheap retry: keep prior verdicts, re-check only the rest
            import glob as _glob
            import yaml
            from .schema import paper_from_md
            cache = {}                              # cite_key -> the whole prior Paper (for the identity check)
            for f in _glob.glob(str(Path(args.out) / "papers" / "*.md")):
                try:
                    old = paper_from_md(Path(f).read_text(encoding="utf-8"))
                except (OSError, ValueError, KeyError, yaml.YAMLError):
                    continue                        # one corrupt file must not abort the whole reuse
                if old.verified.exists and old.verified.via != "(unchecked)":
                    cache[old.cite_key] = old      # only reuse REAL index verdicts, never --no-verify stamps
            for p in pkg.papers:
                old = cache.get(p.cite_key)
                # ONLY reuse when the identity still matches — else the input was edited and the prior
                # verdict is stale; re-check it (a fabricated paper must never inherit exists=True).
                if old and old.arxiv_id == p.arxiv_id and old.doi == p.doi and old.title == p.title:
                    p.verified = old.verified; reused += 1
            if reused:
                print(f"reusing {reused} prior verification(s); re-checking only the {len(pkg.papers) - reused} "
                      f"changed/unverified/errored ...", file=sys.stderr)
            else:
                print(f"--reuse-verification: no reusable prior verified papers in {args.out}/papers/ "
                      f"— running a full verification", file=sys.stderr)
        todo = sum(1 for p in pkg.papers if not p.verified.exists)
        print(f"verifying {todo} citation(s) against arXiv/Crossref (adaptive throttle, base "
              f"{args.throttle}s) ...", file=sys.stderr)
        summary = verify_all(pkg.papers, today=today, throttle=args.throttle,
                             skip_verified=args.reuse_verification)

    if args.ground_fulltext:
        args.ground = True                              # --ground-fulltext implies grounding
    if args.ground and args.no_verify:
        print("warn: --ground skipped because --no-verify was set (grounding needs the network)", file=sys.stderr)
    if args.ground and not args.no_verify:
        from .ground import ground_claims
        src = "ar5iv fulltext" if args.ground_fulltext else "abstracts"
        print(f"grounding {len(pkg.claims)} claim passages against {src} ...", file=sys.stderr)
        g = ground_claims(pkg.papers, pkg.claims, fulltext=args.ground_fulltext, throttle=args.throttle)
        print(f"  grounded {g['grounded']} · unconfirmed {g['unconfirmed']} · ungrounded {g['ungrounded']}",
              file=sys.stderr)

    # running execution gates shells out to the hyperframes CLI on local files — require an explicit
    # --execute opt-in, and never under --no-verify (which stamps execution claims (unchecked) above).
    n_exec = sum(1 for c in pkg.claims if c.execution)
    if n_exec and args.execute and not args.no_verify:
        from .verifier import verify_execution_claims, hyperframes_runner
        base = Path(args.input).resolve().parent
        print(f"executing {n_exec} claim gate(s) via hyperframes (artifacts resolved under {base}) ...",
              file=sys.stderr)
        es = verify_execution_claims(pkg, runner=hyperframes_runner, today=today, base_dir=base)
        print(f"  execution: {es['execution_verified']}/{es['execution_total']} gate(s) verified", file=sys.stderr)
    elif n_exec and not args.no_verify:
        print(f"warn: {n_exec} execution claim(s) present but NOT gated — pass --execute to run them (executes "
              f"the hyperframes CLI on local files). They will be DROPPED as unverified.", file=sys.stderr)

    # V2-a (grounding): ground each grounding-claim passage against its pinned corpus. Unlike execution's warn-and-drop,
    # a grounding-spine claim that isn't gated would ship NEITHER via a paper NOR via a verdict and silently
    # VANISH at the ship gate (and the ships-empty backstop below misses it in a mixed pack) — so refuse to
    # build rather than drop it.
    if args.ground_verify and args.no_verify:
        print("warn: --ground-verify skipped because --no-verify was set (grounding claims stamped unchecked)",
              file=sys.stderr)
    n_ground = sum(1 for c in pkg.claims if c.grounding)
    if n_ground and args.ground_verify and not args.no_verify:
        from .verifier import verify_grounding_claims, load_grounding_corpus
        base = Path(args.input).resolve().parent
        # OFFLINE-ONLY from the CLI (no `get`): --ground-verify reads committed corpus/<source>.txt so the
        # build stays deterministic and never touches the network. A source with no committed file is left
        # ungrounded-unreachable. (The DOI-abstract fallback remains a library option on load_grounding_corpus.)
        corpus = load_grounding_corpus(pkg, base)
        print(f"grounding {n_ground} claim passage(s) against the pinned corpus "
              f"({len(corpus)} source(s) held) ...", file=sys.stderr)
        gs = verify_grounding_claims(pkg, corpus=corpus, today=today)
        print(f"  grounding: {gs['grounding_verified']}/{gs['grounding_total']} passage(s) verified",
              file=sys.stderr)
    elif n_ground and not args.no_verify:
        print(f"error: {n_ground} grounding claim(s) present but NOT gated — pass --ground-verify to check "
              f"them against the pinned corpus (corpus/<source>.txt; offline + deterministic). Refusing to "
              f"build, because an ungated grounding claim ships via neither a paper nor a verdict and would "
              f"silently DROP.", file=sys.stderr)
        return 2

    # V2-b: replay each judgment claim's RECORDED blind-panel through the JudgeVerifier. No flag and no
    # I/O — it's a deterministic re-tally of committed votes (so the build stays byte-identical), and the
    # JudgeVerifier's A/B alternation re-derives the verdict honestly (a faked uniform panel nets to a tie).
    n_judge = sum(1 for c in pkg.claims if c.judgment)
    if n_judge and not args.no_verify:
        from .verifier import verify_judgment_claims
        js = verify_judgment_claims(pkg, today=today)
        print(f"judging {n_judge} recorded panel(s): {js['judgment_verified']}/{js['judgment_total']} "
              f"judged-better (ship)", file=sys.stderr)

    out = assemble(pkg, args.out, built=today,
                   name=args.name or None, version=args.version, license=args.license)
    res = validate(out)
    # a claim-spine package must not silently ship EMPTY (e.g. execution claims dropped for lack of --execute).
    if pkg.claims and json.loads((out / "wikillm.json").read_text())["stats"]["claims"] == 0:
        print("error: every claim was dropped — a claim-spine package would ship EMPTY. "
              "Did the verifier run? (execution claims need --execute; citations need the network).",
              file=sys.stderr)
        return 2
    print("kp-build complete")
    print(f"  topic            : {pkg.topic}")
    print(f"  citations        : {summary['verified']}/{summary['total']} verified")
    if summary.get("rejected"):
        print(f"  REJECTED (not-found / id-title-mismatch — likely fabricated/wrong): {', '.join(summary['rejected'])}")
    if summary.get("unconfirmed"):
        print(f"  unconfirmed (title-only, NOT shippable — add an arXiv id/DOI): {', '.join(summary['unconfirmed'])}")
    if summary.get("errored"):
        print(f"  ERROR reaching index (could not check — retry): {', '.join(summary['errored'])}")
    s = json.loads((out / 'wikillm.json').read_text())["stats"]
    print(f"  shipped          : {s['claims']} claims · {s['open_problems']} open problems · "
          f"{s['debates']} debates · {s['benchmarks']} benchmarks")
    dropped = {k: v for k, v in s["dropped"].items() if v}
    if dropped:
        print(f"  dropped (unverified-anchored): {dropped}")
    print(f"  package          : {out}")
    kj = json.loads((out / "knowledge.json").read_text())
    print(f"  kpm package      : {kj['name']}@{kj['version']}  (publish + `kpm add github:<owner>/<repo>#v{kj['version']}`)")
    print(f"  validation       : {'OK' if res.ok else 'FAILED'}")
    for e in res.errors:
        print(f"      ERROR  - {e}")
    for w in res.warnings:
        print(f"      warn   - {w}")
    return 0 if res.ok else 1


def _cmd_verify(args) -> int:
    pkg = _load(args.input)
    today = datetime.date.today().isoformat()
    summary = verify_all(pkg.papers, today=today)
    print(f"{summary['verified']}/{summary['total']} citations verified  (by status: {summary['by_status']})")
    for p in pkg.papers:
        v = p.verified
        mark = {"verified": "OK   ", "unconfirmed": "WEAK ", "id-title-mismatch": "MISM ",
                "not-found": "FAIL ", "error": "ERR  ", "unverified": "FAIL "}.get(v.status, "FAIL ")
        # show the CANONICAL title the index returned, so a title/canonical divergence is visible
        canon = f"  → index: '{v.canonical_title[:50]}'" if v.canonical_title and v.status != "verified" else ""
        print(f"  [{mark}] {p.cite_key}: {p.title[:55]}  ({v.status}, {v.via}){canon}")
    return 0 if not (summary["rejected"] or summary["errored"]) else 1


def _cmd_falsify(args) -> int:
    """Post-build measurement: does the package actually help? Exit 0 helps / 1 did not help /
    3 INCONCLUSIVE (nothing checkable on one side — mirrors probe/refresh); 2 reserved for usage/IO."""
    from .falsify import score_answer, verdict, helped, judge_prompts, judge_replay
    pkg = Path(args.package_dir)
    if args.emit_judge_prompts is not None:
        if args.emit_judge_prompts < 1:
            # 0/negative must be a usage error, not a silent fall-through into a full
            # (manifest-rewriting) falsify run
            print(f"error: --emit-judge-prompts needs N >= 1 (got {args.emit_judge_prompts}); "
                  f"N is clamped up to an even panel of >= 2", file=sys.stderr)
            return 2
        # emit the blind quality-panel prompts (the non-circular axis) and exit — no scoring, no manifest.
        # Each prompt goes to a FRESH judge; its one-word verdict is a SLOT winner, recorded in order.
        ps = judge_prompts(args.question, Path(args.base).read_text(encoding="utf-8"),
                           Path(args.kp).read_text(encoding="utf-8"), rounds=args.emit_judge_prompts)
        for i, p in enumerate(ps, 1):
            print(f"=== JUDGE PROMPT {i}/{len(ps)} — give to a FRESH judge (no shared context); record "
                  f"its one-word verdict (A/B/TIE) in order ===")
            print(p)
        print(f"\nthen: kp-build falsify {args.package_dir} --question '...' --base {args.base} "
              f"--kp {args.kp} --judge-rounds a,b,tie,...", file=sys.stderr)
        return 0
    judge = None
    if args.judge_rounds:
        # validate + replay the recorded panel BEFORE the two scoring passes — a malformed panel is
        # a usage error and must not cost the (paid, throttled) citation checks. One TRAILING comma
        # is tolerated; an interior empty item is rejected by judge_replay: silently dropping one
        # would shift the parity of every later round and invert the alternation (slot 'a' means
        # the KP answer only on even rounds).
        toks = args.judge_rounds.split(",")
        if len(toks) > 1 and toks[-1].strip() == "":
            toks = toks[:-1]
        judge = judge_replay(toks)
    index = json.loads((pkg / "index.json").read_text())
    spine = [{"arxiv_id": p.get("arxiv_id", ""), "doi": p.get("doi", ""), "cite_key": p["cite_key"]}
             for p in index.get("papers", []) if p.get("verified")]
    base = score_answer(Path(args.base).read_text(), spine=spine, throttle=args.throttle)
    kp = score_answer(Path(args.kp).read_text(), spine=spine, throttle=args.throttle)
    v = verdict(base, kp, judge)
    print("falsification:")
    print(f"  base : {base}")
    print(f"  kp   : {kp}")
    if judge:
        print(f"  judge: {judge}")
    print(f"  VERDICT: {v}")
    if not args.no_record:
        man = json.loads((pkg / "wikillm.json").read_text())
        man["falsification"] = {"run": True, "question": args.question, "base": base, "kp": kp,
                                **({"judge": judge} if judge else {}), "verdict": v}
        # write-then-rename: the manifest holds the package's recorded verdict — a crash mid-write must
        # truncate a temp file, never the record itself.
        tmp = pkg / "wikillm.json.tmp"
        tmp.write_text(json.dumps(man, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, pkg / "wikillm.json")
    h = helped(base, kp, judge)
    # helped() is tri-state; the exit code must carry all three (0/1/3, same map as probe/refresh) —
    # collapsing None into 1 would make "nothing was checkable" indistinguishable from "measured,
    # did not help" to a script
    return 0 if h else (3 if h is None else 1)


def _cmd_probe(args) -> int:
    """Topic-weakness pre-screen: decide whether a package is worth building BEFORE paying for it.
    Two modes: --emit-prompt prints the unaided base-answer task for the topic; --answer scores that
    answer and returns build / skip / inconclusive (exit 0 / 1 / 3; usage/IO errors exit 2)."""
    from .falsify import probe_prompt, probe_verdict, probe_verdict_multi
    if args.emit_prompt:
        print(probe_prompt(args.question or "<the research area>"))
        return 0
    files = args.answer or []
    if not files:
        print("error: --answer FILE required (the unaided agent's answer; repeat for 2-3 independent "
              "samples), or use --emit-prompt to print the prompt to give that agent", file=sys.stderr)
        return 2
    missing = [f for f in files if not Path(f).is_file()]
    if missing:                                         # distinct from an INCONCLUSIVE verdict (exit 3)
        print(f"error: answer file not found: {', '.join(missing)}", file=sys.stderr)
        return 2
    as_of = args.as_of or None        # recency check is OPT-IN (--as-of): a settled topic's old cites are not weakness
    kw = dict(threshold=args.threshold, min_real=args.min_real, throttle=0.2, as_of=as_of)
    texts = [Path(f).read_text(encoding="utf-8") for f in files]
    if len(texts) > 1 and len(set(texts)) < len(texts):
        # the multi-sample screen assumes INDEPENDENT samples — the same file twice adds no
        # information, it just makes the aggregate look better-sampled than it is
        print(f"warn: {len(texts) - len(set(texts))} duplicate --answer file(s) — identical samples "
              f"add no independence to the multi-sample screen", file=sys.stderr)
    if len(texts) == 1:               # single-sample path unchanged (probe_verdict_multi wraps the same rule)
        v = probe_verdict(texts[0], **kw)
    else:
        v = probe_verdict_multi(texts, **kw)
    head = {"build": "BUILD — the topic is model-weak (worth packaging)",
            "skip": "SKIP — the model already knows this (a package adds ~0 value)",
            "inconclusive": "INCONCLUSIVE — re-run"}[v["decision"]]
    print(f"topic pre-screen: {head}")
    for i, s in enumerate(v.get("samples", []), 1):
        print(f"  sample {i}: {s['decision'].upper()} — {s['real']} real · {s['fake']} fabricated/mislabeled "
              f"· {s.get('hedged', 0)} hedged")
    if v["checked"]:
        print(f"  unaided base agent: {v['cited']} cited · {v['real']} real · "
              f"{v['fake']} fabricated/mislabeled · {v.get('hedged', 0)} hedged · "
              f"hallucination {v['hallucination_rate']:.0%}")
    print(f"  -> {v['reason']}")
    return {"build": 0, "skip": 1, "inconclusive": 3}[v["decision"]]    # 2 is reserved for usage/IO errors


def _cmd_expand(args) -> int:
    """Citation-graph expansion: list candidate neighbor papers of a built package's verified spine,
    for the orchestration to relevance-filter, verify, and fold in (deepening coverage past keywords)."""
    import glob
    from .expand import expand, DIRECTIONS
    from .schema import paper_from_md
    d = Path(args.package_dir)
    papers = [paper_from_md(Path(f).read_text(encoding="utf-8")) for f in glob.glob(str(d / "papers" / "*.md"))]
    seeds = [(p.arxiv_id or p.doi) for p in papers if p.verified.exists and (p.arxiv_id or p.doi)]
    existing = [p.arxiv_id for p in papers if p.arxiv_id] + [p.doi for p in papers if p.doi]
    dirs = {"both": DIRECTIONS, "references": ("references",), "citations": ("citations",)}[args.direction]
    if not seeds:
        print("error: no verified papers with an arXiv id / DOI to expand from", file=sys.stderr)
        return 2
    print(f"expanding from {len(seeds)} seed(s) via {args.direction} ...", file=sys.stderr)
    cands = expand(seeds, per_seed=args.limit, directions=dirs, skip=existing)
    print(json.dumps({"seeds": len(seeds), "candidates": cands}, indent=2))
    print(f"  {len(cands)} candidate paper(s) not already in the package "
          f"(relevance-filter + verify before adding)", file=sys.stderr)
    return 0


def _cmd_refresh(args) -> int:
    """Staleness report for a built package. Value concentrates exactly where fields move fastest, so a
    frontier package rots in months — this is the mechanical half of keeping the amortization story true:
    age + post-build citation-graph candidates + the re-probe prompt. Exit 0 fresh / 1 stale / 3
    inconclusive (mirrors probe; 2 stays reserved for usage/IO errors)."""
    from .refresh import refresh
    as_of = args.as_of or datetime.date.today().isoformat()   # the CLI supplies the clock, never the engine
    r = refresh(args.package_dir, as_of=as_of, recency_months=args.recency_months, per_seed=args.limit)
    head = {"stale": "STALE — refresh recommended",
            "fresh": "FRESH — no post-build work found",
            "inconclusive": "INCONCLUSIVE — can't decide from this run (see reason); fix + re-run"}
    print(f"staleness check: {head[r['decision']]}")
    age = f"{r['age_months']} month(s)" if r["age_months"] is not None else "unknown"
    print(f"  built {r['built'] or '?'} · as of {r['as_of']} · age {age} · spine {r['spine_size']} paper(s)")
    print(f"  neighbors: {r['total_candidates']} candidate(s) · {r['new_since_build']} post-build · "
          f"{r['undated_candidates']} undated (reported, not counted as new)")
    for c in r["candidates"][:10]:
        print(f"    + {c.get('arxiv_id') or c.get('doi') or '?'}  {(c.get('title') or '')[:70]}")
    if len(r["candidates"]) > 10:
        print(f"    ... and {len(r['candidates']) - 10} more (--json prints all)")
    print(f"  -> {r['reason']}")
    if args.json:
        print(json.dumps(r, indent=2))
    print("  next: re-probe the topic (the report's 'reprobe_prompt', or `kp-build probe --emit-prompt` "
          "with --as-of), verify + fold the candidates in via the expand path, bump the version.",
          file=sys.stderr)
    return {"fresh": 0, "stale": 1, "inconclusive": 3}[r["decision"]]


def _cmd_report(args) -> int:
    from .report import build_report
    pkg = Path(args.package_dir)
    man = json.loads((pkg / "wikillm.json").read_text(encoding="utf-8"))
    f = man.get("falsification") or {}
    # the report's headline is "does it help?" — refuse to ship one that can't answer it (unless opted out)
    measured = bool(f.get("run")) and (f.get("verdict") or f.get("base") or f.get("kp"))
    if not measured and not args.allow_unmeasured:
        print("error: this package has no falsification result, so the report cannot answer its headline\n"
              "       question (\"does it help?\"). Run the falsification test FIRST, then report:\n"
              "         kp-build falsify <pkg> --question \"<held-out task>\" --base base.txt --kp kp.txt\n"
              "       where base.txt = an unaided agent's answer and kp.txt = a CONTEXT.md-loaded agent's\n"
              "       answer to the same task. (Pass --allow-unmeasured to render a draft anyway.)",
              file=sys.stderr)
        return 2
    out = Path(args.output or (pkg / "report.html"))
    out.write_text(build_report(pkg), encoding="utf-8")
    print(f"wrote {out}  (open in a browser)")
    return 0


def _cmd_validate(args) -> int:
    res = validate(args.package_dir)
    print("OK" if res.ok else "FAILED")
    for e in res.errors:
        print(f"  ERROR  - {e}")
    for w in res.warnings:
        print(f"  warn   - {w}")
    return 0 if res.ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="kp-build", description="Build verified wikillm knowledge packages.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="verify citations, assemble, and validate a package")
    b.add_argument("--input", "-i", required=True)
    b.add_argument("--out", "-o", required=True)
    b.add_argument("--built", default="")
    b.add_argument("--no-verify", action="store_true", help="skip network citation checks (offline/testing)")
    b.add_argument("--throttle", type=float, default=0.4, help="base seconds between citation checks; adapts up on rate limits")
    b.add_argument("--reuse-verification", action="store_true", help="keep prior verdicts in <out> and re-check only the errored/unverified papers (cheap retry)")
    b.add_argument("--ground", action="store_true", help="confirm each claim's passage appears in its paper (abstract-level, free)")
    b.add_argument("--ground-fulltext", action="store_true", help="ground against ar5iv FULLTEXT (slower; enables the 'ungrounded' verdict)")
    b.add_argument("--execute", action="store_true", help="run execution-claim gates via the hyperframes CLI (executes local files / npx; OFF by default — opt-in trust)")
    b.add_argument("--ground-verify", action="store_true", help="hard ship-gate: check each grounding-claim passage against committed corpus/<source>.txt (offline + deterministic; a source with no committed file is ungrounded-unreachable). Distinct from the advisory --ground.")
    b.add_argument("--name", default="", help="kpm package name (default @kp/<topic-slug>); publisher may re-tag")
    b.add_argument("--version", default="0.1.0", help="package semver (default 0.1.0)")
    b.add_argument("--license", default="CC-BY-4.0", help="package license (default CC-BY-4.0)")
    b.set_defaults(func=_cmd_build)
    v = sub.add_parser("verify", help="citation check only")
    v.add_argument("--input", "-i", required=True)
    v.set_defaults(func=_cmd_verify)
    fal = sub.add_parser("falsify", help="score base vs KP-loaded answers; record the verdict in the manifest "
                                         "(exit 0 helps / 1 did not help / 3 inconclusive)")
    fal.add_argument("package_dir")
    fal.add_argument("--question", required=True)
    fal.add_argument("--base", required=True, help="file with the base agent's answer")
    fal.add_argument("--kp", required=True, help="file with the KP-loaded agent's answer")
    fal.add_argument("--throttle", type=float, default=0.2, help="seconds between citation checks (avoid rate limits)")
    fal.add_argument("--emit-judge-prompts", type=int, default=None, metavar="N",
                     help="print N blind quality-panel prompts (KP/base slot-alternated) and exit; give each "
                          "to a FRESH judge, record its A/B/TIE verdicts in order for --judge-rounds")
    fal.add_argument("--judge-rounds", default="",
                     help="recorded blind-panel slot winners, comma-separated (e.g. a,b,tie,a) — the "
                          "non-circular quality axis; even count >=2; judged-worse VETOES a helps verdict")
    fal.add_argument("--no-record", action="store_true",
                     help="score and print only — do not rewrite wikillm.json (e.g. experiments against a "
                          "committed package whose recorded verdict must stay)")
    fal.set_defaults(func=_cmd_falsify)
    prb = sub.add_parser("probe", help="pre-screen a topic: is it model-weak enough to be worth building?")
    prb.add_argument("--answer", action="append", default=[],
                     help="the unaided agent's answer to score; repeat with 2-3 independently sampled answers "
                          "to cut single-sample variance (any weakness-showing sample decides BUILD)")
    prb.add_argument("--question", default="", help="the topic / research area")
    prb.add_argument("--emit-prompt", action="store_true", help="print the base-answer prompt for the topic and exit")
    prb.add_argument("--threshold", type=float, default=0.25, help="hallucination rate at/above which the topic is model-weak (build)")
    prb.add_argument("--min-real", type=int, default=3, dest="min_real", help="fewer real citations than this = too thin (build)")
    prb.add_argument("--as-of", default="", dest="as_of", help="OPT-IN recency check at this YYYY-MM (e.g. today): flag an answer citing only work older than ~30mo as stale on the frontier — for known fast-moving topics")
    prb.set_defaults(func=_cmd_probe)
    exp = sub.add_parser("expand", help="list citation-graph neighbors of a package's verified spine")
    exp.add_argument("package_dir")
    exp.add_argument("--limit", type=int, default=40, help="max neighbors per seed per direction")
    exp.add_argument("--direction", choices=("both", "references", "citations"), default="both")
    exp.set_defaults(func=_cmd_expand)
    rfr = sub.add_parser("refresh", help="staleness report for a built package: age + post-build "
                                         "citation-graph candidates + a re-probe prompt (exit 0 fresh / 1 stale / 3 inconclusive)")
    rfr.add_argument("package_dir")
    rfr.add_argument("--as-of", default="", dest="as_of",
                     help="reference date YYYY-MM[-DD] (default: today) — the staleness clock")
    rfr.add_argument("--recency-months", type=int, default=30, dest="recency_months",
                     help="age beyond which a package is stale on its own (default 30)")
    rfr.add_argument("--limit", type=int, default=40, help="max neighbors per seed per direction")
    rfr.add_argument("--json", action="store_true", help="also print the full machine-readable report")
    rfr.set_defaults(func=_cmd_refresh)
    rep = sub.add_parser("report", help="render a self-contained HTML report (requires a falsification result)")
    rep.add_argument("package_dir")
    rep.add_argument("--output", "-o", default="", help="output .html (default <package_dir>/report.html)")
    rep.add_argument("--allow-unmeasured", action="store_true",
                     help="render even if the package has not been falsified (the 'does it help?' tile will say 'Not measured')")
    rep.set_defaults(func=_cmd_report)
    val = sub.add_parser("validate", help="lint an assembled package")
    val.add_argument("package_dir")
    val.set_defaults(func=_cmd_validate)
    args = ap.parse_args(argv)
    try:
        return args.func(args)
    except (ResearchInputError, OSError) as e:
        # OSError covers FileNotFoundError, NotADirectoryError (e.g. `report <a-file>.json`), PermissionError
        print(f"error: {e}", file=sys.stderr)
        return 2
    except (TypeError, AttributeError, ValueError, KeyError) as e:
        # backstop: malformed input must never surface as a raw traceback / exit 1
        print(f"error: could not process input ({type(e).__name__}: {e})", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
