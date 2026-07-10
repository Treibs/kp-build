---
id: threed-camera-frame-red
statement: '`self.camera.frame` does not exist on a `ThreeDScene` (Cairo): manim 0.20.1
  fails with AttributeError: ''ThreeDCamera'' object has no attribute ''frame''. That
  idiom is manimgl / the 2D MovingCameraScene; in a CE 3D scene camera motion goes
  through move_camera / set_camera_orientation.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: AttributeError: ''ThreeDCamera''
  object has no attribute ''frame''.'
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
  evidence: manim-render:red_violation cleared
  checked: '2026-07-10'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/threed-camera-frame/red
grounding: {}
judgment: {}
---

`self.camera.frame` does not exist on a `ThreeDScene` (Cairo): manim 0.20.1 fails with AttributeError: 'ThreeDCamera' object has no attribute 'frame'. That idiom is manimgl / the 2D MovingCameraScene; in a CE 3D scene camera motion goes through move_camera / set_camera_orientation.

> manim 0.20.1 fails the render with: AttributeError: 'ThreeDCamera' object has no attribute 'frame'.

— *execution verified* via manim-render: manim-render:red_violation cleared
