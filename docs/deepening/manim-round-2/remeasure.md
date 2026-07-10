# Tier-1 remeasure — manim deepening round 2

*Tier-1 numbers are tainted — these tasks selected the beats. Trend signal only; headline
numbers come from pre-registered held-out falsification (tier 2).*

Exactly the failed probe runs — the three render-gate FAILs plus the four render-blind wrong
answers found by hand inspection (the API-shape oracle cannot see those, so their remeasure
verdict is also by hand inspection). Fresh answers, same models and prompts, deepened
**77-claim** payload — 42,734 bytes, sha256 `78240c5496275857…`, assembled from the teach
commit `d698597` by the standard rule stated precisely (review round 1 asked): `CONTEXT.md`
at `d698597` + `\n## Pack claims (all)\n` + the `statement` strings from
`examples/manim.research.json` at `d698597`, sorted by Python `sorted()` (code-point order),
one `- ` bullet each, joined with `\n`, trailing newline. Re-verified reproducible from
`git show d698597:` inputs after the review. Gated by the pinned image. Artifacts in `remeasure-runs/`.

**Payload-desync disclosure (the round's own defect, caught here):** this remeasure was
collected against the payload whose `camera-follow` GREEN **omitted
`self.add(self.camera.frame)`** — without that step, `camera.frame` updaters never run during
`play`, the camera sits still, and the scene renders exit 0. The pack taught that broken
pattern, and **all three camera-follow remeasure answers reproduced it faithfully** (updater
attached, frame never added, camera motionless on video). That smoking gun sent the check
back to the beat's own fixture, which failed the same hand-check. The fixture and claim were
corrected pre-merge and the fix verified on the output video (`b16f33e`; beat-log Part VII
correction). The camera-follow rows below are therefore **evidence of the defect, not of the
fix** — the corrected claim's effect is unmeasured until the next round or tier-2 run.

## Flip table

| task / model | probe verdict | remeasure verdict | taught fix applied? |
|---|---|---|---|
| imgpx-2 / haiku | FAIL `TypeError` (VGroup of ImageMobjects) | **PASS (gate)** | **corner avoided**: the answer groups nothing — each sprite and label is `self.add`-ed directly, so the taught `Group`-vs-`VGroup` rule was never exercised (no credit, same standard as sui round-4's suimport-2). The taught `image-resampling` shape IS applied (`set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])`) |
| frames-3 / haiku | FAIL `TypeError` (hallucinated `filter_kwargs`) | **PASS (gate)** | **yes** — no invented kwarg; the taught resampling call appears verbatim, twice |
| camfollow-3 / haiku | FAIL `NameError: BROWN` | **PASS (gate)** | **yes** for the taught class — `GREY_BROWN` used at every color site. Hand-check caveat: its camera work uses the pre-fix follow pattern (updater, no `self.add`) and does not track — the disclosed defect, not the taught `color-constants` class |
| path-1 / haiku | render-blind: upside-down on the bottom edge | **fixed (hand inspection)** | **yes** — `sprite.flip(UP)` at the direction change, upright on all four edges on video: the taught `sprite-facing` GREEN shape |
| path-3 / haiku | render-blind: orbit inverted 180° | **still wrong (hand inspection)** | no — the answer builds an incremental-rotation updater but the tangent phase is still off (upright at 3 o'clock; feet not consistently toward center). The taught GREEN pins the flip-mirror shape; the orbit-phase shape recurs → **round-3 candidate** (`orbit-phase`, ×2 answers cumulative) |
| camfollow-1 / sonnet | render-blind: camera never follows | **still wrong (hand inspection)** | the answer applies the taught (pre-fix) pattern exactly — `frame.add_updater(...)` before the play, no `self.add(self.camera.frame)` — and the camera stays at the start while the walker leaves the frame. Evidence of the shipped defect (disclosure above) |
| camfollow-3 / sonnet | render-blind: camera loses the climber | **still wrong (hand inspection)** | same — taught pre-fix pattern reproduced, camera motionless |

## Reading (trend only — see taint label above)

- **Render-gate flips: 3/3.** Every gate-level taught class is gone from the remeasure logs
  (no `VGroup` grouping, no invented kwarg, no bare `BROWN`), and the two verifiable taught
  fixes (resampling call, brown constants) appear verbatim.
- **Render-blind flips: 1/4** — path-1's mirror fixed with the taught `flip(UP)` shape; path-3
  and both camera-follow runs still wrong. The camera-follow rows carry the round's central
  lesson: **the pack taught a broken pattern and the models applied it faithfully** — rule
  application worked; the rule was wrong. Only the hand-check protocol (probe → remeasure →
  the beat's own fixture) caught the chain.
- **Engine note (review round 1, minor m3):** the CONTEXT.md briefing cap displaced several
  taught method claims (round-1 and round-2 GREENs, including the corrected camera-follow
  idiom) into the "+N more — see claims/" tail; probe/remeasure payloads are unaffected (they
  append all claim statements), but a consumer loading CONTEXT.md alone does not see them.
  Recorded as engine debt (same family as the report-renderer 0-source debt), not a round
  defect.
- **Round-3 candidate ledger:** `orbit-phase` (tangent-following rotation with correct phase;
  ×2 — probe + remeasure); the corrected `camera-follow` claim's effect (unmeasured);
  `image-group` corner unexercised in its remeasure (avoided) — the class stays watched, not
  re-taught.
- **Post-measure claim freeze note:** the freeze was broken once, deliberately and disclosed —
  the `camera-follow` GREEN was corrected after this remeasure ran because shipping a
  known-wrong teaching claim outweighs payload/pack sync (the desync is pinned by the payload
  sha above). No other claim changed after collection.
