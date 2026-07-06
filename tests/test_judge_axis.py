"""The blind quality-panel axis of falsification (`judge_prompts` / `judge_replay` / veto semantics)
plus the falsify CLI flags that carry it (--emit-judge-prompts / --judge-rounds / --no-record)."""

import json
from pathlib import Path

import pytest

from kp_build.cli import main
from kp_build.falsify import helped, judge_prompts, judge_replay, verdict


# ── judge_prompts: the emit side of the panel ────────────────────────────────────────


def test_judge_prompts_alternates_kp_slot_matching_the_verifier():
    # Round i puts the KP answer in slot A iff i is even — MUST mirror JudgeVerifier's
    # ans_is_a = (i % 2 == 0), because judge_replay re-tallies the recorded slot winners
    # through that same alternation. A drift here silently inverts half the panel.
    ps = judge_prompts("q?", "BASE-TEXT", "KP-TEXT", rounds=4)
    assert len(ps) == 4
    for i, p in enumerate(ps):
        want_a = "KP-TEXT" if i % 2 == 0 else "BASE-TEXT"
        assert f"=== ANSWER A ===\n{want_a}\n" in p
    assert all("q?" in p for p in ps)                       # the task rides along in every prompt
    assert all("EXACTLY one word" in p for p in ps)         # one-word verdict contract


def test_judge_prompts_clamps_rounds_even_and_at_least_two():
    assert len(judge_prompts("q", "b", "k", rounds=5)) == 4     # odd -> rounded down
    assert len(judge_prompts("q", "b", "k", rounds=1)) == 2     # floor is 2 (one round per slot)
    assert len(judge_prompts("q", "b", "k", rounds=0)) == 2


# ── judge_replay: the tally side, THROUGH the same JudgeVerifier the build uses ──────


def test_judge_replay_tallies_slot_winners_through_the_alternation():
    # rounds 0,2 put KP in slot a; rounds 1,3 in slot b.
    # ['a','b','a','a'] -> kp, kp, kp, base -> 3-1 judged-better.
    r = judge_replay(["a", "b", "a", "a"])
    assert r["status"] == "judged-better"
    assert (r["kp_wins"], r["base_wins"], r["ties"]) == (3, 1, 0)


def test_judge_replay_uniform_fake_nets_to_tie():
    # the anti-fraud property inherited from JudgeVerifier: a lazy 'a'-every-round fake
    # gives one win to each side per alternation pair -> judged-tie, never judged-better.
    r = judge_replay(["a", "a"])
    assert r["status"] == "judged-tie" and r["kp_wins"] == r["base_wins"] == 1
    r6 = judge_replay(["a"] * 6)
    assert r6["status"] == "judged-tie" and r6["kp_wins"] == r6["base_wins"] == 3


def test_judge_replay_all_ties_is_judged_tie():
    r = judge_replay(["tie", "tie"])
    assert r["status"] == "judged-tie" and r["ties"] == 2 and r["kp_wins"] == 0


def test_judge_replay_base_sweep_is_judged_worse():
    # base wins both slots: round 0 slot winner 'b' (kp is a), round 1 slot winner 'a' (kp is b)
    r = judge_replay(["b", "a"])
    assert r["status"] == "judged-worse" and r["base_wins"] == 2 and r["kp_wins"] == 0


def test_judge_replay_rejects_odd_and_invalid_panels():
    with pytest.raises(ValueError, match="EVEN"):
        judge_replay(["a"])                                  # odd panel launders one-sided votes
    with pytest.raises(ValueError, match="EVEN"):
        judge_replay(["a", "b", "a"])
    with pytest.raises(ValueError, match="EVEN"):
        judge_replay([])
    with pytest.raises(ValueError, match="must each be"):
        judge_replay(["a", "x"])                             # junk verdicts never count as votes


def test_judge_replay_normalizes_case_and_whitespace():
    r = judge_replay([" A ", "B"])                           # judges reply 'A'/'B'/'TIE' verbatim
    assert r["rounds"] == ["a", "b"] and r["kp_wins"] == 2   # both slot winners map to KP


# ── helped(): the panel is a VETO, never a manufacturer ──────────────────────────────


def _rep(f1, *, fake=0, hall=0.0):
    return {"cited": 4, "checked": 4, "real": 4 - fake, "fake": fake,
            "hallucination_rate": hall, "precision": 1.0 - hall, "recall": f1, "f1": f1}


def test_helped_judged_worse_vetoes_a_mechanical_win():
    base, kp = _rep(0.4, fake=2, hall=0.5), _rep(0.9)
    assert helped(base, kp) is True                                          # mechanical axes say helps
    assert helped(base, kp, {"status": "judged-worse", "kp_wins": 0,
                             "base_wins": 2, "ties": 0}) is False            # panel overturns it


def test_helped_judged_better_never_manufactures_a_win():
    # equal f1, equal hallucination -> the mechanical axes show nothing; a judged-better
    # panel must NOT flip that to True (the mechanical axis that CAN fail must clear first).
    base, kp = _rep(0.5), _rep(0.5)
    assert helped(base, kp) is False
    assert helped(base, kp, {"status": "judged-better", "kp_wins": 4,
                             "base_wins": 0, "ties": 0}) is False


def test_helped_worse_f1_is_not_rescued_by_cleaner_hallucination():
    # when both sides have f1, f1 decides — a cleaner hallucination rate must not overrule
    # a worse f1 (the verdict sentence prints the f1 numbers; exit code must agree with them)
    base = {**_rep(0.4), "fake": 3, "hallucination_rate": 0.375}
    kp = _rep(0.2)                                       # cleaner cites, but WORSE f1
    assert helped(base, kp) is False


def test_helped_inconclusive_guards_run_before_the_panel():
    # unverifiable citations stay None even with a recorded panel — fail-closed ordering
    base, kp = _rep(0.5), {**_rep(0.9), "checked": 0}
    assert helped(base, kp, {"status": "judged-better", "kp_wins": 2,
                             "base_wins": 0, "ties": 0}) is None


# ── verdict(): the sentence renders the same rule ────────────────────────────────────


def test_verdict_renders_panel_tally_and_spine_adoption_framing():
    v = verdict(_rep(0.4, fake=2, hall=0.5), _rep(0.9),
                {"status": "judged-better", "kp_wins": 4, "base_wins": 1, "ties": 1})
    assert "KP HELPS" in v and "PREFERRED" in v and "4-1-1" in v
    assert "spine adoption" in v and "fabricated/mislabeled" in v


def test_verdict_judged_worse_forces_did_not_help():
    v = verdict(_rep(0.4, fake=2, hall=0.5), _rep(0.9),
                {"status": "judged-worse", "kp_wins": 0, "base_wins": 4, "ties": 0})
    assert "DID NOT HELP" in v and "whatever the spine numbers say" in v


def test_verdict_without_panel_says_so():
    # a purely mechanical verdict must disclose what it does NOT certify (the circularity)
    v = verdict(_rep(0.4, fake=2, hall=0.5), _rep(0.9))
    assert "No blind quality panel" in v and "--judge-rounds" in v


def test_verdict_tie_preserved_when_f1_equal_and_no_veto():
    assert "KP TIES" in verdict(_rep(0.5), _rep(0.5))


# ── the falsify CLI flags that carry the panel ───────────────────────────────────────


def _falsify_pkg(tmp_path, monkeypatch):
    import kp_build.falsify as F
    pkg = tmp_path / "pkg"; pkg.mkdir()
    (pkg / "index.json").write_text(json.dumps(
        {"papers": [{"cite_key": "a", "arxiv_id": "2211.17192", "verified": True}]}), encoding="utf-8")
    (pkg / "wikillm.json").write_text(json.dumps({"name": "@kp/x"}, indent=2) + "\n", encoding="utf-8")
    base = tmp_path / "base.txt"; base.write_text("the base answer", encoding="utf-8")
    kp = tmp_path / "kp.txt"; kp.write_text("the kp answer", encoding="utf-8")
    reports = {"the base answer": _rep(0.4, fake=2, hall=0.5), "the kp answer": _rep(0.9)}
    monkeypatch.setattr(F, "score_answer", lambda text, spine=None, **kw: reports[text])
    return pkg, base, kp


def _run(pkg, base, kp, *extra):
    return main(["falsify", str(pkg), "--question", "q?", "--base", str(base),
                 "--kp", str(kp), *extra])


def test_cli_falsify_records_judge_in_manifest(tmp_path, monkeypatch, capsys):
    pkg, base, kp = _falsify_pkg(tmp_path, monkeypatch)
    assert _run(pkg, base, kp, "--judge-rounds", "a,b") == 0            # kp preferred both slots
    man = json.loads((pkg / "wikillm.json").read_text(encoding="utf-8"))
    j = man["falsification"]["judge"]
    assert j["status"] == "judged-better" and j["kp_wins"] == 2
    assert "PREFERRED" in man["falsification"]["verdict"]
    assert not (pkg / "wikillm.json.tmp").exists()                      # atomic rename left no temp
    assert "judge:" in capsys.readouterr().out


def test_cli_falsify_judge_veto_flips_exit_code(tmp_path, monkeypatch):
    pkg, base, kp = _falsify_pkg(tmp_path, monkeypatch)
    assert _run(pkg, base, kp) == 0                                     # mechanical win alone
    assert _run(pkg, base, kp, "--judge-rounds", "b,a") == 1            # base swept -> veto -> exit 1
    man = json.loads((pkg / "wikillm.json").read_text(encoding="utf-8"))
    assert "DID NOT HELP" in man["falsification"]["verdict"]


def test_cli_falsify_no_record_leaves_manifest_untouched(tmp_path, monkeypatch):
    pkg, base, kp = _falsify_pkg(tmp_path, monkeypatch)
    before = (pkg / "wikillm.json").read_bytes()
    assert _run(pkg, base, kp, "--no-record") == 0
    assert (pkg / "wikillm.json").read_bytes() == before                # byte-identical
    assert not (pkg / "wikillm.json.tmp").exists()


def test_cli_falsify_bad_judge_rounds_is_a_usage_error(tmp_path, monkeypatch, capsys):
    pkg, base, kp = _falsify_pkg(tmp_path, monkeypatch)
    before = (pkg / "wikillm.json").read_bytes()
    assert _run(pkg, base, kp, "--judge-rounds", "a") == 2              # odd panel -> ValueError -> 2
    assert (pkg / "wikillm.json").read_bytes() == before                # rejected BEFORE any record
    assert "EVEN" in capsys.readouterr().err


def test_cli_falsify_emit_judge_prompts_scores_nothing(tmp_path, monkeypatch, capsys):
    import kp_build.falsify as F
    pkg, base, kp = _falsify_pkg(tmp_path, monkeypatch)
    def boom(*a, **k):
        raise AssertionError("emit mode must not score answers")
    monkeypatch.setattr(F, "score_answer", boom)
    before = (pkg / "wikillm.json").read_bytes()
    assert _run(pkg, base, kp, "--emit-judge-prompts", "4") == 0
    out = capsys.readouterr()
    assert out.out.count("JUDGE PROMPT") == 4 and "1/4" in out.out
    assert "the kp answer" in out.out and "the base answer" in out.out  # both sides embedded, blind
    assert "--judge-rounds" in out.err                                  # next-step hint
    assert (pkg / "wikillm.json").read_bytes() == before                # no manifest touch
