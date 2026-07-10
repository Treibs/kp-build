---
id: axes-length-green
statement: 'Size coordinate systems with `x_length=`/`y_length=`: `Axes(x_range=[-3,
  3, 1], y_range=[-2, 2, 1], x_length=6, y_length=4, tips=False)`, then plot with
  `axes.plot(lambda x: ..., color=BLUE)`.'
paper: ''
supporting_passage: manim 0.20.1 renders Axes(x_range=..., y_range=..., x_length=6,
  y_length=4) plus axes.plot(...) with exit 0.
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
  artifact: manim-fixtures/axes-length/green
grounding: {}
judgment: {}
---

Size coordinate systems with `x_length=`/`y_length=`: `Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=6, y_length=4, tips=False)`, then plot with `axes.plot(lambda x: ..., color=BLUE)`.

> manim 0.20.1 renders Axes(x_range=..., y_range=..., x_length=6, y_length=4) plus axes.plot(...) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
