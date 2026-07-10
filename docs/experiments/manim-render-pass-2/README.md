# Manim experiment 2 — held-out falsification of deepening round 2

**Verdict: ROUND 2 SHIPS (ship-rule branch 1).** kp77 beat kp64 on the primary (render-pass
**5/6 vs 4/6**; base anchor 2/6), and the pre-registered mechanical secondary is emphatic:
**nearest-neighbor-technique presence kp77 5/6 vs kp64 0/6 vs base 0/6** — the round's
headline beat (the crisp-pixel API) penetrates held-out answers almost universally under the
deepened pack and appears nowhere without it. Qualifier carried with the verdict: the primary
margin is +1 at n=6 (the salience/confirm pair's recorded lesson on small margins applies —
the branch fires under the frozen rule, and the secondary's 5-vs-0 spread is the result that
would survive a re-draw or not; no tooling decision hinges on this verdict).

Pre-registered at `0f531af` before any answer (arms, payload SHAs — kp64 byte-identical to
the round-2 probe payload; kp77 is the **corrected** pack including the camera-follow
`self.add` fix — six tasks with the audit, both metrics, 3-branch rule: [tasks.md](tasks.md)).
Model: claude-haiku-4-5, all arms. Gate: pinned image v0.20.1, container-lifecycle 300 s.
Per-run verdicts + secondary table in [answers/results.txt](answers/results.txt).

## Results

| task | base | kp64 | kp77 |
|---|---|---|---|
| health-bar | FAIL `TypeError: Only values of type VMobject can be added as submobjects of VGroup` — **the round-2 taught `image-group` class**, in an arm without the beat | FAIL `NameError: name 'NONE' is not defined` — `stroke_color=NONE` on the bar rectangle, a hallucinated color/`None` constant (correction, review round 1: the first version called this an invented *resampling* constant; the answer makes no resampling attempt at all) | **PASS** |
| conveyor | FAIL `NameError: name 'RESAMPLING_FILTER' is not defined` (invented resampling constant) | PASS | FAIL `ValueError` (numpy truth-value of an array — an updater comparing points; generic coding bug, no taught class) |
| speech-bubble | FAIL `AttributeError: VGroup object has no attribute 'fade_out'` | PASS | PASS |
| crossing | PASS | FAIL `TypeError: Mobject.scale() got an unexpected keyword argument 'axis'` (a mirror attempt without `flip` — **the `sprite-facing` corner**, in an arm without the beat) | PASS |
| stairs | FAIL `ValueError` (2-D point into a 3-D operation) | PASS | PASS |
| minimap | PASS | PASS | PASS |

- **Render-pass: base 2/6, kp64 4/6, kp77 5/6** → branch 1 fires.
- **Secondary (regex, frozen in the pre-registration): base 0/6, kp64 0/6, kp77 5/6** (all
  except minimap). Bias note from the pre-registration honored: the metric measures technique
  penetration, not visual crispness; kp77's five hits are all the real
  `set_resampling_algorithm`/`RESAMPLING_ALGORITHMS` API, no dodges this draw.

## Failure composition (strict recurrence standard)

- **Two round-2 taught classes fired only in arms lacking the beats**: `image-group`
  (health-bar/base, exact pinned message) and the `sprite-facing` corner (crossing/kp64's
  `scale(axis=)` mirror attempt — template-level: an invented-kwarg mirror where the beat
  teaches `flip(UP)`; kp77's crossing used the taught idiom and passed). One *invented resampling constant* appeared in a beat-less arm (`RESAMPLING_FILTER.BOX`,
  conveyor/base) — the image-resampling RED's hallucination family, ×1 this draw (correction,
  review round 1: the first version also counted kp64's `NONE`, which is a color-constant
  hallucination unrelated to resampling) — while kp77's five resampling calls are all the
  real API.
- **kp77's one failure is not a taught class** (numpy array-truth bug in a conveyor updater).
- **Zero round-2 taught-class recurrence in kp77.**

## Hand-check of every pass (observational, no ship-rule weight — round-2 protocol)

All 11 passing videos were frame-checked against their tasks:

- **Fully sound:** health-bar/kp77 (bar attached, left-anchored depletion, empty after 3
  hits, crisp), conveyor/kp64 (belt scrolls under stationary sprite; blurry), speech-bubble
  both arms (bubble pops at 2 s, rides, fades; kp77 crisp / kp64 blurry), crossing/base and
  crossing/kp77 (approach + pass at center; the full-occlusion instant falls between sampled
  frames — adjacency at center is consistent with a correct pass; z-order not falsifiable
  from samples; kp77 crisp / base blurry), minimap/base and minimap/kp64 (real sprite,
  faithful route + corner map; blurry).
- **Defects recorded:** stairs — BOTH pack arms climb correctly early and then the figure
  exits the frame top (the staircase composition exceeds frame bounds); render-clean,
  wrong-vs-task ("ending on the top step" happens off-screen). minimap/kp77 — substituted a
  blue `Rectangle` for the required `sprite.png` character (task deviation; the route/minimap
  mechanics are correct; also why its secondary regex is honestly 0 on that task — there is
  no image to resample). On this task the base and kp64 arms were *more* faithful.
- **Camera-follow (the corrected claim):** no task in this draw elicited a camera-follow
  shot, so the corrected `self.add(self.camera.frame)` idiom's held-out effect remains
  unmeasured — recorded for the next round's ledger, not claimed.

## Ledger updates

- New composition-tier candidates (render-blind): `frame-bounds` (stairs ×2 — content exceeds
  the visible frame; would need a mechanical bounds check or GREEN+doc) and
  `asset-substitution` (minimap/kp77 ×1 — required asset replaced by a primitive).
- The invented-resampling-constant family (×1 this draw, conveyor/base) corroborates the
  image-resampling beat's RED choice; kp64's `NONE` NameError is a separate color-constant
  hallucination (recorded, not counted in the family).
- Carried: the corrected camera-follow claim's effect; `orbit-phase` (×2, round-2 remeasure).
