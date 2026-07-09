# manim deepening — round 2 — territories

**Date:** 2026-07-09 · **Pack at round start:** 64 claims (38 execution + 26 grounding) at
master `0cdb536` (pack claims unchanged since the manim round-1 merge `c036839`) · **Oracle:**
pinned Docker image `manimcommunity/manim@sha256:f18f53f2…` (tag v0.20.1, exact-version
guard), `manim -ql --disable_caching` via the container-lifecycle protocol · **Design:**
`docs/specs/2026-07-07-kp-deepen-design.md` · **Skill:** `skill-deepen/SKILL.md`.
Precondition check: the committed pack rebuilt fully green (38/38 execution, 26/26 grounding,
validation OK) before this round started.

## Gate 1 — approval

Operator focus directive 2026-07-09 (verbatim): *"I would like a pixel person running through
or around a scene. think like pokemeon style"* — a user-chosen animation domain for the
round, per the deepening thesis that depth follows where the *owner* wants the pack strong.
The five territories below were proposed; the operator selected **"Modify the list"** and then
**"Programmatic pixel art too"** (option text: *"Add/blend a territory: building the pixel
person from Square/VGroup grids in code (no PNG assets) — more robust for render-gating,
still authentically pixel-style"*). Applied as a blend, keeping the round at five
territories: programmatic pixel-art construction replaces standalone layering as territory 5,
and the layering/z-order corners fold into its tasks (they arise naturally in grid + background
composition). No other change.

## Approved territories

Unlike round 1 (which spread across the animation-composition surface), round 2 concentrates
on one authoring domain: **a pixel-art character moving through a scene**. The image/sprite
surface has **zero existing pack claims** — no ImageMobject, path-following, or z-index zone
exists — so four of five territories are entirely unprobed ground.

| # | territory | why it's a candidate (unprobed + stale-knowledge-prone) |
|---|---|---|
| 1 | **ImageMobject pixel-asset surface** (`imgpx`) — loading a sprite PNG and displaying it crisp (nearest-neighbor) at scale | No image zone in the pack. CE's crisp-pixel API (`set_resampling_algorithm` / `RESAMPLING_ALGORITHMS["nearest"]`) is obscure; PIL-style kwargs (`interpolation=`, `filter=`) and manimgl forms are the likely parametric fill-ins. Pixel art displayed without it is blurry — the render gate catches wrong-API shapes; blur itself is render-blind and handled by the hand-check step |
| 2 | **Sprite frame cycling** (`frames`) — walk-cycle animation by swapping frames on a timer (dt-accumulating updaters, `become`/pixel swaps, updater removal/suspension mid-scene) | The pack's updater beats (round 1 + originals) cover tracker patterns, utility namespaces, and the animate-vs-updater hang — not texture/frame swapping. Frame swap via `become()` on `ImageMobject` is version-sensitive and unprobed. Tasks must not restate the five existing updater fixtures |
| 3 | **Path locomotion** (`path`) — `MoveAlongPath` along tracks/shapes, direction flips at corners, facing-the-travel-direction | No path zone exists. Composing locomotion with orientation changes is the heart of "running around a scene"; `MoveAlongPath` + simultaneous flip/rotate composition is semantics-heavy and the rotation-follows-path corner invites stale `angle`/updater APIs |
| 4 | **2D camera follow** (`camfollow`) — a follow-updater on `camera.frame` continuously tracking the moving sprite | Adjacent to two prior artifacts, disclosed: the pack's `moving-camera` beat pins the one-shot `self.play(self.camera.frame.animate…)` move, and the falsification task camera-tour zooms to three *fixed* boxes — the *continuous follow of a moving target* (add_updater on `camera.frame`) is a distinct, untaught shape. manimgl bleed risk (`self.camera_frame`, `frame.reorient`) is high |
| 5 | **Programmatic pixel art + layering** (`pixgrid`) — building the pixel person from `Square`/`VGroup` grids in code; background tiles; z-order (`z_index`, `add_to_back`, draw order) with mixed stacks | The operator-added territory. Grid assembly (`VGroup` + `arrange_in_grid`/manual placement) is untaught; Cairo's layering of `ImageMobject` vs `VMobject` stacks is a known confusion surface with no pack claim. Some layering corners are render-blind — those can only ship GREEN + doc-grounding, per the recorded oracle limitation |

## Deliberately excluded

- **Round-1's standing exclusions stand unchanged:** rate functions (judgment-only — a wrong
  `rate_func` renders clean), the OpenGL renderer surface, the scene/section CLI surface, and
  Text/MathTex authoring depth (shipped beats cover it).
- **Visual pixel-perfection judgments** (does the character *look* like a Pokémon sprite):
  pure aesthetics, no oracle. The render gate + hand-check can observe API shape and gross
  structure only; anything finer is the blind-judge axis's territory, not a render round's.
- **GIF/video sprite assets** (`ImageMobject` from animated files): out of scope — the pinned
  runner renders single scenes from static assets; animated-file handling is a runner
  extension, recorded as a candidate follow-on, not a probe territory.
- **Round-1 territory re-probes** (composition timing, transform family, 3D camera, updater
  utilities, legacy syntax): probed last round; residuals there are round-3 ledger material,
  not this round's focus.

## Probe shape

15 fresh scene-authoring tasks (3 per territory), dual model (`claude-haiku-4-5` primary,
`claude-sonnet-4-6` secondary), **current 64-claim pack loaded** in every run, gated by the
pinned image with the round-1 container-lifecycle protocol (300 s bound, unconditional rm).
Task freshness audited against: the 15 manim round-1 probe tasks, the 5 falsification tasks
(code-walkthrough, live-gauges, camera-tour, surface-hud, score-table), and the pack's 29
fixture zones. Sprite-asset scaffold rule (deterministic, arm-neutral, committed) pre-declared
in `probe/README.md` before any answer. **Hand-check every PASS** (the round-1 lesson: 3 of 6
beats were render-blind) — every passing render's video is opened and eyeballed against the
task before the territory is recorded clean.
