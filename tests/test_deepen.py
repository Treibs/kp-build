"""Step-3 tests: citation-graph expansion + refuter support."""

import json
import urllib.error

from kp_build.expand import neighbors, expand, _paper_path
from kp_build.schema import (Package, Paper, Claim, Verification, claim_to_md, claim_from_md)
from kp_build.assemble import assemble
from kp_build.digest import build_context
from kp_build.report import build_report
from kp_build.cli import _load


S2_REFS = json.dumps({"data": [
    {"citedPaper": {"title": "Seed Ref", "year": 2020, "externalIds": {"ArXiv": "2001.00001", "DOI": "10.1/x"}}},
    {"citedPaper": {"title": "No Ids", "year": 2019, "externalIds": {}}},
]})


# ── citation-graph expansion ─────────────────────────────────────────────────────────

def test_paper_path_arxiv_and_doi():
    assert _paper_path("arXiv:2211.17192") == "arXiv:2211.17192"
    assert _paper_path("2211.17192") == "arXiv:2211.17192"
    assert _paper_path("10.1145/x.y") == "DOI:10.1145/x.y"


def test_neighbors_parses_references():
    cands, err = neighbors("2211.17192", get=lambda u: S2_REFS, direction="references")
    assert err == ""
    assert {"title": "Seed Ref", "year": 2020, "arxiv_id": "2001.00001", "doi": "10.1/x",
            "via": "references"} in cands
    assert any(c["title"] == "No Ids" and c["arxiv_id"] == "" for c in cands)


def test_neighbors_hits_right_url():
    seen = {}
    def g(u):
        seen["url"] = u
        return S2_REFS
    neighbors("arXiv:2211.17192", get=g, direction="citations", limit=10)
    assert "arXiv:2211.17192/citations" in seen["url"] and "limit=10" in seen["url"]


def test_expand_dedups_and_skips():
    cands = expand(["2211.17192", "2402.12374"], get=lambda u: S2_REFS,
                   directions=("references",), skip=["arXiv:2001.00001"])
    keys = [(c["arxiv_id"] or c["doi"] or c["title"]) for c in cands]
    assert "2001.00001" not in keys                 # already in the package -> skipped
    assert keys.count("No Ids") == 1                 # deduped across the two seeds


def test_neighbors_transient_is_distinguished():
    def boom(u): raise urllib.error.HTTPError(u, 503, "down", {}, None)
    cands, err = neighbors("2211.17192", get=boom, sleep=lambda *_: None, max_retries=1)
    assert cands == [] and err == "transient"


def test_neighbors_malformed_json_is_empty_not_crash():
    cands, err = neighbors("2211.17192", get=lambda u: "{not json", direction="references")
    assert cands == [] and err == ""


# ── refuter support ──────────────────────────────────────────────────────────────────

def test_claim_survived_refuter_roundtrip():
    c = Claim(id="c1", statement="s", paper="p", supporting_passage="x", survived_refuter=False)
    assert claim_from_md(claim_to_md(c)).survived_refuter is False
    assert claim_from_md(claim_to_md(Claim(id="c2", statement="s", paper="p",
                                           supporting_passage="x"))).survived_refuter is True


def test_load_accepts_survived_refuter(tmp_path):
    p = tmp_path / "r.json"
    p.write_text(json.dumps({"topic": "T", "papers": [{"cite_key": "a", "title": "A", "arxiv_id": "1.1"}],
                             "claims": [{"id": "c1", "statement": "s", "paper": "a", "survived_refuter": False}]}),
                 encoding="utf-8")
    assert _load(str(p)).claims[0].survived_refuter is False


def _V():
    return Verification(exists=True, status="verified", via="arxiv", checked="2026-06-14")


def test_digest_caps_and_flags_refuted_claim():
    p = Paper(cite_key="p", title="P", arxiv_id="1.1", verified=_V())
    c = Claim(id="c1", statement="Big result.", paper="p", supporting_passage="strong evidence",
              claim_type="result", confidence="high", survived_refuter=False)
    ctx = build_context(Package(topic="T", scope="s", papers=[p], claims=[c]), built="2026-06-14")
    assert "refuter broke this" in ctx and "low" in ctx
    assert "> strong evidence" not in ctx          # a broken claim does not get the high-conf passage


def test_verify_all_throttles_between_papers():
    # a deepened (large) package must not burst past the rate limit -> throttle sleeps between papers
    from kp_build.citations import verify_all
    papers = [Paper(cite_key=f"p{i}", title="Test Paper Title", arxiv_id="2401.00001") for i in range(3)]
    sleeps = []
    HIT = "<feed><entry><title>Test Paper Title</title></entry></feed>"
    verify_all(papers, get=lambda u: HIT, today="2026-06-14", sleep=lambda s: sleeps.append(s), throttle=0.4)
    assert sleeps.count(0.4) == 2          # one throttle pause between each adjacent pair (n-1)
    # default throttle=0.0 must NOT add sleeps (keeps existing behavior / fast tests)
    sleeps2 = []
    verify_all(papers, get=lambda u: HIT, today="2026-06-14", sleep=lambda s: sleeps2.append(s))
    assert 0.4 not in sleeps2


def test_report_marks_refuted_claim_and_survey_depth(tmp_path):
    p = Paper(cite_key="p", title="P", arxiv_id="1.1", verified=_V())
    c = Claim(id="c1", statement="A claim.", paper="p", supporting_passage="x", survived_refuter=False)
    pkg = Package(topic="T", scope="s", papers=[p], claims=[c], coverage={"papers_via_expansion": 4})
    out = assemble(pkg, tmp_path / "kp", built="2026-06-14")
    html = build_report(out)
    assert "refuter broke this" in html and 'class="row claim refuted"' in html
    assert "found via citation-graph expansion" in html
