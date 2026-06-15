from kp_build.falsify import parse_citations, score_citations, verdict, make_prompts


def test_parse_citations():
    ans = ("Related work ...\n\n## Citations\n"
           "2211.17192 | Fast Inference from Transformers via Speculative Decoding\n"
           "- 1706.03762 | Attention Is All You Need\n")
    cites = parse_citations(ans)
    assert ("2211.17192", "Fast Inference from Transformers via Speculative Decoding") in cites
    assert ("1706.03762", "Attention Is All You Need") in cites


def test_parse_citations_doi_edge_cases():
    # a non-CS (DOI-heavy) regression: a DOI's 'YYYY.NNNNN' tail must NOT be mis-read as an arXiv id,
    # and a DOI with internal parens (Lancet 'S0140-6736(YY)…') must be captured whole.
    h = [x for x, _ in parse_citations("STEP-8 (10.1001/jama.2021.23619) and oral (10.1016/s0140-6736(23)01185-6).")]
    assert "10.1001/jama.2021.23619" in h and "10.1016/s0140-6736(23)01185-6" in h
    assert "2021.23619" not in h                 # the DOI tail is NOT a separate (fake) arXiv cite
    h2 = [x for x, _ in parse_citations("see arXiv:2503.01840 and 10.1056/nejmoa2032183")]
    assert "2503.01840" in h2 and "10.1056/nejmoa2032183" in h2    # genuine arXiv id still parsed alongside a DOI
    # an em-dash (or trailing prose) attached to a DOI must not be swallowed into the handle
    h3 = [x for x, _ in parse_citations("GI events (10.1111/dom.14551)—and discontinuation")]
    assert h3 == ["10.1111/dom.14551"]


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


# ── strict id↔title matching: a real id with the WRONG paper's title is a mislabel ──

def test_is_real_strict_title_match():
    from kp_build.falsify import _is_real
    HIT = "<feed><entry><title>Structured Denoising Diffusion Models in Discrete State Spaces</title></entry></feed>"
    g = lambda u: HIT
    # no claimed title -> existence is the floor (nothing to check against) -> real
    assert _is_real("2211.17192", "", get=g) is True
    # claimed title matches canonical (an appended annotation is tolerated) -> real
    assert _is_real("2211.17192", "Structured Denoising Diffusion Models in Discrete State Spaces (D3PM)", get=g) is True
    # real id but a DIFFERENT paper's title (the diffusion-LLM mislabel pattern) -> NOT real
    assert _is_real("2211.17192", "Simple and Effective Masked Diffusion Language Models", get=g) is False
    # a fake id that returns no entry -> not real
    assert _is_real("2499.99999", "Plausible Title", get=lambda u: "<feed></feed>") is False


def test_degenerate_title_falls_back_to_existence():
    from kp_build.falsify import _is_real
    HIT = "<feed><entry><title>Some Real Paper Title</title></entry></feed>"
    # an all-stopword / uninformative title carries no tokens to judge -> existence floor -> real
    assert _is_real("2211.17192", "the of and from", get=lambda u: HIT) is True


def test_annotation_on_short_canonical_title_is_not_a_mislabel():
    """Regression: '(LLaDA)' appended to a SHORT canonical title must not be flagged (real id, right
    paper). Requires accepting a strict match in either direction, not just claimed-covers-canonical."""
    from kp_build.falsify import _is_real
    HIT = "<feed><entry><title>Large Language Diffusion Models</title></entry></feed>"
    assert _is_real("2502.09992", "Large Language Diffusion Models (LLaDA)", get=lambda u: HIT) is True


def test_score_flags_real_id_wrong_title_mislabel():
    """The diffusion-LLM finding in miniature: a real id with the wrong paper's title is a hallucination."""
    from kp_build.falsify import score_citations
    ans = ("## Citations\n"
           "arXiv:2406.07524 — Simplified and Generalized Masked Diffusion for Discrete Data (MD4)\n"
           "arXiv:2502.09992 — Large Language Diffusion Models\n")
    canon = {"2406.07524": "Simple and Effective Masked Diffusion Language Models",
             "2502.09992": "Large Language Diffusion Models"}
    def g(u):
        for aid, t in canon.items():
            if aid in u:
                return f"<feed><entry><title>{t}</title></entry></feed>"
        return "<feed></feed>"
    rep = score_citations(ans, get=g)
    assert rep["cited"] == 2 and rep["fake"] == 1 and rep["real"] == 1
    assert "2406.07524" in rep["fake_list"][0]


def test_parse_em_dash_block_dedups_inline_mention():
    from kp_build.falsify import parse_citations
    ans = ("We build on score-entropy diffusion (arXiv:2310.16834).\n\n## Citations\n"
           "arXiv:2310.16834 — Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution\n")
    cites = parse_citations(ans)
    # ONE entry, and it keeps the title (the block wins over the bare inline mention)
    assert cites == [("2310.16834", "Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution")]


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
