---
id: circle-surround-green
statement: Put a ring around a mobject with `Circle().surround(square, buffer_factor=1.4)`
  — `buffer_factor` scales the ring multiplicatively relative to the mobject.
paper: ''
supporting_passage: manim 0.20.1 renders Circle().surround(square, buffer_factor=1.4)
  with exit 0.
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
  artifact: manim-fixtures/circle-surround/green
grounding: {}
judgment: {}
---

Put a ring around a mobject with `Circle().surround(square, buffer_factor=1.4)` — `buffer_factor` scales the ring multiplicatively relative to the mobject.

> manim 0.20.1 renders Circle().surround(square, buffer_factor=1.4) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
