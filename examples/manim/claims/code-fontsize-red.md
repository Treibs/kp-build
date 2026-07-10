---
id: code-fontsize-red
statement: '`Code(font_size=...)` is not part of the current constructor — the 0.19
  rewrite narrowed the surface, and manim 0.20.1 fails with TypeError: Code.__init__()
  got an unexpected keyword argument ''font_size''. Text styling moved into `paragraph_config`.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: Code.__init__() got an unexpected
  keyword argument ''font_size''.'
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
  artifact: manim-fixtures/code-fontsize/red
grounding: {}
judgment: {}
---

`Code(font_size=...)` is not part of the current constructor — the 0.19 rewrite narrowed the surface, and manim 0.20.1 fails with TypeError: Code.__init__() got an unexpected keyword argument 'font_size'. Text styling moved into `paragraph_config`.

> manim 0.20.1 fails the render with: Code.__init__() got an unexpected keyword argument 'font_size'.

— *execution verified* via manim-render: manim-render:red_violation cleared
