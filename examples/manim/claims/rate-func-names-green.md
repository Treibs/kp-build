---
id: rate-func-names-green
statement: Rate functions carry qualified names — `rate_functions.ease_out_sine`,
  `ease_in_sine`, `linear`, `smooth`; a play call takes them via `rate_func=`.
paper: ''
supporting_passage: manim 0.20.1 renders a slide eased with rate_functions.ease_out_sine,
  exit 0.
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
  artifact: manim-fixtures/rate-func-names/green
grounding: {}
judgment: {}
---

Rate functions carry qualified names — `rate_functions.ease_out_sine`, `ease_in_sine`, `linear`, `smooth`; a play call takes them via `rate_func=`.

> manim 0.20.1 renders a slide eased with rate_functions.ease_out_sine, exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
