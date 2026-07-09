# Manim CE scene authoring (v0.20.1, community edition)

*wikillm knowledge package (`@kp/manim-ce-scene-authoring-v0-20-1-community`) — a research-landscape foundation.*

*verified against `manimcommunity/manim@sha256:f18f53f2e4eaf2ea41713437d34363fb3f5cc6008b03fd798676ac0359396c3b` (tag `v0.20.1`; Python 3.14.3, Manim Community v0.20.1) · docs pinned at `ManimCommunity/manim` @ `1157b746c37130685e0a02d8aa0871d1f164d5f4` · snapshot 2026-07-06*

**Scope:** 

- 0/0 citations verified (arXiv/Crossref); source years n/a
- 77 claims · 0 open problems · 0 debates · 0 benchmarks
- dropped (unverified-anchored): {'claims': 0, 'open_problems': 0, 'debates': 0, 'benchmarks': 0, 'positions': 0, 'relations': 0}

**Load `CONTEXT.md` into your agent** to inherit this field without re-running the research. `index.json` is the machine-readable graph (nodes + edges); the subdirectories hold the notes.

## Distribution

This is a [0xLT/kpm](https://github.com/0xLT/kpm) knowledge package (`knowledge.json`). Publish it as a tagged GitHub repo, then any consumer installs it with kpm — no re-research:

```bash
kpm add github:<owner>/<repo>#v0.1.0
kpm compose            # composes into a vault; load CONTEXT.md into your agent
```

Confidence is corpus-relative (conditional on the cited sources). Built 2026-07-06; revision beats added 2026-07-07; deepening round 1 beats added 2026-07-08; deepening round 2 beats added 2026-07-09.

## The plain-terms story

Ask an AI for a Manim animation and it may write code for a library that no longer exists — a blend of 3blue1brown's `manimgl` and pre-0.19 Manim CE. The probe receipts (2026-07-06, 39 renders against the pinned image): both models wrote `Code(code=...)` (the API was rewritten in 0.19), a small model called `title.fix_in_frame()` (pure manimgl) and `self.camera_frame` (does not exist in CE), and a strong model named its Scene class `MarkupText`, fatally shadowing manim's own class under `from manim import *`. Every rule in this pack already ran through the real renderer, and every RED claim ships the broken form a model actually wrote alongside the pinned error it produces.

## Honest scope (what the probe actually measured)

The weakness is real but *localized* — this is not a blanket "models can't write Manim" claim (they mostly can). Probe render-pass: strong model 19/23 (~83%), small model 12/18 (~67%). Basic plotting, `TransformMatchingTex`, 3D scenes, graphs, boolean ops, dt-updaters, and custom `Animation` subclasses were green on both models, so the beat plan is weighted away from them and into the four measured weakness territories:

| territory | reproduced in the pinned container |
|---|---|
| recently-rewritten APIs | `Code(code=...)`, `Axes(width=, height=)`, string `Table` labels — all `TypeError` |
| manimgl bleed | `fix_in_frame()`, `self.camera_frame` — both `AttributeError` |
| animation × updater semantics | animating the carrier of a structure-changing updater — `ValueError: zip() argument 2 is longer than argument 1` (and on 0.20.1, a post-traceback hang) |
| namespace collisions | Scene subclass named after a manim class under `from manim import *` — `TypeError` at first use |

For strong models on common scene types, render-pass is near ceiling; the pack's measured value is (a) weaker/cheaper models and (b) the four territories above, for all models. The falsification protocol tests exactly that claim, not a broader one.

## Falsification (pre-registered, dual model)

Five held-out tasks in the weakness territories (none a pack fixture), pre-registered with an explicit ship rule at `a8bb596` **before any answer was collected** — protocol, answers, and raw render log in [`docs/experiments/manim-render-pass/`](../../docs/experiments/manim-render-pass/). Metric: render-pass in the pinned container, 300 s timeout = FAIL.

| | base | kp |
|---|---|---|
| claude-haiku-4-5 (primary) | 2/5 | **3/5** |
| claude-sonnet-4-6 (secondary) | 4/5 | 4/5 |

**Before/after, primary model:** without the pack, haiku wrote the pre-0.19 `Code(code=...)`, zoomed a plain `Scene`'s camera (`AttributeError`), and — on the live-gauges task — animated the carrier of a digit-count-changing updater, hitting the pack's documented post-traceback writer-thread hang *in the wild* (300 s timeout). With the pack loaded, the camera task and the live-gauges task both pass (`MovingCameraScene`, `always_redraw`). Verdict under the pre-registered rule: branch 1 (haiku kp > base) → ships.

Honest gaps recorded (not patched post-hoc): both kp arms fixed `Code(code=)` → `code_string=` and then failed on `Code(font_size=)` — a kwarg-surface gap; kp-haiku over-applied labels-are-mobjects to `Table` *data cells* (they must be strings). Sonnet ties at ceiling, as the honest-scope section predicted.

**Revision beats (2026-07-07).** Both gaps are now closed by fixture-proven beats, added *after* the falsification and clearly separated from it (the 3/5-vs-2/5 result above was measured on the 42-claim pack): `code-fontsize` (text styling goes in `paragraph_config`, not the `Code` constructor — RED: `TypeError: … unexpected keyword argument 'font_size'`) and `table-data-cells` (data cells stay strings for the default `element_to_mobject`; mobject cells belong in `MobjectTable` — RED: `TypeError: sequence item 0: expected str instance, Text found`). Provenance in [`examples/manim-fixtures/beat-log.md`](../manim-fixtures/beat-log.md), Part V.

## Deepening round 1 (2026-07-08)

A structured deepening pass over five unprobed territories (30 fresh renders, pack-loaded arm, dual model — full ledger in [`docs/deepening/manim-round-1/`](../../docs/deepening/manim-round-1/)). Two render-gate failures and three render-blind wrong answers (correct-looking code the API-shape oracle cannot see) yielded six new beats, every one fixture-proven through the pinned image before commit: `circle-surround` (`Circle.surround()` takes `buffer_factor`, not `buffer`), `cube-side-length` (`Cube(side_length=)`, not `size=`), `threed-camera-frame` (Cairo `ThreeDCamera` has no `.frame` — steer with `move_camera`/`set_camera_orientation`), `camera-phi-theta` (CE convention: `phi` = polar from +Z, `theta` = azimuth — swapped angles render fine and look wrong), `camera-distance-kwarg` (`distance=` is silently swallowed by `**kwargs`; use `focal_distance`/`zoom` — includes a green-gated *finding* fixture proving `distance=99` renders exit 0), and `lag-ratio-total` (`AnimationGroup` `lag_ratio` semantics: next animation starts when `lag_ratio × 100%` of the previous has played — total duration math, not a stagger delay). Three probed territories came back **clean** (transform-family, updater-utilities, deleted-name surface) — recorded as findings, not taught. **Honesty invariant:** the falsification numbers above were measured on the 42-claim pack; round-1 remeasure numbers are tainted by construction (the tasks selected the beats) and live only in the round ledger. Provenance in beat-log Part VI.

## Deepening round 2 (2026-07-09)

An operator-directed deepening pass — the round's domain was chosen by the pack's owner ("a pixel person running through or around a scene, Pokémon style") rather than by coverage instinct: five pixel-sprite territories, 30 fresh renders, pack-loaded arm, dual model, full ledger in [`docs/deepening/manim-round-2/`](../../docs/deepening/manim-round-2/). The render gate failed 3 haiku answers; the protocol's hand-check of every passing video found 4 more visually-wrong passes the gate cannot see — including both of claude-sonnet-4-6's camera-follow tasks (the camera never tracks; the model that passes every render gate fails the follow shot silently) and a one-sided systematic gap: every task demanded crisp pixel edges, claude-haiku-4-5 used no nearest-neighbor technique at all (all its image passes ship blurry), claude-sonnet-4-6 was crisp on 11 of 12 — but touched the CE API in only half of those and the taught dictionary form in just 2 (numbers regenerated from the committed answers after review round 1 corrected an initial overcount). Five beats, every one fixture-proven through the pinned image before commit: `image-resampling` (`set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])` for hard pixel edges — RED pins the hallucinated `filter_kwargs` kwarg), `image-group` (images group with `Group`; `VGroup` is vector-only — the pack's second rule pinned under that TypeError message, disclosed), `color-constants` (no bare `BROWN`; the real browns are `LIGHT_BROWN`/`DARK_BROWN`/`GREY_BROWN`), `camera-follow` (the continuous follow shot is an updater on `camera.frame` — and the frame must be added to the scene first or the updater never runs; the beat's own first GREEN omitted that step, rendered exit 0 with a motionless camera, and was caught by the round's hand-check protocol on its own remeasure — corrected pre-merge, beat-log Part VII correction — render-blind, GREEN + doc), and `sprite-facing` (direction changes are a `flip(UP)` mirror, not a rotation — render-blind, GREEN + doc). The operator-added programmatic-pixel-art territory came back **fully clean both models** (assembly, occlusion behind a tree, damage effects) — recorded as a finding. Pack grew 64 → 77 claims. **Honesty invariant:** the falsification numbers above were measured on the 42-claim pack; round-2 remeasure numbers are tainted by construction and live only in the round ledger. Provenance in beat-log Part VII.

## The RED/GREEN two-sided gate

46 execution claims (29 green-gated + 17 RED), each gated by a real render inside the digest-pinned container (`manim -ql --disable_caching`, container-lifecycle timeout — detached run, bounded wait, unconditional remove). A GREEN fixture must render clean; a RED fixture must FAIL with the pinned fragment in `expected_error.txt`. Refresh = bump the digest pin and re-run: a RED that starts rendering means the weakness healed and the claim retires; a GREEN that breaks means the idiom moved — both staleness signals mechanical, and the digest pin keeps the old verification environment reconstructible forever. (One green-gated claim is a *finding*, not a method: the `camera-distance-kwarg/silent` fixture renders exit 0 to prove the silent-swallow failure mode live.) 31 grounding claims anchor the rules to verbatim passages from the docs pinned at the same tag (`--ground-verify`, offline).
