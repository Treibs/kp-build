---
id: lag-ratio-total-green
statement: Stagger several animations inside one play with `AnimationGroup(*anims,
  lag_ratio=0.5)` — each next animation starts when the current one is 50% played.
paper: ''
supporting_passage: manim 0.20.1 renders AnimationGroup(*fades, lag_ratio=0.5) with
  exit 0.
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
  artifact: manim-fixtures/lag-ratio-total/green
grounding: {}
judgment: {}
---

Stagger several animations inside one play with `AnimationGroup(*anims, lag_ratio=0.5)` — each next animation starts when the current one is 50% played.

> manim 0.20.1 renders AnimationGroup(*fades, lag_ratio=0.5) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
