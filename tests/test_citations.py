import io
import urllib.error

import pytest

from kp_build.citations import titles_match, titles_match_strict, verify_paper, verify_all
from kp_build.schema import Paper

ARXIV_HIT = "<feed><entry><title>Attention Is All You Need</title></entry></feed>"
ARXIV_MISS = "<feed></feed>"


def _arxiv(title):
    return f"<feed><entry><title>{title}</title></entry></feed>"


def _crossref_search(title, doi="10.1/x", typ="journal-article"):
    import json
    return json.dumps({"message": {"items": [{"title": [title], "DOI": doi, "type": typ}]}})


def _crossref_doi(title):
    import json
    return json.dumps({"message": {"title": [title]}})


def _crossref_doi_miss():
    return '{"message": {}}'          # Crossref reached, but no record for this DOI


def _openalex(title):
    import json
    return json.dumps({"title": title, "display_name": title})


def _raises(code):
    def g(url):
        raise urllib.error.HTTPError(url, code, "err", {}, io.BytesIO(b""))
    return g


# ── title matching ───────────────────────────────────────────────────────────────


def test_titles_match_loose():
    assert titles_match("Attention Is All You Need", "Attention is all you need")
    assert not titles_match("Attention Is All You Need", "A Survey of Reinforcement Learning")


def test_titles_match_strict_accepts_real_variations():
    assert titles_match_strict("Attention Is All You Need", "Attention is all you need")[0]
    # truncated subtitle, >=4 meaningful tokens, full coverage
    assert titles_match_strict("BERT Pre-training of Deep Bidirectional Transformers",
                               "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding")[0]


def test_titles_match_strict_rejects_the_exploits():
    # the exact false-accepts the QA reproduced
    assert not titles_match_strict("Language Models", "Large Language Models")[0]
    assert not titles_match_strict("Deep Learning", "What's Deep About Deep Learning?")[0]
    assert not titles_match_strict("Speculative Decoding for Efficient Inference",
                                   "EdgeSD: Edge-Cloud Collaborative Speculative Decoding")[0]


# ── identifier path: verdict is FINAL, no rescue ─────────────────────────────────


def test_arxiv_id_with_matching_title_verifies():
    p = Paper(cite_key="v", title="Attention Is All You Need", arxiv_id="1706.03762")
    verify_paper(p, get=lambda u: ARXIV_HIT, today="2026-06-14")
    assert p.verified.exists and p.verified.status == "verified" and p.verified.via == "arxiv"
    assert p.url == "https://arxiv.org/abs/1706.03762"


def test_arxiv_id_missing_is_not_found_not_rescued():
    # The id does not resolve. Even if a title search WOULD match, we must NOT fall through.
    def g(u):
        return ARXIV_MISS if "export.arxiv" in u else _crossref_search("Attention Is All You Need")
    p = Paper(cite_key="x", title="Attention Is All You Need", arxiv_id="2401.99999")
    verify_paper(p, get=g, today="2026-06-14")
    assert not p.verified.exists and p.verified.status == "not-found"


def test_arxiv_id_with_wrong_title_is_mismatch_not_rescued():
    # Real id, but the claimed title is a DIFFERENT paper. Must reject, never rescue via title search.
    def g(u):
        return ARXIV_HIT if "export.arxiv" in u else _crossref_search("Totally Different Title About Cats")
    p = Paper(cite_key="x", title="Totally Different Title About Cats", arxiv_id="1706.03762")
    verify_paper(p, get=g, today="2026-06-14")
    assert not p.verified.exists and p.verified.status == "id-title-mismatch"
    assert p.verified.canonical_title == "Attention Is All You Need"


def test_doi_path_verifies_and_mismatch_rejects():
    p = Paper(cite_key="a", title="Attention Is All You Need", doi="10.1/a")
    verify_paper(p, get=lambda u: _crossref_doi("Attention Is All You Need"), today="2026-06-14")
    assert p.verified.exists and p.verified.via == "crossref"
    q = Paper(cite_key="b", title="Something Unrelated Entirely Here", doi="10.1/b")
    verify_paper(q, get=lambda u: _crossref_doi("Attention Is All You Need"), today="2026-06-14")
    assert not q.verified.exists and q.verified.status == "id-title-mismatch"


# ── DOI backends: Crossref first, OpenAlex fallback (broaden reach, soundness unchanged) ──────────


def _route(crossref, openalex):
    """A stub get() that serves different bodies to the Crossref vs OpenAlex hosts."""
    def g(u):
        if "crossref.org" in u:
            return crossref() if callable(crossref) else crossref
        if "openalex.org" in u:
            return openalex() if callable(openalex) else openalex
        return "{}"
    return g


def test_openalex_doi_title_parses():
    from kp_build.citations import _openalex_doi_title
    t, err = _openalex_doi_title("10.1/x", lambda u: _openalex("Some Real Paper"))
    assert t == "Some Real Paper" and err == ""


def test_doi_uses_crossref_first_no_openalex_call():
    # Crossref resolves -> we never touch OpenAlex
    seen = {"openalex": False}
    def g(u):
        if "openalex.org" in u:
            seen["openalex"] = True
        return _crossref_doi("Attention Is All You Need") if "crossref.org" in u else "{}"
    p = Paper(cite_key="a", title="Attention Is All You Need", doi="10.1/x")
    verify_paper(p, get=g, today="2026-06-14")
    assert p.verified.exists and p.verified.via == "crossref" and seen["openalex"] is False


def test_doi_falls_back_to_openalex_when_crossref_has_no_record():
    # a real DataCite/preprint DOI: Crossref has no record -> OpenAlex resolves -> verified via openalex
    p = Paper(cite_key="a", title="Attention Is All You Need", doi="10.5555/datacite")
    verify_paper(p, get=_route(_crossref_doi_miss, _openalex("Attention Is All You Need")), today="2026-06-14")
    assert p.verified.exists and p.verified.status == "verified" and p.verified.via == "openalex"


def test_doi_falls_back_to_openalex_when_crossref_transient():
    # Crossref rate-limited (429) but OpenAlex authoritatively resolves the DOI -> verified via openalex
    def g(u):
        if "crossref.org" in u:
            raise urllib.error.HTTPError(u, 429, "x", {}, io.BytesIO(b""))
        return _openalex("Attention Is All You Need")
    p = Paper(cite_key="a", title="Attention Is All You Need", doi="10.1/x")
    verify_paper(p, get=g, today="2026-06-14", sleep=lambda _s: None, max_retries=1)
    assert p.verified.exists and p.verified.via == "openalex"


def test_doi_openalex_wrong_title_is_still_a_mismatch():
    # SOUNDNESS: a DOI that resolves in OpenAlex to a DIFFERENT paper is rejected, not laundered
    p = Paper(cite_key="a", title="Attention Is All You Need", doi="10.5555/x")
    verify_paper(p, get=_route(_crossref_doi_miss, _openalex("A Completely Different Paper")), today="2026-06-14")
    assert not p.verified.exists and p.verified.status == "id-title-mismatch" and p.verified.via == "openalex"


def test_doi_absent_from_both_is_not_found():
    # fabricated DOI: neither index has it -> not-found (not rescued)
    p = Paper(cite_key="a", title="Imaginary Paper", doi="10.9999/fake")
    verify_paper(p, get=_route(_crossref_doi_miss, "{}"), today="2026-06-14")
    assert not p.verified.exists and p.verified.status == "not-found"


# ── title-only path: NEVER verified (the laundering fix) ─────────────────────────


def test_title_only_strict_hit_is_unconfirmed_not_verified():
    p = Paper(cite_key="t", title="Speculative Decoding for Fast Inference")
    verify_paper(p, get=lambda u: _crossref_search("Speculative Decoding for Fast Inference"), today="2026-06-14")
    assert p.verified.status == "unconfirmed" and p.verified.exists is False
    assert p.doi == "10.1/x"  # recorded as a candidate hint only


def test_title_only_fabricated_short_titles_are_rejected():
    # The exact fakes that previously got 'verified' against unrelated real works.
    def g_lm(u): return _crossref_search("Large Language Models")
    p = Paper(cite_key="fake1", title="Language Models")
    verify_paper(p, get=g_lm, today="2026-06-14")
    assert p.verified.exists is False and p.verified.status == "not-found"

    def g_dl(u): return _crossref_search("What's Deep About Deep Learning?")
    q = Paper(cite_key="fake2", title="Deep Learning")
    verify_paper(q, get=g_dl, today="2026-06-14")
    assert q.verified.exists is False


def test_title_only_component_type_filtered_out():
    # A Crossref 'component' (supplementary) record must not satisfy a title-only verification.
    def g(u): return _crossref_search("Speculative Decoding for Fast Inference", typ="component")
    p = Paper(cite_key="c", title="Speculative Decoding for Fast Inference")
    verify_paper(p, get=g, today="2026-06-14")
    assert p.verified.exists is False


# ── transient errors are distinguished from a real negative ──────────────────────


def test_transient_error_is_error_status_not_notfound():
    p = Paper(cite_key="v", title="Attention Is All You Need", arxiv_id="1706.03762")
    verify_paper(p, get=_raises(429), today="2026-06-14", sleep=lambda _s: None, max_retries=2)
    assert p.verified.exists is False and p.verified.status == "error"


def test_transient_then_success_retries():
    state = {"n": 0}
    def g(u):
        state["n"] += 1
        if state["n"] == 1:
            raise urllib.error.HTTPError(u, 503, "x", {}, io.BytesIO(b""))
        return ARXIV_HIT
    p = Paper(cite_key="v", title="Attention Is All You Need", arxiv_id="1706.03762")
    verify_paper(p, get=g, today="2026-06-14", sleep=lambda _s: None, max_retries=2)
    assert p.verified.exists and p.verified.status == "verified"


# ── summary ──────────────────────────────────────────────────────────────────────


def test_verify_all_breakdown():
    papers = [
        Paper(cite_key="ok", title="Attention Is All You Need", arxiv_id="1706.03762"),
        Paper(cite_key="bad", title="Imaginary Work", arxiv_id="2401.99999"),
        Paper(cite_key="weak", title="Speculative Decoding for Fast Inference"),
    ]
    def g(u):
        if "export.arxiv" in u:
            return ARXIV_HIT if "1706.03762" in u else ARXIV_MISS
        return _crossref_search("Speculative Decoding for Fast Inference")
    s = verify_all(papers, get=g, today="2026-06-14", sleep=lambda _s: None)
    assert s["verified"] == 1 and s["rejected"] == ["bad"] and s["unconfirmed"] == ["weak"]


# ── live ─────────────────────────────────────────────────────────────────────────


@pytest.mark.network
def test_real_arxiv_verifies_and_fakes_rejected_live():
    real = Paper(cite_key="v", title="Attention Is All You Need", arxiv_id="1706.03762")
    verify_paper(real, today="2026-06-14")
    assert real.verified.exists is True
    for t in ["Speculative Decoding for Efficient Inference", "Language Models", "Deep Learning"]:
        fake = Paper(cite_key="FAKE", title=t)
        verify_paper(fake, today="2026-06-14")
        assert fake.verified.exists is False, f"LAUNDERED: {t} -> {fake.verified.canonical_title}"
