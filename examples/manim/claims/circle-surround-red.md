---
id: circle-surround-red
statement: '`Circle.surround()` has no additive `buff`/`buffer` parameter (the manimgl
  shape): manim 0.20.1 fails with TypeError: Circle.surround() got an unexpected keyword
  argument ''buffer''. The CE parameter is the multiplicative `buffer_factor`.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: TypeError: Circle.surround()
  got an unexpected keyword argument ''buffer''.'
claim_type: finding
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
  evidence: manim-render:red_violation cleared
  checked: '2026-07-09'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/circle-surround/red
grounding: {}
judgment: {}
---

`Circle.surround()` has no additive `buff`/`buffer` parameter (the manimgl shape): manim 0.20.1 fails with TypeError: Circle.surround() got an unexpected keyword argument 'buffer'. The CE parameter is the multiplicative `buffer_factor`.

> manim 0.20.1 fails the render with: TypeError: Circle.surround() got an unexpected keyword argument 'buffer'.

— *execution verified* via manim-render: manim-render:red_violation cleared
