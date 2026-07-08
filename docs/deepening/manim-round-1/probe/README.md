# manim round-1 probe — protocol (declared before any answer was collected)

**Arm: current pack loaded** (this is deepening — residual gaps are what matter). Prompt =
task text + the standard instruction (below) + a line `--- Reference pack (verified) ---` +
the pack payload (`examples/manim/CONTEXT.md` + a `## Pack claims (all)` section with every
claim statement, sorted, one bullet each — 29,853 bytes for the 48-claim pack at `d908cca`).
Fresh context per task per model; headless, no tools.

- Models (pinned IDs): `claude-haiku-4-5` (the pack's falsification primary) and
  `claude-sonnet-4-6`, every task.
- Instruction (verbatim): *"Answer with the complete Manim Community Edition (v0.20.1) Python
  scene only, in a single ```python code block starting with `from manim import *`. No
  explanations, no tools. If the task needs multiple scenes, put them all in the same code
  block."*

## Mechanical repair rule (arm-neutral, pre-declared)

- The answer is saved verbatim (`<model>.answer`). The **first fenced code block** is the
  source (the whole answer if unfenced); written unchanged to `scene.py`. **No source edit,
  ever.**
- The whole answer is gated as **ONE unit**: `manim -ql --disable_caching -a --media_dir
  /tmp/media scene.py` in the pinned oracle image
  (`manimcommunity/manim@sha256:f18f53f2…`, tag v0.20.1 — the same image, quality flag, and
  caching flag as the pack's `manim-render` runner). The `-a` flag renders **every** Scene
  subclass in the file, so a failure in ANY scene is observed (the multi-module analog of the
  sui probes' one-package rule; the runner's single-scene invocation would interactively
  prompt on multi-scene files).
- Container lifecycle mirrors the runner's containment (the recorded hang class): detached
  `docker run -d` with the answer directory mounted read-only, `docker wait` bounded at
  300 s, `docker logs`, then unconditional `docker rm -f`. A wait expiry is recorded as
  `FAIL render_timeout` — a render that never finishes is a failure, never a pass.
- **PASS** = container exit 0. **FAIL** = nonzero exit or timeout; the first error line from
  the normalized log (ANSI stripped, box-drawing characters dropped, whitespace collapsed —
  the runner's normalization) is recorded in `<model>.result`. Full normalized logs are
  committed as `<model>.renderlog`.
- Layout: `probe/<territory>-<k>/{task.md, <model>.answer, <model>.result, <model>.renderlog}`;
  summary in `probe/results.txt`.

## Recorded oracle limitation

The render gate observes API-shape failures (exceptions), not visual/timing correctness. A
scene that renders but animates the wrong thing (e.g. a stale `Transform` source) records as
PASS here; territory 3 was chosen knowing this — such corners can only ship as GREEN +
doc-grounding beats, and any PASS-but-visually-wrong observation is recorded in the triage as
an oracle-limitation note, not a FAIL.
