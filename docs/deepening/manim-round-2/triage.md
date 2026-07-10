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
| all 9 haiku PNG-sprite passes (12 PNG tasks − 3 gate-fails; the 3 pixgrid passes use no PNGs) | every sprite renders **blurry**: across all 12 haiku PNG-task answers there are **zero** uses of any nearest-neighbor technique — no `set_resampling_algorithm`, no constructor kwarg, no PIL preprocessing — and the one attempt is the hallucinated `filter_kwargs` gate-fail above. Every task text demanded hard pixel edges. sonnet, same 12 tasks (regenerated from the answers, corrected in review round 1 — the first version of this row said "9 via the API", which does not regenerate): **CE resampling surface 6/12** — the taught dictionary form `RESAMPLING_ALGORITHMS["nearest"]` 2× (imgpx-2, imgpx-3), other argument forms 3× (`0`, `PILImage.NEAREST`, `PILResampling.NEAREST`), constructor kwarg `resampling_algorithm=0` 1× — plus **PIL preprocessing 5/12** (NEAREST pre-upscale 4×: frames-1, frames-3, path-3, camfollow-3; squares rebuild 1×: imgpx-1) and nothing 1/12 (camfollow-1). 11/12 crisp by *some* technique | **beat-worthy** (`image-resampling`, GREEN side) | the asymmetry stands and is one-sided — haiku 0 techniques vs sonnet 11/12 — but sonnet's spread (6 API / 5 preprocessing, only 2 in the canonical form) is itself evidence the *canonical* form is under-taught. GREEN teaches it; the RED above pins the hallucinated form; the omission form is render-blind and recorded here |
| camfollow-1 / sonnet, camfollow-3 / sonnet | the camera never tracks: camfollow-1 sits at signpost 1 while the walker leaves the frame; camfollow-3 loses the climber right after the start | **beat-worthy** (`camera-follow`, GREEN + doc only) | the pack's `moving-camera` beat pins the one-shot `frame.animate` move; the *continuous follow-updater on `camera.frame`* is untaught and both hard follow tasks failed on it — for the model that passes every render gate. Render-blind corner → ships GREEN + doc per the recorded oracle limitation (no RED is possible: a non-following camera renders exit 0) |
| path-1 / haiku, path-3 / haiku | track lap runs **upside-down** across the bottom edge (tangent rotation where the task asked for horizontal mirroring); planet orbit **inverted 180°** (head toward center, feet out) | **beat-worthy** (`sprite-facing`, GREEN + doc only) | orientation semantics: `rotate` follows a tangent, `flip` mirrors facing — and tangent-following needs the right phase. Two failures in one territory, render-blind by nature → GREEN + doc |
| path-1 / sonnet | upright on every edge; whether the leftward legs mirror horizontally cannot be resolved at 480p | recorded, not failed | hand-check honesty: only what is observable is recorded |
| pixgrid-3 / sonnet | the five broken-off cells are the original grid cells (verified in code — real removal, not copies); the resulting gaps read as dark features against the black background | recorded (aesthetic note) | mechanically correct; the visual ambiguity is composition, not API |
| sonnet PIL-preprocessing answers ×5 (imgpx-1 squares rebuild; frames-1, frames-3, path-3, camfollow-3 `NEAREST` pre-upscale) | legal avoidance of the CE resampling API — crisp output without touching `set_resampling_algorithm` (list harmonized with the corrected count above; the first version named only imgpx-1 and frames-3) | recorded (dodge, not failure) | same standard as sui round-4's `Battery has copy` dodge: compile/render-clean avoidance of the invited corner is recorded, never punished |

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
| `image-resampling` | GREEN + RED + doc | RED = observed `filter_kwargs` TypeError; GREEN = `set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])`; haiku 0/12 on any technique vs sonnet 6/12 on the CE API (2 in the taught form) + 5/12 PIL preprocessing |
| `image-group` | GREEN + RED + doc | RED = observed VGroup TypeError; GREEN = `Group` of image mobjects |
| `color-constants` | GREEN + RED + doc | RED = observed `BROWN` NameError; GREEN = the real brown constants |
| `camera-follow` | GREEN + doc (render-blind) | both sonnet follow tasks failed on video; GREEN = follow-updater on `camera.frame` in a `MovingCameraScene` |
| `sprite-facing` | GREEN + doc (render-blind) | haiku path-1/path-3 orientation defects; GREEN = flip-for-facing + phase-correct tangent rotation |

Corpus: `MovingCameraScene` grounding already present; `image-resampling`, `image-group`,
`color-constants`, and `sprite-facing` doc claims need excerpts from the SAME pinned
ManimCommunity/manim commit `1157b746` (v0.20.1) — the sui round-4 precedent (extension from
pinned commits, no pin change).


## Corrections (review round 1, 2026-07-09)

- The image-resampling hand-check row and beat-list line above were corrected after the
  branch's adversarial review round 1: the original row claimed "sonnet 9/12 via
  `set_resampling_algorithm(RESAMPLING_ALGORITHMS[\"nearest\"])` plus two disclosed dodges",
  which does not regenerate from the committed answers (the true spread — regenerated by
  grep, then independently by the reviewer — is 6/12 CE-API in any argument form, only 2 in
  the taught form, plus 5/12 PIL preprocessing of which the first version disclosed only
  frames-3 and imgpx-1). The haiku denominators were also fixed (12 PNG tasks, 9 PNG passes;
  the hallucinated-kwarg answer is inside the 12, not a 13th). Same defect family as sui
  round 4's suimport-2 attribution: prose written from memory instead of regenerated from
  artifacts.
- The image-group failure row's adjacency disclosure (the loaded `table-labels` beat pins the
  same error string for a different rule) was added in commit `b16f33e` — after the teach and
  remeasure commits. Recorded here because triage rows are otherwise expected to be frozen at
  their commit; the addition strengthened the disclosure and changed no verdict.
