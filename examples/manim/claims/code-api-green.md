---
id: code-api-green
statement: Construct a syntax-highlighted code block with `Code(code_string=..., language=...)`
  — the 0.19 rewrite renamed the source kwarg to `code_string` (a file path goes in
  `code_file`).
paper: ''
supporting_passage: manim 0.20.1 renders a scene constructing Code(code_string=...,
  language="python") with exit 0.
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
  artifact: manim-fixtures/code-api/green
grounding: {}
judgment: {}
---

Construct a syntax-highlighted code block with `Code(code_string=..., language=...)` — the 0.19 rewrite renamed the source kwarg to `code_string` (a file path goes in `code_file`).

> manim 0.20.1 renders a scene constructing Code(code_string=..., language="python") with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
