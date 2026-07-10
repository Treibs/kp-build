# manim round-2 probe — protocol (declared before any answer was collected)

**Arm: current pack loaded** (this is deepening — residual gaps are what matter). Prompt =
task text + the standard instruction (below) + a line `--- Reference pack (verified) ---` +
the pack payload (`examples/manim/CONTEXT.md` + a `## Pack claims (all)` section with every
claim statement, sorted, one bullet each) — assembled from the 64-claim pack at master
`0cdb536` by the same rule as every prior probe. Fresh context per task per model; headless,
no tools; collection from a neutral scratch working directory.

- Models (pinned IDs): `claude-haiku-4-5` (the pack's falsification primary) and
  `claude-sonnet-4-6`, every task.
- Instruction (verbatim, unchanged from round 1): *"Answer with the complete Manim Community
  Edition (v0.20.1) Python scene only, in a single ```python code block starting with
  `from manim import *`. No explanations, no tools. If the task needs multiple scenes, put
  them all in the same code block."*

## Sprite-asset scaffold rule (arm-neutral, pre-declared)

Territories 1–4 animate a pixel-art character from PNG assets. The assets are **provided by
the apparatus, identical for every task and model**: `sprite.png` (a 16×16 pixel person,
frame 0) and `sprite_0.png … sprite_3.png` (a 4-frame walk cycle: step-right, together,
step-left, together). They are generated deterministically by the committed
[`make_sprites.py`](make_sprites.py) (byte-identical on every run; frames 1 and 3 are the
same "together" pose by design) and committed next to it. Task texts state exactly which
files sit in the working directory; the gate mounts the task's answer directory containing
`scene.py` plus copies of these PNGs, so an answer that loads them by relative filename
renders. This is scaffold, not answer content — no answer text is ever edited.

## Mechanical repair rule (arm-neutral, unchanged from round 1)

- The answer is saved verbatim (`<model>.answer`). The **first fenced code block** is the
  source (the whole answer if unfenced); written unchanged to `scene.py`. **No source edit,
  ever.**
- The whole answer is gated as **ONE unit**: `manim -ql --disable_caching -a --media_dir
  /tmp/media scene.py` in the pinned oracle image (`manimcommunity/manim@sha256:f18f53f2…`,
  tag v0.20.1 — the same image, quality flag, and caching flag as the pack's `manim-render`
  runner). `-a` renders every Scene subclass so a failure in ANY scene is observed.
- Container lifecycle mirrors the runner's containment (the recorded hang class): detached
  `docker run -d` with the answer directory mounted read-only, `docker wait` bounded at
  300 s, `docker logs`, then unconditional `docker rm -f`. A wait expiry is recorded as
  `FAIL render_timeout` — a render that never finishes is a failure, never a pass.
- **PASS** = container exit 0. **FAIL** = nonzero exit or timeout; the first error line from
  the normalized log (ANSI stripped, box-drawing characters dropped, whitespace collapsed) is
  recorded in `<model>.result`. Full normalized logs are committed as `<model>.renderlog`.
- **Hand-check every PASS** (the round-1 lesson: 3 of 6 beats were render-blind): every
  passing render's output video is opened and eyeballed against the task text before triage;
  PASS-but-visually-wrong observations are recorded in the triage as oracle-limitation notes.
- Layout: `probe/<territory>-<k>/{task.md, <model>.answer, <model>.result, <model>.renderlog}`;
  summary in `probe/results.txt`. Sprite PNGs live once at the probe root (this directory),
  not per-task; the gate copies them into each mounted directory at render time.

## Held-out check (done before collection)

Every task was checked against the 15 manim round-1 probe tasks, the 5 falsification tasks
(code-walkthrough, live-gauges, camera-tour, surface-hud, score-table), and the pack's 29
fixture zones — and restates none of them. Disclosed adjacencies (mechanics differ):
`camfollow-*` vs the pack's `moving-camera` beat (one-shot `frame.animate` move — the probe's
corner is the *continuous follow-updater* on a moving target) and vs the falsification
camera-tour (sequential zooms to three *fixed* boxes); `frames-*` vs the pack's updater beats
(tracker/lifecycle patterns — the probe's corner is *asset swapping on a dt timer*, an
untaught shape). One draft was dropped by the audit: a "pulsing idle sprite" task (restates
updutil-3's scale-oscillation updater with an image instead of a circle).

## Task index

| territory | tasks |
|---|---|
| 1 imgpx (ImageMobject pixel surface) | imgpx-1 (big crisp sprite), imgpx-2 (three sizes side by side), imgpx-3 (hurt blink) |
| 2 frames (sprite frame cycling) | frames-1 (walk cycle in place), frames-2 (walk and stop), frames-3 (two walkers, different cadence) |
| 3 path (path locomotion) | path-1 (rectangular track lap), path-2 (zig-zag dash + hop), path-3 (circular orbit, facing travel) |
| 4 camfollow (2D camera follow) | camfollow-1 (side-scroll follow), camfollow-2 (zoom then track), camfollow-3 (climb with visible ground) |
| 5 pixgrid (programmatic pixel art + layering) | pixgrid-1 (build person from squares over tiles), pixgrid-2 (walk behind a tree), pixgrid-3 (damage flash, pixels fall away) |
