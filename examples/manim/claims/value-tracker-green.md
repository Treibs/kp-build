---
id: value-tracker-green
statement: '`ValueTracker` + `.animate.set_value` is the canonical animation driver:
  `self.play(tracker.animate.set_value(PI / 2))` with dependent mobjects rebuilt via
  always_redraw.'
paper: ''
supporting_passage: manim 0.20.1 renders a ValueTracker-driven always_redraw line
  animated via tracker.animate.set_value with exit 0.
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
  artifact: manim-fixtures/value-tracker/green
grounding: {}
judgment: {}
---

`ValueTracker` + `.animate.set_value` is the canonical animation driver: `self.play(tracker.animate.set_value(PI / 2))` with dependent mobjects rebuilt via always_redraw.

> manim 0.20.1 renders a ValueTracker-driven always_redraw line animated via tracker.animate.set_value with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
