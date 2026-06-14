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
