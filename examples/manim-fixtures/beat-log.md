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
