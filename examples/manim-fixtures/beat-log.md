# manim fixture beat log — experiment record

The container is the arbiter. Every row below is an observation from the pinned oracle image
`manimcommunity/manim@sha256:f18f53f2e4eaf2ea41713437d34363fb3f5cc6008b03fd798676ac0359396c3b`
(tag `v0.20.1`; Manim Community v0.20.1), rendered via the `manim-render` runner's
container-lifecycle gate (`manim -ql --disable_caching --media_dir /tmp/media scene.py`,
detached run + bounded wait + unconditional rm). RED fragments in `expected_error.txt` are
pasted from the observed (normalized) log line, never from memory.

## Part I — rewritten APIs (proven 2026-07-06)

| beat | red result: exit + fragment observed | green: exit | notes |
|---|---|---|---|
| code-api | exit 1; `Code.__init__() got an unexpected keyword argument 'code'` | 0 | 0.19 rewrite: `code=` → `code_string=`. Fragment matched the probe candidate verbatim. |
| axes-length | exit 1; `TypeError: Mobject.__init__() got an unexpected keyword argument 'width'` | 0 | Observed kwarg was `'width'`; fragment kept generic (`Mobject.__init__() got an unexpected keyword argument`) because which of `width`/`height` is named varies with kwargs-dict order. |
| table-labels | exit 1; `Only values of type VMobject can be added as submobjects of VGroup` | 0 | String labels rejected — labels must be mobjects (`Text(...)`). |
| barchart-update | (no red — rebuilding the chart also renders; the beat's value is the `change_bar_values` idiom) | 0 | GREEN only. |

All 7 Part I fixtures proved OK through the real runner (greens gate `render_error`,
reds gate `red_violation`; proving script exit 0). No scene code changed from the plan
candidates; no hangs — every container exited within the bounded wait.

## Part II — manimgl boundary (proven 2026-07-06)

| beat | red result: exit + fragment observed | green: exit | notes |
|---|---|---|---|
| fixed-frame | exit 1; `AttributeError: Text object has no attribute 'fix_in_frame'` | 0 | manimgl's `fix_in_frame()` doesn't exist in CE; use `add_fixed_in_frame_mobjects`. Candidate fragment was generic; observed line is deterministic, pasted verbatim. |
| moving-camera | exit 1; `AttributeError: 'CameraFrameZoom' object has no attribute 'camera_frame'` | 0 | `self.camera_frame` (manimgl) doesn't exist on a plain `Scene`; CE is `MovingCameraScene` + `self.camera.frame`. Observed line pasted verbatim (scene-class name is part of it, deterministic). |
| create-rename | exit 1; `name 'ShowCreation' is not defined` | 0 | manimgl `ShowCreation` → CE `Create`. Fragment matched the harness-check-proven candidate verbatim. |

## Part III — animation × updater (proven 2026-07-06)

| beat | red result: exit + fragment observed | green: exit | notes |
|---|---|---|---|
| animate-live-updater | exit 1; `ValueError: zip() argument 2 is longer than argument 1` | (no green — the safe forms are the next beats) | **Hang class — see below.** RED only. |
| updater-detach | — | 0 | Drive the tracker, detach the updater before animating the carrier. |
| always-redraw | — | 0 | Rebuild-per-frame live label; probe-green on both models. |
| updater-lifecycle | — | 0 | dt-updater add → wait → remove → animate. |
| value-tracker | — | 0 | `ValueTracker` + `.animate.set_value` canonical driver. |

### animate-live-updater hang investigation (2026-07-06)

The plan's candidate scene (bare `self.play` of the carrier + tracker) crashes with the
documented `ValueError: zip() argument 2 is longer than argument 1` mid-interpolation — and
then **hangs forever post-traceback**: the runner raised `render_timeout` after 300 s
(wall-clock 5 m 09 s; the container WAS force-removed — `docker ps` clean afterward).

Root cause (read from the pinned image's source): `SceneFileWriter.open_partial_movie_stream`
(scene_file_writer.py:583) starts a **non-daemon** `writer_thread` blocking on `queue.get()`;
the sentinel `(-1, None)` is only sent by `close_partial_movie_stream`, which an exception
escaping `play` never reaches — so interpreter shutdown blocks joining the thread. Any
mid-render-loop crash hangs by construction on 0.20.1 (every other RED in this pack crashes
before `file_writer.begin_animation`, which is why only this beat hung).

Restructure (plan's hang fallback — "the exception escapes the render loop"): the fixture
wraps the crashing `self.play` in `try/except`, releases the stranded writer thread with the
writer's own sentinel (`self.renderer.file_writer.queue.put((-1, None))`), and **re-raises** —
the weakness still fires unmodified inside manim, manim's CLI prints the genuine traceback,
and the process exits 1. Proven through the real runner: **exit 1 with the fragment in
10.7 s wall-clock** (including the version probe), gate `red_violation` → `{"codes": []}`.
The post-traceback hang is itself part of the documented weakness (recorded here; the probe
container hung ~4 h the same way).

All 11 Part II+III fixtures proved OK through the real runner in one batch (proving script
exit 0, 1 m 08 s wall-clock; the two updated AttributeError fragments re-proven after the
verbatim-paste update). Scene code changed from the plan candidates only for
animate-live-updater/red (the try/except/sentinel restructure above); fragments updated from
candidates for fixed-frame and moving-camera (observed text wins).

## Part IV — spine (proven 2026-07-06)

| beat | red result: exit + fragment observed | green: exit | notes |
|---|---|---|---|
| scene-anatomy | (no red — the beat's value is the `construct`/`add`/`play`/`wait` anatomy itself) | 0 | GREEN only. |
| class-shadowing | exit 1; `TypeError: Scene.__init__() got an unexpected keyword argument 'font_size'` | 0 | `class Text(Scene)` shadows `manim.Text` under `from manim import *`; the inner `Text("hello", font_size=40)` recursively constructs the Scene subclass. Candidate fragment was generic; observed line is deterministic (`'font_size'` is the first kwarg Text passes that Scene rejects), pasted verbatim and re-proven. |
| mathtex | exit 1; `LaTeX compilation error` (then `ValueError: latex error converting to dvi`) | 0 | `$` delimiters inside `MathTex` break LaTeX — MathTex is already math mode. Fragment matched the harness-check-proven candidate verbatim. |
| config-surface | (no red — pinned by experiment: `config.frame_width` is readable inside a scene) | 0 | GREEN only. |

All 6 Part IV fixtures proved OK through the real runner in one batch (proving script exit 0;
greens gate `render_error`, reds gate `red_violation`). No scene code changed from the plan
candidates; no hangs — both reds crash before `file_writer.begin_animation`, so the containers
exited within the bounded wait. class-shadowing/red re-proven after the verbatim-paste update.
Full fixture census: **24** (15 green + 9 red).

## Part V — falsification revision beats (proven 2026-07-07)

Both beats were queued from the pre-registered falsification run (docs/experiments/manim-render-pass/):
the pack moved models past one error and into a new gap (code-fontsize), and one beat was
over-applied past its boundary (table-data-cells). Same oracle, same runner, same discipline.

| beat | red result: exit + fragment observed | green: exit | notes |
|---|---|---|---|
| code-fontsize | exit 1; `TypeError: Code.__init__() got an unexpected keyword argument 'font_size'` | 0 | The 0.19 rewrite narrowed the constructor: text styling moved into `paragraph_config` (a dict passed to the underlying Paragraph; `font_size` is a documented `default_paragraph_config` key). Both kp arms in the falsification hit exactly this. |
| table-data-cells | exit 1; `TypeError: sequence item 0: expected str instance, Text found` | 0 | Data cells feed `element_to_mobject` (default Paragraph) — mobjects in DATA cells crash inside Paragraph's `"\n".join`. The mobject-cell form is `MobjectTable`. Boundary beat for table-labels (labels ARE mobjects). kp-haiku failed this in the falsification. |

All 4 Part V fixtures proved OK through the real runner in one batch (greens gate
`render_error`, reds gate `red_violation`, all `{"codes": []}`). Fragments pasted from the
observed container output. No hangs — both reds crash before `file_writer.begin_animation`.
Full fixture census: **28** (17 green + 11 red).

## Part VI — deepening round 1 beats (proven 2026-07-08)

All six beats came out of the manim round-1 deepening probe (provenance, task texts, gated
answers, and triage reasoning: `docs/deepening/manim-round-1/` — cross-linked, not duplicated
here). Three are execution beats seeded by observed probe failures; three are render-blind
(the failure renders clean, so no RED is possible — recorded oracle limitation) and ship as
GREEN + doc-grounding. One novel artifact kind: `camera-distance-kwarg/silent` is a
green-gated **finding** — the fixture passes `distance=99` (a manimgl-ism) and renders exit 0,
proving the swallow is silent.

| beat | red result: exit + fragment observed | green: exit | notes |
|---|---|---|---|
| circle-surround | exit 1; `TypeError: Circle.surround() got an unexpected keyword argument 'buffer'` | 0 | CE `surround` scales by multiplicative `buffer_factor`; additive `buff`/`buffer` is the manimgl shape. Probe: legacy-3 haiku, observed live. |
| cube-side-length | exit 1; `Mobject.__init__() got an unexpected keyword argument 'size'` | 0 | `Cube(size=…)` falls through VGroup→Mobject init. CE parameter is `side_length`. Probe: camera3d-3 haiku, observed live. |
| threed-camera-frame | exit 1; `AttributeError: 'ThreeDCamera' object has no attribute 'frame'` | 0 | manimgl `camera.frame` bleed on `ThreeDScene`; unreached in the probe answer (Cube crash fired first), RED generated its own observed error. Distinct from `moving-camera` (2D, where `self.camera.frame` IS correct) and `fixed-frame`. Red class renamed `ThreeDFrameZoom` to avoid sharing a name with the moving-camera red. |
| camera-phi-theta | (render-blind — any phi/theta renders clean) | 0 | Haiku swapped the convention twice (math θ=polar); CE: `phi` = polar, `theta` = azimuth. GREEN animates phi 0→90°. |
| camera-distance-kwarg | (render-blind — `distance=` is silently absorbed by `**kwargs`) | 0 (green) + 0 (silent) | `silent/` proves the no-error absorption at render time; doc claim pins the real signature (`focal_distance`, `zoom`). |
| lag-ratio-total | (render-blind — any lag_ratio renders clean) | 0 | Sonnet computed lag_ratio as a fraction of total duration and passed it to a bare `self.play`, which staggers nothing between animations (observed render: 1.0 s instead of 3 s); doc claim pins the AnimationGroup per-animation overlap semantics. |

All 10 Part VI fixtures proved through the pinned image before commit (same flags and
containment as the runner); fragments pasted from observed container output only. All three
reds crash before `file_writer.begin_animation` — no hang-class exposure. Corpus extended
with four passages from the same pinned commit (`1157b746`, tag v0.20.1) to ground the six
doc claims. Full fixture census: **38** (24 green-gated + 14 red).
