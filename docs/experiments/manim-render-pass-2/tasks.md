# Experiment 2 — held-out falsification of manim deepening round 2 (pre-registered)

**This file is committed BEFORE any answer is collected.** The commit that introduces it is
the pre-registration point. Operator instruction 2026-07-09: "run the tier-2 falsifications
for both packs."

## Question and arms

Does deepening round 2 (pack 64 → 77 claims, PR #22, pixel-sprite domain) improve held-out
scene authoring in the pinned renderer? Three arms:

- **base** — task text + the standard instruction only. No pack; no ship-rule weight.
- **kp64** — the pre-round-2 payload, assembled from master `0cdb536`
  (`examples/manim/CONTEXT.md` + `## Pack claims (all)` + Python-`sorted()` statement
  strings, one `- ` bullet each, trailing newline): **39,831 bytes, sha256
  `4283ff118adf9a6ca05129e8efc31f64001c74a78e61c6d3188ea5c4aa525a0b`** — byte-identical to
  the round-2 probe payload (same rule, same inputs; claims unchanged `c036839..0cdb536`).
- **kp77** — the post-round-2 payload from master `772daa0`, same rule: **42,969 bytes,
  sha256 `62bdbbbec735cd96a1de60df73e9faa33d5c1d138945c3d6d000425dda2d9b63`**. This is the
  **corrected** pack (the camera-follow claim includes `self.add(self.camera.frame)`), so the
  experiment measures the round as merged, not the pre-fix payload the round-2 remeasure saw.

**The headline comparison is kp77 vs kp64.**

- Model, all arms: `claude-haiku-4-5` (the pack's falsification primary; continuous with the
  first falsification). Fresh context per task per arm; headless, no tools; neutral scratch
  working directory. Instruction (verbatim, unchanged): *"Answer with the complete Manim
  Community Edition (v0.20.1) Python scene only, in a single ```python code block starting
  with `from manim import *`. No explanations, no tools. If the task needs multiple scenes,
  put them all in the same code block."*
- Prompt assembly for pack arms: task text, then the instruction, then
  `--- Reference pack (verified) ---`, then the payload.
- **Sprite scaffold (arm-neutral, same as the round-2 probe):** every task references the
  committed deterministic sprite assets (`sprite.png`, `sprite_0..3.png` from
  `docs/deepening/manim-round-2/probe/`); the gate mounts the answer directory containing
  `scene.py` plus copies of those PNGs. Scaffold, not answer content.
- Gate: first fenced block → `scene.py`, rendered as ONE unit (`manim -ql --disable_caching
  -a --media_dir /tmp/media scene.py`) in the pinned image
  (`manimcommunity/manim@sha256:f18f53f2…`), container-lifecycle bound at 300 s (timeout =
  FAIL). Renderlogs committed normalized.

## Metrics and ship rule (frozen)

- **Primary: render-pass** (container exit 0).
- **Secondary (mechanical, pre-registered): nearest-neighbor-technique presence** — an answer
  counts as carrying the technique iff its text matches the regex alternation
  `set_resampling_algorithm | resampling_algorithm\s*= | RESAMPLING_ALGORITHMS |
  Image\.NEAREST | Resampling\.NEAREST | NEAREST` (case-sensitive, any one suffices).
  Rationale: the round's headline beat teaches the crisp-pixel API; every task below shows a
  PNG sprite scaled up, so the technique is always apt. Known conservative bias, disclosed in
  advance: a squares-rebuild dodge produces crisp output without matching the regex and
  counts as absent — the metric measures *technique penetration*, not visual crispness.
- **Branch 1** — kp77 > kp64 on the primary → round-2 improves held-out render-pass.
- **Branch 2** — primary tied AND kp77 > kp64 on the secondary → scoped headline: the taught
  crisp-pixel technique penetrates held-out answers.
- **Branch 3** — anything else → **no headline**; composition reported observationally.
- n = 6 per arm; denominators everywhere; absolute numbers not comparable across experiments.
- **Observational (no ship-rule weight):** hand-check of every passing video (the round-2
  protocol), including whether camera-following answers add the frame to the scene (the
  corrected claim's step) — recorded, since render-pass cannot see it.

## Tasks

Six scene-authoring tasks. Held-out audit run **before** this freeze — checked against the 30
manim round-1/round-2 probe tasks, the 5 first-falsification tasks (code-walkthrough,
live-gauges, camera-tour, surface-hud, score-table), and the 46 fixture zones at `772daa0`.
**One draft dropped by the audit:** a boss-intro camera zoom-and-shake (restates the
falsification's camera-tour zoom mechanics and round-2 camfollow-2's zoom-then-track).
Disclosed adjacencies kept (mechanics differ): `crossing` shares occlusion-during-motion with
round-2 pixgrid-2 (tree pass) but stages it between two moving actors; `stairs` shares
vertical ascent with round-2 camfollow-3 (ladder) but has no camera work and discrete
per-step hops.

1. **health-bar** — The character (`sprite.png`, 1.5 units, crisp pixels) walks from left to
   center over 3 seconds with a small green health bar hovering just above it the whole way
   (bar + character move as one). At center, three red hits land one per second: each hit
   shrinks the bar's filled portion by a third (the empty track stays full-width), and the
   bar must stay attached above the character throughout.
2. **conveyor** — The character stands at center, feet on a conveyor belt: a horizontal strip
   of alternating gray tiles spanning the frame. For 4 seconds the belt tiles scroll
   continuously to the left beneath the stationary character; tiles that scroll off the left
   edge reappear on the right, so the belt never runs out.
3. **speech-bubble** — The character walks from the left edge to the right edge over 5
   seconds. Two seconds in, a speech bubble (a rounded white rectangle containing the text
   "!") pops in just above the character and rides along with it for 1.5 seconds, then fades
   out while the character keeps walking.
4. **crossing** — Two copies of the character (1.5 units, crisp pixels) walk toward each
   other from opposite edges, passing at center: the left-starting one must pass IN FRONT of
   the right-starting one — fully covering it where they overlap — and both keep walking to
   the far edge. The right-starting character faces left (mirrored) for its whole walk.
5. **stairs** — A staircase of five solid blocks rises from left to right. The character
   climbs it in 5 distinct hops — each hop an arc up-and-over onto the next step, with a
   brief landing pause on each — ending on the top step. The character faces right the whole
   climb and must stand ON each step (feet at the step's top surface), never inside it.
6. **minimap** — The character walks a large L-shaped route (right along the bottom, then up
   the right side) over 6 seconds. In the top-left corner a minimap shows the whole route as
   a thin polyline with a small dot that mirrors the character's position at 1/10 scale in
   real time; the minimap stays fixed in the corner the whole run.

## Layout

`answers/<task>/{base,kp64,kp77}.answer` (verbatim), `.renderlog` (normalized), `.result`
(`PASS` / `FAIL <first error line>`); summary + secondary-metric table in
`answers/results.txt`; verdict + analysis in `README.md` (written after gating).
