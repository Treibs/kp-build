---
id: cube-side-length-red
statement: '`Cube(size=…)` is not a CE parameter: the kwarg falls through to `Mobject.__init__`
  and manim 0.20.1 fails with TypeError: Mobject.__init__() got an unexpected keyword
  argument ''size''. The CE parameter is `side_length`.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: Mobject.__init__() got an
  unexpected keyword argument ''size''.'
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
  checked: '2026-07-10'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/cube-side-length/red
grounding: {}
judgment: {}
---

`Cube(size=…)` is not a CE parameter: the kwarg falls through to `Mobject.__init__` and manim 0.20.1 fails with TypeError: Mobject.__init__() got an unexpected keyword argument 'size'. The CE parameter is `side_length`.

> manim 0.20.1 fails the render with: Mobject.__init__() got an unexpected keyword argument 'size'.

— *execution verified* via manim-render: manim-render:red_violation cleared
