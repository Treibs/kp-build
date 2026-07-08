---
id: moving-camera-green
statement: 'To move the camera in 2D, subclass `MovingCameraScene` and animate `self.camera.frame`:
  `self.play(self.camera.frame.animate.scale(0.5).move_to(dot))`.'
paper: ''
supporting_passage: manim 0.20.1 renders a MovingCameraScene animating self.camera.frame
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
  artifact: manim-fixtures/moving-camera/green
grounding: {}
judgment: {}
---

To move the camera in 2D, subclass `MovingCameraScene` and animate `self.camera.frame`: `self.play(self.camera.frame.animate.scale(0.5).move_to(dot))`.

> manim 0.20.1 renders a MovingCameraScene animating self.camera.frame with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
