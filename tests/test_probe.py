"""Topic-weakness pre-screen (`kp-build probe`) — the build/skip go/no-go gate."""

from kp_build.falsify import probe_prompt, probe_verdict
from kp_build.cli import main


def _hit(title):
    return f"<feed><entry><title>{title}</title></entry></feed>"


REAL = {"2211.17192": "Fast Inference", "2310.16834": "Score Entropy Discrete Diffusion",
        "1706.03762": "Attention Is All You Need"}


def _get_real(u):
    for aid, t in REAL.items():
        if aid in u:
            return _hit(t)
    return "<feed></feed>"          # anything else: no entry -> not real


def test_probe_prompt_has_topic_and_citation_block():
    p = probe_prompt("speculative decoding for LLM inference")
    assert "speculative decoding for LLM inference" in p and "## Citations" in p


def test_skip_when_model_cites_cleanly():
    # 3 real papers, 0 fabrication -> the model knows the field -> SKIP (a package adds ~0 value)
    ans = ("## Citations\n2211.17192 | Fast Inference\n2310.16834 | Score Entropy Discrete Diffusion\n"
           "1706.03762 | Attention Is All You Need\n")
    v = probe_verdict(ans, get=_get_real)
    assert v["decision"] == "skip" and v["real"] == 3 and v["fake"] == 0


def test_build_when_model_fabricates():
    # 2 real + 2 that don't resolve -> hallucination 50% >= 0.25 -> model-weak -> BUILD
    ans = ("## Citations\n2211.17192 | Fast Inference\n2499.99998 | Fabricated One\n"
           "2499.99999 | Fabricated Two\n2310.16834 | Score Entropy Discrete Diffusion\n")
    v = probe_verdict(ans, get=_get_real)
    assert v["decision"] == "build" and v["fake"] == 2 and v["hallucination_rate"] >= 0.25


def test_build_when_too_thin():
    # cites only 2 real (< min_real=3), no fabrication -> too thin -> BUILD
    ans = "## Citations\n2211.17192 | Fast Inference\n2310.16834 | Score Entropy Discrete Diffusion\n"
    v = probe_verdict(ans, get=_get_real)
    assert v["decision"] == "build" and v["real"] == 2 and "thin" in v["reason"]


def test_build_when_no_citations():
    v = probe_verdict("Just prose, no papers cited at all.", get=lambda u: "<feed></feed>")
    assert v["decision"] == "build" and v["cited"] == 0


def test_inconclusive_when_index_unreachable(monkeypatch):
    import kp_build.falsify as F
    monkeypatch.setattr(F, "score_citations", lambda a, get=None: {
        "cited": 2, "checked": 0, "unresolved": 2, "real": 0, "fake": 0, "fake_list": [],
        "precision": 0.0, "hallucination_rate": None})
    assert F.probe_verdict("## Citations\n2211.17192 | X\n")["decision"] == "inconclusive"


def test_threshold_is_tunable():
    ans = ("## Citations\n2211.17192 | Fast Inference\n2310.16834 | Score Entropy Discrete Diffusion\n"
           "1706.03762 | Attention Is All You Need\n2499.99999 | One Fabrication\n")   # 3 real, 1 fake = 25%
    assert probe_verdict(ans, get=_get_real, threshold=0.25)["decision"] == "build"    # 25% meets the bar
    assert probe_verdict(ans, get=_get_real, threshold=0.40)["decision"] == "skip"     # raise the bar -> known


# ── CLI ──────────────────────────────────────────────────────────────────────────

def test_cli_probe_emit_prompt(capsys):
    assert main(["probe", "--emit-prompt", "--question", "diffusion language models"]) == 0
    assert "diffusion language models" in capsys.readouterr().out


def test_cli_probe_exit_codes(tmp_path, monkeypatch):
    import kp_build.falsify as F
    ans = tmp_path / "a.txt"; ans.write_text("x", encoding="utf-8")
    base = {"checked": 4, "cited": 8, "real": 5, "fake": 3, "hallucination_rate": 0.375}
    monkeypatch.setattr(F, "probe_verdict", lambda *a, **k: {**base, "decision": "build", "reason": "weak"})
    assert main(["probe", "--answer", str(ans)]) == 0           # build -> exit 0
    monkeypatch.setattr(F, "probe_verdict", lambda *a, **k: {**base, "decision": "skip", "reason": "knows it"})
    assert main(["probe", "--answer", str(ans)]) == 1           # skip -> exit 1


def test_cli_probe_requires_answer_or_prompt(capsys):
    assert main(["probe"]) == 2 and "required" in capsys.readouterr().err
