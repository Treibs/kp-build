"""Passage-presence grounding — confirm a claim's quote actually appears in its paper.

The citation spine is verified (the paper EXISTS); grounding is the next layer: does the claim's
supporting_passage actually occur in that paper? Without it a passage is drafter-QUOTED — the agent
said it's a quote, but nothing checked. This module fetches the paper's text (the arXiv abstract for
free via the Atom feed; optionally the ar5iv fulltext) and matches the passage against it:

  grounded    — the passage is present (verbatim-ish) in the text we checked.
  unconfirmed — not found in the ABSTRACT, but fulltext wasn't checked (it may be in the body).
  ungrounded  — we checked the FULLTEXT and the passage is not there (a real grounding failure).

A grounded claim is machine-confirmed; an ungrounded one is capped + flagged like a refuted claim.
Abstract grounding is a positive-only signal (it can't tell 'in the body' from 'fabricated'); only
fulltext grounding produces the negative `ungrounded` verdict.
"""

from __future__ import annotations

import difflib
import html
import re
import time
from collections import Counter
from typing import Callable

from .citations import _http_get, _safe, _resolve, _arxiv_abstract, strip_arxiv_prefix

_WORD = re.compile(r"[a-z0-9]+")
_AR5IV = "https://ar5iv.org/abs/"
_MIN_CHARS = 24          # below this a passage is too short to ground reliably (would match by coincidence)
_MIN_WORDS = 5
_MAX_FUZZY = 200000      # bound the fuzzy pass; covers any real paper, caps the worst case
_CONTIGUITY = 0.6        # the SINGLE longest contiguous match must cover this much of the passage


def _norm(s: str) -> str:
    """Lowercase, words-only, single-spaced — so a verbatim quote matches modulo case/whitespace/punct."""
    return " ".join(_WORD.findall(s.lower()))


def passage_in_text(passage: str, text: str, *, contiguity: float = _CONTIGUITY) -> bool:
    """Is the passage present in the text? Sound by construction — a fabricated or generic passage must
    NOT ground:
      - too short (< _MIN_CHARS / _MIN_WORDS) -> never grounds (a few common words match by coincidence);
      - an exact normalized substring -> grounds (a genuine verbatim quote);
      - otherwise the SINGLE longest contiguous match must cover >= *contiguity* of the passage. We use
        the longest block (not the SUM of scattered blocks) so a word-salad whose tokens merely appear
        scattered across the text does NOT clear the bar — only a near-verbatim quote with one small edit
        has a long contiguous run."""
    p, t = _norm(passage), _norm(text)
    if len(p) < _MIN_CHARS or len(p.split()) < _MIN_WORDS or not t:
        return False
    if p in t:
        return True
    if len(t) > _MAX_FUZZY:
        return False
    m = difflib.SequenceMatcher(None, p, t, autojunk=False).find_longest_match(0, len(p), 0, len(t))
    return m.size / len(p) >= contiguity


def fetch_paper_text(paper, *, get: Callable[[str], str] = _http_get, fulltext: bool = False,
                     sleep=time.sleep, max_retries: int = 2) -> tuple[str, str]:
    """Return (text, source) for a paper: the ar5iv fulltext (HTML stripped to text) if requested and
    available, else the arXiv abstract. ('', '') if nothing could be fetched."""
    if fulltext and paper.arxiv_id:
        raw, err = _resolve(lambda u, g: _safe(u, g), f"{_AR5IV}{strip_arxiv_prefix(paper.arxiv_id)}",
                            get=get, sleep=sleep, max_retries=max_retries)
        if err == "" and raw:
            body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
            body = html.unescape(re.sub(r"(?s)<[^>]+>", " ", body))   # decode &amp;/&gt; so they don't mis-tokenize
            if len(body) > 500:
                return body, "fulltext"
    if paper.arxiv_id:
        summary, err = _resolve(_arxiv_abstract, paper.arxiv_id, get=get, sleep=sleep, max_retries=max_retries)
        if err == "" and summary:
            return summary, "abstract"
    return "", ""


def ground_claims(papers, claims, *, get: Callable[[str], str] = _http_get, fulltext: bool = False,
                  sleep=time.sleep, throttle: float = 0.0) -> dict:
    """Set claim.grounded IN PLACE for each claim anchored to a VERIFIED paper, by checking its
    supporting_passage against the paper's text. One fetch per paper (cached). Returns a breakdown."""
    verified = {p.cite_key: p for p in papers if p.verified.exists}
    needed = sorted({c.paper for c in claims if c.paper in verified})
    texts: dict[str, tuple[str, str]] = {}
    for i, key in enumerate(needed):
        texts[key] = fetch_paper_text(verified[key], get=get, fulltext=fulltext, sleep=sleep)
        if throttle and i < len(needed) - 1:
            sleep(throttle)
    counts: Counter = Counter()
    for c in claims:
        if c.paper not in verified:
            continue                            # anchored to an unverified paper — will be dropped anyway
        text, src = texts.get(c.paper, ("", ""))
        if not c.supporting_passage or not text:
            c.grounded = "unconfirmed"          # no passage, or couldn't fetch the source
        elif passage_in_text(c.supporting_passage, text):
            c.grounded = "grounded"
        else:
            c.grounded = "ungrounded" if src == "fulltext" else "unconfirmed"
        counts[c.grounded] += 1
    return {"by_status": dict(counts), "grounded": counts.get("grounded", 0),
            "ungrounded": counts.get("ungrounded", 0), "unconfirmed": counts.get("unconfirmed", 0)}
