# manim round-2 triage

Probe: 15 tasks × 2 models, pack-loaded (64 claims), pinned image v0.20.1. **Render gate:
haiku 12/15, sonnet 15/15** ([probe/results.txt](probe/results.txt)). Per protocol, **every
PASS was hand-checked** against its task text on re-rendered video frames (the gate observes
exceptions, not visual correctness). The hand-check matters this round: it found **4
visually-wrong passes** (2 per model) and one systematic render-blind gap.

## Render-gate failures (3, all haiku)

| task / model | observed error | verdict | reason |
|---|---|---|---|
| imgpx-2 / haiku | `TypeError: Only values of type VMobject can be added as submobjects of VGroup` — `VGroup(*sprites)` over `ImageMobject`s | **beat-worthy** (`image-group`) | `VGroup` is for vector mobjects only; image mobjects group with `Group`. **Disclosed adjacency:** the loaded `table-labels` beat pins this same error *string* for a different rule (Table label lists take mobjects, not strings — fix: wrap in `Text`). Different pinned rule and fix → loaded-rule-**adjacent** under the exp-5 recurrence standard, not ignored; taught as its own class (the pack will pin two rules under this message, like sui's four E05001 shapes) |
| frames-3 / haiku | `TypeError: Mobject.__init__() got an unexpected keyword argument 'filter_kwargs'` — `ImageMobject("sprite_0.png", filter_kwargs={"order": 0})` | **beat-worthy** (`image-resampling`, RED side) | a hallucinated scipy-style kwarg standing in for the real crisp-pixel API (`set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])`). The territory's predicted stale-knowledge shape, observed verbatim |
| camfollow-3 / haiku | `NameError: name 'BROWN' is not defined` | **beat-worthy** (`color-constants`) | `BROWN` is not a CE color constant (`GREY_BROWN`/`DARK_BROWN`/`LIGHT_BROWN` are — the same answer used `GREY_BROWN` correctly 12 lines earlier). Single-answer class, but taught because the fix is a pinnable constant list, the class is a NameError the gate observes exactly, and the 0.20 changelog documents active drift in the color-constant surface (`YELLOW_C` fix, three `PURE_*` additions) |

## Hand-check findings (render-blind — the gate passed all of these)

| runs | observation | verdict | reason |
|---|---|---|---|
| ALL 12 haiku passes with PNG sprites | every sprite renders **blurry**; 0/12 haiku answers called any resampling API (the 13th hallucinated one, above). Every task text demanded hard pixel edges. sonnet: 14/15 crisp — 9 via `set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])`, plus two disclosed dodges (imgpx-1 rebuilt the PNG as squares via PIL; frames-3 pre-upscaled 16× with PIL `NEAREST`) | **beat-worthy** (`image-resampling`, GREEN side) | the strongest possible knowledge asymmetry: the weak model never reaches for the API the strong model uses routinely. GREEN teaches the API; the RED above pins the hallucinated form; the omission form itself is render-blind and recorded here |
| camfollow-1 / sonnet, camfollow-3 / sonnet | the camera never tracks: camfollow-1 sits at signpost 1 while the walker leaves the frame; camfollow-3 loses the climber right after the start | **beat-worthy** (`camera-follow`, GREEN + doc only) | the pack's `moving-camera` beat pins the one-shot `frame.animate` move; the *continuous follow-updater on `camera.frame`* is untaught and both hard follow tasks failed on it — for the model that passes every render gate. Render-blind corner → ships GREEN + doc per the recorded oracle limitation (no RED is possible: a non-following camera renders exit 0) |
| path-1 / haiku, path-3 / haiku | track lap runs **upside-down** across the bottom edge (tangent rotation where the task asked for horizontal mirroring); planet orbit **inverted 180°** (head toward center, feet out) | **beat-worthy** (`sprite-facing`, GREEN + doc only) | orientation semantics: `rotate` follows a tangent, `flip` mirrors facing — and tangent-following needs the right phase. Two failures in one territory, render-blind by nature → GREEN + doc |
| path-1 / sonnet | upright on every edge; whether the leftward legs mirror horizontally cannot be resolved at 480p | recorded, not failed | hand-check honesty: only what is observable is recorded |
| pixgrid-3 / sonnet | the five broken-off cells are the original grid cells (verified in code — real removal, not copies); the resulting gaps read as dark features against the black background | recorded (aesthetic note) | mechanically correct; the visual ambiguity is composition, not API |
| imgpx-1 / sonnet, frames-3 / sonnet | two legal dodges of the resampling corner (squares rebuild; PIL 16× `NEAREST` pre-upscale) | recorded (dodge, not failure) | same standard as sui round-4's `Battery has copy` dodge: compile/render-clean avoidance of the invited corner is recorded, never punished |

## Clean territories / clean corners

- **pixgrid (programmatic pixel art + layering): fully clean, both models, corners exercised** —
  staggered assembly over tiles, mid-pass occlusion behind the tree (both models), white-flash
  + real cell removal. The operator-added territory produced the round's best renders and no
  defects; z-order/`add_to_back` knowledge is present in both models. A finding, not a failure.
- **frames (cycling) mechanics**: all gate-passing walk cycles genuinely cycle (dt-updater
  timers in every answer; no hand-unrolled sequences); the corner that failed was the *asset*
  surface (resampling, grouping), not the updater timing the round-1 beats taught.
- **camfollow / haiku**: both passing haiku follows genuinely track (signposts scroll, zoom
  sequence real) — the weak model is *better* than the strong one at this corner in this draw
  (n=3 tasks; recorded as-is, no mechanism claimed).

## Beat list for this round (5)

| beat | shape | evidence |
|---|---|---|
| `image-resampling` | GREEN + RED + doc | RED = observed `filter_kwargs` TypeError; GREEN = `set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])`; haiku 0/12 vs sonnet 9/12 on the API |
| `image-group` | GREEN + RED + doc | RED = observed VGroup TypeError; GREEN = `Group` of image mobjects |
| `color-constants` | GREEN + RED + doc | RED = observed `BROWN` NameError; GREEN = the real brown constants |
| `camera-follow` | GREEN + doc (render-blind) | both sonnet follow tasks failed on video; GREEN = follow-updater on `camera.frame` in a `MovingCameraScene` |
| `sprite-facing` | GREEN + doc (render-blind) | haiku path-1/path-3 orientation defects; GREEN = flip-for-facing + phase-correct tangent rotation |

Corpus: `MovingCameraScene` grounding already present; `image-resampling`, `image-group`,
`color-constants`, and `sprite-facing` doc claims need excerpts from the SAME pinned
ManimCommunity/manim commit `1157b746` (v0.20.1) — the sui round-4 precedent (extension from
pinned commits, no pin change).
