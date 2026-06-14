import json
from pathlib import Path

from kp_build.schema import Package, Paper, Claim, OpenProblem, Debate, Position, Verification
from kp_build.assemble import assemble
from kp_build.validate import validate


def _pkg():
    V = lambda: Verification(exists=True, via="arxiv", checked="2026-06-14")
    papers = [
        Paper(cite_key="a2023", title="Paper A", year=2023, arxiv_id="2301.00001", verified=V(),
              key_contributions=["thing one"]),
        Paper(cite_key="b2024", title="Paper B", year=2024, arxiv_id="2401.00002", verified=V()),
        Paper(cite_key="fake", title="Fake", verified=Verification(exists=False, via="unverified")),
    ]
    claims = [
        Claim(id="c1", statement="A shows X.", paper="a2023", supporting_passage="A shows X clearly.",
              claim_type="result", confidence="high"),
        Claim(id="c2", statement="Fake claim.", paper="fake", supporting_passage="...", confidence="low"),
    ]
    problems = [OpenProblem(id="p1", statement="Y is unsolved.", flagged_by=["a2023", "b2024"],
                            why_it_matters="blocks scale")]
    debates = [Debate(id="d1", question="A vs B?",
                      positions=[Position("A wins", ["a2023"], "faster"), Position("B wins", ["b2024"], "better")])]
    return Package(topic="Test Topic", scope="narrow scope", papers=papers, claims=claims,
                   open_problems=problems, debates=debates)


def test_assemble_writes_only_verified_anchored_nodes(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    # the fake-anchored claim is dropped; the verified one stays
    assert (out / "claims" / "c1.md").is_file()
    assert not (out / "claims" / "c2.md").is_file()
    assert (out / "open-problems" / "p1.md").is_file()
    assert (out / "debates" / "d1.md").is_file()
    assert (out / "CONTEXT.md").is_file() and (out / "README.md").is_file()
    manifest = json.loads((out / "wikillm.json").read_text())
    assert manifest["stats"]["papers_verified"] == 2 and manifest["stats"]["claims"] == 1


def test_assembled_package_validates_clean(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    r = validate(out)
    assert r.ok, r.errors


def test_validate_catches_unverified_citation_breach(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    # hand-inject a claim that cites the unverified paper -> spine breach
    (out / "claims" / "bad.md").write_text(
        "---\nid: bad\nstatement: x\npaper: fake\nsupporting_passage: y\n"
        "claim_type: finding\nconfidence: low\n---\n", encoding="utf-8")
    r = validate(out)
    assert not r.ok and any("UNVERIFIED" in e for e in r.errors)


def test_context_md_has_papers_and_open_problems(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    ctx = (out / "CONTEXT.md").read_text()
    assert "Verified papers" in ctx and "[a2023]" in ctx
    assert "Open problems" in ctx and "Y is unsolved" in ctx
    assert "fake" not in ctx.lower().split("citation spine")[1] if "citation spine" in ctx else True
