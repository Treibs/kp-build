# Manim deepening round 3 — triage

Inputs: `probe/results.txt` (gate verdicts regenerated from `.result` files; hand-check
verdicts from viewed contact sheets of every gate-PASS render, per the standing
hand-check-every-PASS rule adopted after the round-2 camera-follow fixture bug).

Failure population: 2 gate FAILs (both haiku) + 4 hand-check visual FAILs (all haiku).
Sonnet: 15/15 gate-pass, 0 visual fails (1 partial, 1 pass-with-note — see below).

## Verdict table

| task | model | observed failure | verdict | reason |
|---|---|---|---|---|
| fb-3 | haiku | `NameError: name 'ease_out' is not defined` | **beat-worthy** | Invented rate-function name. Manim 0.20.1 exposes `rate_functions.ease_out_sine` / `ease_out_quad` etc.; there is no bare `ease_out`. Wrong parametric API-surface knowledge → **rate-func-names** beat (green + red + doc; RED `expected_error.txt` pasted from the observed oracle output). |
| px-1 | haiku | `NameError: name 'DARK_GREEN' is not defined` | not beat-worthy (loaded-rule-adjacent) | Invented color constant. The pack already teaches the class — the color-constants beat (bare `BROWN` NameError + "the color-constant surface drifts across releases"). Same mechanism, different constant; a rule restated is not a new rule. Recorded as an invented-constant recurrence in the ledger. |
| cf-3 | haiku | visual: sprite rendered as a speck (`.scale(1.5)` on a 16-px `ImageMobject`) | **beat-worthy** (×3, same class) | Sprite-scale collapse: the model treats `.scale(1.5)` as "make it sprite-sized," but `.scale()` multiplies the current (tiny, pixel-derived) size. Correct idiom sets absolute size: `sprite.height = 2`. New class this round, fired 3/13 haiku passes → **image-scale-height** beat (green + doc; no RED — the failure exits 0, and RED fragments come only from observed oracle error output). |
| px-2 | haiku | visual: pilot sprite speck (same relative-`.scale(n)` shape — `pilot.scale(1)`) | beat-worthy (same class as cf-3) | Counted under image-scale-height; no separate beat. |
| px-3 | haiku | visual: runner sprite speck (same relative-`.scale(n)` shape — `.scale(1.5)`) | beat-worthy (same class as cf-3) | Counted under image-scale-height; no separate beat. |
| sl-3 | haiku | visual: Ken-Burns zoom target far exceeds frame bounds; focused frame mostly off-screen | **beat-worthy** | The model scales content against invented dimensions instead of the config frame. Correct idiom fits to the actual frame: `scale_to_fit_height(config.frame_height - 1)` → **frame-fit** beat (green + doc; exits 0, so no RED). |

**Scope note (rate-func-names vs the exclusion list):** `territories.md` lists rate
functions among the round's deliberate territory exclusions — the round did not *probe*
them. The beat is legitimate anyway under the triage standard: the failure was observed
live in an in-scope frame-bounds probe answer (fb-3 chose `rate_func=ease_out` unprompted),
and measured failures outrank the exclusion of a territory nobody probed.

## Clean / notable territories

- **orb (orbit)** — both models pass all gates. orb-2's inverted-phase diagnostic
  (designed to re-elicit the round-2 orbit-phase class) was answered CORRECTLY by both
  models: **the round-2 orbit-phase class did not recur**. orb-3 flags are unresolvable
  at 480p on both models — recorded as PARTIAL, a rendering-scale measurement limit,
  not a model failure.
- **cf (camera follow)** — first measurement since the round-2 camera-follow fixture
  correction: 6/6 answers (both models × 3 tasks) carry `self.add(self.camera.frame)`
  (grep-verified, `results.txt`), and viewed videos confirm the camera actually tracks.
  The corrected idiom is adopted at source level. Model already strong on the mechanism;
  the only cf failure (cf-3 haiku) is the sprite-scale class, not a follow failure.
- **fb (frame bounds)** and **sl (sheet slicing)** — sonnet clean; haiku failures all
  triaged above. sl-1/sl-2 show correct per-territory scaffold use (tasks mounted ONLY
  `sprite_sheet.png`; answers sliced it rather than inventing assets).
- **px (parallax)** — sonnet's px-1 has a minor depth-order note (fence rail in front
  of the character's legs where the task asked for behind); single occurrence, judgment
  call on a soft constraint, not beat-worthy. Watch for recurrence.

## Beats shipped this round (3 beats, +7 claims → 84)

| beat | claims | seed failures |
|---|---|---|
| image-scale-height | green + doc | cf-3, px-2, px-3 (haiku), sprite-scale collapse ×3 |
| rate-func-names | green + red + doc | fb-3 (haiku), `ease_out` NameError |
| frame-fit | green + doc | sl-3 (haiku), zoom overshoot |

All fixtures proven through the pinned Docker oracle before commit; the two visual-class
beats ship green+doc only (no observed oracle error text exists for exit-0 failures —
honesty rule: RED fragments only from observed oracle output). Corpus extensions
(mobject `height` property, `rate_functions` excerpts, `config.frame_height`) are
byte-verbatim doc-claim anchors in `examples/corpus/manim-api-docs.txt`.

## Recurrence ledger updates

- invented-constant family: **continues** — `ease_out` (fb-3), `DARK_GREEN` (px-1);
  now taught for rate functions, already-taught for colors.
- orbit-phase (round 2): **did not recur** (orb-2 diagnostic passed both models).
- camera-follow static-frame (round-2 fixture bug): **did not recur**; corrected idiom
  adopted 6/6.
- NEW candidate class for round 4: **sprite-scale collapse** (taught this round;
  remeasure + next falsification will tell whether teaching lands).
