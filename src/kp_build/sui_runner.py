"""ExecutionVerifier runner for the pinned Sui CLI (the sui-move pack's oracle).

Two-sided RED/GREEN gate: a fixture directory is a Move package; if it carries an
``expected_error.txt`` it is a RED fixture (the naive-from-memory form) and must FAIL to build
with that fragment in the compiler output — a RED that starts compiling means the weakness it
documents has healed on a newer toolchain, and the claim must stop verifying (staleness signal,
spec §3/§7). Without the marker file it is GREEN and must build clean.

Toolchain pin (honest scope, mirrors the hyperframes pin doctrine): ``sui --version`` must
report ``SUI_PINNED_VERSION``, checked once per process; a mismatch RAISES (ExecutionVerifier
maps that to ``error``, never a pass). A malicious binary can forge its version string — as with
``KP_BUILD_HYPERFRAMES_BIN``, supplying the binary (``KP_BUILD_SUI_BIN``, or ``sui`` on PATH) is
the operator's explicit trust decision; the release asset's sha256 is recorded in the pack's
CONTEXT.md for out-of-band audit, not enforced here (there is no registry to re-query — the
binary IS the artifact).
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

SUI_PINNED_VERSION = "1.74.1"
_TIMEOUT = 300

# Per-process cache, mirroring verifier._hyperframes_integrity_ok: a multi-claim build checks
# the version once, not per fixture. Module-level and explicit so tests can reset it.
_sui_version_ok = False


def sui_move_runner(artifact, tool, *, gate_code=None, _run=None):
    """Runner contract: ``{"codes": [...]}`` on a run, ``None`` if artifact/tool can't produce a
    result, RAISES on timeout/crash/pin-failure. See module docstring for the RED/GREEN table.

    Fail-closed cross-check (the F1/F2 hardening): mode used to be inferred SOLELY from the
    fixture-side marker file, so deleting (or planting) ``expected_error.txt`` flipped the mode and
    a broken claim verified vacuously against codes its gate could never see. When the caller
    threads the claim's ``gate_code`` through (ExecutionVerifier does), the claim-side expectation
    (``red_violation`` ⇒ RED) is cross-checked against the fixture-side marker BEFORE any compile:
    a mismatch returns the claim's own gate plus ``red_green_mode_mismatch`` so the gate FIRES.
    An empty/whitespace marker in RED mode is unverifiable — its fragment check would be vacuous —
    and fires ``red_violation`` + ``red_gate_unverifiable`` (gate_code or not). ``gate_code=None``
    (a legacy two-arg caller) skips only the claim-side cross-check, nothing else."""
    global _sui_version_ok
    if tool != "sui-move-build" or artifact is None:
        return None
    d = Path(artifact)
    if not (d / "Move.toml").is_file():
        return None
    marker = d / "expected_error.txt"
    is_red = marker.is_file()
    frag = marker.read_text(encoding="utf-8").strip() if is_red else ""
    if gate_code is not None and (gate_code == "red_violation") != is_red:
        return {"codes": [gate_code, "red_green_mode_mismatch"]}
    if is_red and not frag:
        return {"codes": ["red_violation", "red_gate_unverifiable"]}
    run = _run or subprocess.run
    binary = os.environ.get("KP_BUILD_SUI_BIN") or "sui"
    if not _sui_version_ok:
        v = run([binary, "--version"], capture_output=True, text=True, timeout=60)
        ver = (getattr(v, "stdout", "") or "").strip()
        if ver != f"sui {SUI_PINNED_VERSION}" and not ver.startswith(f"sui {SUI_PINNED_VERSION}-"):
            raise RuntimeError(
                f"sui toolchain pin failed: need 'sui {SUI_PINNED_VERSION}', got {ver!r} — "
                "a claim verified on a different compiler is not the claim we shipped; "
                "point KP_BUILD_SUI_BIN at the pinned release binary")
        _sui_version_ok = True
    p = run([binary, "move", "build"], cwd=str(d), capture_output=True, text=True, timeout=_TIMEOUT)
    out = (p.stdout or "") + (getattr(p, "stderr", "") or "")   # real compiler errors land on STDERR
    failed = p.returncode != 0
    if is_red:                                 # RED: must fail, with the documented fragment
        if not failed:
            return {"codes": ["red_violation", "red_compiled"]}
        if frag not in out:                    # frag is non-empty here (empty short-circuits above)
            return {"codes": ["red_violation", "red_wrong_error"]}
        return {"codes": []}
    return {"codes": (["build_error"] if failed else [])}
