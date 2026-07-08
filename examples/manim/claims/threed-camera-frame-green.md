---
id: threed-camera-frame-green
statement: Zoom or move a `ThreeDScene` camera with `self.move_camera(zoom=2, run_time=…)`
  — the same parameter family as `set_camera_orientation`.
paper: ''
supporting_passage: manim 0.20.1 renders self.move_camera(zoom=2) on a ThreeDScene
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
  checked: '2026-07-08'
execution:
  tool: manim-render
  gate_code: render_error
  artifact: manim-fixtures/threed-camera-frame/green
grounding: {}
judgment: {}
---

Zoom or move a `ThreeDScene` camera with `self.move_camera(zoom=2, run_time=…)` — the same parameter family as `set_camera_orientation`.

> manim 0.20.1 renders self.move_camera(zoom=2) on a ThreeDScene with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
