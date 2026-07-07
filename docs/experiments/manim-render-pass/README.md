# manim falsification — render-pass (pre-registered, dual model)

**Pre-registration:** [`tasks.md`](tasks.md), committed at `a8bb596` **before any
answer was collected**. Five held-out tasks in the measured weakness territories
(none a pack fixture), two arms (base / kp), two models (claude-haiku-4-5 primary,
claude-sonnet-4-6 secondary), metric = render-pass in the pinned container
(`manimcommunity/manim@sha256:f18f53f2…`), 300 s timeout = FAIL.

Harness notes (arm-neutral, applied identically to every answer): prompts are
exactly the pre-registered text; every model wrapped its source in a markdown
fence, so the first fenced block of each raw output (saved verbatim as
`answers/…/task<N>.py.raw`) was taken as the answer. No answer needed the
pre-registered multi-Scene repair — all 20 defined exactly one Scene subclass.

## Results

| Task | base haiku | kp haiku | base sonnet | kp sonnet |
|---|---|---|---|---|
| 1 code-walkthrough | FAIL `Code(code=)` | FAIL `Code(font_size=)` | FAIL `Code(code=)` | FAIL `Code(font_size=)` |
| 2 live-gauges | **FAIL timeout 300 s** | PASS | PASS | PASS |
| 3 camera-tour | FAIL `Camera…no attribute 'frame'` | PASS | PASS | PASS |
| 4 surface-hud | PASS | PASS | PASS | PASS |
| 5 score-table | PASS | FAIL `Text` in table data | PASS | PASS |
| **render-pass** | **2/5** | **3/5** | **4/5** | **4/5** |

Raw log: [`results.txt`](results.txt).

**Verdict under the pre-registered ship rule:** primary (haiku) kp 3/5 > base 2/5
→ **rule branch 1 → the pack ships.** Secondary (sonnet) ties 4/5 vs 4/5,
consistent with the probe's honest-scope prediction: for strong models on common
scene types render-pass is near ceiling, and the pack's measured value is on the
weaker/cheaper model.

## Failure detail

- **base haiku task 2 — the hang beat, in the wild.** The base answer attached a
  digit-count-changing updater to a `DecimalNumber` and then animated a
  ValueTracker through `self.play(...)` — the exact naive form of the pack's
  animate-live-updater RED fixture. On 0.20.1 the mid-interpolation crash strands
  the SceneFileWriter's non-daemon writer thread, so the render hung past the
  traceback and hit the 300 s container timeout. The kp answer used
  `always_redraw` per the pack and passed.
- **base haiku task 3** used camera zoom on a plain `Scene`
  (`AttributeError: 'Camera' object has no attribute 'frame'`); the kp answer
  used `MovingCameraScene` + `self.camera.frame` per the pack and passed.
- **task 1 — an honest new gap, both models.** Both base arms wrote the pre-0.19
  `Code(code=...)` (the pack's beat, confirmed). Both kp arms *fixed* that —
  `code_string=` per the pack — and then failed on a kwarg the pack never
  mentions: `Code.__init__() got an unexpected keyword argument 'font_size'`.
  The pack teaches the renamed source kwarg but not the constructor's full
  (narrowed) kwarg surface. Recorded for a pack revision, not patched post-hoc.
- **kp haiku task 5 — an over-generalization gap.** The kp answer wrapped table
  *data cells* in `Text(...)` (`Table` data must be strings; `MobjectTable` takes
  mobjects), over-applying the pack's labels-are-mobjects beat. The base answer
  kept string data and passed. The beat statement scopes to labels; a revision
  should state the data-cell contrast explicitly.

## Scope of the shipping claim

The pack raises render-pass for the small model (haiku 3/5 vs 2/5) and removes
two weakness-territory failures (manimgl camera bleed, the updater hang) at the
cost of one over-generalization (task 5). It does not raise render-pass for
claude-sonnet-4-6 at this task difficulty (tie at 4/5) — its sonnet-visible
effect is changing *which* error occurs on the shared `Code` gap, not whether
one occurs.
