---
id: image-scale-height-green
statement: An image is sized in scene units with the `height` property (`sprite.height
  = 2`) or `scale_to_fit_height` — `.scale(n)` multiplies the image's native pixel
  size, so `.scale(1.5)` on a 16-pixel sprite renders a near-invisible speck (exit
  0; only a video check sees it).
paper: ''
supporting_passage: manim 0.20.1 renders an ImageMobject sized via the height property
  to 2 units, exit 0.
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
  artifact: manim-fixtures/image-scale-height/green
grounding: {}
judgment: {}
---

An image is sized in scene units with the `height` property (`sprite.height = 2`) or `scale_to_fit_height` — `.scale(n)` multiplies the image's native pixel size, so `.scale(1.5)` on a 16-pixel sprite renders a near-invisible speck (exit 0; only a video check sees it).

> manim 0.20.1 renders an ImageMobject sized via the height property to 2 units, exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
