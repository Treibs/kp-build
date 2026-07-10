---
id: image-resampling-green
statement: 'Pixel art shown through `ImageMobject` keeps hard pixel edges when scaled
  by setting nearest-neighbor resampling: `sprite.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])`.
  Without it the default (bicubic) blurs every upscaled sprite — the scene still renders,
  so the omission is invisible to a render gate.'
paper: ''
supporting_passage: manim 0.20.1 renders an ImageMobject built from a raw uint8 array
  with set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"]) and height=4, exit
  0.
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: manim-render
  canonical_title: ''
  match_score: 0.0
  evidence: manim-render:render_error cleared
  checked: '2026-07-10'
execution:
  tool: manim-render
  gate_code: render_error
  artifact: manim-fixtures/image-resampling/green
grounding: {}
judgment: {}
---

Pixel art shown through `ImageMobject` keeps hard pixel edges when scaled by setting nearest-neighbor resampling: `sprite.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])`. Without it the default (bicubic) blurs every upscaled sprite — the scene still renders, so the omission is invisible to a render gate.

> manim 0.20.1 renders an ImageMobject built from a raw uint8 array with set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"]) and height=4, exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
