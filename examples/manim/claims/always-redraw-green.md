---
id: always-redraw-green
statement: '`always_redraw(lambda: ...)` rebuilds the mobject every frame — the safe
  pattern for live labels: `label = always_redraw(lambda: DecimalNumber(tracker.get_value(),
  num_decimal_places=1).next_to(dot, UP))`.'
paper: ''
supporting_passage: manim 0.20.1 renders always_redraw-built dot and label driven
  by a ValueTracker with exit 0.
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
  checked: '2026-07-06'
execution:
  tool: manim-render
  gate_code: render_error
  artifact: manim-fixtures/always-redraw/green
grounding: {}
judgment: {}
---

`always_redraw(lambda: ...)` rebuilds the mobject every frame — the safe pattern for live labels: `label = always_redraw(lambda: DecimalNumber(tracker.get_value(), num_decimal_places=1).next_to(dot, UP))`.

> manim 0.20.1 renders always_redraw-built dot and label driven by a ValueTracker with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
