"""Falsification harness — what it measures, and what it honestly cannot.

It compares a BASE agent (no package) against a KP-LOADED agent on a held-out task, on up to THREE
axes:

- **precision / citation integrity** (mechanical) — what fraction of the cited papers actually exist
  AND are the paper the answer names. A resolvable arXiv id / DOI is real ONLY if its canonical title
  strictly matches the claimed title (so a real id bearing the WRONG paper's title — a mislabel —
  counts as a hallucination, mirroring the build-time citation gate). An id cited with no title falls
  back to existence (nothing to match); a title-only cite must strictly match a real work.
- **spine adoption** (mechanical; reported under the ``recall`` key) — what fraction of the package's
  verified spine the answer actually used.
- **blind quality panel** (judgment; OPTIONAL, via ``judge_prompts``/``judge_replay``) — the
  JudgeVerifier's slot-alternated blind panel comparing the two answers directly on the held-out task.

HONEST LIMIT — the mechanical axes are structurally stacked toward the KP side, by construction:
the KP prompt hands the agent the spine and instructs it to use only those papers (so KP precision
~1.0 is instruction-following, not a finding), and spine adoption is measured against that same spine
(the treatment is the answer key, so KP recall ~1.0 too). What the mechanical axes genuinely measure
is (a) the BASE side — how much an unaided model fabricates/mislabels/misses, a real model-weakness
measurement — and (b) that the package was correctly assembled and adopted by the loaded agent. They
CANNOT show the package made the answer *better*. That is what the quality panel is for: it is the
only non-circular axis here, and in the combined verdict it acts as a VETO — a panel that prefers the
base answer overturns a mechanical "helps", but a panel win never manufactures one (fail-closed).
"""

from __future__ import annotations

import re
import time
from pathlib import Path

from .citations import (
    _http_get, _arxiv_title, _crossref_doi_title, _crossref_search_strict,
    titles_match_strict, _meaningful, _resolve, strip_arxiv_prefix,
)

_TASK = (
    "Write a tight related-work paragraph for the research area below, then list the 3 most "
    "important OPEN PROBLEMS in it. Cite specific real papers. "
    "End your answer with a section exactly like:\n\n## Citations\n"
    "<arxiv_id or DOI> | <paper title>\n(one per line, only papers you actually cited)\n\n"
    "Research area: {question}\n"
)
_INSTR_KP = (
    "You have been given a verified knowledge package (a field briefing) below. Use ONLY the papers "
    "it lists — every one has been verified to exist. Do not invent citations beyond this list.\n\n"
    "=== FIELD BRIEFING (CONTEXT.md) ===\n{context}\n=== END BRIEFING ===\n\n"
)

_ARXIV_RE = re.compile(r"\b(\d{4}\.\d{4,5})(v\d+)?\b")
_DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s|\]–—]+)", re.I)   # allow () (Lancet 'S0140-6736(26)…') but stop at em/en-dash (prose, never in a DOI); trailing ')' etc. stripped below

# MASKED citation attempts — a model that writes 'arXiv:2510.xxxxx' / 'arXiv:XXXX.XXXXX' / 'arXiv: forthcoming'
# is signalling it WANTED to cite a paper here but could not recall its id — direct evidence it knows the topic has
# work it cannot name. parse_citations() drops these so they are never scored as a fabrication; count_hedges() tallies
# them for the probe. High-precision by construction: a masked id needs an 'arXiv:' marker OR a VALID arXiv YYMM
# prefix (year + month 01-12), so prose like '2.8x'/'100x', config numbers ('1024.xxxx', '2048.xx'), bare 'xxxx',
# real ids and DOIs do NOT match. All runs are bounded (no overlapping unbounded quantifiers) -> linear, ReDoS-safe.
_END = r"(?=[\s)\].,;:]|$)"      # boundary that also closes a '?'-mask run (a trailing \b can't — '?' is non-word)
_HEDGE_RE = re.compile(
    r"""(?ix)
      \b \d{2} (?: 0[1-9] | 1[0-2] ) \. [x?]{2,6} """ + _END + r"""   # bare VALID-YYMM masked id: 2510.xxxxx / 2502.?????
    | \b arxiv: \s* [\dx?]{0,6} \.? [x?]{2,6} """ + _END + r"""        # arXiv:XXXX.XXXXX / arXiv:2510.????? / arXiv:xxxxx
    | \b arxiv: \s* (?: forthcoming | tbd | pending | to\s+appear | in\s+press | under\s+review | n/a ) \b
    """
)


def count_hedges(answer: str) -> int:
    """Count MASKED citation attempts (placeholder arXiv ids like 'arXiv:2510.xxxxx'/'arXiv:XXXX.?????' + explicit
    'arXiv: forthcoming/TBD'). A hedge is the model admitting it could not recall a citation it wanted to make —
    frontier weakness the precision metric is blind to, because a masked id is dropped from citation scoring (it is
    neither a real cite nor a fabrication) rather than counted against the model."""
    return len(_HEDGE_RE.findall(answer))


def make_prompts(pkg_dir: str | Path, question: str) -> dict:
    ctx = (Path(pkg_dir) / "CONTEXT.md").read_text(encoding="utf-8")
    task = _TASK.format(question=question)
    return {"base": task, "kp": _INSTR_KP.format(context=ctx) + task}


def probe_prompt(question: str) -> str:
    """The unaided base-answer task for a topic PRE-SCREEN — no package (that's the point). Dispatch
    one agent with this; its answer reveals whether the model already knows the field or fabricates.
    Nudges toward RECENT work so a model that knows the classics but not the frontier still reveals
    weakness (it tends to fabricate recent papers) rather than getting a false SKIP on old citations."""
    return _TASK.format(question=question) + (
        "\nEmphasize the most RECENT work (roughly the last two years) — that is where a knowledge "
        "package adds the most, and where an unaided model most often fabricates.\n")


def _norm_handle(h: str) -> str:
    """Dedup/identity key for a citation or spine handle: strip a leading 'arxiv:' (any case),
    lowercase, and strip a trailing arXiv version (vN) — but NEVER on a DOI (a DOI contains '/' and a
    trailing 'vN' there is part of the identifier, not a version). ONE normalization, applied
    identically to the cited side AND the spine side so their handle sets actually intersect."""
    s = strip_arxiv_prefix(h).lower()
    return s if "/" in s else re.sub(r"v\d+$", "", s)


_SEP_RE = re.compile(r"\s*(?:\||—|–|\s-\s)\s*")                       # block handle↔title separators
_LEAD_ID_RE = re.compile(r"(?i)\s*((?:arxiv:)?\d{4}\.\d{4,5}(?:v\d+)?|10\.\d{4,9}/\S+)\s+(.*)")


def parse_citations(answer: str) -> list[tuple[str, str]]:
    """Pull (handle, title) pairs. Reads the '## Citations' block — handle and title separated by
    '|', '—', '–', or ' - ' (or just whitespace after a leading id) — AND any arXiv ids / DOIs inline
    in the prose, deduped by normalized handle. A *titled* block entry is recorded before the bare
    inline scan, so the title survives to be strict-checked rather than lost to an untitled duplicate."""
    out: list[tuple[str, str]] = []
    seen: set = set()

    def add(handle: str, title: str):
        if _HEDGE_RE.match(handle.strip()):                  # a masked/placeholder id is a HEDGE, not a citation:
            return                                           # drop it (count_hedges tallies it) so it is never
        handle = strip_arxiv_prefix(handle)                  # title-searched and mislabeled as a fabrication
        key = _norm_handle(handle) or title.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append((handle, title.strip()))

    m = re.search(r"##\s*Citations\s*(.+)$", answer, re.S | re.I)
    for line in (m.group(1) if m else "").splitlines():
        line = re.sub(r"^[-*•·\s]+", "", line).strip()
        line = re.sub(r"^\d+[.)]\s+", "", line)                      # ordered-list marker (also before an id)
        if not line:
            continue
        sep = _SEP_RE.search(line)
        if sep:
            add(line[:sep.start()], line[sep.end():])
        else:
            mid = _LEAD_ID_RE.match(line)
            add(*(mid.groups() if mid else (line, "")))

    # inline ids/DOIs anywhere (catch cites not in a clean block); untitled, so existence-only.
    # DOIs FIRST, masking each matched span, so a DOI-internal 'YYYY.NNNNN' tail (e.g. the '2021.23619'
    # in '10.1001/jama.2021.23619') is not then mis-read by the arXiv scan as a fabricated arXiv id.
    masked = list(answer)
    for mobj in _DOI_RE.finditer(answer):
        add(mobj.group(1).rstrip(".,;:)]'\"!?>}"), "")    # strip trailing prose/quote punctuation, not DOI chars
        masked[mobj.start():mobj.end()] = " " * (mobj.end() - mobj.start())
    for mobj in _ARXIV_RE.finditer("".join(masked)):
        add(mobj.group(1), "")
    return out


def _handle_kind(handle: str) -> str:
    if re.match(r"^\s*(arxiv:)?\d{4}\.\d{4,5}", handle, re.I):
        return "arxiv"
    if re.search(r"10\.\d{4,9}/", handle):
        return "doi"
    return "title"


def _title_ok(claimed: str, canonical: str) -> bool:
    """Gate a resolved id's claimed title against its canonical one. An uninformative claimed title
    (no meaningful tokens) falls back to existence. Otherwise accept iff the titles strictly match in
    EITHER direction: claimed⊇canonical tolerates a legitimate annotation ('(LLaDA)', '(SEDD)') on a
    short title, canonical⊇claimed tolerates a truncated subtitle — but a DIFFERENT paper's title
    (low overlap both ways) is rejected as a mislabel. Mirrors the build gate's title strictness while
    not punishing the annotations agents naturally add in a citations list."""
    if not _meaningful(claimed):
        return True
    return titles_match_strict(claimed, canonical)[0] or titles_match_strict(canonical, claimed)[0]


def _is_real(handle: str, title: str, get=_http_get, *, sleep=time.sleep, max_retries: int = 2):
    """Tri-state. REAL (True) iff the id/DOI resolves AND — when a title is supplied — the canonical
    title strictly matches it (a 'real id, wrong paper' mislabel is False, mirroring the build gate).
    Returns None when the index can't be reached (transient error after retries) so the caller can
    EXCLUDE it — a rate-limit burst must not be scored as a fabrication. Transient errors are retried
    with backoff exactly like the build gate (it shares _resolve)."""
    kind = _handle_kind(handle)
    if kind == "arxiv":
        ct, err = _resolve(_arxiv_title, strip_arxiv_prefix(handle), get=get, sleep=sleep, max_retries=max_retries)
    elif kind == "doi":
        ct, err = _resolve(_crossref_doi_title, handle.strip(), get=get, sleep=sleep, max_retries=max_retries)
    else:
        hit, err = _resolve(_crossref_search_strict, title or handle, get=get, sleep=sleep, max_retries=max_retries)
        return None if err == "transient" else bool(hit)
    if err == "transient":
        return None
    return _title_ok(title, ct) if ct else False


def _arxiv_ym(handle: str):
    """Absolute month index (year*12+month) encoded in an arXiv id's YYMM prefix, else None. arXiv ids
    are YYMM.NNNNN, so '2503.12345' -> March 2025. Lets the probe judge how RECENT a real cite is without
    any network call (a DOI carries no date, so it returns None — the recency signal simply abstains)."""
    m = re.match(r"\s*(?:arxiv:)?(\d{2})(\d{2})\.\d{4,5}", handle, re.I)
    if not m:
        return None
    yy, mm = int(m.group(1)), int(m.group(2))
    return (2000 + yy) * 12 + mm if 1 <= mm <= 12 else None


def score_citations(answer: str, *, get=_http_get, throttle: float = 0.0, sleep=time.sleep) -> dict:
    """Precision / integrity: of the cited papers we could CHECK, how many actually exist and are the
    paper named. Citations the index couldn't resolve (transient) are excluded from the denominator so
    a rate-limited run neither inflates nor deflates precision. *throttle* sleeps between citation
    checks to avoid bursting the index on a long citation list. Also reports ``newest_real_ym`` — the
    month of the most recent REAL arXiv cite — so a recall-aware caller can spot a stale answer."""
    cites = parse_citations(answer)
    verdicts = []
    for i, (h, t) in enumerate(cites):
        verdicts.append((h, t, _is_real(h, t, get, sleep=sleep)))   # inject sleep so retries are fast in tests
        if throttle and i < len(cites) - 1:
            sleep(throttle)
    checkable = [(h, t, v) for h, t, v in verdicts if v is not None]
    fake = [f"{h} | {t}" for h, t, v in checkable if not v]
    n = len(checkable)
    real_yms = [ym for h, t, v in checkable if v for ym in (_arxiv_ym(h),) if ym]
    return {"cited": len(cites), "checked": n, "unresolved": len(cites) - n,
            "real": n - len(fake), "fake": len(fake), "fake_list": fake,
            "newest_real_ym": max(real_yms) if real_yms else None,
            "precision": (n - len(fake)) / n if n else 0.0,
            "hallucination_rate": (len(fake) / n) if n else 0.0}


def _spine_handles(spine: list[dict]) -> list[set]:
    """For each spine paper, the set of recognizable handles (arxiv id / doi, lowercased)."""
    out = []
    for p in spine:
        hs = set()
        if p.get("arxiv_id"):
            hs.add(_norm_handle(p["arxiv_id"]))        # same normalization as the cited side
        if p.get("doi"):
            hs.add(_norm_handle(p["doi"]))             # identical normalization to the cited side
        out.append(hs)
    return out


def score_answer(answer: str, *, spine: list[dict] | None = None, get=_http_get,
                 throttle: float = 0.0, sleep=time.sleep) -> dict:
    """Full score: precision (integrity) + recall (coverage of the verified spine) + f1.

    *spine* is a list of the package's VERIFIED papers as {arxiv_id, doi, cite_key}. recall = fraction
    of spine papers the answer cited. f1 balances not-hallucinating with actually-using-the-field.
    """
    base = score_citations(answer, get=get, throttle=throttle, sleep=sleep)
    cited_handles = {_norm_handle(h) for h, _ in parse_citations(answer)}
    recall, covered = None, None
    if spine:
        sh = _spine_handles(spine)
        covered = sum(1 for hs in sh if hs & cited_handles)
        recall = covered / len(spine) if spine else 0.0
    p = base["precision"]
    f1 = (2 * p * recall / (p + recall)) if (recall is not None and (p + recall) > 0) else None
    return {**base, "recall": recall, "spine_covered": covered, "spine_size": len(spine) if spine else 0,
            "f1": round(f1, 3) if f1 is not None else None}


def _as_of_months(s) -> "int | None":
    """Absolute month index for a YYYY-MM[-DD] reference date, else None (recency signal abstains). Validates the
    month (01-12) and abstains on a bad one — mirrors _arxiv_ym, so a typo'd --as-of can't shift the reference."""
    m = re.match(r"\s*(\d{4})-(\d{2})", s or "")
    if not m:
        return None
    mm = int(m.group(2))
    return int(m.group(1)) * 12 + mm if 1 <= mm <= 12 else None


def probe_verdict(base_answer: str, *, get=_http_get, threshold: float = 0.25, min_real: int = 3,
                  min_sample: int = 3, throttle: float = 0.0, sleep=time.sleep,
                  as_of: "str | None" = None, recency_months: int = 30) -> dict:
    """PRE-FLIGHT: should we even build a package for this topic? Score an UNAIDED agent's answer.

    A package only helps where the model is WEAK, which shows up as the base agent FABRICATING /
    MISLABELING citations, HEDGING (writing placeholder ids it can't recall), being STALE (citing only
    old work on a moving frontier), or being unable to ground at all. Decision tree (order matters):
      1. cited nothing                                   -> BUILD (the model lacks the field)
      2. nothing resolvable (all transient)              -> INCONCLUSIVE (index unreachable; re-run)
      3. fabrication >= threshold, on >= min_sample cites -> BUILD (definitive — even if some unresolved)
      4. too few confirmed-real ONLY because cites were unreachable (real<min_real but real+unresolved>=
         min_real) -> INCONCLUSIVE (a transient must not masquerade as 'too thin' and force a build)
      5. genuinely grounded < min_real real papers       -> BUILD (too thin)
      6. HEDGED on a citation it couldn't recall AND real < 2*min_real -> BUILD (the hedging blind-spot:
         a masked id is proof it knows the frontier holds work it cannot name)
      7. STALE: every real cite is older than *recency_months* before *as_of* (recall-aware) -> BUILD
         (it cites only older work and misses the recent frontier — the coverage weakness the precision
         screen is blind to; needs *as_of* + at least one dated arXiv cite, else this rule abstains)
      8. cites >= min_real real papers cleanly, recent, no hedging -> SKIP (it already knows this)
    The min_sample gate on (3) keeps a 0/0.5/1.0 fabrication rate from a 1-2 cite sample from flipping
    the call. Returns the citation report plus {hedged, stale, decision, reason}."""
    rep = score_citations(base_answer, get=get, throttle=throttle, sleep=sleep)
    cited, checked, real, fake = rep["cited"], rep["checked"], rep["real"], rep["fake"]
    unresolved, hall = rep["unresolved"], rep["hallucination_rate"]
    hedged = count_hedges(base_answer)
    asof_m, newest = _as_of_months(as_of), rep.get("newest_real_ym")
    stale_by = (asof_m - newest) if (asof_m and newest) else None   # months since the newest real cite
    stale = bool(stale_by is not None and stale_by > recency_months)
    if cited == 0:
        decision, reason = "build", "the unaided model cited no real papers at all — it lacks this field; a package will help"
    elif checked == 0:
        decision, reason = "inconclusive", (f"none of the {cited} base citations could be checked (index "
                                            f"unreachable / rate-limited) — re-run")
    elif hall >= threshold and checked >= min_sample:
        decision, reason = "build", (f"the unaided model fabricates/mislabels {fake}/{checked} citations "
                                     f"({hall:.0%}) — it is weak on this topic; a verified package will help")
    elif real < min_real and unresolved and real + unresolved >= min_real:
        decision, reason = "inconclusive", (f"only {real} citation(s) confirmed real, but {unresolved} were "
                                            f"unreachable — can't tell if the model is genuinely thin; re-run")
    elif real < min_real:
        decision, reason = "build", (f"the unaided model grounded only {real} real citation(s) — too thin; "
                                     f"a package will help")
    elif hedged and real < 2 * min_real:
        decision, reason = "build", (f"the unaided model hedged on {hedged} citation(s) it could not recall "
                                     f"(placeholder ids like 'arXiv:2510.xxxxx') while grounding only {real} real "
                                     f"— it knows the frontier holds work it cannot name; a package will help")
    elif stale and real >= min_real:
        age = f"~{stale_by} months" if stale_by < 24 else f"~{stale_by // 12}y"
        decision, reason = "build", (f"the unaided model's most recent real citation is {age} old "
                                     f"(nothing in the last {recency_months} months) — it cites only older work and "
                                     f"is stale on the recent frontier; a package adds the current literature")
    else:
        decision, reason = "skip", (f"the unaided model already cites {real} real papers cleanly and recently "
                                    f"({hall:.0%} fabrication, {hedged} hedged) — it knows this field; a package "
                                    f"adds little value")
    return {**rep, "hedged": hedged, "stale": stale, "decision": decision, "reason": reason,
            "threshold": threshold, "min_real": min_real}


def probe_verdict_multi(answers: list, **kw) -> dict:
    """Aggregate the pre-screen over SEVERAL independently sampled unaided answers (2-3 recommended).

    A single sampled answer is high-variance exactly where the decision matters (near the fabrication
    threshold / min_real boundary) — the sleep pilot's false SKIP came from one clean-looking sample
    that the full falsification then contradicted. Aggregation is asymmetric BY DESIGN: a fabrication
    or hedge the model produced in ANY sample is real, observed weakness (weakness can't be un-observed
    by a luckier sample), while "knows the field cleanly" must hold in EVERY sample to SKIP. So:
    any BUILD -> build; else any INCONCLUSIVE -> inconclusive; else skip. The false-SKIP rate can only
    go down with more samples; the price is a higher build rate, which `falsify` still gates after the
    build. Returns the DECIDING sample's report plus {samples: [per-sample verdicts], n}."""
    if not answers:
        raise ValueError("probe_verdict_multi needs at least one answer")
    per = [probe_verdict(a, **kw) for a in answers]
    pick = (next((v for v in per if v["decision"] == "build"), None)
            or next((v for v in per if v["decision"] == "inconclusive"), None)
            or per[0])
    agg = {**pick, "samples": per, "n": len(per)}
    if len(per) > 1:
        counts = ", ".join(f"{sum(1 for v in per if v['decision'] == d)} {d}"
                           for d in ("build", "skip", "inconclusive")
                           if any(v["decision"] == d for v in per))
        agg["reason"] = (f"{pick['reason']} [{len(per)}-sample probe: {counts}; "
                         f"sample {per.index(pick) + 1} decided]")
    return agg


_JUDGE_PROMPT = (
    "You are ONE judge on a blind quality panel. Below are two ANONYMOUS answers (A and B) to the "
    "same task. You do not know which system produced which, and you must not try to guess.\n\n"
    "The task both answered:\n{task}\n"
    "Judge which answer would serve a researcher better on: correct framing of the field, specific "
    "and checkable citations, and genuinely useful open problems. Ignore length, formatting polish, "
    "and confidence of tone.\n\n"
    "=== ANSWER A ===\n{a}\n=== END ANSWER A ===\n\n"
    "=== ANSWER B ===\n{b}\n=== END ANSWER B ===\n\n"
    "Reply with EXACTLY one word: A, B, or TIE."
)


def judge_prompts(question: str, base_answer: str, kp_answer: str, rounds: int = 6) -> list[str]:
    """Blind-panel prompts for the falsification's QUALITY axis — the non-circular one.

    Round i puts the KP answer in slot A iff i is even — this MUST mirror JudgeVerifier's
    ``ans_is_a = (i % 2 == 0)`` because :func:`judge_replay` re-tallies the recorded slot winners
    through that same alternation; a drift here would silently invert half the panel. Give each prompt
    to a FRESH judge (no shared context — a judge that saw a previous round can de-anonymize the
    slots), record each one-word verdict as a SLOT winner ('a'/'b'/'tie') in order, and feed the list
    to ``kp-build falsify --judge-rounds``. Rounds are clamped even (>=2), same as the verifier."""
    n = max(2, rounds - (rounds % 2))
    task = _TASK.format(question=question)
    out = []
    for i in range(n):
        kp_is_a = (i % 2 == 0)
        a, b = (kp_answer, base_answer) if kp_is_a else (base_answer, kp_answer)
        out.append(_JUDGE_PROMPT.format(task=task, a=a, b=b))
    return out


def judge_replay(recorded: list) -> dict:
    """Re-tally recorded blind-panel slot winners through the SAME JudgeVerifier the build uses.

    ``recorded`` is the ordered list of slot verdicts ('a'/'b'/'tie') from the panel that judged the
    :func:`judge_prompts` comparisons. Running them through JudgeVerifier (answer = the KP answer,
    baseline = base) keeps ONE implementation of the alternation math and inherits its anti-fraud
    property: a lazy uniform fake ('a' every round) nets to a tie. The even-length >=2 gate is
    enforced here too — an odd panel can launder a one-sided vote into a verdict (same defense as
    verify_judgment_claims). Returns {status, kp_wins, base_wins, ties, rounds}."""
    from types import SimpleNamespace
    from .verifier import JudgeVerifier
    rounds = [str(r).strip().lower() for r in recorded]
    bad = sorted({r for r in rounds if r not in ("a", "b", "tie")})
    if bad:
        raise ValueError(f"judge rounds must each be 'a', 'b', or 'tie' — got: {', '.join(bad)}")
    if len(rounds) < 2 or len(rounds) % 2 != 0:
        raise ValueError("judge rounds must be an EVEN number of recorded comparisons (>=2) — the KP "
                         "answer must occupy slot a and slot b equally for position bias (and a lazy "
                         "uniform fake) to cancel")
    seq = iter(rounds)
    replay = lambda task, a, b: {"winner": next(seq, "tie")}
    v = JudgeVerifier(replay, rounds=len(rounds)).verify(
        SimpleNamespace(task="held-out falsification task", answer="kp", baseline="base"))
    m = re.match(r"panel (\d+)-(\d+)-(\d+)", v.evidence)     # JudgeVerifier's own tally is the source of truth
    kp_w, base_w, ties = (int(x) for x in m.groups())
    return {"status": v.status, "kp_wins": kp_w, "base_wins": base_w, "ties": ties, "rounds": rounds}


def helped(base_report: dict, kp_report: dict, judge: "dict | None" = None) -> "bool | None":
    """The single helps / not / inconclusive(None) rule — shared by :func:`verdict` and the CLI exit
    code so the sentence and the exit status can never drift (one rule, two renderers).

    The quality panel is a VETO only: judged-worse overturns a mechanical "helps" (the package made
    the answer worse, whatever the spine numbers say), but judged-better never manufactures one — the
    mechanical axes are stacked toward the KP side (see module docstring), so a helps verdict must
    clear the axis that CAN fail and must not rest on the one that can't."""
    if kp_report.get("cited", 0) == 0:
        return None
    if base_report.get("checked") == 0 or kp_report.get("checked") == 0:
        return None
    if judge and judge.get("status") == "judged-worse":
        return False
    if base_report.get("f1") is not None and kp_report.get("f1") is not None:
        # when both sides were scored against the spine, f1 IS the metric — a cleaner
        # hallucination rate must not overrule a worse f1 (the sentence prints the f1s)
        return kp_report["f1"] > base_report["f1"]
    return kp_report["hallucination_rate"] < base_report["hallucination_rate"]


def verdict(base_report: dict, kp_report: dict, judge: "dict | None" = None) -> str:
    """One-line comparison. Prefers f1 (precision+spine adoption) when available, else precision.
    *judge* is an optional :func:`judge_replay` result — the blind quality axis; without it the
    sentence says so explicitly, because a purely mechanical verdict mostly certifies base weakness
    plus package adoption (see module docstring), not answer quality."""
    if kp_report.get("cited", 0) == 0:
        return "INCONCLUSIVE — the KP answer cited nothing; check the task ran."
    if base_report.get("checked") == 0 or kp_report.get("checked") == 0:
        # every cited id was unreachable (index outage) — precision/f1 here is 0-by-default, not earned
        return "INCONCLUSIVE — citations could not be verified (citation index unreachable); re-run."
    if judge:
        tally = f"{judge['kp_wins']}-{judge['base_wins']}-{judge['ties']} (kp-base-tie)"
        q = {"judged-better": f" Blind quality panel: the KP answer was PREFERRED, {tally}.",
             "judged-worse": (f" Blind quality panel: the BASE answer was preferred, {tally} — the "
                              f"package did not improve the answer, whatever the spine numbers say."),
             "judged-tie": f" Blind quality panel: split, {tally} — no quality difference shown."
             }.get(judge["status"], f" Blind quality panel: {judge['status']}, {tally}.")
    else:
        q = (" (No blind quality panel was run — this verdict certifies citation integrity + spine "
             "adoption, which the KP side nearly satisfies by construction; add --judge-rounds for "
             "the non-circular quality axis.)")
    h = helped(base_report, kp_report, judge)
    if base_report.get("f1") is not None and kp_report.get("f1") is not None:
        b, k = base_report["f1"], kp_report["f1"]
        verb = "HELPS" if h else ("TIES" if (k == b and not (judge and judge.get("status") == "judged-worse"))
                                  else "DID NOT HELP")
        return (f"KP {verb} — f1 {b:.2f} (base) → {k:.2f} (KP). "
                f"precision {base_report['precision']:.2f}→{kp_report['precision']:.2f}, "
                f"spine adoption {base_report.get('recall',0):.2f}→{kp_report.get('recall',0):.2f}, "
                f"{base_report['fake']} fabricated/mislabeled cites in base vs {kp_report['fake']} in KP."
                + q)
    b, k = base_report["hallucination_rate"], kp_report["hallucination_rate"]
    if h:
        return (f"KP HELPS on integrity — hallucination {b:.0%} (base) → {k:.0%} (KP); "
                f"{base_report['fake']} fabricated/mislabeled cites avoided." + q)
    if judge and judge.get("status") == "judged-worse":
        return f"KP DID NOT HELP — integrity {b:.0%} → {k:.0%}." + q
    if k == b == 0:
        return "TIE on citation integrity (both clean) — compare spine adoption and open-problem quality." + q
    return f"KP DID NOT HELP on integrity ({b:.0%} → {k:.0%}) — deepen the survey or rethink." + q
