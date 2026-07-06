"""Passage-presence grounding gate — the matcher, fetch, and grounding pass."""

from kp_build.ground import passage_in_text, fetch_paper_text, ground_claims, _norm
from kp_build.citations import _arxiv_abstract
from kp_build.schema import (Paper, Claim, Verification, claim_to_md, claim_from_md)


def _V():
    return Verification(exists=True, status="verified", via="arxiv", checked="2026-06-14")


# ── matcher ──────────────────────────────────────────────────────────────────────

def test_norm_collapses_case_whitespace_punct():
    assert _norm("We  observe 2-3x  SPEEDUPS!") == "we observe 2 3x speedups"


def test_passage_exact_substring_grounds():
    assert passage_in_text("we observe 2-3x speedups",
                           "In experiments, we observe 2-3x speedups across the board.")


def test_passage_near_verbatim_trailing_diff_grounds():
    # a long contiguous run with only a trailing-word difference still grounds
    assert passage_in_text("we observe two to three times speedups in inference",
                           "we observe two to three times speedups in decoding tasks")


def test_passage_misquote_mid_edit_not_grounded():
    # a WRONG number mid-passage splits the contiguous match -> not grounded (correct: it's a misquote)
    assert not passage_in_text("we observe two to four times speedups overall",
                               "we observe two to three times speedups overall in tests")


def test_passage_scattered_words_not_grounded():
    # a generic phrase whose words appear SCATTERED across the abstract must NOT ground (false-positive guard).
    # CHECKED + absent -> False (a real absence), distinct from None (couldn't check).
    assert passage_in_text("our model achieves state of the art",
                           "in this paper our system achieves strong results improving the state of the art performance") is False


def test_passage_too_short_is_none_not_false():
    # a short/generic passage can't be reliably verified -> None ("couldn't check"), never a False absence
    assert passage_in_text("clear improvements", "We show clear improvements over prior baselines.") is None
    assert passage_in_text("we show that", "we show that diffusion language models scale well.") is None


def test_passage_oversized_text_is_none():
    # a >200k-char body can't be fuzzy-scanned -> None (never a hard False that would flag a real quote)
    big = "diffusion sampling decoding strategies in fine detail again " * 5000
    assert len(big) > 200000
    assert passage_in_text("we observe a notable speedup in inference latency overall here", big) is None


def test_passage_grounds_in_long_body_above_old_cutoff():
    # a near-verbatim quote in a >30000-char body still grounds (the old 30000 cutoff would have failed it)
    filler = "We discuss diffusion sampling and decoding strategies in detail. " * 600
    body = filler + "we observe a 2.8x speedup in decoding without any quality degradation at all" + filler
    assert len(body) > 30000
    assert passage_in_text("we observe a 2.8x speedup in decoding without any quality loss whatsoever", body)


def test_passage_fabricated_not_found():
    assert not passage_in_text("the model reaches 99 percent accuracy on the imagenet benchmark",
                               "We study masked diffusion language models and their sampling.")


def test_passage_empty_inputs_are_none():
    assert passage_in_text("", "anything") is None and passage_in_text("a long enough passage here", "") is None


def test_passage_fuzzy_tampered_number_at_end_is_none():
    # a long quote with ONE tampered number near the end still clears 60% contiguity (the tamper sits
    # outside the longest block) — previously True; the digit guard must abstain -> None, not False
    assert passage_in_text("the method improves decoding throughput across all evaluated model sizes in 2019",
                           "the method improves decoding throughput across all evaluated model sizes in 2016 experiments") is None


def test_passage_exact_substring_with_numbers_still_true():
    # the digit guard is fuzzy-path-only: an exact normalized substring containing numbers stays True
    assert passage_in_text("the model reaches 87.5 percent accuracy on imagenet",
                           "in our tests the model reaches 87.5 percent accuracy on imagenet overall") is True


def test_passage_fuzzy_all_numbers_present_still_true():
    # a trailing-word fuzzy diff whose numbers ALL appear in the text still grounds
    assert passage_in_text("we observe a 2.8x speedup in decoding on the benchmark suite",
                           "we observe a 2.8x speedup in decoding on the evaluation suite overall") is True


def test_passage_fuzzy_no_numbers_unchanged_true():
    # a number-free passage never triggers the digit guard — fuzzy acceptance behaves exactly as before
    assert passage_in_text("the approach generalizes across model families without extra tuning steps",
                           "the approach generalizes across model families without any manual effort") is True


def test_passage_digit_grouping_variants_do_not_trip_the_guard():
    # '1,000' (passage) vs '1000' (text) is the SAME number in a different grouping — _norm turns the
    # comma into a space so the naive runs {'1','000'} vs {'1000'} would falsely abstain a legitimate
    # verbatim quote; the guard now matches runs against the grouping-collapsed form too, both directions
    quote = "the benchmark evaluates retrieval and reranking quality across scientific abstracts totaling {n} documents"
    assert passage_in_text(quote.format(n="1,000"), quote.format(n="1000") + " overall") is True
    assert passage_in_text(quote.format(n="1000"), quote.format(n="1,000") + " overall") is True


def test_passage_digit_grouping_collapse_does_not_rescue_a_tamper():
    # degrouping must not launder a genuinely different number: 1,000 tampered to 1,500 still abstains
    quote = "the benchmark evaluates retrieval and reranking quality across scientific abstracts totaling {n} documents"
    assert passage_in_text(quote.format(n="1,500"), quote.format(n="1,000") + " overall") is None


def test_degrouping_must_not_synthesize_a_run_from_adjacent_numbers():
    # 'figure 1' next to '500' is TWO numbers — collapsing the space between them would synthesize a
    # '1500' run and launder exactly the tamper the guard exists to catch. Only raw COMMA grouping
    # collapses; a passage claiming 1500 against a text that says '... figure 1 500 ...' abstains.
    prefix = "the benchmark evaluates retrieval and reranking quality across scientific abstracts totaling"
    assert passage_in_text(f"{prefix} 1500 documents",
                           f"{prefix} per figure 1 500 documents") is None


# ── fetch ────────────────────────────────────────────────────────────────────────

def test_arxiv_abstract_parses_summary():
    feed = "<feed><entry><title>T</title><summary>The   abstract text\nhere.</summary></entry></feed>"
    summary, err = _arxiv_abstract("2401.1", get=lambda u: feed)
    assert err == "" and summary == "The abstract text here."


def test_fetch_abstract():
    feed = "<feed><entry><title>T</title><summary>This paper studies masked diffusion language models.</summary></entry></feed>"
    text, src = fetch_paper_text(Paper(cite_key="a", title="T", arxiv_id="2401.1"), get=lambda u: feed)
    assert src == "abstract" and "masked diffusion" in text


def test_fetch_fulltext_strips_html_and_falls_back():
    body = "We observe a 2.8x speedup in decoding. " * 20            # > 500 chars after strip
    def g(u):
        if "ar5iv" in u:
            return f"<html><body><script>junk()</script><p>{body}</p></body></html>"
        return "<feed><entry><summary>fallback</summary></entry></feed>"
    text, src = fetch_paper_text(Paper(cite_key="a", title="T", arxiv_id="2401.1"), get=g, fulltext=True)
    assert src == "fulltext" and "2.8x speedup" in text and "junk" not in text


# ── grounding pass ───────────────────────────────────────────────────────────────

def test_ground_claims_against_abstract():
    p = Paper(cite_key="a", title="T", arxiv_id="2401.1", verified=_V())
    feed = "<feed><entry><summary>We observe 2-3x speedups without changing the output distribution.</summary></entry></feed>"
    claims = [Claim(id="c1", statement="s", paper="a", supporting_passage="2-3x speedups without changing the output distribution"),
              Claim(id="c2", statement="s", paper="a", supporting_passage="a fabricated quote about bananas and rockets and unicorns")]
    rep = ground_claims([p], claims, get=lambda u: feed)
    assert claims[0].grounded == "grounded"        # in the abstract
    assert claims[1].grounded == "unconfirmed"     # not in abstract (abstract-only never says 'ungrounded')
    assert rep["grounded"] == 1 and rep["unconfirmed"] == 1


def test_ground_fulltext_miss_is_ungrounded():
    p = Paper(cite_key="a", title="T", arxiv_id="2401.1", verified=_V())
    body = "We study masked diffusion sampling and decoding strategies in detail. " * 20
    def g(u):
        return f"<html><body><p>{body}</p></body></html>" if "ar5iv" in u else "<feed></feed>"
    claims = [Claim(id="c1", statement="s", paper="a", supporting_passage="the model reaches 99 percent accuracy on imagenet")]
    ground_claims([p], claims, get=g, fulltext=True)
    assert claims[0].grounded == "ungrounded"      # fulltext checked, passage absent -> real failure


def test_ground_oversized_fulltext_is_unconfirmed_not_ungrounded():
    # a >200k-char fulltext can't be fuzzy-checked -> 'unconfirmed' (soft), NEVER a false 'ungrounded'
    p = Paper(cite_key="a", title="T", arxiv_id="2401.1", verified=_V())
    big = "diffusion sampling decoding strategies in fine detail again " * 5000
    def g(u):
        return f"<html><body><p>{big}</p></body></html>" if "ar5iv" in u else "<feed></feed>"
    claims = [Claim(id="c1", statement="s", paper="a",
                    supporting_passage="we observe a notable speedup in inference latency overall here")]
    ground_claims([p], claims, get=g, fulltext=True)
    assert claims[0].grounded == "unconfirmed"


def test_arxiv_abstract_unescapes_entities():
    feed = "<feed><entry><summary>We show that x &gt; 10 holds in all cases.</summary></entry></feed>"
    summary, err = _arxiv_abstract("2401.1", get=lambda u: feed)
    assert err == "" and "x > 10" in summary and "&gt;" not in summary


def test_fetch_fulltext_unescapes_entities():
    body = "Here we prove that x &gt; y always holds in the limiting case for every input. " * 10
    def g(u):
        return f"<html><body><p>{body}</p></body></html>" if "ar5iv" in u else "<feed></feed>"
    text, src = fetch_paper_text(Paper(cite_key="a", title="T", arxiv_id="2401.1"), get=g, fulltext=True)
    assert src == "fulltext" and "x > y" in text and "&gt;" not in text


def test_cli_ground_with_no_verify_warns_and_skips(tmp_path, monkeypatch, capsys):
    import json
    import kp_build.ground as G
    from kp_build.cli import main
    inp = tmp_path / "r.json"
    inp.write_text(json.dumps({"topic": "T", "papers": [{"cite_key": "a", "title": "A", "arxiv_id": "2401.1"}],
                               "claims": [{"id": "c1", "statement": "s", "paper": "a", "supporting_passage": "a passage here"}]}),
                   encoding="utf-8")
    called = []
    monkeypatch.setattr(G, "ground_claims", lambda *a, **k: called.append(1) or {"grounded": 0, "unconfirmed": 0, "ungrounded": 0})
    main(["build", "-i", str(inp), "-o", str(tmp_path / "o"), "--no-verify", "--ground"])
    err = capsys.readouterr().err
    assert called == [] and "warn" in err and "ground" in err.lower()    # skipped + warned


def test_ground_skips_unverified_paper():
    p = Paper(cite_key="bad", title="T", verified=Verification(exists=False, status="not-found"))
    claims = [Claim(id="c1", statement="s", paper="bad", supporting_passage="anything")]
    ground_claims([p], claims, get=lambda u: "<feed></feed>")
    assert claims[0].grounded == "unchecked"       # untouched — its paper isn't verified


def test_digest_surfaces_grounded_and_caps_ungrounded():
    from kp_build.digest import build_context
    from kp_build.schema import Package
    p = Paper(cite_key="p", title="P", arxiv_id="1.1", verified=_V())
    g = Claim(id="c1", statement="A confirmed claim.", paper="p", supporting_passage="evid",
              claim_type="finding", confidence="high", grounded="grounded")
    u = Claim(id="c2", statement="An unconfirmed claim.", paper="p", supporting_passage="strong evidence here",
              claim_type="result", confidence="high", grounded="ungrounded")
    ctx = build_context(Package(topic="T", scope="s", papers=[p], claims=[g, u]), built="2026-06-14")
    assert "✓grounded" in ctx
    assert "passage not found in the paper" in ctx and "> strong evidence here" not in ctx   # capped, no quote


def test_report_shows_grounded_and_ungrounded_pills(tmp_path):
    from kp_build.assemble import assemble
    from kp_build.report import build_report
    from kp_build.schema import Package
    p = Paper(cite_key="p", title="P", arxiv_id="1.1", verified=_V())
    claims = [Claim(id="c1", statement="A.", paper="p", supporting_passage="GROUNDEDPASSAGE", grounded="grounded"),
              Claim(id="c2", statement="B.", paper="p", supporting_passage="UNGROUNDEDPASSAGE", grounded="ungrounded")]
    out = assemble(Package(topic="T", scope="s", papers=[p], claims=claims), tmp_path / "kp", built="2026-06-14")
    html = build_report(out)
    assert "✓ grounded" in html and "passage not in paper" in html
    assert 'class="row claim refuted"' in html        # the ungrounded claim gets the flagged style
    assert "GROUNDEDPASSAGE" in html                  # grounded claim's passage is shown
    assert "UNGROUNDEDPASSAGE" not in html            # ungrounded claim's passage is suppressed, not exposed


def test_cli_build_ground_wires_through(tmp_path, monkeypatch):
    import json
    import kp_build.citations as C
    import kp_build.ground as G
    from kp_build.cli import main
    from kp_build.schema import Verification
    inp = tmp_path / "r.json"
    inp.write_text(json.dumps({"topic": "T", "papers": [{"cite_key": "a", "title": "A", "arxiv_id": "2401.1"}],
                               "claims": [{"id": "c1", "statement": "s", "paper": "a", "supporting_passage": "a passage here"}]}),
                   encoding="utf-8")
    out = tmp_path / "pkg"
    monkeypatch.setattr(C, "verify_paper",
                        lambda p, **k: setattr(p, "verified", Verification(exists=True, status="verified", via="arxiv")))
    seen = {}

    def spy(papers, claims, **kw):
        seen["fulltext"] = kw.get("fulltext")
        for c in claims:
            c.grounded = "grounded"
        return {"grounded": len(claims), "unconfirmed": 0, "ungrounded": 0}

    monkeypatch.setattr(G, "ground_claims", spy)
    main(["build", "-i", str(inp), "-o", str(out), "--ground"])
    assert seen.get("fulltext") is False
    seen.clear()
    main(["build", "-i", str(inp), "-o", str(out), "--ground-fulltext"])     # implies --ground
    assert seen.get("fulltext") is True


def test_claim_grounded_roundtrips():
    c = Claim(id="c1", statement="s", paper="p", supporting_passage="x", grounded="grounded")
    assert claim_from_md(claim_to_md(c)).grounded == "grounded"
    assert claim_from_md(claim_to_md(Claim(id="c2", statement="s", paper="p",
                                           supporting_passage="x"))).grounded == "unchecked"
