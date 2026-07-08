# Tier-1 remeasure — manim deepening round 1

**Date:** 2026-07-08 · **Pack:** deepened 64-claim pack (commit `dde95c9`), payload = `CONTEXT.md` + all 64 claim statements (same assembly as the probe payload) · **Oracle:** same digest-pinned image and gate as the probe (`manim -ql --disable_caching -a`, 300 s container-lifecycle timeout) · **Models:** same pinned IDs as the probe (claude-haiku-4-5, claude-sonnet-4-6), fresh context per task.

> **Tier-1 numbers are tainted — these tasks selected the beats. Trend signal only; headline numbers come from pre-registered held-out falsification (tier 2).**

## What was re-run

Exactly the failed probe runs — the two render-gate FAILs plus the three render-blind wrong answers found by hand inspection (the API-shape oracle cannot see those, so their remeasure verdict is also by hand inspection, recorded below).

## Flip table

| task | model | probe failure | remeasure gate | remeasure behavior | flip |
|---|---|---|---|---|---|
| legacy-3 | haiku-4-5 | `TypeError: Circle.surround() got an unexpected keyword argument 'buffer'` | PASS | — (gate-class failure) | FAIL→PASS |
| camera3d-3 | haiku-4-5 | `TypeError: Mobject.__init__() got an unexpected keyword argument 'size'` (`Cube(size=2)`), plus unreached `self.camera.frame` manimgl bleed | PASS | — (gate-class failure) | FAIL→PASS |
| camera3d-1 | haiku-4-5 | rendered, but phi/theta convention swapped (view stayed top-down); `distance=` silently swallowed | PASS | **correct**: `set_camera_orientation(phi=70*DEGREES, theta=0)` (phi = polar from vertical, per CE convention), orbit via animated `move_camera(theta=2*PI, run_time=4)`, no `distance=` | WRONG→CORRECT |
| camera3d-2 | haiku-4-5 | rendered, but phi/theta swapped — "straight down → side-on" never left top-down | PASS | **correct**: `phi=0` (straight down) animated to `phi=90*DEGREES` over 2 s (side-on), no `distance=` | WRONG→CORRECT |
| compose-1 | sonnet-4-6 | rendered, but `lag_ratio≈0.111` → ~1.44 s total vs the required 3 s | PASS | **correct**: `lag_ratio=0.5` with five unit fades → natural duration 1 + 4×0.5 = 3 s, matching `run_time=3` exactly; each fade starts when the previous is halfway done | WRONG→CORRECT |

**Result: 5/5 flipped** (2 gate FAIL→PASS, 3 hand-inspected WRONG→CORRECT).

## Notes

- Behavioral verdicts (camera3d-1, camera3d-2, compose-1) are hand-inspected against the task text, not gate-decided — same method that found them in the probe.
- Raw artifacts per run in `remeasure-runs/<task>/<model>.{answer,result,renderlog}` (renderlogs ANSI-stripped; `.stderr` gitignored).
- The tainted label above is the only legitimate reading of these numbers: the six beats were drafted *from* these five failures, so a flip here demonstrates the beats teach what they were written to teach — nothing more. Held-out value is a tier-2 question.
