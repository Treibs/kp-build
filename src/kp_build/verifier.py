"""The pluggable verifier seam (V2-a §4.0).

A ``Verifier`` turns a verifiable item into a :class:`Verification` whose ``exists`` is the UNIVERSAL
ship gate, and whose ``kind`` records which oracle produced it. Transport/IO is injected at
construction (mirroring the injected ``get`` the citation path already uses), so every verifier is
deterministic and offline-testable with a fake transport.

This module is intentionally a NARROW lift: ``CitationVerifier`` delegates to the existing, well-tested
``citations.verify_paper`` so its verdicts are byte-identical to the legacy path — the seam adds an
abstraction boundary, not new behavior. ``DocGroundingVerifier`` / ``ExecutionVerifier`` plug in here.
"""

from __future__ import annotations

import time
from typing import Callable, Protocol, runtime_checkable

from .schema import Paper, Verification
from .ground import passage_in_text
from . import citations


@runtime_checkable
class Verifier(Protocol):
    """A pluggable oracle. ``kind`` is the verifier family; ``verify`` returns a Verification whose
    ``exists`` decides shipping. Implementations inject their transport at construction."""

    kind: str

    def verify(self, item) -> Verification: ...


class CitationVerifier:
    """Citation existence/precision via arXiv → DOI(Crossref → OpenAlex) → strict title match.

    Wraps :func:`citations.verify_paper` unchanged (kind='existence'). The verdict is identical to the
    pre-seam build path; this is the legacy verifier given a seam-shaped interface.
    """

    kind = "existence"

    def __init__(self, *, get: Callable[[str], str] = citations._http_get, today: str = "",
                 sleep: Callable[[float], None] = time.sleep, max_retries: int = 2) -> None:
        self._get = get
        self._today = today
        self._sleep = sleep
        self._max_retries = max_retries

    def verify(self, item: Paper) -> Verification:
        """Verify a Paper; returns its Verification (and sets ``item.verified``, as the legacy path does)."""
        return citations.verify_paper(
            item, get=self._get, today=self._today,
            sleep=self._sleep, max_retries=self._max_retries,
        ).verified


class DocGroundingVerifier:
    """Grounds a quoted passage against a PINNED, offline corpus (V2-a §4.4).

    No network at verify time — the corpus (``{source_key: full_text}``; abstracts, datasheet/standard
    text, paper bodies) is injected at construction, so a built pack re-grounds deterministically and
    offline. The tri-state :func:`ground.passage_in_text` maps to a Verification:

      present (True)  -> ``verified``
      absent  (False) -> ``ungrounded``
      unsure  (None)  -> ``unconfirmed``        (passage too short / corpus text too large to fuzzy-scan)

    A source MISSING from the corpus -> ``ungrounded-unreachable``: a COVERAGE DEBT (an oracle exists in
    principle, we just don't hold the text), NEVER laundered into ``verified`` (the review's two-stamp scheme).
    Operates on a **Claim** — grounding its ``supporting_passage`` against ``corpus[claim.paper]`` (the corpus
    is keyed by ``cite_key``).

    NOTE (review M6 — honest deferral): this is a tested LIBRARY building block for offline re-grounding; it is
    **not yet wired into ``kp-build build``** (no research.json directive declares a grounding-claim, and the
    mesh pack is citation-verified via the existing path). So ``kind='grounding'`` is *declared, not yet
    build-enforced*. Grounding a **Relation** is NOT supported here (the corpus is cite_key-keyed, not node-id)
    — both await a future increment.
    """

    kind = "grounding"

    def __init__(self, corpus: dict, *, today: str = "", contiguity: float | None = None) -> None:
        self._corpus = corpus
        self._today = today
        self._contiguity = contiguity

    def verify(self, item) -> Verification:
        passage = getattr(item, "supporting_passage", "") or getattr(item, "description", "")
        source = getattr(item, "paper", "") or getattr(item, "source", "")
        text = self._corpus.get(source)
        if text is None:                          # oracle exists in principle, text not held -> coverage debt
            return Verification(kind="grounding", exists=False, status="ungrounded-unreachable",
                                via="doc-corpus", evidence="source not in pinned corpus", checked=self._today)
        present = passage_in_text(passage, text,
                                  **({} if self._contiguity is None else {"contiguity": self._contiguity}))
        status = {True: "verified", False: "ungrounded", None: "unconfirmed"}[present]
        return Verification(kind="grounding", exists=(present is True), status=status, via="doc-corpus",
                            evidence=(passage[:160] if present is True else ""), checked=self._today)


class ExecutionVerifier:
    """Runs a mechanical tool against an artifact and gates the claim on the result (V2-a §7).

    The RUNNER is injected (like ``get`` / ``corpus``), so this is PURE LOGIC — deterministic and
    offline-testable with a fake runner; no sandbox here (lint/inspect ship v2-a, render is v2-b).
    Runner contract: ``runner(artifact, tool) -> {"codes": [gate codes present]}`` on a successful run,
    or ``None`` if the artifact/tool could not produce a result; it RAISES on a real run failure
    (timeout/crash). Statuses:

      verified        — ran clean AND the asserted gate is ABSENT (the mechanical fundamental holds)
      output-mismatch — ran clean but the gate FIRED (the artifact violates what it claims)
      not-found       — the runner produced no result (artifact/tool missing)
      error           — the run RAISED (timeout/crash) — UNKNOWN, never trusted

    A claim with no mechanical oracle (``aesthetic`` true, or no ``gate_code``) returns ``unverifiable``
    — it never guesses ``pass`` for taste; aesthetic quality routes to the v2-b judge panel.
    """

    kind = "execution"

    def __init__(self, runner, *, today: str = "") -> None:
        self._runner = runner
        self._today = today

    def verify(self, item) -> Verification:
        gate = getattr(item, "gate_code", "")
        if getattr(item, "aesthetic", False) or not gate:
            return Verification(kind="execution", exists=False, status="unverifiable", via="execution",
                                evidence="no mechanical oracle (aesthetic / no gate)", checked=self._today)
        tool = getattr(item, "tool", "") or "execution"
        try:
            result = self._runner(getattr(item, "artifact", None), getattr(item, "tool", ""))
        except Exception as e:                      # timeout / crash -> UNKNOWN, never trusted
            return Verification(kind="execution", exists=False, status="error", via=tool,
                                evidence=f"run failed: {type(e).__name__}", checked=self._today)
        if result is None:
            return Verification(kind="execution", exists=False, status="not-found", via=tool,
                                evidence="artifact/tool not found", checked=self._today)
        raw = result.get("codes") if isinstance(result, dict) else None
        if not isinstance(raw, list):                   # malformed runner output -> untrusted, never fail-OPEN
            return Verification(kind="execution", exists=False, status="error", via=tool,
                                evidence="runner returned non-list 'codes'", checked=self._today)
        fired = gate in raw
        return Verification(kind="execution", exists=(not fired),
                            status=("output-mismatch" if fired else "verified"), via=tool,
                            evidence=f"{tool}:{gate} {'fired' if fired else 'cleared'}", checked=self._today)


def hyperframes_runner(artifact, tool, *, _run=None):
    """The default ExecutionVerifier runner — shells to the hyperframes CLI and extracts the gate codes.
    Returns ``{"codes": [...]}``, or ``None`` if no parseable result; raises on timeout/crash (→ ``error``).
    ``_run`` (a ``subprocess.run``-shaped callable) is injectable so the parse/extraction is unit-testable."""
    import subprocess
    import json as _json
    run = _run or subprocess.run
    p = run(["npx", "--yes", "hyperframes@0.6.91", tool, "--json", str(artifact)],
            capture_output=True, text=True, timeout=180)
    out = (p.stdout or "").strip()
    i = out.find("{")
    if i < 0:
        return None
    try:
        d = _json.loads(out[i:])
    except Exception:                               # malformed slice -> no result, never a crash
        return None
    if tool == "lint":
        return {"codes": [f.get("code") for f in d.get("findings", [])]}
    if tool == "inspect":
        return {"codes": [x.get("code") for x in d.get("issues", [])]}
    if tool == "validate":
        return {"codes": (["contrastFailures"] if d.get("contrastFailures", 0) else [])}
    return None


def verify_execution_claims(pkg, *, runner, today: str = "", base_dir=None) -> dict:
    """Build step: run the ExecutionVerifier (injected ``runner``) on every claim carrying an ``execution``
    directive, setting its per-claim ``verified``. Citation/academic claims are untouched. Returns a summary.

    M5: relative artifacts are resolved under ``base_dir`` (the pack root) and an artifact that escapes the
    base is refused (``error``), so a crafted directive can't make the runner read a file outside the pack."""
    from types import SimpleNamespace
    from pathlib import Path as _Path
    base = _Path(base_dir).resolve() if base_dir else None
    ev = ExecutionVerifier(runner, today=today)
    total = verified = 0
    for c in getattr(pkg, "claims", []):
        d = getattr(c, "execution", None) or {}
        if not d:
            continue
        total += 1
        artifact = d.get("artifact")
        if base is not None and artifact and not d.get("aesthetic"):
            resolved = (base / artifact).resolve()
            if not resolved.is_relative_to(base):           # belt: never escape the pack base
                c.verified = Verification(kind="execution", exists=False, status="error", via="execution",
                                          evidence="artifact escapes pack base", checked=today)
                continue
            artifact = str(resolved)
        c.verified = ev.verify(SimpleNamespace(
            artifact=artifact, tool=d.get("tool", ""),
            gate_code=d.get("gate_code", ""), aesthetic=d.get("aesthetic", False)))
        verified += bool(c.verified.exists)
    return {"execution_total": total, "execution_verified": verified}


def verify_grounding_claims(pkg, *, corpus: dict, today: str = "") -> dict:
    """Build step: run the DocGroundingVerifier against the injected, pinned ``corpus`` on every claim
    carrying a ``grounding`` directive, setting its per-claim ``verified``. Citation/academic/execution
    claims are untouched. Returns a summary.

    No network: the corpus is loaded offline by the caller and keyed by the directive's ``source`` (a
    no-paper grounding claim has no cite_key). The directive's OWN ``supporting_passage`` is grounded
    (the verbatim quote to check), not the claim's display passage. A source missing from the corpus
    yields ``ungrounded-unreachable`` (coverage debt) — never laundered into ``verified``."""
    from types import SimpleNamespace
    gv = DocGroundingVerifier(corpus, today=today)
    total = verified = 0
    for c in getattr(pkg, "claims", []):
        d = getattr(c, "grounding", None) or {}
        if not d:
            continue
        total += 1
        c.verified = gv.verify(SimpleNamespace(
            supporting_passage=d.get("supporting_passage", ""), source=d.get("source", ""), paper=""))
        verified += bool(c.verified.exists)
    return {"grounding_total": total, "grounding_verified": verified}
