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
    if v is None or isinstance(v, int):
        return v
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        errs.append(f"{where}: year {v!r} is not an integer")
        return None


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

    # papers: required cite_key, no duplicates, coerced year
    seen: dict[str, int] = {}
    papers = []
    for i, p in enumerate(d.get("papers") or []):
        ck = p.get("cite_key")
        if not ck:
            errs.append(f"papers[{i}]: missing cite_key"); continue
        if ck in seen:
            errs.append(f"duplicate cite_key {ck!r} (papers[{seen[ck]}] and papers[{i}])"); continue
        seen[ck] = i
        papers.append(Paper(
            cite_key=ck, title=p.get("title", ""), authors=list(p.get("authors") or []),
            year=_coerce_year(p.get("year"), f"papers[{i}] ({ck})", errs), venue=p.get("venue", ""),
            arxiv_id=str(p.get("arxiv_id", "")), arxiv_version=str(p.get("arxiv_version", "")),
            doi=str(p.get("doi", "")), url=p.get("url", ""),
            key_contributions=list(p.get("key_contributions") or []), verified=Verification()))
    keys = set(seen)

    def _ref(k, where):
        if k and k not in keys:
            errs.append(f"{where}: references undefined cite_key {k!r}")

    claims = []
    for i, c in enumerate(d.get("claims") or []):
        for fld in ("id", "statement", "paper"):
            if not c.get(fld):
                errs.append(f"claims[{i}]: missing {fld}")
        _ref(c.get("paper"), f"claims[{i}] ({c.get('id', '?')})")
        if c.get("claim_type") and c["claim_type"] not in CLAIM_TYPES:
            errs.append(f"claims[{i}]: claim_type {c['claim_type']!r} not in {CLAIM_TYPES}")
        if c.get("confidence") and c["confidence"] not in CONFIDENCE:
            errs.append(f"claims[{i}]: confidence {c['confidence']!r} not in {CONFIDENCE}")
        for k in (c.get("corroborated_by") or []):
            _ref(k, f"claims[{i}] corroborated_by")
        claims.append(Claim(id=c.get("id", ""), statement=c.get("statement", ""), paper=c.get("paper", ""),
                            supporting_passage=c.get("supporting_passage", ""),
                            claim_type=c.get("claim_type", "finding"), confidence=c.get("confidence", "medium"),
                            corroborated_by=list(c.get("corroborated_by") or [])))

    problems = []
    for i, o in enumerate(d.get("open_problems") or []):
        if not o.get("id") or not o.get("statement"):
            errs.append(f"open_problems[{i}]: missing id/statement")
        if not (o.get("flagged_by") or []):
            errs.append(f"open_problems[{i}] ({o.get('id', '?')}): flagged_by is empty")
        for k in (o.get("flagged_by") or []):
            _ref(k, f"open_problems[{i}]")
        if o.get("status") and o["status"] not in PROBLEM_STATUS:
            errs.append(f"open_problems[{i}]: status {o['status']!r} not in {PROBLEM_STATUS}")
        problems.append(OpenProblem(id=o.get("id", ""), statement=o.get("statement", ""),
                                    flagged_by=list(o.get("flagged_by") or []),
                                    status=o.get("status", "open"), why_it_matters=o.get("why_it_matters", "")))

    debates = []
    for i, db in enumerate(d.get("debates") or []):
        positions = []
        for j, p in enumerate(db.get("positions") or []):
            for k in (p.get("papers") or []):
                _ref(k, f"debates[{i}].positions[{j}]")
            positions.append(Position(stance=p.get("stance", ""), papers=list(p.get("papers") or []),
                                      summary=p.get("summary", "")))
        debates.append(Debate(id=db.get("id", ""), question=db.get("question", ""),
                              positions=positions, resolved=bool(db.get("resolved", False))))

    benchmarks = []
    for i, b in enumerate(d.get("benchmarks") or []):
        if not b.get("id") or not b.get("name"):
            errs.append(f"benchmarks[{i}]: missing id/name")
        _ref(b.get("paper"), f"benchmarks[{i}]")
        benchmarks.append(Benchmark(id=b.get("id", ""), name=b.get("name", ""), dataset=b.get("dataset", ""),
                                    metric=b.get("metric", ""), value=str(b.get("value", "")),
                                    method=b.get("method", ""), paper=b.get("paper", "")))

    if errs:
        raise ResearchInputError("invalid research input:\n  - " + "\n  - ".join(errs))

    return Package(topic=d["topic"], scope=d.get("scope", ""), papers=papers, claims=claims,
                   open_problems=problems, debates=debates, benchmarks=benchmarks,
                   coverage=dict(d.get("coverage") or {}))


def _cmd_build(args) -> int:
    pkg = _load(args.input)
    today = args.built or datetime.date.today().isoformat()
    if args.no_verify:
        for p in pkg.papers:
            p.verified = Verification(exists=True, status="verified", via="(unchecked)", checked=today)
        summary = {"total": len(pkg.papers), "verified": len(pkg.papers),
                   "rejected": [], "unconfirmed": [], "errored": []}
    else:
        print(f"verifying {len(pkg.papers)} citations against arXiv/Crossref ...", file=sys.stderr)
        summary = verify_all(pkg.papers, today=today)

    out = assemble(pkg, args.out, built=today)
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
    val = sub.add_parser("validate", help="lint an assembled package")
    val.add_argument("package_dir")
    val.set_defaults(func=_cmd_validate)
    args = ap.parse_args(argv)
    try:
        return args.func(args)
    except ResearchInputError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
