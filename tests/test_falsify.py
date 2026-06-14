from kp_build.falsify import parse_citations, score_citations, verdict, make_prompts


def test_parse_citations():
    ans = ("Related work ...\n\n## Citations\n"
           "2211.17192 | Fast Inference from Transformers via Speculative Decoding\n"
           "- 1706.03762 | Attention Is All You Need\n")
    cites = parse_citations(ans)
    assert ("2211.17192", "Fast Inference from Transformers via Speculative Decoding") in cites
    assert ("1706.03762", "Attention Is All You Need") in cites


def test_score_citations_flags_fakes_mocked():
    ans = ("## Citations\n"
           "2211.17192 | Fast Inference from Transformers via Speculative Decoding\n"
           "2499.99999 | A Fabricated Paper\n")
    HIT = "<entry><title>Fast Inference from Transformers via Speculative Decoding</title></entry>"
    MISS = "<feed></feed>"
    def fake_get(u):
        return HIT if "2211.17192" in u else MISS
    rep = score_citations(ans, get=fake_get)
    assert rep["cited"] == 2 and rep["real"] == 1 and rep["fake"] == 1
    assert rep["hallucination_rate"] == 0.5


def test_verdict_kp_helps():
    base = {"cited": 4, "real": 2, "fake": 2, "hallucination_rate": 0.5}
    kp = {"cited": 4, "real": 4, "fake": 0, "hallucination_rate": 0.0}
    v = verdict(base, kp)
    assert "KP HELPS" in v


def test_make_prompts_injects_context(tmp_path):
    (tmp_path / "CONTEXT.md").write_text("# Field briefing\nverified papers here", encoding="utf-8")
    p = make_prompts(tmp_path, "speculative decoding")
    assert "FIELD BRIEFING" in p["kp"] and "verified papers here" in p["kp"]
    assert "speculative decoding" in p["base"] and "FIELD BRIEFING" not in p["base"]


# ── P0-4: id resolves = real regardless of human title; recall/f1 ───────────────

def test_is_real_id_resolves_regardless_of_title():
    from kp_build.falsify import _is_real
    HIT = "<feed><entry><title>Whatever Canonical Title</title></entry></feed>"
    # arxiv id resolves -> real even though the cited title is blank or different
    assert _is_real("2211.17192", "", get=lambda u: HIT) is True
    assert _is_real("2211.17192", "A Completely Different Human Title", get=lambda u: HIT) is True
    # a fake id that returns no entry -> not real
    assert _is_real("2499.99999", "Plausible Title", get=lambda u: "<feed></feed>") is False


def test_score_answer_recall_and_f1():
    from kp_build.falsify import score_answer
    spine = [{"arxiv_id": "2211.17192", "cite_key": "a"}, {"arxiv_id": "1706.03762", "cite_key": "b"}]
    ans = "## Citations\n2211.17192 | X\n"   # cites 1 of 2 spine papers
    HIT = "<feed><entry><title>X</title></entry></feed>"
    rep = score_answer(ans, spine=spine, get=lambda u: HIT)
    assert rep["spine_covered"] == 1 and rep["recall"] == 0.5 and rep["precision"] == 1.0
    assert rep["f1"] == round(2 * 1.0 * 0.5 / 1.5, 3)


def test_parse_inline_ids_without_pipe_block():
    from kp_build.falsify import parse_citations
    ans = "As shown in arXiv:2211.17192 and 1706.03762, and doi 10.1145/3292500.3330701, speculation works."
    handles = {h for h, _ in parse_citations(ans)}
    assert "2211.17192" in handles and "1706.03762" in handles
    assert any("10.1145/3292500.3330701" in h for h in handles)
