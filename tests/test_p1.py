import json

import pytest

from kp_build.schema import (Package, Paper, Claim, OpenProblem, Debate, Position, Benchmark,
                             Verification)
from kp_build.assemble import assemble
from kp_build.validate import validate
from kp_build.digest import build_context
from kp_build.cli import _load, ResearchInputError


def V():
    return Verification(exists=True, status="verified", via="arxiv", checked="2026-06-14")


# ── P1-a: input robustness ───────────────────────────────────────────────────────


def _write(tmp, obj):
    p = tmp / "r.json"
    p.write_text(json.dumps(obj), encoding="utf-8")
    return str(p)


def test_load_aggregates_errors(tmp_path):
    bad = {"topic": "T", "papers": [
        {"cite_key": "a", "title": "A", "year": "twenty"},
        {"cite_key": "a", "title": "dup"}],
        "claims": [{"id": "c1", "statement": "s", "paper": "ghost"}],
        "open_problems": [{"id": "o1", "statement": "x", "flagged_by": []}]}
    with pytest.raises(ResearchInputError) as e:
        _load(_write(tmp_path, bad))
    msg = str(e.value)
    assert "duplicate cite_key 'a'" in msg and "year 'twenty'" in msg
    assert "undefined cite_key 'ghost'" in msg and "flagged_by is empty" in msg


def test_load_coerces_year_and_parses_benchmarks(tmp_path):
    good = {"topic": "T", "papers": [{"cite_key": "a", "title": "A", "year": "2023", "arxiv_id": "2301.1"}],
            "benchmarks": [{"id": "b1", "name": "spd", "method": "X", "value": "2.8x", "paper": "a"}],
            "coverage": {"queries": ["q1"]}}
    pkg = _load(_write(tmp_path, good))
    assert pkg.papers[0].year == 2023
    assert pkg.benchmarks[0].value == "2.8x" and pkg.coverage["queries"] == ["q1"]


def test_load_bad_json_is_clean_error(tmp_path):
    p = tmp_path / "r.json"; p.write_text("{not json", encoding="utf-8")
    with pytest.raises(ResearchInputError):
        _load(str(p))


# ── P1-b: assemble integrity ─────────────────────────────────────────────────────


def _pkg():
    papers = [Paper(cite_key="ok", title="Ok", year=2024, arxiv_id="2401.1", verified=V()),
              Paper(cite_key="ok2", title="Ok2", year=2022, arxiv_id="2201.1", verified=V()),
              Paper(cite_key="bad", title="Bad", verified=Verification(exists=False, status="not-found"))]
    return Package(
        topic="T", scope="s", papers=papers,
        claims=[Claim(id="c1", statement="X.", paper="ok", supporting_passage="X happens.",
                      claim_type="result", confidence="high", corroborated_by=["ok2", "bad"]),
                Claim(id="c2", statement="dropped.", paper="bad", supporting_passage="y", confidence="low")],
        open_problems=[OpenProblem(id="o1", statement="gap", flagged_by=["ok", "bad"], why_it_matters="m")],
        debates=[Debate(id="d1", question="q?", positions=[
            Position("A", ["ok"], "a"), Position("B", ["bad"], "b")])],
        benchmarks=[Benchmark(id="b1", name="speed", method="ok-method", metric="speedup", value="2.8x", paper="ok"),
                    Benchmark(id="b2", name="x", paper="bad")],
        coverage={"queries": ["speculative decoding"]})


def test_assemble_prunes_refs_and_reports_drops(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    man = json.loads((out / "wikillm.json").read_text())
    s = man["stats"]
    assert s["claims"] == 1 and s["dropped"]["claims"] == 1          # bad-anchored claim dropped
    assert s["benchmarks"] == 1 and s["dropped"]["benchmarks"] == 1
    # the open problem kept, but its flagged_by pruned to verified only
    op = (out / "open-problems" / "o1.md").read_text()
    assert "[[papers/ok]]" in op and "[[papers/bad]]" not in op
    # debate kept, but the 'bad'-only position dropped
    db = (out / "debates" / "d1.md").read_text()
    assert "ok" in db and "[[papers/bad]]" not in db
    # claim's corroborated_by pruned to verified (ok2 kept, bad removed)
    assert validate(out).ok, validate(out).errors


def test_assemble_denormalizes_id_into_chunks(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    chunk = (out / "claims" / "c1.md").read_text()
    assert "arXiv:2401.1" in chunk  # the chunk resolves to a real id standalone


def test_assemble_manifest_coverage_and_source_span(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    man = json.loads((out / "wikillm.json").read_text())
    assert man["coverage"]["queries"] == ["speculative decoding"]
    assert man["source_span"]["oldest"] == 2022 and man["source_span"]["newest"] == 2024


def test_validate_flags_benchmark_anchored_to_unverified(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    (out / "benchmarks" / "evil.md").write_text(
        "---\nid: evil\nname: x\npaper: bad\n---\n", encoding="utf-8")
    r = validate(out)
    assert not r.ok and any("UNVERIFIED" in e and "bad" in e for e in r.errors)


# ── P1-c: digest payload ─────────────────────────────────────────────────────────


def test_digest_high_value_kept_claims_truncated_under_budget():
    papers = [Paper(cite_key="p", title="P", arxiv_id="2401.1", verified=V())]
    claims = [Claim(id=f"c{i}", statement=f"Claim number {i} with some length to it.", paper="p",
                    supporting_passage="", claim_type="finding", confidence="medium") for i in range(40)]
    op = OpenProblem(id="o", statement="A crucial open problem.", flagged_by=["p"], why_it_matters="it matters")
    ctx = build_context(Package(topic="T", scope="s", papers=papers, claims=claims, open_problems=[op]),
                        built="2026-06-14", max_tokens=300)
    assert "Verified papers" in ctx and "[p]" in ctx          # spine survives
    assert "A crucial open problem." in ctx                    # open problems survive
    assert "more — see `claims/`" in ctx                       # claims truncated with honest footer
    assert _count_more(ctx) < 40                               # not all claims shown


def _count_more(ctx):
    import re
    m = re.search(r"\(\+(\d+) more", ctx)
    return 40 - int(m.group(1)) if m else 40


def test_digest_passage_and_single_source_cap():
    papers = [Paper(cite_key="p", title="P", arxiv_id="2401.1", verified=V()),
              Paper(cite_key="q", title="Q", arxiv_id="2401.2", verified=V())]
    claims = [Claim(id="c1", statement="Big result.", paper="p", supporting_passage="We measured 2.8x.",
                    claim_type="result", confidence="high"),                       # single-source
              Claim(id="c2", statement="Confirmed result.", paper="p", supporting_passage="Also seen.",
                    claim_type="result", confidence="high", corroborated_by=["q"])]
    ctx = build_context(Package(topic="T", scope="s", papers=papers, claims=claims), built="2026-06-14")
    assert "> We measured 2.8x." in ctx                         # supporting passage carried
    assert "medium (single-source)" in ctx                      # unearned 'high' capped
    assert "(corroborated by 1)" in ctx                         # corroboration surfaced


def test_digest_sota_table():
    papers = [Paper(cite_key="p", title="P", arxiv_id="2401.1", verified=V())]
    b = Benchmark(id="b1", name="speed", method="Medusa", dataset="MT-Bench", metric="speedup", value="2.8x", paper="p")
    ctx = build_context(Package(topic="T", scope="s", papers=papers, benchmarks=[b]), built="2026-06-14")
    assert "SOTA snapshot" in ctx and "| Medusa | MT-Bench | speedup | 2.8x | [p] |" in ctx


# ── container-type robustness: malformed input containers are clean errors, not crashes ──


def test_load_rejects_wrong_container_types_cleanly(tmp_path):
    for bad in [
        {"topic": "T", "papers": ["junk"]},                                  # list of strings
        {"topic": "T", "papers": [{"cite_key": ["x"], "title": "A"}]},        # unhashable cite_key
        {"topic": "T", "papers": "nope"},                                    # not a list
        {"topic": "T", "coverage": ["abc"]},                                 # coverage not an object
    ]:
        with pytest.raises(ResearchInputError):
            _load(_write(tmp_path, bad))


def test_cli_never_raw_traceback_on_malformed(tmp_path):
    from kp_build.cli import main
    p = tmp_path / "b.json"; p.write_text('{"topic":"T","papers":["junk"]}', encoding="utf-8")
    rc = main(["build", "-i", str(p), "-o", str(tmp_path / "o"), "--no-verify"])
    assert rc == 2   # clean exit, not a crash


def test_string_in_list_field_is_single_element_not_chars(tmp_path):
    pkg = _load(_write(tmp_path, {"topic": "T", "papers": [
        {"cite_key": "a", "title": "A", "authors": "Solo Author", "arxiv_id": "1.1"}]}))
    assert pkg.papers[0].authors == ["Solo Author"]      # not ['S','o','l',...]


def test_year_boolean_rejected(tmp_path):
    with pytest.raises(ResearchInputError) as e:
        _load(_write(tmp_path, {"topic": "T", "papers": [{"cite_key": "a", "title": "A", "year": True}]}))
    assert "boolean" in str(e.value)


def test_duplicate_node_id_rejected(tmp_path):
    bad = {"topic": "T",
           "papers": [{"cite_key": "p", "title": "P", "arxiv_id": "1.1"}],
           "claims": [{"id": "x", "statement": "a", "paper": "p"},
                      {"id": "x", "statement": "b", "paper": "p"}]}
    with pytest.raises(ResearchInputError) as e:
        _load(_write(tmp_path, bad))
    assert "duplicate node id 'x'" in str(e.value)


def test_claim_from_md_uses_defaults_not_none():
    from kp_build.schema import claim_from_md
    c = claim_from_md("---\nid: c1\nstatement: s\npaper: p\n---\n")
    assert c.claim_type == "finding" and c.confidence == "medium"   # not None


def test_digest_corroboration_filtered_to_verified_standalone():
    # standalone build_context (unpruned) must not count an unverified corroborator
    papers = [Paper(cite_key="p", title="P", arxiv_id="1.1", verified=V()),
              Paper(cite_key="bad", title="Bad", verified=Verification(exists=False, status="not-found"))]
    c = Claim(id="c1", statement="Big.", paper="p", supporting_passage="", claim_type="result",
              confidence="high", corroborated_by=["bad"])
    ctx = build_context(Package(topic="T", scope="s", papers=papers, claims=[c]), built="2026-06-14")
    assert "corroborated by" not in ctx and "medium (single-source)" in ctx


def test_validate_corroborator_only_paper_not_orphan(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    # ok2 is verified and used only as a corroborator of c1 — must not be flagged orphan
    assert not any("ok2" in w and "orphan" in w for w in validate(out).warnings)
