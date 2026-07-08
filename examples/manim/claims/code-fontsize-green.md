---
id: code-fontsize-green
statement: 'Size the text of a Code block through `paragraph_config`: `Code(code_string=...,
  language=..., paragraph_config={"font_size": 18})` — text styling kwargs go to the
  underlying Paragraph objects, not the Code constructor.'
paper: ''
supporting_passage: 'manim 0.20.1 renders a scene constructing Code(code_string=...,
  language="python", paragraph_config={"font_size": 18}) with exit 0.'
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
  artifact: manim-fixtures/code-fontsize/green
grounding: {}
judgment: {}
---

Size the text of a Code block through `paragraph_config`: `Code(code_string=..., language=..., paragraph_config={"font_size": 18})` — text styling kwargs go to the underlying Paragraph objects, not the Code constructor.

> manim 0.20.1 renders a scene constructing Code(code_string=..., language="python", paragraph_config={"font_size": 18}) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
