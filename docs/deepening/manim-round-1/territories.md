# manim deepening — round 1 — territories

**Date:** 2026-07-08 · **Pack at round start:** 48 claims (28 execution + 20 grounding) at
master `d908cca` (claims unchanged since the pack merged at `2ce3157`) · **Oracle:** pinned
Docker image `manimcommunity/manim@sha256:f18f53f2…` (tag v0.20.1, exact-version guard),
`manim -ql --disable_caching` via the `manim-render` container-lifecycle runner
· **Design:** `docs/specs/2026-07-07-kp-deepen-design.md` · **Skill:** `skill-deepen/SKILL.md`

This is the manim pack's **first** deepening round. Directory note: the existing
`docs/deepening/round-1..3/` are all sui-move rounds from before deepening went multi-pack;
from this round on, round directories are prefixed with the pack name (`manim-round-1`).
Round numbering is per pack.

## Gate 1 — approval

Owner directive 2026-07-08: "go deeper on the animation to ultimately improve the LLM's
ability to create detailed animations using manim", followed by explicit approval of the
five proposed territories: "approved — run the manim round with all five territories."
No changes were made to the proposed list.

## Approved territories

All five are **animation-focused** by design (the owner's stated goal), biased toward
corners where parametric knowledge is likely stale — the 0.x → CE rewrite moved or deleted
most of the animation-composition surface.

| # | territory | why it's a candidate (unprobed + stale-knowledge-prone) |
|---|---|---|
| 1 | **Removed animation syntax** | The old `self.play(mob.method, arg)` form (pre-0.19 method-animation passing) and deleted animation names (`FadeInFrom`, `FadeOutAndShift`, `ShrinkToCenter`, …) are the highest-volume training-data forms; the pack pins only `ShowCreation` → `Create` (`create-rename`) — tasks here must NOT restate that fixture. |
| 2 | **Composition primitives** | `AnimationGroup` / `Succession` / `LaggedStart` with `lag_ratio` / `run_time` semantics are the heart of "detailed animations" (sequencing + overlap); zero pack fixtures touch them. |
| 3 | **Transform-family mismatches** | `Transform` vs `ReplacementTransform` staleness (animating the stale source afterward), `TransformMatchingTex` applied to `Text` — semantics-heavy, partially render-detectable; unprobed. |
| 4 | **3D camera movement** | manimgl bleed: `self.camera.frame` / `reorient` on a `ThreeDScene` vs CE's `set_camera_orientation` / `move_camera` / `begin_ambient_camera_rotation`. The pack's `moving-camera` beat covers only the 2D `MovingCameraScene` case; 3D is unprobed. |
| 5 | **Updater utilities** | manimgl's `always` / `f_always` (NameError in CE), CE's own `always_shift` / `always_rotate` / `turn_animation_into_updater` (untaught utility namespace), and play/updater suspension semantics (`suspend_mobject_updating`). The pack's five updater beats cover tracker patterns, not the utility namespace — tasks must not restate them. |

## Deliberately excluded

- **Rate functions** (`rate_func`, `there_and_back`, …) — render-pass cannot distinguish a
  wrong-but-valid rate function from the right one; pure-judgment corner, deferred to a
  blind-judge axis.
- **OpenGL renderer surface** (`--renderer=opengl`, interactive `self.interact()`) — a
  different oracle configuration, not the pinned gate.
- **Scene/section CLI surface** (`--save_sections`, partial renders) — already grounded by
  `render-cli-doc`; CLI behavior, not authoring knowledge.
- **Text/MathTex authoring depth** — covered by the shipped `mathtex`, `text-pango`,
  `markuptext` beats; restating them adds nothing.

## Recorded oracle limitation (carried into triage and the ledger)

The render-pass gate proves an animation **renders**, not that it looks or is timed right.
Failures here are API-shape failures (exceptions at render time); corners whose failure mode
is *visually wrong but renders clean* (e.g. a stale `Transform` source silently animating a
ghost) can only ship as GREEN + doc-grounding beats. True animation-correctness measurement
needs a runner extension (ffprobe frame/duration assertions) or the V2-c blind-judge axis —
recorded as a candidate follow-on, out of scope for this round.

## Known risk (carried from the pack build)

Mid-`play` REDs can hit the recorded hang class (`SceneFileWriter` non-daemon writer thread
blocking on `queue.get()` post-traceback — beat-log Part III). The runner's container-
lifecycle gate (detached run + bounded `docker wait` + unconditional rm) contains it at 300 s
per render; RED fixtures that crash mid-play are still preferred minimized to crash as early
as possible.
