"""kp-build output must be a valid 0xLT/kpm package (knowledge.json contract).

These tests pin the *contract* shape (mirroring kpm's own manifest validator) so a drift is caught
in unit tests. The end-to-end proof — real `kpm doctor`/`kpm pack` accepting the package — is run
separately (see scripts/kpm_pack_check or the session log); here we lock the invariants that make
that pass: a well-formed manifest, the entrypoint present, and path-qualified wikilinks.
"""

import json
import re

from kp_build.schema import (Package, Paper, Claim, OpenProblem, Debate, Position, Benchmark,
                             Verification)
from kp_build.assemble import assemble, build_knowledge_json
from kp_build.validate import validate

# the exact rules from 0xLT/kpm src/manifest/knowledge.ts
NAME_RE = re.compile(r"^(?:@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
KPM_KEYS = {"name", "version", "description", "license", "type", "files", "entrypoint",
            "knowledgeDependencies"}


def V():
    return Verification(exists=True, status="verified", via="arxiv", checked="2026-06-14")


def _pkg():
    papers = [Paper(cite_key="leviathan2023", title="Fast Inference", year=2023, arxiv_id="2211.17192", verified=V()),
              Paper(cite_key="chen2024", title="Sequoia", year=2024, arxiv_id="2402.12374", verified=V())]
    return Package(
        topic="Speculative decoding for LLM inference",
        scope="Methods that accelerate autoregressive decoding by drafting then verifying tokens.",
        papers=papers,
        claims=[Claim(id="c1", statement="Drafting cuts latency.", paper="leviathan2023",
                      supporting_passage="2-3x speedup observed.", claim_type="result",
                      confidence="high", corroborated_by=["chen2024"])],
        open_problems=[OpenProblem(id="o1", statement="Optimal draft length is unsolved.",
                                   flagged_by=["leviathan2023"], why_it_matters="It bounds the gain.")],
        debates=[Debate(id="d1", question="Tree vs linear drafting?",
                        positions=[Position("tree", ["chen2024"], "Trees verify more per step.")])],
        benchmarks=[Benchmark(id="b1", name="MT-Bench", method="Sequoia", dataset="MT-Bench",
                              metric="speedup", value="2.8x", paper="chen2024")],
        coverage={"queries": ["speculative decoding"]})


def test_knowledge_json_is_valid_kpm_manifest(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    m = json.loads((out / "knowledge.json").read_text())
    # only the protocol's closed key set
    assert set(m) <= KPM_KEYS, f"unknown keys: {set(m) - KPM_KEYS}"
    assert NAME_RE.match(m["name"]) and m["name"] == "@kp/speculative-decoding-for-llm-inference"
    assert VERSION_RE.match(m["version"]) and m["version"] == "0.1.0"
    assert m["type"] == "knowledge-package"
    assert m["entrypoint"] == "README.md" and (out / "README.md").is_file()
    assert isinstance(m["files"], list) and m["files"]
    # the wikillm payload rides alongside, carried by the files glob
    assert "wikillm.json" in m["files"] and "index.json" in m["files"]


def test_publisher_can_override_name_version_license(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14",
                   name="@acme/spec-decode", version="1.2.3", license="MIT")
    m = json.loads((out / "knowledge.json").read_text())
    assert m["name"] == "@acme/spec-decode" and m["version"] == "1.2.3" and m["license"] == "MIT"


def test_build_knowledge_json_defaults():
    m = build_knowledge_json(_pkg(), name=None, version="0.1.0", license="CC-BY-4.0")
    assert m["name"].startswith("@kp/") and m["license"] == "CC-BY-4.0"


def test_validate_requires_and_checks_knowledge_json(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    assert validate(out).ok, validate(out).errors
    # corrupt the manifest → kp-build's own lint must fail (before kpm pack would)
    (out / "knowledge.json").write_text(json.dumps(
        {"name": "Bad Name", "version": "v1", "type": "wrong"}), encoding="utf-8")
    r = validate(out)
    assert not r.ok
    assert any("name must be" in e for e in r.errors)
    assert any("semver" in e for e in r.errors)
    assert any("knowledge-package" in e for e in r.errors)


def test_validate_flags_missing_knowledge_json(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    (out / "knowledge.json").unlink()
    r = validate(out)
    assert not r.ok and any("missing knowledge.json" in e for e in r.errors)


def test_wikilinks_are_path_qualified(tmp_path):
    """Every [[wikilink]] in every note must be papers/<key> so kpm resolves it by exact path."""
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    for sub in ("claims", "open-problems", "debates", "benchmarks"):
        for f in (out / sub).glob("*.md"):
            for link in re.findall(r"\[\[([^\]]+)\]\]", f.read_text()):
                assert link.startswith("papers/"), f"{f}: bare wikilink [[{link}]] (collision-prone)"
                assert (out / f"{link}.md").is_file(), f"{f}: [[{link}]] has no target file"
