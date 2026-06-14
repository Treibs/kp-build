"""Assemble a Package into a portable wikillm directory + index + manifest."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .schema import (
    Package, SCHEMA_VERSION,
    paper_to_md, claim_to_md, problem_to_md, debate_to_md,
)
from .digest import build_context


def assemble(pkg: Package, out_dir: str | Path, *, built: str, falsification: dict | None = None) -> Path:
    """Write *pkg* to *out_dir* as a wikillm package. Returns the path.

    Only claims/problems/debates that resolve to a VERIFIED paper are written — the citation
    spine is the gate, enforced here at write time and re-checked by validate().
    """
    out = Path(out_dir)
    for sub in ("papers", "claims", "open-problems", "debates"):
        (out / sub).mkdir(parents=True, exist_ok=True)

    verified = {p.cite_key for p in pkg.papers if p.verified.exists}

    for p in pkg.papers:
        (out / "papers" / f"{p.cite_key}.md").write_text(paper_to_md(p), encoding="utf-8")
    claims = [c for c in pkg.claims if c.paper in verified]
    for c in claims:
        (out / "claims" / f"{c.id}.md").write_text(claim_to_md(c), encoding="utf-8")
    problems = [op for op in pkg.open_problems if any(k in verified for k in op.flagged_by)]
    for op in problems:
        (out / "open-problems" / f"{op.id}.md").write_text(problem_to_md(op), encoding="utf-8")
    debates = [d for d in pkg.debates if any(k in verified for pos in d.positions for k in pos.papers)]
    for d in debates:
        (out / "debates" / f"{d.id}.md").write_text(debate_to_md(d), encoding="utf-8")

    # machine-readable graph
    index = {
        "schema": SCHEMA_VERSION,
        "papers": [{"cite_key": p.cite_key, "title": p.title, "year": p.year,
                    "arxiv_id": p.arxiv_id, "doi": p.doi, "verified": p.verified.exists} for p in pkg.papers],
        "claims": [{"id": c.id, "paper": c.paper, "type": c.claim_type, "confidence": c.confidence} for c in claims],
        "open_problems": [{"id": op.id, "flagged_by": op.flagged_by, "status": op.status} for op in problems],
        "debates": [{"id": d.id, "positions": [pos.stance for pos in d.positions]} for d in debates],
    }
    (out / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "schema": SCHEMA_VERSION,
        "topic": pkg.topic,
        "scope": pkg.scope,
        "built": built,
        "stats": {"papers_verified": len(verified), "papers_total": len(pkg.papers),
                  "claims": len(claims), "open_problems": len(problems), "debates": len(debates)},
        "falsification": falsification or {"run": False},
    }
    (out / "wikillm.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    (out / "CONTEXT.md").write_text(build_context(pkg, built=built), encoding="utf-8")
    (out / "README.md").write_text(_readme(pkg, manifest), encoding="utf-8")
    return out


def _readme(pkg: Package, manifest: dict) -> str:
    s = manifest["stats"]
    return (f"# {pkg.topic}\n\n*wikillm knowledge package — a research-landscape foundation.*\n\n"
            f"**Scope:** {pkg.scope}\n\n"
            f"- {s['papers_verified']}/{s['papers_total']} citations verified (arXiv/Crossref)\n"
            f"- {s['claims']} grounded claims · {s['open_problems']} open problems · {s['debates']} debates\n\n"
            f"**Load `CONTEXT.md` into your agent** to inherit this field without re-running the research. "
            f"`index.json` is the machine-readable graph; `papers/`, `claims/`, `open-problems/`, `debates/` "
            f"hold the individual notes.\n\n"
            f"Confidence is corpus-relative (conditional on the cited sources). Built {manifest['built']}.\n")
