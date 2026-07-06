"""Staleness report (`kp-build refresh`) — has the field moved on since this package was built?

A knowledge package's value concentrates exactly where it rots fastest. We build packages for
frontier topics BECAUSE the unaided model is weak there — and the model is weak there because the
field is moving. The same motion that makes a package worth building guarantees it goes stale: six
months after `built`, the verified spine is still verified (those papers did not stop existing) but
it may no longer be the field. Verification is a statement about the past; freshness is a statement
about the present, and nothing in an assembled package can testify to the present.

This module is the mechanical half of the answer. It re-runs the same citation-graph expansion the
build used (`expand.expand`) from the package's verified spine and asks one checkable question: has
work appeared that POST-DATES the build? An arXiv id carries its own date (the YYMM prefix — the
same month-index idiom the probe's recency rule uses), so "newer than the build" is decidable with
no extra network calls; a year-only candidate is judged coarsely; a candidate with no dating signal
is COUNTED and reported, never silently dropped. Relevance is still a judgment call — like expand,
we return raw candidates and leave "does this obsolete a claim?" to the orchestration, which can
re-run the weakness probe with the included ``reprobe_prompt``.

Two honesty rules shape the design. First, the engine never reads the wall clock: ``as_of`` is
required and caller-supplied, so a refresh report is deterministic and replayable (the CLI passes
today; a test passes anything). Second, the verdict mirrors the probe's tri-state: a zero-candidate
expansion is INCONCLUSIVE, not fresh — expand() degrades silently per-seed, so a zero total cannot
distinguish a quiet field from an unreachable index, and we abstain rather than guess. The same rule
covers a manifest whose ``built`` date is missing or unparseable: with no build date, neither age nor
"post-dates the build" is computable, so the verdict is INCONCLUSIVE — never a default "fresh" that
would let a rotting package pass forever on a broken field.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from .citations import _http_get
from .expand import expand
# Private-by-convention reuse, acknowledged: the YYMM month-index idiom (_arxiv_ym) and the as-of
# validator (_as_of_months) grew up in falsify's recency rule. refresh shares them rather than
# re-implementing, so the probe's staleness clock and this one can never drift apart.
from .falsify import _arxiv_ym, _as_of_months, probe_prompt
from .schema import paper_from_md


def refresh(package_dir: str | Path, *, as_of: str, get=_http_get, recency_months: int = 30,
            per_seed: int = 40, sleep=time.sleep) -> dict:
    """Mechanical staleness report for an assembled package at ``package_dir``.

    ``as_of`` is REQUIRED ("YYYY-MM" or "YYYY-MM-DD") — the caller supplies the clock; the engine
    never calls date.today() itself. Raises ValueError on a bad ``as_of``, a directory that is not
    an assembled package, or a package with no verified spine to expand from (the CLI maps
    ValueError to exit 2). Returns the report dict described in the module docstring.
    """
    asof_m = _as_of_months(as_of)
    if asof_m is None:
        raise ValueError(f"as_of must be 'YYYY-MM' or 'YYYY-MM-DD' with a valid month, got {as_of!r}")

    root = Path(package_dir)
    manifest_path = root / "wikillm.json"
    if not manifest_path.is_file():
        raise ValueError(f"{root} is not an assembled package (no wikillm.json)")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    topic = manifest.get("topic", "")
    built = manifest.get("built") or ""

    papers = [paper_from_md(p.read_text(encoding="utf-8"))
              for p in sorted((root / "papers").glob("*.md"))]
    # verified spine = the papers the package actually stands on, with a graph-walkable handle
    spine = [p for p in papers if p.verified.exists and (p.arxiv_id or p.doi)]
    seeds = [p.arxiv_id or p.doi for p in spine]
    if not seeds:
        raise ValueError("package has no verified spine papers with an arXiv id or DOI — "
                         "nothing to expand from; build/verify the package first")

    # a candidate we already hold — verified or not — is not "new", so skip EVERY id in the package
    existing_ids = ({p.arxiv_id for p in papers if p.arxiv_id}
                    | {p.doi for p in papers if p.doi})

    built_m = _as_of_months(built)                       # None -> built missing/unparseable: abstain
    age_months = (asof_m - built_m) if built_m is not None else None
    built_year = ((built_m - 1) // 12) if built_m is not None else None   # invert year*12+mm (mm 1-12)

    cands = expand(seeds, get=get, per_seed=per_seed, skip=existing_ids, sleep=sleep)

    new_since_build: list[dict] = []
    undated = 0
    for c in cands:
        if built_m is None:
            # no build month to compare against — EVERY candidate is unjudgeable, dated or not
            # (counting a dated candidate as merely 'undated' here would mislabel the failure)
            undated += 1
            continue
        ym = _arxiv_ym(c.get("arxiv_id") or "")
        if ym is not None:
            # month-resolution: the arXiv YYMM prefix post-dates the build's month index
            if ym > built_m:
                new_since_build.append(c)
        elif isinstance(c.get("year"), int):
            # year-only candidates (DOI/S2 metadata) are judged COARSELY: strict '>' because a
            # same-year paper may still pre-date the build month — the asymmetry undercounts
            # (a false 'fresh' beat a false 'stale' here; the arXiv path has real resolution)
            if c["year"] > built_year:
                new_since_build.append(c)
        else:
            # no dating signal at all (no arXiv YYMM, no year) — reported, never silently dropped
            undated += 1

    fields = ("title", "year", "arxiv_id", "doi", "via")
    new_list = [{k: c.get(k) for k in fields} for c in new_since_build]

    stale_by_age = age_months is not None and age_months > recency_months
    age_str = (f"~{age_months} month(s) old at {as_of}" if age_months is not None
               else "of unknown age (built date missing/unparseable — the age signal abstains)")
    if built_m is None:
        # fail-CLOSED: with no build date, neither staleness signal can run — a package with a broken
        # 'built' field must not read as fresh forever (the age test can never fire and no candidate
        # can ever count as post-build). Same abstain doctrine as the zero-candidate case below.
        decision = "inconclusive"
        reason = (f"the manifest's built date is missing/unparseable ({built!r}) — neither age nor "
                  f"'post-dates the build' can be computed, so none of the {len(cands)} expansion "
                  f"candidate(s) can be judged; fix the manifest's 'built' field and re-run")
    elif stale_by_age or new_list:
        decision = "stale"
        if new_list and stale_by_age:
            reason = (f"{len(new_list)} expansion candidate(s) post-date the {built} build AND the "
                      f"package is {age_str} (> {recency_months} months) — the field moved while the "
                      f"package stood still; refresh it")
        elif new_list:
            reason = (f"citation-graph expansion surfaced {len(new_list)} paper(s) post-dating the "
                      f"{built} build — the field has moved on from the verified spine; refresh it")
        else:
            reason = (f"the package is {age_str} (> {recency_months} months) — stale by age alone; "
                      f"even a quiet expansion cannot clear a clock this old")
    elif not cands:
        # expand() degrades silently per-seed (a transient seed just contributes nothing), so a
        # ZERO total is the honest abstain: it cannot distinguish 'quiet field' from 'index
        # unreachable'. Mirrors the probe's checked==0 -> INCONCLUSIVE rule.
        decision = "inconclusive"
        reason = (f"expansion returned zero candidates across {len(seeds)} seed(s) — can't tell a "
                  f"quiet field from an unreachable index (per-seed failures are silent); re-run")
    else:
        decision = "fresh"
        undated_note = f"; {undated} undated candidate(s) reported unjudged" if undated else ""
        reason = (f"the package is {age_str} (<= {recency_months} months) and none of the "
                  f"{len(cands)} expansion candidates post-date the build — the verified spine "
                  f"still covers the field{undated_note}")

    report = {
        "topic": topic, "built": built, "as_of": as_of, "age_months": age_months,
        "spine_size": len(spine), "seeds": seeds,
        "candidates": new_list, "new_since_build": len(new_list),
        "undated_candidates": undated, "total_candidates": len(cands),
        "decision": decision, "reason": reason,
        # so the orchestrator can re-run the weakness probe with --as-of and close the loop
        "reprobe_prompt": probe_prompt(topic),
    }
    # distribution metadata rides along when the manifest carries it (older manifests don't)
    for k in ("name", "version"):
        if manifest.get(k):
            report[k] = manifest[k]
    return report
