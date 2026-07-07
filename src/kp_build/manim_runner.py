"""ExecutionVerifier runner for the pinned Manim CE Docker image (the manim pack's oracle).

Two-sided RED/GREEN gate: a fixture directory holds a single-Scene ``scene.py``; if it carries an
``expected_error.txt`` it is RED (the naive-from-memory form) and must FAIL to render with that
fragment in the logs — a RED that starts rendering means the weakness it documents has healed on a
newer toolchain and the claim must stop verifying (staleness signal, spec §3/§7). Without the
marker it is GREEN and must render clean. The claim-side ``gate_code`` is cross-checked against
the fixture-side marker BEFORE any render (the sui PR #9 fail-closed hardening): a mismatch or an
empty RED marker fires the claim's own gate, never a vacuous pass.

Toolchain pin: the image is referenced BY DIGEST (``MANIM_IMAGE``) — Python, Manim, TeX, ffmpeg
and fonts are frozen byte-for-byte, so the old verification environment stays reconstructible. A
version guard runs ``manim --version`` in the container once per process and requires exactly
``Manim Community v0.20.1`` (exact match — the 1.74.1/1.74.10 prefix-collision lesson). Escape
hatches: ``KP_BUILD_MANIM_IMAGE`` (alternate image ref), ``KP_BUILD_DOCKER_BIN`` (docker binary).

Containment (probe-earned): ``timeout N docker run`` kills only the client and orphans the
container (a probe render hung for hours post-traceback). The runner therefore starts the render
detached, bounds ``docker wait``, reads ``docker logs``, and ALWAYS force-removes the container;
a wait expiry raises ``render_timeout`` (ExecutionVerifier maps raises to ``error`` — fail closed).

Log matching: manim's rich console emits ANSI codes inside messages and hard-wraps lines with
box-drawing characters, so fragments are matched after normalization (strip ANSI, drop box chars,
collapse whitespace) — of both the logs and the fragment.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

MANIM_PINNED_VERSION = "0.20.1"
MANIM_IMAGE = ("manimcommunity/manim@sha256:"
               "f18f53f2e4eaf2ea41713437d34363fb3f5cc6008b03fd798676ac0359396c3b")
_TIMEOUT = 300

# Per-process cache, mirroring sui_runner._sui_version_ok: a multi-claim build checks the
# version once, not per fixture. Module-level and explicit so tests can reset it.
_manim_version_ok = False

_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_BOX = str.maketrans({c: " " for c in "│┃╭╮╰╯─━┌┐└┘├┤"})


def _normalize(text: str) -> str:
    """Make rich-console output greppable: no ANSI, no box art, single-spaced."""
    return " ".join(_ANSI.sub("", text).translate(_BOX).split())


def manim_render_runner(artifact, tool, *, gate_code=None, _run=None):
    """Runner contract: ``{"codes": [...]}`` on a run, ``None`` if artifact/tool can't produce a
    result, RAISES on timeout/crash/pin-failure. See module docstring for the RED/GREEN table."""
    global _manim_version_ok
    if tool != "manim-render" or artifact is None:
        return None
    d = Path(artifact)
    if not (d / "scene.py").is_file():
        return None
    marker = d / "expected_error.txt"
    is_red = marker.is_file()
    frag = marker.read_text(encoding="utf-8").strip() if is_red else ""
    if gate_code is not None and (gate_code == "red_violation") != is_red:
        return {"codes": [gate_code, "red_green_mode_mismatch"]}
    if is_red and not frag:
        return {"codes": ["red_violation", "red_gate_unverifiable"]}
    run = _run or subprocess.run
    docker = os.environ.get("KP_BUILD_DOCKER_BIN") or "docker"
    image = os.environ.get("KP_BUILD_MANIM_IMAGE") or MANIM_IMAGE
    if not _manim_version_ok:
        v = run([docker, "run", "--rm", image, "manim", "--version"],
                capture_output=True, text=True, timeout=120)
        ver = (getattr(v, "stdout", "") or "").strip()
        if ver != f"Manim Community v{MANIM_PINNED_VERSION}":
            raise RuntimeError(
                f"manim toolchain pin failed: need 'Manim Community v{MANIM_PINNED_VERSION}', "
                f"got {ver!r} — a claim verified on a different renderer is not the claim we "
                "shipped; point KP_BUILD_MANIM_IMAGE at the digest-pinned image")
        _manim_version_ok = True
    p = run([docker, "run", "-d", "-v", f"{d.resolve()}:/manim:ro", image,
             "manim", "-ql", "--disable_caching", "--media_dir", "/tmp/media", "scene.py"],
            capture_output=True, text=True, timeout=60)
    cid = (getattr(p, "stdout", "") or "").strip()
    if p.returncode != 0 or not cid:
        raise RuntimeError(
            f"docker failed to start the render container: {getattr(p, 'stderr', '')!r}")
    try:
        try:
            w = run([docker, "wait", cid], capture_output=True, text=True, timeout=_TIMEOUT)
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                f"manim render_timeout after {_TIMEOUT}s — container {cid[:12]} force-removed; "
                "a render that never finishes is a failure, never a pass") from None
        exit_str = (getattr(w, "stdout", "") or "").strip()
        if not exit_str and getattr(w, "returncode", 0) != 0:
            raise RuntimeError(
                f"docker wait failed (returncode={w.returncode}): "
                f"{getattr(w, 'stderr', '')!r} — a lost container is a failure, never a pass")
        code = int(exit_str or "0")
        lg = run([docker, "logs", cid], capture_output=True, text=True, timeout=60)
        out = (getattr(lg, "stdout", "") or "") + (getattr(lg, "stderr", "") or "")
    finally:
        run([docker, "rm", "-f", cid], capture_output=True, text=True, timeout=60)
    failed = code != 0
    if is_red:                                 # RED: must fail, with the documented fragment
        if not failed:
            return {"codes": ["red_violation", "red_rendered"]}
        if _normalize(frag) not in _normalize(out):
            return {"codes": ["red_violation", "red_wrong_error"]}
        return {"codes": []}
    return {"codes": (["render_error"] if failed else [])}
