---
id: config-surface-green
statement: 'Read global frame geometry from `config` inside a scene: `Rectangle(width=config.frame_width
  - 1, ...)` renders clean — `config.frame_width` is readable at construct time.'
paper: ''
supporting_passage: manim 0.20.1 renders Rectangle(width=config.frame_width - 1, height=0.5)
  with exit 0.
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
  artifact: manim-fixtures/config-surface/green
grounding: {}
judgment: {}
---

Read global frame geometry from `config` inside a scene: `Rectangle(width=config.frame_width - 1, ...)` renders clean — `config.frame_width` is readable at construct time.

> manim 0.20.1 renders Rectangle(width=config.frame_width - 1, height=0.5) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
