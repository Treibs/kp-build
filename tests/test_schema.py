from kp_build.schema import (
    Claim, Debate, OpenProblem, Paper, Position, Verification, slugify,
    paper_to_md, paper_from_md, claim_to_md, claim_from_md,
    problem_to_md, problem_from_md, debate_to_md, debate_from_md,
)


def test_slugify_deterministic():
    assert slugify("Speculative Decoding for LLMs!") == "speculative-decoding-for-llms"
    assert slugify("") == "node"


def test_paper_roundtrip():
    p = Paper(cite_key="vaswani2017", title="Attention Is All You Need",
              authors=["Vaswani", "Shazeer"], year=2017, venue="NeurIPS",
              arxiv_id="1706.03762", url="https://arxiv.org/abs/1706.03762",
              verified=Verification(exists=True, via="arxiv", canonical_title="Attention Is All You Need", checked="2026-06-14"),
              key_contributions=["the Transformer", "self-attention"])
    back = paper_from_md(paper_to_md(p))
    assert back == p
    assert back.verified.exists is True and back.verified.via == "arxiv"


def test_claim_roundtrip_and_body_has_passage_and_link():
    c = Claim(id="c1", statement="X improves Y.", paper="vaswani2017",
              supporting_passage="X improves Y by 2 points.", claim_type="result",
              confidence="high", corroborated_by=["smith2020"])
    md = claim_to_md(c)
    assert "X improves Y by 2 points." in md and "[[papers/vaswani2017]]" in md
    assert claim_from_md(md) == c


def test_open_problem_roundtrip():
    op = OpenProblem(id="p1", statement="Z is unsolved.", flagged_by=["vaswani2017", "smith2020"],
                     status="open", why_it_matters="It blocks scaling.")
    md = problem_to_md(op)
    assert "[[papers/vaswani2017]]" in md and "blocks scaling" in md
    assert problem_from_md(md) == op


def test_debate_roundtrip():
    d = Debate(id="d1", question="Does A beat B?",
               positions=[Position(stance="A wins", papers=["x2021"], summary="A is faster."),
                          Position(stance="B wins", papers=["y2022"], summary="B is more accurate.")],
               resolved=False)
    back = debate_from_md(debate_to_md(d))
    assert back == d
    assert len(back.positions) == 2 and back.positions[0].papers == ["x2021"]
