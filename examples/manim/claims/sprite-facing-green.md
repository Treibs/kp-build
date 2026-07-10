---
id: sprite-facing-green
statement: 'A sprite that changes travel direction faces the new direction with a
  horizontal mirror — `sprite.flip(UP)` — not a rotation: rotating 180 degrees puts
  a walking figure on its head, and a tangent-following orbit needs its rotation phase
  checked the same way (both failure shapes render exit 0 and were observed on video
  in this round''s probe).'
paper: ''
supporting_passage: manim 0.20.1 renders a sprite that traverses right, mirrors with
  flip(UP), and traverses back left along MoveAlongPath, exit 0.
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
  artifact: manim-fixtures/sprite-facing/green
grounding: {}
judgment: {}
---

A sprite that changes travel direction faces the new direction with a horizontal mirror — `sprite.flip(UP)` — not a rotation: rotating 180 degrees puts a walking figure on its head, and a tangent-following orbit needs its rotation phase checked the same way (both failure shapes render exit 0 and were observed on video in this round's probe).

> manim 0.20.1 renders a sprite that traverses right, mirrors with flip(UP), and traverses back left along MoveAlongPath, exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
