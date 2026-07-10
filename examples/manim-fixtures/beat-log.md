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
| lag-ratio-total | (render-blind — any lag_ratio renders clean) | 0 | Sonnet computed lag_ratio as a fraction of total duration and passed it to a bare `self.play`, which staggers nothing between animations (observed render: 1.0 s instead of 3 s; a second, self-corrected block in the same answer reached AnimationGroup but kept the fraction-of-total `lag_ratio=0.5/3` — wrong under either block); doc claim pins the AnimationGroup per-animation overlap semantics. |

All 10 Part VI fixtures proved through the pinned image before commit (same flags and
containment as the runner); fragments pasted from observed container output only. All three
reds crash before `file_writer.begin_animation` — no hang-class exposure. Corpus extended
with four passages from the same pinned commit (`1157b746`, tag v0.20.1) to ground the six
doc claims. Full fixture census: **38** (24 green-gated + 14 red).

## Part VII — deepening round 2 beats (proven 2026-07-09)

All five beats came out of the manim round-2 pixel-sprite probe (operator-chosen domain:
"a pixel person running through or around a scene, Pokémon style"; provenance, task texts,
gated answers, hand-check verdicts: `docs/deepening/manim-round-2/` — cross-linked, not
duplicated). Three are execution beats seeded by observed probe failures; two are render-blind
(recorded oracle limitation) and ship GREEN + doc-grounding. The image fixtures build their
pixel art from raw `uint8` numpy arrays, so no binary assets enter the fixture tree.

| beat | red result: exit + fragment observed | green: exit | notes |
|---|---|---|---|
| image-resampling | exit 1; `TypeError: Mobject.__init__() got an unexpected keyword argument 'filter_kwargs'` | 0 | The round's headline gap: every task demanded crisp pixels; haiku used no nearest-neighbor technique in any of its 12 PNG-task answers (all 9 of its PNG passes ship blurry — render-blind in the omission form) and hallucinated a scipy-style kwarg once (frames-3, the RED, observed live); sonnet used the CE resampling surface 6/12 (the taught dictionary form only 2×; other argument forms and a constructor kwarg for the rest) plus PIL nearest preprocessing 5/12 — 11/12 crisp by some technique (numbers corrected in review round 1; regenerated from the committed answers). |
| image-group | exit 1; `Only values of type VMobject can be added as submobjects of VGroup` | 0 | Probe: imgpx-2 haiku, observed live. **Second rule pinned under this message** — `table-labels` pins the strings-vs-mobjects rule with the same fragment; here the rule is images-need-`Group`. Disclosed in both the red claim and the round-2 triage (loaded-rule-adjacent, exp-5 standard). |
| color-constants | exit 1; `NameError: name 'BROWN' is not defined` | 0 | Probe: camfollow-3 haiku (the same answer used `GREY_BROWN` correctly 12 lines earlier). Single answer, taught anyway: pinnable constant list + documented drift in the surface (0.20 changelog: `YELLOW_C` fix, `PURE_*` additions). |
| camera-follow | (render-blind — a camera that never follows renders exit 0) | 0 | Both sonnet camera-follow probe tasks failed on video (camera static, subject leaves frame) while passing the gate 15/15 overall. GREEN is the follow-updater on `camera.frame`; the claim explicitly contrasts the one-shot `frame.animate` form the `moving-camera` beat pins. |
| sprite-facing | (render-blind — any orientation renders clean) | 0 | Haiku's track lap ran upside-down (tangent rotation where mirroring was asked) and its planet orbit was inverted 180°; both observed on video, both render exit 0. GREEN mirrors with `flip(UP)` between opposite `MoveAlongPath` legs. |

All 8 Part VII fixtures proved through the pinned image before commit (same flags and
containment as the runner); fragments pasted from observed container output only. All three
reds crash before `file_writer.begin_animation` — no hang-class exposure. The camera-follow
green attaches its updater to `camera.frame` while animating a *different* mobject (the safe
side of the `animate-live-updater` hang class — the updater target is structure-stable).
Corpus extended with four passages from the same pinned commit (`1157b746`, tag v0.20.1) to
ground the five doc claims. Full fixture census: **46** (29 green-gated + 17 red).

### Part VII correction — camera-follow GREEN (2026-07-09, same day, pre-merge)

The camera-follow GREEN as first committed attached the updater to `camera.frame` but did
**not** add the frame to the scene — and `camera.frame` updaters never run during `play`
unless `self.add(self.camera.frame)` happens first. The scene rendered exit 0 with the camera
sitting still: the beat's own fixture was a live instance of the render-blind failure mode it
was written to teach. Caught by hand-checking the remeasure videos (all three remeasure
camera-follow answers reproduced the broken pattern the pack had just taught them — the
smoking gun that sent the check back to the fixture itself). Fixed by adding
`self.add(self.camera.frame)`; the fix was verified on the output video (marks scroll, runner
stays centered) before re-commit, and the green claim now names the `self.add` step as part
of the idiom. The remeasure was collected against the pre-fix payload — disclosed in the
round-2 remeasure ledger, which treats its camera-follow rows as evidence of the defect, not
of the fix.

## Part VIII — deepening round 3 beats (proven 2026-07-10)

All three beats came out of the manim round-3 gap-seeded probe (five sprite-animation
territories: orbit, camera-follow, frame-bounds, sheet-slicing, parallax; per-territory
scaffold mounts — the sheet-slicing tasks were given ONLY `sprite_sheet.png`; provenance,
task texts, gated answers, hand-check verdicts: `docs/deepening/manim-round-3/` —
cross-linked, not duplicated). One is an execution beat seeded by an observed NameError;
two are render-blind classes caught only by the standing hand-check-every-PASS protocol
and ship GREEN + doc-grounding. Fixture sprites are raw `uint8` numpy arrays as in Part VII.

| beat | red result: exit + fragment observed | green: exit | notes |
|---|---|---|---|
| rate-func-names | exit 1; `NameError: name 'ease_out' is not defined` | 0 | Probe: fb-3 haiku, observed live. The invented-constant family's third member (`filter_kwargs`, `BROWN`, now `ease_out`): manim 0.20.1's easing family is suffixed (`rate_functions.ease_out_sine`, `ease_out_quad`, …); there is no bare `ease_out`. |
| image-scale-height | (render-blind — a speck-sized sprite renders exit 0) | 0 | The round's headline class, fired ×3 in haiku's gate-passing renders (cf-3, px-2, px-3 — grep-verified `.scale(1.5)` in exactly the three failing answers): `.scale(n)` on a pixel-derived `ImageMobject` multiplies its already-tiny intrinsic size. GREEN sets absolute size via the `height` property (`sprite.height = 2`); passing probe answers used the same idiom. |
| frame-fit | (render-blind — off-frame content renders exit 0) | 0 | Probe: sl-3 haiku — a Ken-Burns zoom scaled against invented dimensions and pushed the focused frame mostly off-screen. GREEN sizes against the actual frame: `scale_to_fit_height(config.frame_height - 1)`. |

Also observed, not taught: `NameError: name 'DARK_GREEN' is not defined` (px-1 haiku) —
loaded-rule-adjacent under the Part VII `color-constants` beat (same class, different
constant; a rule restated is not a new rule — exp-5 standard). Round-2 corrections measured
as landed this round: the corrected camera-follow idiom (`self.add(self.camera.frame)`)
appears in 6/6 follow answers across both models (grep-verified in the round ledger) and the
viewed videos actually track; the round-2 orbit-phase class did not recur under a
purpose-built inverted-phase diagnostic (orb-2, both models correct). All 4 Part VIII
fixtures proved through the pinned image before commit; the RED fragment pasted from
observed container output only; all crash-free greens exit clean before any hang-class
exposure. Corpus extended with three passages from the same pinned commit (`1157b746`,
tag v0.20.1) to ground the three doc claims. Full fixture census: **50** (32 green-gated
+ 18 red).
