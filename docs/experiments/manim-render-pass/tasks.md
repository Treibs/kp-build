# Held-out tasks — manim falsification (pre-registered)

**This file is committed before any answer is collected** — the commit timestamp is the
pre-registration. The probe tasks are tainted (they selected the beats); these five are fresh
prompts in the measured weakness territories, none appearing as a pack fixture.

## Tasks

1. **code-walkthrough** — Display a syntax-highlighted Python function (any short function),
   then visually highlight two different lines of it in sequence.
2. **live-gauges** — Three numeric counters count up simultaneously from 0 to different
   targets while a bar next to each grows in proportion; the numbers must update live.
3. **camera-tour** — Three labeled boxes spread across the frame; zoom the camera into each
   one in sequence, then zoom back out to the full layout.
4. **surface-hud** — A 3D surface plot with a title pinned to a screen corner that stays
   fixed while the camera orbits the surface.
5. **score-table** — A table comparing two algorithms across three criteria; highlight the
   winning cell in each row, one row at a time.

## Protocol

- **base** arm: fresh agent context, ONLY the task text plus: "Write a single Manim Community
  Edition scene file (one Scene subclass) that renders with `manim`. Answer with the Python
  source only. Do not use any tools — write from memory."
- **kp** arm: identical prompt PLUS the pack (CONTEXT.md + all claim statements from
  `examples/manim/`). Fresh context per task.
- Models: **primary = claude-haiku-4-5** (probe render-pass baseline ~67% — real headroom);
  **secondary = claude-sonnet-4-6** (probe ~83%; ties expected). Both arms, both models,
  all 5 tasks: 20 answers.
- Metric: **render-pass** in the pinned container
  (`manimcommunity/manim@sha256:f18f53f2e4eaf2ea41713437d34363fb3f5cc6008b03fd798676ac0359396c3b`),
  same gate command as the fixtures
  (`-ql --disable_caching --media_dir /tmp/media`), container-lifecycle timeout 300 s
  (timeout = FAIL). Exit 0 = PASS.
- Arm-neutral mechanical repair (pre-registered): the answer is saved as `scene.py` unchanged.
  If it contains more than one Scene subclass, the render command names the FIRST-defined
  subclass; no other edit of any kind.

## Ship rule (pre-registered — no post-hoc metric may be substituted)

- **Branch 1:** haiku kp > haiku base (render-pass /5) → the pack ships (primary cleared).
- **Branch 2:** haiku tied AND sonnet kp > sonnet base → ships with the scoped claim
  (helps the strong model; small-model claim unproven at this N).
- **Branch 3:** haiku kp < haiku base → exit 1, does not ship. Both tied or secondary
  not better → exit 3 (inconclusive), does not ship.
