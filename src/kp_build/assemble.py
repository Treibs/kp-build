"""Assemble a Package into a portable wikillm directory + index + manifest.

Only nodes anchored to a VERIFIED paper are written, and a kept node's references are PRUNED to
verified cite_keys before serialization — so a package never ships (or validates against) a dangling
or unverified reference. Everything dropped is counted and reported (never silent).
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from .schema import (
    Package, SCHEMA_VERSION, slugify,
    paper_to_md, claim_to_md, problem_to_md, debate_to_md, benchmark_to_md, paper_ref_str,
)
from .digest import build_context


def build_knowledge_json(pkg: Package, *, name: str | None, version: str, license: str) -> dict:
    """The 0xLT/kpm package contract (`knowledge.json`) — the distribution envelope.

    kp-build owns the wikillm *content*; kpm owns *distribution*. Emitting a valid knowledge.json
    makes a wikillm package a first-class kpm package: `kpm add`/`install`/`compose`/`pack` work on
    it directly, so "build once, share" is the existing kpm CLI, not a layer we reinvent. The field
    set is CLOSED by the protocol (name/version/description/license/type/files/entrypoint/
    knowledgeDependencies) — wikillm-specific metadata rides alongside in wikillm.json/index.json,
    which the files glob carries into the package. name/version/license are publisher-overridable.
    """
    return {
        "name": name or f"@kp/{slugify(pkg.topic)}",      # publisher re-tags at publish time
        "version": version,                                # exact semver
        "description": (pkg.scope or pkg.topic)[:300],
        "license": license,
        "type": "knowledge-package",
        "files": ["**/*.md", "wikillm.json", "index.json"],
        "entrypoint": "README.md",
    }


def assemble(pkg: Package, out_dir: str | Path, *, built: str, falsification: dict | None = None,
             name: str | None = None, version: str = "0.1.0", license: str = "CC-BY-4.0") -> Path:
    out = Path(out_dir)
    for sub in ("papers", "claims", "open-problems", "debates", "benchmarks"):
        (out / sub).mkdir(parents=True, exist_ok=True)

    verified = {p.cite_key for p in pkg.papers if p.verified.exists}
    refs = {p.cite_key: paper_ref_str(p) for p in pkg.papers if p.verified.exists}
    drops = {"claims": 0, "open_problems": 0, "debates": 0, "benchmarks": 0, "positions": 0}

    for p in pkg.papers:
        (out / "papers" / f"{p.cite_key}.md").write_text(paper_to_md(p), encoding="utf-8")

    # prune unverified refs into COPIES — never mutate the caller's input dataclasses (ASSM-1)
    claims = []
    for c in pkg.claims:
        if c.paper in verified:
            c2 = replace(c, corroborated_by=[k for k in c.corroborated_by if k in verified])
            (out / "claims" / f"{c2.id}.md").write_text(
                claim_to_md(c2, paper_ref=refs.get(c2.paper, "")), encoding="utf-8")
            claims.append(c2)
        else:
            drops["claims"] += 1

    problems = []
    for op in pkg.open_problems:
        kept_flags = [k for k in op.flagged_by if k in verified]
        if kept_flags:
            op2 = replace(op, flagged_by=kept_flags)
            (out / "open-problems" / f"{op2.id}.md").write_text(
                problem_to_md(op2, refs=refs), encoding="utf-8")
            problems.append(op2)
        else:
            drops["open_problems"] += 1

    debates = []
    for d in pkg.debates:
        kept_pos = [replace(pos, papers=vp) for pos in d.positions
                    if (vp := [k for k in pos.papers if k in verified])]
        drops["positions"] += sum(1 for pos in d.positions if not [k for k in pos.papers if k in verified])
        if kept_pos:
            d2 = replace(d, positions=kept_pos)
            (out / "debates" / f"{d2.id}.md").write_text(debate_to_md(d2), encoding="utf-8")
            debates.append(d2)
        else:
            drops["debates"] += 1

    benchmarks = []
    for b in pkg.benchmarks:
        if b.paper in verified:
            (out / "benchmarks" / f"{b.id}.md").write_text(benchmark_to_md(b), encoding="utf-8")
            benchmarks.append(b)
        else:
            drops["benchmarks"] += 1

    # machine-readable graph: nodes + explicit edges
    edges = ([{"from": c.id, "to": c.paper, "rel": "anchored-by"} for c in claims]
             + [{"from": op.id, "to": k, "rel": "flagged-by"} for op in problems for k in op.flagged_by]
             + [{"from": b.id, "to": b.paper, "rel": "reported-in"} for b in benchmarks]
             + [{"from": c.id, "to": k, "rel": "corroborated-by"} for c in claims for k in c.corroborated_by])
    index = {
        "schema": SCHEMA_VERSION,
        "papers": [{"cite_key": p.cite_key, "title": p.title, "year": p.year, "arxiv_id": p.arxiv_id,
                    "doi": p.doi, "verified": p.verified.exists} for p in pkg.papers],
        "claims": [{"id": c.id, "paper": c.paper, "type": c.claim_type, "confidence": c.confidence,
                    "corroborated_by": c.corroborated_by} for c in claims],
        "open_problems": [{"id": op.id, "flagged_by": op.flagged_by, "status": op.status} for op in problems],
        "debates": [{"id": d.id, "positions": [pos.stance for pos in d.positions]} for d in debates],
        "benchmarks": [{"id": b.id, "name": b.name, "value": b.value, "metric": b.metric,
                        "method": b.method, "paper": b.paper} for b in benchmarks],
        "edges": edges,
    }
    (out / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    years = [p.year for p in pkg.papers if p.verified.exists and isinstance(p.year, int)]
    checked = [p.verified.checked for p in pkg.papers if p.verified.checked]
    manifest = {
        "schema": SCHEMA_VERSION, "topic": pkg.topic, "scope": pkg.scope, "built": built,
        "stats": {"papers_verified": len(verified), "papers_total": len(pkg.papers),
                  "claims": len(claims), "open_problems": len(problems), "debates": len(debates),
                  "benchmarks": len(benchmarks), "dropped": drops},
        "source_span": {"oldest": min(years) if years else None, "newest": max(years) if years else None,
                        "latest_checked": max(checked) if checked else built},
        "coverage": pkg.coverage or {"note": "not recorded — coverage completeness is unverified"},
        "falsification": falsification or {"run": False},
    }
    (out / "wikillm.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # the 0xLT/kpm distribution envelope — makes this a valid, installable kpm package
    knowledge = build_knowledge_json(pkg, name=name, version=version, license=license)
    (out / "knowledge.json").write_text(json.dumps(knowledge, indent=2) + "\n", encoding="utf-8")

    (out / "CONTEXT.md").write_text(build_context(pkg, built=built), encoding="utf-8")
    (out / "README.md").write_text(_readme(pkg, manifest, knowledge), encoding="utf-8")
    return out


def _readme(pkg: Package, manifest: dict, knowledge: dict | None = None) -> str:
    s = manifest["stats"]
    sp = manifest["source_span"]
    span = f"{sp['oldest']}–{sp['newest']}" if sp["oldest"] else "n/a"
    name = (knowledge or {}).get("name", "@kp/<name>")
    distro = (
        f"\n## Distribution\n\n"
        f"This is a [0xLT/kpm](https://github.com/0xLT/kpm) knowledge package (`knowledge.json`). "
        f"Publish it as a tagged GitHub repo, then any consumer installs it with kpm — no re-research:\n\n"
        f"```bash\nkpm add github:<owner>/<repo>#v{(knowledge or {}).get('version', '0.1.0')}\n"
        f"kpm compose            # composes into a vault; load CONTEXT.md into your agent\n```\n"
    )
    return (f"# {pkg.topic}\n\n*wikillm knowledge package (`{name}`) — a research-landscape foundation.*\n\n"
            f"**Scope:** {pkg.scope}\n\n"
            f"- {s['papers_verified']}/{s['papers_total']} citations verified (arXiv/Crossref); source years {span}\n"
            f"- {s['claims']} claims · {s['open_problems']} open problems · {s['debates']} debates · {s['benchmarks']} benchmarks\n"
            f"- dropped (unverified-anchored): {s['dropped']}\n\n"
            f"**Load `CONTEXT.md` into your agent** to inherit this field without re-running the research. "
            f"`index.json` is the machine-readable graph (nodes + edges); the subdirectories hold the notes.\n"
            f"{distro}\n"
            f"Confidence is corpus-relative (conditional on the cited sources). Built {manifest['built']}.\n")
