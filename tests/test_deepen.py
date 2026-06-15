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


def test_expand_continues_past_a_transient_seed():
    # one seed's expansion fails transiently; the other seeds must still aggregate (no raise)
    def g(u):
        if "BADSEED" in u:
            raise urllib.error.HTTPError(u, 503, "rate", {}, None)
        return S2_REFS
    cands = expand(["BADSEED", "2402.12374"], get=g, directions=("references",), sleep=lambda *_: None)
    keys = {(c["arxiv_id"] or c["doi"] or c["title"]) for c in cands}
    assert cands and ("2001.00001" in keys or "No Ids" in keys)   # good seed's candidates survived


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


def test_load_survived_refuter_null_defaults_true(tmp_path):
    # explicit JSON null must behave like an absent key (default True), not silently demote the claim
    p = tmp_path / "r.json"
    p.write_text(json.dumps({"topic": "T", "papers": [{"cite_key": "a", "title": "A", "arxiv_id": "1.1"}],
                             "claims": [{"id": "c1", "statement": "s", "paper": "a", "survived_refuter": None}]}),
                 encoding="utf-8")
    assert _load(str(p)).claims[0].survived_refuter is True


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
    assert sleeps2 == []        # no throttle and no retries on clean hits -> zero sleeps


def test_verify_all_adaptive_backoff_then_recovers(monkeypatch):
    import kp_build.citations as C
    from kp_build.schema import Verification
    # p0,p1 come back 'error' (rate-limited), p2,p3 verify -> throttle ramps on errors, decays on success
    seq = iter(["error", "error", "verified", "verified"])
    monkeypatch.setattr(C, "verify_paper",
                        lambda p, **k: setattr(p, "verified", Verification(exists=(s := next(seq)) == "verified", status=s)))
    papers = [Paper(cite_key=f"p{i}", title="T") for i in range(4)]
    sleeps = []
    C.verify_all(papers, sleep=lambda s: sleeps.append(s), throttle=0.5)
    assert sleeps == [1.0, 2.0, 1.0]           # 0.5->1.0 (err) ->2.0 (err) ->1.0 (ok, decaying); last: no sleep


def test_verify_all_skip_verified_rechecks_only_errors(monkeypatch):
    import kp_build.citations as C
    from kp_build.schema import Verification
    checked = []
    monkeypatch.setattr(C, "verify_paper",
                        lambda p, **k: (checked.append(p.cite_key), setattr(p, "verified", Verification(exists=True, status="verified"))))
    papers = [Paper(cite_key="a", title="A", verified=Verification(exists=True, status="verified")),
              Paper(cite_key="b", title="B", verified=Verification(exists=False, status="error"))]
    rep = C.verify_all(papers, sleep=lambda s: None, skip_verified=True)
    assert checked == ["b"] and rep["verified"] == 2     # 'a' kept (no network), 'b' re-checked -> verified


def test_verify_all_throttle_caps_at_max(monkeypatch):
    import kp_build.citations as C
    from kp_build.schema import Verification
    monkeypatch.setattr(C, "verify_paper", lambda p, **k: setattr(p, "verified", Verification(exists=False, status="error")))
    papers = [Paper(cite_key=f"p{i}", title="T") for i in range(6)]
    sleeps = []
    C.verify_all(papers, sleep=lambda s: sleeps.append(s), throttle=1.0, max_throttle=4.0)
    assert sleeps == [2.0, 4.0, 4.0, 4.0, 4.0] and max(sleeps) == 4.0     # backoff doubles then holds at the cap


def test_verify_all_throttle_zero_decays_back_to_zero(monkeypatch):
    import kp_build.citations as C
    from kp_build.schema import Verification
    seq = iter(["error", "verified", "verified", "verified"])
    monkeypatch.setattr(C, "verify_paper",
                        lambda p, **k: setattr(p, "verified", Verification(exists=(s := next(seq)) == "verified", status=s)))
    papers = [Paper(cite_key=f"p{i}", title="T") for i in range(4)]
    sleeps = []
    C.verify_all(papers, sleep=lambda s: sleeps.append(s), throttle=0.0)
    assert sleeps == [2.0]            # error bumps to 2.0 once, then recovery returns to 0 (no sticky sleep)


def _spy_verify(hits):
    # a stub standing in for a REAL index verification (via="arxiv"), recording every paper it checks
    from kp_build.schema import Verification
    return lambda p, **k: (hits.append(p.cite_key),
                           setattr(p, "verified", Verification(exists=True, status="verified", via="arxiv")))


def test_cli_reuse_verification_skips_and_reverifies_changed_identity(tmp_path, monkeypatch):
    import json
    import kp_build.citations as C
    from kp_build.cli import main
    inp = tmp_path / "r.json"

    def write(papers):
        inp.write_text(json.dumps({"topic": "T", "papers": papers}), encoding="utf-8")

    write([{"cite_key": "a", "title": "Paper A", "arxiv_id": "2401.00001"},
           {"cite_key": "b", "title": "Paper B", "arxiv_id": "2401.00002"}])
    out = tmp_path / "pkg"
    hits = []
    monkeypatch.setattr(C, "verify_paper", _spy_verify(hits))
    assert main(["build", "-i", str(inp), "-o", str(out)]) == 0    # first REAL verify -> both checked
    assert sorted(hits) == ["a", "b"]
    hits.clear()
    # unchanged input -> both reused (via=arxiv), ZERO network checks
    main(["build", "-i", str(inp), "-o", str(out), "--reuse-verification"])
    assert hits == []
    # change a's identity (same cite_key, new id+title) -> a MUST be re-checked, not inherit the stale verdict
    write([{"cite_key": "a", "title": "A Different Paper", "arxiv_id": "2401.99999"},
           {"cite_key": "b", "title": "Paper B", "arxiv_id": "2401.00002"}])
    hits.clear()
    main(["build", "-i", str(inp), "-o", str(out), "--reuse-verification"])
    assert hits == ["a"]             # a re-verified (identity changed); b reused (unchanged)


def test_reuse_verification_does_not_reuse_unchecked_no_verify_stamps(tmp_path, monkeypatch):
    # a --no-verify build stamps via="(unchecked)"; --reuse-verification must NOT treat those as
    # verified-and-reusable — an unchecked paper gets a real re-check, never masquerading as verified.
    import json
    import kp_build.citations as C
    from kp_build.cli import main
    inp = tmp_path / "r.json"
    inp.write_text(json.dumps({"topic": "T", "papers": [
        {"cite_key": "a", "title": "A", "arxiv_id": "2401.00001"},
        {"cite_key": "b", "title": "B", "arxiv_id": "2401.00002"}]}), encoding="utf-8")
    out = tmp_path / "pkg"
    assert main(["build", "-i", str(inp), "-o", str(out), "--no-verify"]) == 0   # via="(unchecked)"
    hits = []
    monkeypatch.setattr(C, "verify_paper", _spy_verify(hits))
    main(["build", "-i", str(inp), "-o", str(out), "--reuse-verification"])
    assert sorted(hits) == ["a", "b"]     # unchecked stamps not reused -> both really checked


def test_score_citations_throttles_between_cites():
    from kp_build.falsify import score_citations
    ans = "## Citations\n2211.17192 | A\n2310.16834 | B\n2401.00001 | C\n"
    sleeps = []
    score_citations(ans, get=lambda u: "<feed></feed>", throttle=0.3, sleep=lambda s: sleeps.append(s))
    assert sleeps == [0.3, 0.3]                 # one pause between each of the 3 cites


def test_report_marks_refuted_claim_and_survey_depth(tmp_path):
    p = Paper(cite_key="p", title="P", arxiv_id="1.1", verified=_V())
    c = Claim(id="c1", statement="A claim.", paper="p", supporting_passage="x", survived_refuter=False)
    pkg = Package(topic="T", scope="s", papers=[p], claims=[c], coverage={"papers_via_expansion": 4})
    out = assemble(pkg, tmp_path / "kp", built="2026-06-14")
    html = build_report(out)
    assert "refuter broke this" in html and 'class="row claim refuted"' in html
    assert "found via citation-graph expansion" in html
