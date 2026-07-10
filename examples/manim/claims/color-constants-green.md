---
id: color-constants-green
statement: Manim CE's brown constants are `LIGHT_BROWN`, `DARK_BROWN`, `GRAY_BROWN`/`GREY_BROWN`
  — a scene using them renders on manim 0.20.1.
paper: ''
supporting_passage: manim 0.20.1 renders a scene coloring mobjects with DARK_BROWN,
  LIGHT_BROWN and GREY_BROWN, exit 0.
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
  checked: '2026-07-09'
execution:
  tool: manim-render
  gate_code: render_error
  artifact: manim-fixtures/color-constants/green
grounding: {}
judgment: {}
---

Manim CE's brown constants are `LIGHT_BROWN`, `DARK_BROWN`, `GRAY_BROWN`/`GREY_BROWN` — a scene using them renders on manim 0.20.1.

> manim 0.20.1 renders a scene coloring mobjects with DARK_BROWN, LIGHT_BROWN and GREY_BROWN, exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
