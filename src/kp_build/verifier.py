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
    Operates on a **Claim** (or a directive namespace) — grounding its ``supporting_passage`` against
    ``corpus[source]``, where ``source`` is the claim's ``paper`` (cite_key) or its grounding directive's
    ``source`` key.

    WIRED INTO BUILD (V2-a, the seam's third verifier): :func:`verify_grounding_claims` runs this on every claim carrying a ``grounding``
    directive under ``kp-build build --ground-verify``, and :func:`load_grounding_corpus` assembles the pinned
    corpus from committed ``corpus/<source>.txt`` files (offline) with a Crossref-abstract fallback for DOI
    sources. See ``examples/http-semantics-grounding`` and ``examples/vwt-grounding``. Still out of scope:
    grounding a **Relation** (the corpus is source-keyed, not node-id-keyed) — a future increment.
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
        # the asserted gate fired, OR the tool itself could not run (inspect_error sentinel) — either way
        # the mechanical fundamental is NOT confirmed, so the claim must not verify (no crashed-tool pass).
        fired = gate in raw or "inspect_error" in raw
        if "inspect_error" in raw and gate != "inspect_error":
            evidence = f"{tool} could not run (inspect_error) — gate {gate} not evaluated"  # honest cause
        else:
            evidence = f"{tool}:{gate} {'fired' if fired else 'cleared'}"
        return Verification(kind="execution", exists=(not fired),
                            status=("output-mismatch" if fired else "verified"), via=tool,
                            evidence=evidence, checked=self._today)


class JudgeVerifier:
    """The v2-b aesthetic/quality verifier — judges an answer RELATIVE to a baseline, blind (V2-b §judge).

    Quality and taste are not mechanically checkable, so this is deliberately NOT an absolute score: the
    design review's keystone is that a taste verdict is non-reproducible and tautological unless it is
    *relative* (does a pack-loaded answer beat the unaided one?). So ``verify`` needs a ``baseline`` and a
    panel of blind comparisons. The JUDGE is injected (like ``get`` / ``runner`` / ``corpus``) so this is
    pure logic, offline-testable with a fake. Judge contract:
    ``judge(task, a, b) -> {"winner": "a" | "b" | "tie", "reason"?: str}`` — it sees two ANONYMOUS options.

    Anti-tautology guarantee: across ``rounds`` the verifier ALTERNATES which option (answer vs baseline)
    occupies slot a/b, so a purely position-biased judge nets to a tie. Statuses:

      judged-better — the panel preferred the answer over the baseline (exists=True; ships as helpful)
      judged-worse  — the panel preferred the baseline
      judged-tie    — split / all position-bias / no usable votes (never fail-open to 'better')
      unverifiable  — no baseline supplied (relative-only; never a guessed absolute pass)
    """

    kind = "judgment"

    def __init__(self, judge, *, rounds: int = 4, today: str = "") -> None:
        self._judge = judge
        self._rounds = max(2, rounds - (rounds % 2))      # keep it even so a/b alternation is balanced
        self._today = today

    def verify(self, item) -> Verification:
        answer = getattr(item, "answer", "") or ""
        baseline = getattr(item, "baseline", "") or ""
        task = getattr(item, "task", "") or ""
        if not baseline or not answer:                    # relative needs BOTH sides — no absolute taste
            return Verification(kind="judgment", exists=False, status="unverifiable", via="judge-panel",  # gate,
                                evidence="judgment is relative — needs a non-empty answer AND baseline",   # and an
                                checked=self._today)                                                       # empty
            # ^ an empty answer can never "win" against a baseline (review should-fix #3 — close the fail-open)
        answer_wins = baseline_wins = ties = 0
        for i in range(self._rounds):
            ans_is_a = (i % 2 == 0)                       # alternate slots to cancel position bias
            a, b = (answer, baseline) if ans_is_a else (baseline, answer)
            try:
                w = (self._judge(task, a, b) or {}).get("winner", "tie")
            except Exception:
                w = "error"
            if w in ("a", "b"):
                (answer_wins, baseline_wins) = ((answer_wins + (w == "a"), baseline_wins + (w == "b"))
                                                if ans_is_a else
                                                (answer_wins + (w == "b"), baseline_wins + (w == "a")))
            else:
                ties += 1                                 # tie / error / junk -> no vote, never trusted
        if answer_wins > baseline_wins:
            status, exists = "judged-better", True
        elif baseline_wins > answer_wins:
            status, exists = "judged-worse", False
        else:
            status, exists = "judged-tie", False
        return Verification(kind="judgment", exists=exists, status=status, via="judge-panel",
                            evidence=f"panel {answer_wins}-{baseline_wins}-{ties} (answer-baseline-tie) "
                                     f"over {self._rounds} rounds", checked=self._today)


def hyperframes_runner(artifact, tool, *, _run=None):
    """The default ExecutionVerifier runner — shells to the hyperframes CLI and extracts the gate codes.
    Returns ``{"codes": [...]}``, or ``None`` if no parseable result; raises on timeout/crash (→ ``error``).
    ``_run`` (a ``subprocess.run``-shaped callable) is injectable so the parse/extraction is unit-testable."""
    import subprocess
    import json as _json
    run = _run or subprocess.run
    p = run(["npx", "--yes", "hyperframes@0.6.91", tool, "--json", str(artifact)],
            capture_output=True, text=True, timeout=180)
    stdout, stderr = (p.stdout or ""), (getattr(p, "stderr", "") or "")
    out = stdout.strip()
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
        # inspect COULD NOT honestly analyze: it crashed (ok:false/error — e.g. root data-duration missing,
        # so no totalDuration), OR a StaticGuard contract violation (printed to stderr while stdout still
        # reads ok:true). Either way -> the 'inspect_error' sentinel (a failure), never read as clean.
        invalid = "Invalid HyperFrame contract" in stdout or "Invalid HyperFrame contract" in stderr
        if not d.get("ok", True) or d.get("error") or invalid:
            return {"codes": ["inspect_error"]}
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


def load_grounding_corpus(pkg, base_dir, *, get=None) -> dict:
    """Assemble the offline grounding corpus ``{source: text}`` for a pack's grounding claims.

    Primary path: a committed, pack-local ``corpus/<source>.txt`` (read OFFLINE, keyed by the directive's
    ``source``), so a built pack re-grounds deterministically from a clean clone. Fallback: a ``source``
    with no committed file but naming a ``pkg`` paper that has a DOI is fetched via
    :func:`ground.fetch_doc_corpus` (the live DOI path) when ``get`` is provided. A ``source`` with neither
    is omitted, so :func:`verify_grounding_claims` honestly stamps it ``ungrounded-unreachable``."""
    from pathlib import Path as _Path
    from .ground import fetch_doc_corpus
    cdir = (_Path(base_dir).resolve() / "corpus") if base_dir else None
    sources = {(getattr(c, "grounding", None) or {}).get("source", "")
               for c in getattr(pkg, "claims", [])}
    sources.discard("")
    corpus: dict = {}
    need_fetch = []
    for s in sorted(sources):
        f = (cdir / f"{s}.txt") if cdir else None
        if f is not None and f.is_file() and f.resolve().is_relative_to(cdir):   # belt: stay inside corpus/
            corpus[s] = f.read_text(encoding="utf-8")
        else:
            need_fetch.append(s)
    if need_fetch and get is not None:
        by_key = {p.cite_key: p for p in getattr(pkg, "papers", [])}
        papers = [by_key[s] for s in need_fetch if s in by_key and by_key[s].doi]
        if papers:
            corpus.update(fetch_doc_corpus(papers, get=get))
    return corpus


def verify_judgment_claims(pkg, *, today: str = "") -> dict:
    """Build step: for every claim carrying a ``judgment`` directive, REPLAY its recorded blind-panel
    through the JudgeVerifier and set the per-claim ``verified``. Other claims are untouched.

    DETERMINISTIC by design — the LLM panel ran once (in research) and its per-comparison slot winners
    ('a'/'b'/'tie') are recorded in ``directive['rounds']``; here a replay-judge just returns them in
    order, so a rebuild is byte-identical (a live judge would not be). Crucially this runs them through
    the SAME JudgeVerifier as everything else — its A/B alternation means a hand-faked uniform panel nets
    to a tie, so an author can't write 'answer wins' without a panel that genuinely favours it in both
    slot positions."""
    from types import SimpleNamespace
    total = verified = 0
    for c in getattr(pkg, "claims", []):
        d = getattr(c, "judgment", None) or {}
        if not d:
            continue
        total += 1
        rounds = list(d.get("rounds") or [])
        if len(rounds) < 2 or len(rounds) % 2 != 0:
            # defense-in-depth: a malformed (odd / length-1) panel must ABSTAIN, never be tallied — feeding
            # a short iterator into JudgeVerifier's force-even round count would pad a free 'tie' (or truncate
            # a balancing vote) and could launder a fake into judged-better. cli._load already rejects these,
            # but a directly-constructed claim must not slip past either.
            c.verified = Verification(kind="judgment", exists=False, status="unverifiable", via="judge-panel",
                                      evidence="recorded panel is not an even-length (>=2) comparison set",
                                      checked=today)
            continue
        seq = iter(rounds)
        replay = lambda task, a, b, _seq=seq: {"winner": next(_seq, "tie")}   # deterministic recorded panel
        c.verified = JudgeVerifier(replay, rounds=len(rounds), today=today).verify(
            SimpleNamespace(task=d.get("task", ""), answer=d.get("answer", ""), baseline=d.get("baseline", "")))
        verified += bool(c.verified.exists)
    return {"judgment_total": total, "judgment_verified": verified}
