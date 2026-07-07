# Manim CE scene authoring (v0.20.1, community edition)

*wikillm knowledge package (`@kp/manim-ce-scene-authoring-v0-20-1-community`) — a research-landscape foundation.*

*verified against `manimcommunity/manim@sha256:f18f53f2e4eaf2ea41713437d34363fb3f5cc6008b03fd798676ac0359396c3b` (tag `v0.20.1`; Python 3.14.3, Manim Community v0.20.1) · docs pinned at `ManimCommunity/manim` @ `1157b746c37130685e0a02d8aa0871d1f164d5f4` · snapshot 2026-07-06*

**Scope:** 

- 0/0 citations verified (arXiv/Crossref); source years n/a
- 42 claims · 0 open problems · 0 debates · 0 benchmarks
- dropped (unverified-anchored): {'claims': 0, 'open_problems': 0, 'debates': 0, 'benchmarks': 0, 'positions': 0, 'relations': 0}

**Load `CONTEXT.md` into your agent** to inherit this field without re-running the research. `index.json` is the machine-readable graph (nodes + edges); the subdirectories hold the notes.

## Distribution

This is a [0xLT/kpm](https://github.com/0xLT/kpm) knowledge package (`knowledge.json`). Publish it as a tagged GitHub repo, then any consumer installs it with kpm — no re-research:

```bash
kpm add github:<owner>/<repo>#v0.1.0
kpm compose            # composes into a vault; load CONTEXT.md into your agent
```

Confidence is corpus-relative (conditional on the cited sources). Built 2026-07-06.

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

## The RED/GREEN two-sided gate

24 execution claims (15 GREEN + 9 RED), each gated by a real render inside the digest-pinned container (`manim -ql --disable_caching`, container-lifecycle timeout — detached run, bounded wait, unconditional remove). A GREEN fixture must render clean; a RED fixture must FAIL with the pinned fragment in `expected_error.txt`. Refresh = bump the digest pin and re-run: a RED that starts rendering means the weakness healed and the claim retires; a GREEN that breaks means the idiom moved — both staleness signals mechanical, and the digest pin keeps the old verification environment reconstructible forever. 18 grounding claims anchor the rules to verbatim passages from the docs pinned at the same tag (`--ground-verify`, offline).
