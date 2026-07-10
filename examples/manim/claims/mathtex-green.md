---
id: mathtex-green
statement: '`MathTex(r"e^{i\pi} + 1 = 0")` is already LaTeX math mode — no `$` delimiters;
  pair it with `Text(...)` (Pango, no LaTeX) for plain captions.'
paper: ''
supporting_passage: manim 0.20.1 renders MathTex(r"e^{i\pi} + 1 = 0") beside a Text
  caption with exit 0.
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
  artifact: manim-fixtures/mathtex/green
grounding: {}
judgment: {}
---

`MathTex(r"e^{i\pi} + 1 = 0")` is already LaTeX math mode — no `$` delimiters; pair it with `Text(...)` (Pango, no LaTeX) for plain captions.

> manim 0.20.1 renders MathTex(r"e^{i\pi} + 1 = 0") beside a Text caption with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
