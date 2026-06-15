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
    assert "<link" not in html and "cdn" not in html.lower() and "http-equiv" not in html  # zero external deps
    assert "https://" not in html.split("<style>")[0]               # no remote resource before content
    # core content present across the (now tabbed) panels
    for needle in ("Speculative decoding", "lev2023", "Optimal draft length unsolved",
                   "Tree vs linear?", "MT-Bench", "Drafting cuts latency.",
                   "Does it help?", "Are citations real?", "Spine", "Graph"):
        assert needle in html, needle
    # arxiv link + graph data + tab structure
    assert "https://arxiv.org/abs/2211.17192" in html
    assert '"nodes"' in html and '"edges"' in html
    assert 'data-tab="spine"' in html and 'id="tab-graph"' in html


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
    assert "verdict good" in html and "HELPS" in html       # verdict tone + word
    assert "base f1 <b>0.37</b>" in html and "0.91" in html  # the delta line
    assert "2406.07524 | wrong paper" in html               # base's mislabel surfaced
    assert "Base mislabeled / fabricated" in html


def test_report_placeholder_in_package_text_not_expanded(tmp_path):
    # a package whose topic is literally a template token must NOT re-expand the graph JSON into it
    out = assemble(_pkg(topic="__GRAPH__"), tmp_path / "kp", built="2026-06-14")
    html = build_report(out)
    assert "<title>__GRAPH__ — wikillm report</title>" in html      # topic kept as literal text
    assert html.count('G={"nodes"') == 1                            # graph blob injected exactly once


def test_report_handles_no_falsification(tmp_path):
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    html = build_report(out)
    assert "Not measured" in html and "kp-build falsify" in html
    assert "verdict good" not in html                        # no fabricated verdict when not run


def test_report_cli_requires_falsification(tmp_path):
    from kp_build.cli import main
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")     # unmeasured by default
    assert main(["report", str(out), "-o", str(tmp_path / "r.html")]) == 2
    assert not (tmp_path / "r.html").exists()                       # refused — no report without the metric
    # --allow-unmeasured renders a draft
    assert main(["report", str(out), "-o", str(tmp_path / "r2.html"), "--allow-unmeasured"]) == 0
    assert (tmp_path / "r2.html").exists()
    # once falsified, report works without the flag
    man = json.loads((out / "wikillm.json").read_text())
    man["falsification"] = {"run": True, "verdict": "KP HELPS", "base": {"f1": 0.4}, "kp": {"f1": 0.9}}
    (out / "wikillm.json").write_text(json.dumps(man), encoding="utf-8")
    assert main(["report", str(out), "-o", str(tmp_path / "r3.html")]) == 0
    assert (tmp_path / "r3.html").exists()


def test_report_falsify_cta_always_shown_when_unmeasured(tmp_path):
    # run flag set but NO verdict/base/kp data -> still the "Not measured / Run kp-build falsify" CTA
    out = assemble(_pkg(), tmp_path / "kp", built="2026-06-14")
    man = json.loads((out / "wikillm.json").read_text())
    man["falsification"] = {"run": True}
    (out / "wikillm.json").write_text(json.dumps(man), encoding="utf-8")
    html = build_report(out)
    assert "Not measured" in html and "Run <code>kp-build falsify</code>" in html
    assert "verdict good" not in html
