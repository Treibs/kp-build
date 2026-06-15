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
import re
import sys
from pathlib import Path

from .schema import (Package, Paper, Claim, OpenProblem, Debate, Position, Benchmark, Verification,
                     CLAIM_TYPES, CONFIDENCE, PROBLEM_STATUS)
from .citations import verify_all
from .assemble import assemble
from .validate import validate


class ResearchInputError(ValueError):
    """Malformed research JSON — reported with all problems aggregated, not a raw traceback."""


def _coerce_year(v, where, errs):
    if v is None:
        return None
    if isinstance(v, bool):                       # bool is an int subclass — reject explicitly (F4)
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
    """A list-of-strings field. A bare string becomes a single element (never iterated char-by-char,
    F2); a non-list/non-string is an error rather than a silent corruption."""
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    if isinstance(v, list):
        return [str(x) for x in v]
    errs.append(f"{where}: expected a list, got {type(v).__name__}")
    return []


def _section(d, key, errs):
    """Return d[key] as a list of dict elements; aggregate type errors instead of crashing (F1)."""
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
        for fld in ("id", "statement", "paper"):
            if not c.get(fld):
                errs.append(f"claims[{i}]: missing {fld}")
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
                            corroborated_by=corr, survived_refuter=bool(c.get("survived_refuter", True))))

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

    if errs:
        raise ResearchInputError("invalid research input:\n  - " + "\n  - ".join(errs))

    return Package(topic=d["topic"], scope=str(d.get("scope", "")), papers=papers, claims=claims,
                   open_problems=problems, debates=debates, benchmarks=benchmarks,
                   coverage=cov)


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
        summary = {"total": len(pkg.papers), "verified": len(pkg.papers),
                   "rejected": [], "unconfirmed": [], "errored": []}
    else:
        print(f"verifying {len(pkg.papers)} citations against arXiv/Crossref "
              f"(throttle {args.throttle}s/paper) ...", file=sys.stderr)
        summary = verify_all(pkg.papers, today=today, throttle=args.throttle)

    out = assemble(pkg, args.out, built=today,
                   name=args.name or None, version=args.version, license=args.license)
    res = validate(out)
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
    from .falsify import score_answer, verdict
    pkg = Path(args.package_dir)
    index = json.loads((pkg / "index.json").read_text())
    spine = [{"arxiv_id": p.get("arxiv_id", ""), "doi": p.get("doi", ""), "cite_key": p["cite_key"]}
             for p in index.get("papers", []) if p.get("verified")]
    base = score_answer(Path(args.base).read_text(), spine=spine)
    kp = score_answer(Path(args.kp).read_text(), spine=spine)
    v = verdict(base, kp)
    print("falsification:")
    print(f"  base : {base}")
    print(f"  kp   : {kp}")
    print(f"  VERDICT: {v}")
    # record into the manifest
    man = json.loads((pkg / "wikillm.json").read_text())
    man["falsification"] = {"run": True, "question": args.question, "base": base, "kp": kp, "verdict": v}
    (pkg / "wikillm.json").write_text(json.dumps(man, indent=2) + "\n", encoding="utf-8")
    helped = (kp.get("f1") is not None and base.get("f1") is not None and kp["f1"] > base["f1"]) or \
             (kp["hallucination_rate"] < base["hallucination_rate"])
    return 0 if helped else 1


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
    b.add_argument("--throttle", type=float, default=0.4, help="seconds between citation checks (avoid rate limits on large packages)")
    b.add_argument("--name", default="", help="kpm package name (default @kp/<topic-slug>); publisher may re-tag")
    b.add_argument("--version", default="0.1.0", help="package semver (default 0.1.0)")
    b.add_argument("--license", default="CC-BY-4.0", help="package license (default CC-BY-4.0)")
    b.set_defaults(func=_cmd_build)
    v = sub.add_parser("verify", help="citation check only")
    v.add_argument("--input", "-i", required=True)
    v.set_defaults(func=_cmd_verify)
    fal = sub.add_parser("falsify", help="score base vs KP-loaded answers; record the verdict in the manifest")
    fal.add_argument("package_dir")
    fal.add_argument("--question", required=True)
    fal.add_argument("--base", required=True, help="file with the base agent's answer")
    fal.add_argument("--kp", required=True, help="file with the KP-loaded agent's answer")
    fal.set_defaults(func=_cmd_falsify)
    exp = sub.add_parser("expand", help="list citation-graph neighbors of a package's verified spine")
    exp.add_argument("package_dir")
    exp.add_argument("--limit", type=int, default=40, help="max neighbors per seed per direction")
    exp.add_argument("--direction", choices=("both", "references", "citations"), default="both")
    exp.set_defaults(func=_cmd_expand)
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
