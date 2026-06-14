import pytest
from kp_build.citations import titles_match, verify_paper, verify_all
from kp_build.schema import Paper


def test_titles_match():
    assert titles_match("Attention Is All You Need", "Attention is all you need")
    assert titles_match("Speculative Decoding", "Fast Inference via Speculative Decoding")  # contains
    assert not titles_match("Attention Is All You Need", "A Survey of Reinforcement Learning")


# ── mocked HTTP (no network) ─────────────────────────────────────────────────────

ARXIV_HIT = "<feed><entry><title>Attention Is All You Need</title></entry></feed>"
ARXIV_MISS = "<feed></feed>"
CROSSREF_DOI = '{"message":{"title":["Optuna: A Next-generation Hyperparameter Optimization Framework"]}}'
CROSSREF_SEARCH = '{"message":{"items":[{"title":["Speculative Decoding for Fast Inference"],"DOI":"10.1/abc"}]}}'


def test_verify_via_arxiv():
    p = Paper(cite_key="v", title="Attention Is All You Need", arxiv_id="1706.03762")
    verify_paper(p, get=lambda u: ARXIV_HIT, today="2026-06-14")
    assert p.verified.exists and p.verified.via == "arxiv"
    assert p.url == "https://arxiv.org/abs/1706.03762"


def test_arxiv_miss_then_unverified():
    p = Paper(cite_key="fake", title="A Nonexistent Paper", arxiv_id="2401.99999")
    verify_paper(p, get=lambda u: ARXIV_MISS, today="2026-06-14")
    assert p.verified.exists is False and p.verified.via == "unverified"


def test_arxiv_title_mismatch_rejected():
    # The id resolves, but to a DIFFERENT paper than claimed -> not verified as this cite.
    p = Paper(cite_key="x", title="Totally Different Title About Cats", arxiv_id="1706.03762")
    verify_paper(p, get=lambda u: ARXIV_HIT, today="2026-06-14")
    assert p.verified.exists is False


def test_verify_via_crossref_doi():
    p = Paper(cite_key="optuna", title="Optuna: A Next-generation Hyperparameter Optimization Framework",
              doi="10.1145/3292500.3330701")
    verify_paper(p, get=lambda u: CROSSREF_DOI, today="2026-06-14")
    assert p.verified.exists and p.verified.via == "crossref"


def test_verify_via_title_search_backfills_doi():
    p = Paper(cite_key="spec", title="Speculative Decoding for Fast Inference")
    verify_paper(p, get=lambda u: CROSSREF_SEARCH, today="2026-06-14")
    assert p.verified.exists and p.verified.via == "crossref" and p.doi == "10.1/abc"


def test_verify_all_summary():
    papers = [
        Paper(cite_key="ok", title="Attention Is All You Need", arxiv_id="1706.03762"),
        Paper(cite_key="bad", title="Imaginary Work", arxiv_id="2401.99999"),
    ]
    def fake(u):
        return ARXIV_HIT if "1706.03762" in u else ARXIV_MISS
    summary = verify_all(papers, get=fake, today="2026-06-14")
    assert summary["verified"] == 1 and summary["unverified"] == ["bad"]


@pytest.mark.network
def test_real_arxiv_live():
    p = Paper(cite_key="v", title="Attention Is All You Need", arxiv_id="1706.03762")
    verify_paper(p, today="2026-06-14")
    assert p.verified.exists is True
