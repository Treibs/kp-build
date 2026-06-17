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
