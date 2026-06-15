"""Validate an assembled wikillm package — the structural + citation-integrity gate."""

from __future__ import annotations

import glob
import re
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
    for required in ("CONTEXT.md", "wikillm.json", "index.json", "README.md", "knowledge.json"):
        if not (d / required).is_file():
            errs.append(f"missing {required}")

    # the 0xLT/kpm distribution contract must be well-formed (else kpm pack/doctor will reject it)
    kj = d / "knowledge.json"
    if kj.is_file():
        errs += _check_knowledge_json(kj)

    return ValidationResult(ok=not errs, errors=errs, warnings=warns)


_NAME_RE = re.compile(r"^(?:@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*$")
_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def _check_knowledge_json(path: Path) -> List[str]:
    """Mirror 0xLT/kpm's manifest rules so a malformed envelope fails here, not only in `kpm pack`."""
    import json
    try:
        m = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        return [f"knowledge.json is not readable JSON: {e}"]
    if not isinstance(m, dict):
        return ["knowledge.json must be a JSON object"]
    out: List[str] = []
    if not _NAME_RE.match(str(m.get("name", ""))):
        out.append("knowledge.json: name must be a lowercase npm-style package name")
    if not _VERSION_RE.match(str(m.get("version", ""))):
        out.append("knowledge.json: version must be an exact semver")
    if m.get("type") != "knowledge-package":
        out.append('knowledge.json: type must be "knowledge-package"')
    files = m.get("files")
    if not isinstance(files, list) or not files:
        out.append("knowledge.json: files must be a non-empty list of globs")
    else:
        for i, entry in enumerate(files):
            if not isinstance(entry, str):
                out.append(f"knowledge.json: files[{i}] must be a string"); continue
            pat = entry[1:] if entry.startswith("!") else entry     # kpm allows a leading '!' exclude
            if pat.startswith("/") or ".." in pat.split("/"):
                out.append(f"knowledge.json: files[{i}] {entry!r} must be a safe relative path")
    ep = m.get("entrypoint", "README.md")
    if not isinstance(ep, str) or not ep.lower().endswith(".md"):
        out.append("knowledge.json: entrypoint must be a markdown file")
    elif not (path.parent / ep).is_file():
        out.append(f"knowledge.json: entrypoint '{ep}' does not exist in the package")
    return out
