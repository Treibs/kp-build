---
id: create-rename-green
statement: 'Draw a VMobject''s outline with `Create`: `self.play(Create(circle))`
  — the CE name for the drawing-on animation.'
paper: ''
supporting_passage: manim 0.20.1 renders self.play(Create(circle)) with exit 0.
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
  checked: '2026-07-08'
execution:
  tool: manim-render
  gate_code: render_error
  artifact: manim-fixtures/create-rename/green
grounding: {}
judgment: {}
---

Draw a VMobject's outline with `Create`: `self.play(Create(circle))` — the CE name for the drawing-on animation.

> manim 0.20.1 renders self.play(Create(circle)) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
