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
    Works on any item exposing a passage + source: a Claim (``supporting_passage`` / ``paper``) or a
    Relation (``description`` / ``source``).
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
        fired = gate in (result.get("codes", []) if isinstance(result, dict) else [])
        return Verification(kind="execution", exists=(not fired),
                            status=("output-mismatch" if fired else "verified"), via=tool,
                            evidence=f"{tool}:{gate} {'fired' if fired else 'cleared'}", checked=self._today)
