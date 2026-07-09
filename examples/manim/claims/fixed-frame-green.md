---
id: fixed-frame-green
statement: In a `ThreeDScene`, pin a screen-space overlay with `self.add_fixed_in_frame_mobjects(title)`
  (after `self.set_camera_orientation(...)`) so camera movement does not affect it.
paper: ''
supporting_passage: manim 0.20.1 renders a ThreeDScene using self.add_fixed_in_frame_mobjects(title)
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
  checked: '2026-07-09'
execution:
  tool: manim-render
  gate_code: render_error
  artifact: manim-fixtures/fixed-frame/green
grounding: {}
judgment: {}
---

In a `ThreeDScene`, pin a screen-space overlay with `self.add_fixed_in_frame_mobjects(title)` (after `self.set_camera_orientation(...)`) so camera movement does not affect it.

> manim 0.20.1 renders a ThreeDScene using self.add_fixed_in_frame_mobjects(title) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
