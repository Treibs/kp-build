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
