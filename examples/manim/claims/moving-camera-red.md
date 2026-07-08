---
id: moving-camera-red
statement: '`self.camera_frame` (manimgl) does not exist on a plain `Scene`: manim
  0.20.1 fails with AttributeError: ''CameraFrameZoom'' object has no attribute ''camera_frame''.
  CE camera movement is `MovingCameraScene` + `self.camera.frame`.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: AttributeError: ''CameraFrameZoom''
  object has no attribute ''camera_frame''.'
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
  checked: '2026-07-08'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/moving-camera/red
grounding: {}
judgment: {}
---

`self.camera_frame` (manimgl) does not exist on a plain `Scene`: manim 0.20.1 fails with AttributeError: 'CameraFrameZoom' object has no attribute 'camera_frame'. CE camera movement is `MovingCameraScene` + `self.camera.frame`.

> manim 0.20.1 fails the render with: AttributeError: 'CameraFrameZoom' object has no attribute 'camera_frame'.

— *execution verified* via manim-render: manim-render:red_violation cleared
