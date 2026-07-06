"""Regression tests pinning hardening fixes: transient-vs-fabrication scoring, path-safe cite keys,
spine-id normalization, HTML-escaped reports, clean CLI failure modes on bad input, f1-based verdicts
(incl. the total-outage INCONCLUSIVE), and assemble() input immutability."""

import json
import urllib.error

import pytest

from kp_build.cli import _load, main, ResearchInputError
from kp_build.falsify import parse_citations, score_citations, score_answer, _is_real, verdict
from kp_build.assemble import assemble
from kp_build.validate import validate
from kp_build.report import build_report
from kp_build.schema import (Package, Paper, Claim, OpenProblem, Debate, Position, Benchmark,
                             Verification)


def V(exists=True, status="verified"):
    return Verification(exists=exists, status=status, via="arxiv", checked="2026-06-14")


def _pkg(topic="Speculative decoding"):
    papers = [Paper(cite_key="ok", title="Ok Paper", year=2024, arxiv_id="2401.0001", verified=V()),
              Paper(cite_key="bad", title="Bad", verified=V(False, "not-found"))]
    return Package(
        topic=topic, scope="s", papers=papers,
        claims=[Claim(id="c1", statement="X.", paper="ok", supporting_passage="p",
                      claim_type="result", confidence="high", corroborated_by=["ok", "bad"])],
        open_problems=[OpenProblem(id="o1", statement="gap", flagged_by=["ok", "bad"], why_it_matters="m")],
        debates=[Debate(id="d1", question="q?", positions=[Position("A", ["ok", "bad"], "s")])],
        benchmarks=[Benchmark(id="b1", name="bench", method="M", value="1x", paper="ok")],
        coverage={"queries": ["q"]})


def _write(tmp, obj):
    p = tmp / "r.json"; p.write_text(json.dumps(obj), encoding="utf-8"); return str(p)


# ── a transient API error must NOT be scored as a fabrication ────────────────────────

def test_is_real_transient_returns_none():
    def boom(u): raise urllib.error.HTTPError(u, 429, "rate", {}, None)
    assert _is_real("2211.17192", "Some Title", get=boom, sleep=lambda *_: None, max_retries=1) is None


def test_score_citations_excludes_unreachable(monkeypatch):
    import kp_build.falsify as F
    ans = "## Citations\n2211.17192 | Real Paper\n2499.99999 | Unreachable\n"
    monkeypatch.setattr(F, "_is_real", lambda h, t, get, **kw: True if "2211.17192" in h else None)
    rep = F.score_citations(ans, get=lambda u: "")
    assert rep["cited"] == 2 and rep["checked"] == 1 and rep["unresolved"] == 1
    assert rep["real"] == 1 and rep["fake"] == 0 and rep["precision"] == 1.0   # not deflated by the 429


# ── a cite_key with path-unsafe chars is a clean error, not a FileNotFoundError ──────

def test_cite_key_with_slash_is_clean_error(tmp_path):
    with pytest.raises(ResearchInputError) as e:
        _load(_write(tmp_path, {"topic": "T", "papers": [{"cite_key": "openai/2023", "title": "X", "arxiv_id": "1.1"}]}))
    assert "unsafe characters" in str(e.value)


def test_build_with_unsafe_cite_key_exits_clean(tmp_path):
    inp = _write(tmp_path, {"topic": "T", "papers": [{"cite_key": "a/b", "title": "X", "arxiv_id": "1.1"}]})
    rc = main(["build", "-i", inp, "-o", str(tmp_path / "o"), "--no-verify"])
    assert rc == 2 and not (tmp_path / "o").exists()


# ── a spine arxiv_id with an 'arXiv:' prefix still counts toward recall ──────────────

def test_prefixed_spine_id_is_covered():
    spine = [{"arxiv_id": "arXiv:2211.17192", "cite_key": "a"}]
    seen = {}
    def g(u):
        seen["url"] = u
        return "<feed><entry><title>X</title></entry></feed>"
    rep = score_answer("## Citations\n2211.17192 | X\n", spine=spine, get=g)
    assert "2211.17192" in seen["url"]                       # the normalized id actually hit the URL
    assert rep["spine_covered"] == 1 and rep["recall"] == 1.0


# ── manifest-derived values are HTML-escaped in the report ───────────────────────────

def test_report_escapes_manifest_stat_and_scorecard_values(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    man = json.loads((out / "wikillm.json").read_text())
    man["stats"]["papers_verified"] = "<script>alert(1)</script>"
    man["falsification"] = {"run": True, "verdict": "KP HELPS",
                            "base": {"spine_covered": "<img src=x onerror=alert(1)>", "spine_size": 19},
                            "kp": {"spine_covered": 16, "spine_size": 19}}
    (out / "wikillm.json").write_text(json.dumps(man), encoding="utf-8")
    html = build_report(out)
    assert "<script>alert(1)</script>" not in html and "<img src=x onerror=alert(1)>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html


# ── an ordered-list arXiv citation is a single, titled entry (not double-counted) ────

def test_ordered_list_arxiv_cite_single_entry():
    cites = parse_citations("## Citations\n1. 1706.03762 | Attention Is All You Need\n")
    assert cites == [("1706.03762", "Attention Is All You Need")]


# ── passing a file where a package dir is expected exits cleanly ─────────────────────

def test_report_on_nondir_exits_clean(tmp_path):
    f = tmp_path / "pkg.json"; f.write_text("{}", encoding="utf-8")
    assert main(["report", str(f)]) == 2          # NotADirectoryError caught by the backstop


# ── a bad --name fails fast, before the slow verify/assemble ─────────────────────────

def test_bad_name_fails_before_build(tmp_path):
    inp = _write(tmp_path, {"topic": "T", "papers": [{"cite_key": "a", "title": "A", "arxiv_id": "1.1"}]})
    rc = main(["build", "-i", inp, "-o", str(tmp_path / "o"), "--no-verify", "--name", "Bad Name!"])
    assert rc == 2 and not (tmp_path / "o").exists()


# ── validate flags a path-unsafe files glob in knowledge.json ────────────────────────

def test_validate_flags_unsafe_files_glob(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    kj = json.loads((out / "knowledge.json").read_text())
    kj["files"] = ["../../etc/passwd"]
    (out / "knowledge.json").write_text(json.dumps(kj), encoding="utf-8")
    r = validate(out)
    assert not r.ok and any("safe relative path" in e for e in r.errors)


# ── verdict() uses the f1 branch when f1 values are present ──────────────────────────

def test_verdict_f1_branch():
    base = {"cited": 8, "f1": 0.37, "precision": 0.62, "recall": 0.26, "fake": 3, "hallucination_rate": 0.375}
    kp = {"cited": 16, "f1": 0.91, "precision": 1.0, "recall": 0.84, "fake": 0, "hallucination_rate": 0.0}
    v = verdict(base, kp)
    assert "HELPS" in v and "0.37" in v and "0.91" in v
    assert "DID NOT HELP" in verdict(base, {**kp, "f1": 0.20})


# ── a version-suffixed DOI must normalize identically on both sides ──────────────────

def test_norm_handle_keeps_doi_strips_only_arxiv_version():
    from kp_build.falsify import _norm_handle
    assert _norm_handle("10.1234/datasetv2") == "10.1234/datasetv2"   # DOI 'v2' is part of the id
    assert _norm_handle("arXiv:2211.17192v3") == "2211.17192"          # arXiv vN IS a version


def test_doi_version_suffix_still_covers_spine():
    rep = score_answer("## Citations\n10.1234/datasetv2 | X\n",
                       spine=[{"doi": "10.1234/datasetv2", "cite_key": "a"}],
                       get=lambda u: '{"message":{"title":["X"]}}')
    assert rep["spine_covered"] == 1 and rep["recall"] == 1.0


# ── total index outage -> inconclusive verdict, not a deflated "TIE" ─────────────────

def test_verdict_inconclusive_when_nothing_checkable():
    base = {"cited": 3, "checked": 0, "precision": 0.0, "hallucination_rate": 0.0, "f1": None, "recall": 1.0}
    kp = {"cited": 3, "checked": 3, "precision": 1.0, "hallucination_rate": 0.0, "f1": 0.9, "recall": 0.9}
    assert "INCONCLUSIVE" in verdict(base, kp)


# ── assemble() must not mutate the caller's input dataclasses ────────────────────────

def test_assemble_does_not_mutate_input(tmp_path):
    pkg = _pkg()
    c, op, d = pkg.claims[0], pkg.open_problems[0], pkg.debates[0]
    assemble(pkg, tmp_path / "kp", built="2026-06-14")
    assert c.corroborated_by == ["ok", "bad"]                # 'bad' not pruned off the INPUT
    assert op.flagged_by == ["ok", "bad"]
    assert d.positions[0].papers == ["ok", "bad"]
