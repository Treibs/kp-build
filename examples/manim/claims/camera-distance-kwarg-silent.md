---
id: camera-distance-kwarg-silent
statement: 'Passing manimgl-style `distance=` to `set_camera_orientation` raises NO
  error — manim 0.20.1 renders it with exit 0: the kwarg is absorbed by the signature''s
  `**kwargs` and the camera call carries on without it. The failure is silent; the
  CE parameters are `focal_distance` and `zoom`.'
paper: ''
supporting_passage: manim 0.20.1 renders set_camera_orientation(..., distance=99)
  with exit 0 — the unknown kwarg is silently accepted.
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
  evidence: manim-render:render_error cleared
  checked: '2026-07-08'
execution:
  tool: manim-render
  gate_code: render_error
  artifact: manim-fixtures/camera-distance-kwarg/silent
grounding: {}
judgment: {}
---

Passing manimgl-style `distance=` to `set_camera_orientation` raises NO error — manim 0.20.1 renders it with exit 0: the kwarg is absorbed by the signature's `**kwargs` and the camera call carries on without it. The failure is silent; the CE parameters are `focal_distance` and `zoom`.

> manim 0.20.1 renders set_camera_orientation(..., distance=99) with exit 0 — the unknown kwarg is silently accepted.

— *execution verified* via manim-render: manim-render:render_error cleared
