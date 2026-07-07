"""Offline tests for the manim-render execution runner — fake `_run`, no docker, no image."""
import subprocess
import types

import pytest

from kp_build import manim_runner
from kp_build.manim_runner import manim_render_runner, MANIM_IMAGE, MANIM_PINNED_VERSION


def _fake_run(version="Manim Community v0.20.1", wait_code="0", logs="",
              cid="c0ffee123456"):
    """A subprocess.run-shaped fake answering the runner's docker calls in order:
    version guard, detached run (returns cid), wait (exit code), logs, rm -f."""
    calls = []

    def run(cmd, **kw):
        calls.append((list(cmd), kw))
        p = types.SimpleNamespace(returncode=0, stdout="", stderr="")
        if "--version" in cmd:
            p.stdout = version + "\n"
        elif cmd[1] == "run":                      # detached render start
            p.stdout = cid + "\n"
        elif cmd[1] == "wait":
            p.stdout = wait_code + "\n"
        elif cmd[1] == "logs":
            p.stdout = logs
        return p

    run.calls = calls
    return run


@pytest.fixture(autouse=True)
def _reset_pin_cache():
    manim_runner._manim_version_ok = False
    yield
    manim_runner._manim_version_ok = False


def _green(tmp_path):
    d = tmp_path / "green"
    d.mkdir()
    (d / "scene.py").write_text("from manim import *\n")
    return d


def _red(tmp_path, fragment="got an unexpected keyword argument 'code'"):
    d = tmp_path / "red"
    d.mkdir()
    (d / "scene.py").write_text("from manim import *\n")
    (d / "expected_error.txt").write_text(fragment + "\n")
    return d


def test_green_success_returns_no_codes(tmp_path):
    r = manim_render_runner(_green(tmp_path), "manim-render", _run=_fake_run())
    assert r == {"codes": []}


def test_green_failure_returns_render_error(tmp_path):
    r = manim_render_runner(_green(tmp_path), "manim-render",
                            _run=_fake_run(wait_code="1", logs="Traceback ..."))
    assert r == {"codes": ["render_error"]}


def test_red_failing_with_expected_fragment_is_clean(tmp_path):
    run = _fake_run(wait_code="1",
                    logs="TypeError: Code.__init__() got an unexpected keyword argument 'code'")
    r = manim_render_runner(_red(tmp_path), "manim-render", _run=run)
    assert r == {"codes": []}


def test_red_that_renders_fires_red_violation(tmp_path):
    # the weakness healed on a newer toolchain — the claim must NOT verify
    r = manim_render_runner(_red(tmp_path), "manim-render", _run=_fake_run(wait_code="0"))
    assert r["codes"] == ["red_violation", "red_rendered"]


def test_red_failing_with_a_different_error_fires_red_violation(tmp_path):
    run = _fake_run(wait_code="1", logs="ModuleNotFoundError: No module named 'scipy'")
    r = manim_render_runner(_red(tmp_path), "manim-render", _run=run)
    assert r["codes"] == ["red_violation", "red_wrong_error"]


def test_green_fixture_with_red_gate_code_fires_mode_mismatch(tmp_path):
    run = _fake_run()
    r = manim_render_runner(_green(tmp_path), "manim-render",
                            gate_code="red_violation", _run=run)
    assert r == {"codes": ["red_violation", "red_green_mode_mismatch"]}
    assert run.calls == []                        # cross-check happens BEFORE any docker call


def test_red_fixture_with_green_gate_code_fires_mode_mismatch(tmp_path):
    run = _fake_run()
    r = manim_render_runner(_red(tmp_path), "manim-render",
                            gate_code="render_error", _run=run)
    assert r == {"codes": ["render_error", "red_green_mode_mismatch"]}
    assert run.calls == []


def test_empty_red_marker_is_unverifiable(tmp_path):
    d = _red(tmp_path, fragment="")
    (d / "expected_error.txt").write_text("   \n")
    run = _fake_run()
    r = manim_render_runner(d, "manim-render", gate_code="red_violation", _run=run)
    assert r == {"codes": ["red_violation", "red_gate_unverifiable"]}
    assert run.calls == []


def test_version_pin_mismatch_raises_never_passes(tmp_path):
    with pytest.raises(RuntimeError, match="toolchain pin"):
        manim_render_runner(_green(tmp_path), "manim-render",
                            _run=_fake_run(version="Manim Community v0.21.0"))


def test_version_prefix_collision_rejected(tmp_path):
    # the sui 1.74.1 vs 1.74.10 lesson: exact match, not prefix
    with pytest.raises(RuntimeError, match="toolchain pin"):
        manim_render_runner(_green(tmp_path), "manim-render",
                            _run=_fake_run(version="Manim Community v0.20.10"))


def test_version_checked_once_per_process(tmp_path):
    run = _fake_run()
    g = _green(tmp_path)  # plan called _green twice; second mkdir() would raise FileExistsError
    manim_render_runner(g, "manim-render", _run=run)
    manim_render_runner(g, "manim-render", _run=run)
    version_calls = [c for c, _ in run.calls if "--version" in c]
    assert len(version_calls) == 1


def test_unknown_tool_returns_none(tmp_path):
    assert manim_render_runner(_green(tmp_path), "lint", _run=_fake_run()) is None


def test_missing_scene_py_returns_none(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    assert manim_render_runner(d, "manim-render", _run=_fake_run()) is None


def test_none_artifact_returns_none():
    assert manim_render_runner(None, "manim-render", _run=_fake_run()) is None


def test_wait_timeout_removes_container_and_raises(tmp_path):
    calls = []

    def run(cmd, **kw):
        calls.append(list(cmd))
        p = types.SimpleNamespace(returncode=0, stdout="", stderr="")
        if "--version" in cmd:
            p.stdout = "Manim Community v0.20.1\n"
        elif cmd[1] == "run":
            p.stdout = "abc123\n"
        elif cmd[1] == "wait":
            raise subprocess.TimeoutExpired(cmd, 300)
        return p

    with pytest.raises(RuntimeError, match="render_timeout"):
        manim_render_runner(_green(tmp_path), "manim-render", _run=run)
    assert ["docker", "rm", "-f", "abc123"] in calls   # cleanup even on timeout


def test_container_removed_after_normal_run(tmp_path):
    run = _fake_run(cid="feedface")
    manim_render_runner(_green(tmp_path), "manim-render", _run=run)
    assert ["docker", "rm", "-f", "feedface"] in [c for c, _ in run.calls]


def test_render_command_shape(tmp_path):
    run = _fake_run()
    g = _green(tmp_path)
    manim_render_runner(g, "manim-render", _run=run)
    render = next(c for c, _ in run.calls if "-d" in c)
    assert render[:3] == ["docker", "run", "-d"]
    assert f"{g.resolve()}:/manim:ro" in render        # read-only mount
    assert MANIM_IMAGE in render                       # digest-pinned image
    assert "--disable_caching" in render
    assert "/tmp/media" in render                      # media redirected off the ro mount
    assert render[-1] == "scene.py"                    # no scene name: single-scene auto-render


def test_env_overrides_docker_bin_and_image(tmp_path, monkeypatch):
    monkeypatch.setenv("KP_BUILD_DOCKER_BIN", "/opt/podman")
    monkeypatch.setenv("KP_BUILD_MANIM_IMAGE", "localhost/manim:test")
    run = _fake_run()
    manim_render_runner(_green(tmp_path), "manim-render", _run=run)
    for c, _ in run.calls:
        assert c[0] == "/opt/podman"
    render = next(c for c, _ in run.calls if "-d" in c)
    assert "localhost/manim:test" in render


def test_fragment_matches_through_ansi_and_wrapping(tmp_path):
    # manim logs are rich-formatted: ANSI codes inside the message, hard wraps with box chars
    logs = ("\x1b[31mTypeError:\x1b[0m Code.\x1b[1m__init__\x1b[0m() got an\n"
            "│ unexpected keyword argument \x1b[32m'code'\x1b[0m │\n")
    d = _red(tmp_path, fragment="Code.__init__() got an unexpected keyword argument 'code'")
    r = manim_render_runner(d, "manim-render", _run=_fake_run(wait_code="1", logs=logs))
    assert r == {"codes": []}


def test_logs_combine_stdout_and_stderr(tmp_path):
    def run(cmd, **kw):
        p = types.SimpleNamespace(returncode=0, stdout="", stderr="")
        if "--version" in cmd:
            p.stdout = "Manim Community v0.20.1\n"
        elif cmd[1] == "run":
            p.stdout = "abc\n"
        elif cmd[1] == "wait":
            p.stdout = "1\n"
        elif cmd[1] == "logs":
            p.stderr = "ValueError: zip() argument 2 is longer than argument 1"
        return p

    d = _red(tmp_path, fragment="zip() argument 2 is longer")
    assert manim_render_runner(d, "manim-render", _run=run) == {"codes": []}


def test_wait_command_failure_raises_never_passes(tmp_path):
    # docker wait itself failing (daemon lost the container) must fail closed, not read as exit 0
    def run(cmd, **kw):
        p = types.SimpleNamespace(returncode=0, stdout="", stderr="")
        if "--version" in cmd:
            p.stdout = "Manim Community v0.20.1\n"
        elif cmd[1] == "run":
            p.stdout = "abc\n"
        elif cmd[1] == "wait":
            p.returncode, p.stderr = 1, "No such container: abc"
        return p

    with pytest.raises(RuntimeError, match="docker wait failed"):
        manim_render_runner(_green(tmp_path), "manim-render", _run=run)


def test_docker_run_start_failure_raises(tmp_path):
    def run(cmd, **kw):
        p = types.SimpleNamespace(returncode=0, stdout="", stderr="")
        if "--version" in cmd:
            p.stdout = "Manim Community v0.20.1\n"
        elif cmd[1] == "run":
            p.returncode, p.stderr = 125, "docker: no such image"
        return p

    with pytest.raises(RuntimeError, match="failed to start"):
        manim_render_runner(_green(tmp_path), "manim-render", _run=run)
