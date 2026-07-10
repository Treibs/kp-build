---
id: axes-length-red
statement: '`Axes(width=6, height=4)` — the sizing kwargs both probe models pass from
  memory — does not render: the kwargs fall through to Mobject and manim 0.20.1 fails
  with TypeError: Mobject.__init__() got an unexpected keyword argument ''width''
  (which of width/height is named varies with kwargs-dict order; the pinned fragment
  is kept generic). Use `x_length`/`y_length`.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: TypeError: Mobject.__init__()
  got an unexpected keyword argument ''width'' — the fixture pins the dict-order-stable
  prefix Mobject.__init__() got an unexpected keyword argument.'
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
  artifact: manim-fixtures/axes-length/red
grounding: {}
judgment: {}
---

`Axes(width=6, height=4)` — the sizing kwargs both probe models pass from memory — does not render: the kwargs fall through to Mobject and manim 0.20.1 fails with TypeError: Mobject.__init__() got an unexpected keyword argument 'width' (which of width/height is named varies with kwargs-dict order; the pinned fragment is kept generic). Use `x_length`/`y_length`.

> manim 0.20.1 fails the render with: TypeError: Mobject.__init__() got an unexpected keyword argument 'width' — the fixture pins the dict-order-stable prefix Mobject.__init__() got an unexpected keyword argument.

— *execution verified* via manim-render: manim-render:red_violation cleared
