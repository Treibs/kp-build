"""Validate an assembled wikillm package — the structural + citation-integrity gate."""

from __future__ import annotations

import glob
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from .schema import paper_from_md, claim_from_md, problem_from_md, debate_from_md, benchmark_from_md


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def validate(pkg_dir: str | Path) -> ValidationResult:
    """Lint a package directory.

    Hard errors (ok=False): a claim/problem/debate cites a paper that is missing or unverified;
    a missing CONTEXT.md/manifest. Warnings: orphan papers (cited by nothing), empty
    open-problems register (a likely coverage gap, not a structural failure).
    """
    d = Path(pkg_dir)
    errs: List[str] = []
    warns: List[str] = []

    papers = {p.cite_key: p for f in glob.glob(str(d / "papers" / "*.md")) for p in [paper_from_md(Path(f).read_text())]}
    verified = {k for k, p in papers.items() if p.verified.exists}
    cited: set = set()

    def check(key: str, where: str):
        cited.add(key)
        if key not in papers:
            errs.append(f"{where} cites unknown paper '{key}'")
        elif key not in verified:
            errs.append(f"{where} cites UNVERIFIED paper '{key}' (citation spine breach)")

    for f in glob.glob(str(d / "claims" / "*.md")):
        c = claim_from_md(Path(f).read_text())
        check(c.paper, f"claim {c.id}")
        for k in c.corroborated_by:                  # corroborators count as cited (ASSM-CONSIST-1)
            check(k, f"claim {c.id} corroborated_by")
    for f in glob.glob(str(d / "open-problems" / "*.md")):
        op = problem_from_md(Path(f).read_text())
        if not op.flagged_by:
            errs.append(f"open-problem {op.id} is flagged by no paper")
        for k in op.flagged_by:
            check(k, f"open-problem {op.id}")
    for f in glob.glob(str(d / "debates" / "*.md")):
        db = debate_from_md(Path(f).read_text())
        for pos in db.positions:
            for k in pos.papers:
                check(k, f"debate {db.id} ({pos.stance})")
    for f in glob.glob(str(d / "benchmarks" / "*.md")):
        b = benchmark_from_md(Path(f).read_text())
        check(b.paper, f"benchmark {b.id}")

    for k in papers:
        if k not in cited:
            warns.append(f"paper '{k}' is cited by nothing (orphan)")

    # Surface the citation-spine health: anything not strongly verified is visible, never hidden.
    nonverified = {k: p.verified.status for k, p in papers.items() if not p.verified.exists}
    if nonverified:
        from collections import Counter
        warns.append(f"{len(nonverified)} paper(s) NOT verified (cannot anchor claims): "
                     + ", ".join(f"{k}[{s}]" for k, s in sorted(nonverified.items())))
        if any(s == "error" for s in nonverified.values()):
            warns.append("some papers are status=error (index unreachable) — re-run verification before trusting coverage")
    if papers and not verified:
        errs.append("citation spine has ZERO verified papers — the package proves nothing (re-survey with real arXiv ids/DOIs)")
    if not glob.glob(str(d / "open-problems" / "*.md")):
        warns.append("no open problems — likely a coverage gap (the most valuable section is empty)")
    for required in ("CONTEXT.md", "wikillm.json", "index.json"):
        if not (d / required).is_file():
            errs.append(f"missing {required}")

    return ValidationResult(ok=not errs, errors=errs, warnings=warns)
