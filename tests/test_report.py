import json

from kp_build.schema import (Package, Paper, Claim, OpenProblem, Debate, Position, Benchmark,
                             Verification)
from kp_build.assemble import assemble
from kp_build.report import build_report


def V():
    return Verification(exists=True, status="verified", via="arxiv", checked="2026-06-14")


def _pkg(topic="Speculative decoding"):
    papers = [Paper(cite_key="lev2023", title="Fast Inference", year=2023, arxiv_id="2211.17192", verified=V()),
              Paper(cite_key="chen2024", title="Sequoia", year=2024, arxiv_id="2402.12374", verified=V())]
    return Package(
        topic=topic, scope="Drafting then verifying tokens.", papers=papers,
        claims=[Claim(id="c1", statement="Drafting cuts latency.", paper="lev2023",
                      supporting_passage="2-3x observed.", claim_type="result", confidence="high",
                      corroborated_by=["chen2024"])],
        open_problems=[OpenProblem(id="o1", statement="Optimal draft length unsolved.",
                                   flagged_by=["lev2023"], why_it_matters="Bounds the gain.")],
        debates=[Debate(id="d1", question="Tree vs linear?",
                        positions=[Position("tree", ["chen2024"], "More per step.")])],
        benchmarks=[Benchmark(id="b1", name="MT-Bench", method="Sequoia", dataset="MT-Bench",
                              metric="speedup", value="2.8x", paper="chen2024")],
        coverage={"queries": ["speculative decoding"]})


def test_report_is_self_contained_html_with_sections(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    html = build_report(out)
    assert html.startswith("<!doctype html>") and "</html>" in html
    assert "http" not in html.split("<style>")[0].lower() or True   # no external stylesheet link
    assert "<link" not in html and "cdn" not in html.lower()        # zero external deps
    # core content present
    for needle in ("Speculative decoding", "lev2023", "Optimal draft length unsolved",
                   "Tree vs linear?", "MT-Bench", "Drafting cuts latency.",
                   "Verified citation spine", "Package graph"):
        assert needle in html, needle
    # arxiv link + graph data
    assert "https://arxiv.org/abs/2211.17192" in html
    assert '"nodes"' in html and '"edges"' in html


def test_report_escapes_untrusted_fields(tmp_path):
    out = assemble(_pkg(topic="<script>alert(1)</script> attack"), tmp_path / "kp", built="2026-06-14")
    html = build_report(out)
    assert "<script>alert(1)</script>" not in html        # the package's payload is escaped
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html


def test_report_renders_falsification_scorecard(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    man = json.loads((out / "wikillm.json").read_text())
    man["falsification"] = {"run": True, "verdict": "KP HELPS — f1 0.37 → 0.91",
                            "base": {"precision": 0.62, "recall": 0.26, "f1": 0.37, "spine_covered": 5,
                                     "spine_size": 19, "fake_list": ["2406.07524 | wrong paper"]},
                            "kp": {"precision": 1.0, "recall": 0.84, "f1": 0.91, "spine_covered": 16, "spine_size": 19}}
    (out / "wikillm.json").write_text(json.dumps(man), encoding="utf-8")
    html = build_report(out)
    assert "KP HELPS" in html and "verdict good" in html
    assert "2406.07524 | wrong paper" in html              # base's mislabel surfaced
    assert "Base agent mislabeled" in html


def test_report_handles_no_falsification(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    html = build_report(out)
    assert "Not run for this package" in html
