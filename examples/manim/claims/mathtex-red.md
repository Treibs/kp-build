---
id: mathtex-red
statement: '`MathTex(r"$e^{i\pi} + 1 = 0$")` — wrapping the string in `$` delimiters
  as if it were text mode — breaks LaTeX: manim 0.20.1 fails with LaTeX compilation
  error (followed by ValueError: latex error converting to dvi). MathTex is already
  math mode.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: LaTeX compilation error (then
  ValueError: latex error converting to dvi).'
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
  checked: '2026-07-08'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/mathtex/red
grounding: {}
judgment: {}
---

`MathTex(r"$e^{i\pi} + 1 = 0$")` — wrapping the string in `$` delimiters as if it were text mode — breaks LaTeX: manim 0.20.1 fails with LaTeX compilation error (followed by ValueError: latex error converting to dvi). MathTex is already math mode.

> manim 0.20.1 fails the render with: LaTeX compilation error (then ValueError: latex error converting to dvi).

— *execution verified* via manim-render: manim-render:red_violation cleared
