"""Offline tests for the sui-move execution runner — fake `_run`, no Sui binary, no network."""
import subprocess

import pytest

from kp_build import sui_runner
from kp_build.sui_runner import sui_move_runner, SUI_PINNED_VERSION


def _fake_run(version="sui 1.74.1-8fc60f1fa966", returncode=0, output=""):
    """A subprocess.run-shaped fake: answers `sui --version` then the build call."""
    calls = []

    def run(cmd, **kw):
        calls.append((list(cmd), kw))
        class P:  # noqa: N801 — minimal CompletedProcess stand-in
            pass
        p = P()
        if "--version" in cmd:
            p.returncode, p.stdout, p.stderr = 0, version, ""
        else:
            p.returncode, p.stdout, p.stderr = returncode, output, ""
        return p

    run.calls = calls
    return run


@pytest.fixture(autouse=True)
def _reset_pin_cache():
    sui_runner._sui_version_ok = False
    yield
    sui_runner._sui_version_ok = False


def _green(tmp_path):
    d = tmp_path / "green"
    d.mkdir(exist_ok=True)
    (d / "Move.toml").write_text('[package]\nname = "x"\nedition = "2024"\n')
    return d


def _red(tmp_path, fragment="Visibility annotations are required"):
    d = tmp_path / "red"
    d.mkdir()
    (d / "Move.toml").write_text('[package]\nname = "x"\nedition = "2024"\n')
    (d / "expected_error.txt").write_text(fragment + "\n")
    return d


def test_green_success_returns_no_codes(tmp_path):
    r = sui_move_runner(_green(tmp_path), "sui-move-build", _run=_fake_run(returncode=0))
    assert r == {"codes": []}


def test_green_failure_returns_build_error(tmp_path):
    r = sui_move_runner(_green(tmp_path), "sui-move-build", _run=_fake_run(returncode=1))
    assert r == {"codes": ["build_error"]}


def test_red_failing_with_expected_fragment_is_clean(tmp_path):
    run = _fake_run(returncode=1, output="error[E...]: Visibility annotations are required on struct declarations")
    r = sui_move_runner(_red(tmp_path), "sui-move-build", _run=run)
    assert r == {"codes": []}


def test_red_that_compiles_fires_red_violation(tmp_path):
    # the weakness healed on a newer toolchain — the claim must NOT verify
    r = sui_move_runner(_red(tmp_path), "sui-move-build", _run=_fake_run(returncode=0))
    assert r["codes"] == ["red_violation", "red_compiled"]


def test_red_failing_with_a_different_error_fires_red_violation(tmp_path):
    run = _fake_run(returncode=1, output="error: unbound module 'sui::nonsense'")
    r = sui_move_runner(_red(tmp_path), "sui-move-build", _run=run)
    assert r["codes"] == ["red_violation", "red_wrong_error"]


def test_version_pin_mismatch_raises_never_passes(tmp_path):
    with pytest.raises(RuntimeError, match="toolchain pin"):
        sui_move_runner(_green(tmp_path), "sui-move-build", _run=_fake_run(version="sui 1.99.0-abc"))


def test_version_pin_rejects_later_patch_prefix_collision(tmp_path):
    # startswith("sui 1.74.1") would false-accept 1.74.10 — the pin must not
    with pytest.raises(RuntimeError, match="toolchain pin"):
        sui_move_runner(_green(tmp_path), "sui-move-build", _run=_fake_run(version="sui 1.74.10-abc"))


def test_version_checked_once_per_process(tmp_path):
    run = _fake_run(returncode=0)
    sui_move_runner(_green(tmp_path), "sui-move-build", _run=run)
    sui_move_runner(_green(tmp_path), "sui-move-build", _run=run)
    version_calls = [c for c, _ in run.calls if "--version" in c]
    assert len(version_calls) == 1


def test_unknown_tool_returns_none(tmp_path):
    assert sui_move_runner(_green(tmp_path), "lint", _run=_fake_run()) is None


def test_missing_move_toml_returns_none(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    assert sui_move_runner(d, "sui-move-build", _run=_fake_run()) is None


def test_timeout_propagates_as_error(tmp_path):
    def boom(cmd, **kw):
        raise subprocess.TimeoutExpired(cmd, 300)
    sui_runner._sui_version_ok = True     # reach the build call
    with pytest.raises(subprocess.TimeoutExpired):
        sui_move_runner(_green(tmp_path), "sui-move-build", _run=boom)


def test_build_runs_in_fixture_dir(tmp_path):
    run = _fake_run(returncode=0)
    g = _green(tmp_path)
    sui_move_runner(g, "sui-move-build", _run=run)
    build_calls = [(c, kw) for c, kw in run.calls if "--version" not in c]
    assert build_calls[0][0][-2:] == ["move", "build"]
    assert build_calls[0][1].get("cwd") == str(g)
