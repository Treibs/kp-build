---
id: camera-distance-kwarg-green
statement: 'Set 3D camera distance and magnification with the CE names: `set_camera_orientation(phi=…,
  theta=…, focal_distance=8, zoom=1.2)`.'
paper: ''
supporting_passage: manim 0.20.1 renders set_camera_orientation(..., focal_distance=8,
  zoom=1.2) with exit 0.
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
  artifact: manim-fixtures/camera-distance-kwarg/green
grounding: {}
judgment: {}
---

Set 3D camera distance and magnification with the CE names: `set_camera_orientation(phi=…, theta=…, focal_distance=8, zoom=1.2)`.

> manim 0.20.1 renders set_camera_orientation(..., focal_distance=8, zoom=1.2) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
