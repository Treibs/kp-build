"""Regression harness for the shipped example packs (graft from the Stage-3 'harden-the-seam' lens).

The examples/ README calls the research.json files "regression fixtures", but until now nothing
rebuilt them in CI. Two layers:
  1. every examples/*.research.json must still assemble + validate + ship a non-empty pack offline
     (--no-verify), guarding against an assembly/schema regression silently emptying a pack;
  2. the doc-grounding fixtures must additionally pass the REAL --ground-verify gate offline and
     deterministically (critic #5: under --no-verify the grounding claims are stamped unchecked, so
     layer 1 alone never exercises the gate — the demonstrand needs its own assertion).
"""
import json
from pathlib import Path

import pytest

from kp_build import cli

REPO = Path(__file__).resolve().parent.parent
RESEARCH = sorted((REPO / "examples").glob("*.research.json"))


@pytest.mark.parametrize("rj", RESEARCH, ids=lambda p: p.stem)
def test_example_pack_builds_nonempty_offline(rj, tmp_path):
    """Every shipped input still builds, validates, and ships a non-empty claim spine (offline)."""
    out = tmp_path / rj.stem
    rc = cli.main(["build", "-i", str(rj), "-o", str(out), "--no-verify", "--built", "2026-01-01"])
    assert rc == 0, f"{rj.name} failed to build under --no-verify"
    stats = json.loads((out / "wikillm.json").read_text())["stats"]
    assert stats["claims"] > 0, f"{rj.name} shipped an EMPTY claim spine"


def test_rfc9110_grounding_gate_fires_offline_and_deterministic(tmp_path):
    """RFC 9110 fixture: --ground-verify ships the 6 verbatim claims and DROPS the fabricated PATCH
    clause (ungrounded), fully offline from the committed corpus, byte-identical on rebuild."""
    inp = "examples/http-semantics-grounding.research.json"
    a, b = tmp_path / "a", tmp_path / "b"
    assert cli.main(["build", "-i", inp, "-o", str(a), "--ground-verify", "--built", "2026-01-01"]) == 0
    assert json.loads((a / "wikillm.json").read_text())["stats"]["claims"] == 6
    assert (a / "claims" / "get-semantics.md").exists()
    assert not (a / "claims" / "patch-fabricated.md").exists()          # the held-out fabrication drops
    assert cli.main(["build", "-i", inp, "-o", str(b), "--ground-verify", "--built", "2026-01-01"]) == 0
    assert (a / "CONTEXT.md").read_text() == (b / "CONTEXT.md").read_text()   # deterministic


def test_vwt_grounding_gate_fires_offline(tmp_path):
    """Variable-Width Transformers fixture: --ground-verify ships the 3 verbatim claims and DROPS the
    inflated-numbers fabrication (wrong %, wrong direction) — offline from the committed abstract."""
    inp = "examples/vwt-grounding.research.json"
    out = tmp_path / "vwt"
    assert cli.main(["build", "-i", inp, "-o", str(out), "--ground-verify", "--built", "2026-01-01"]) == 0
    assert json.loads((out / "wikillm.json").read_text())["stats"]["claims"] == 3
    assert not (out / "claims" / "inflated-numbers-fabricated.md").exists()
