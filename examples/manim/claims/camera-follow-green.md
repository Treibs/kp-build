---
id: camera-follow-green
statement: 'A camera that continuously tracks a moving mobject is an updater on `self.camera.frame`
  in a `MovingCameraScene`: `self.camera.frame.add_updater(lambda f: f.move_to(runner.get_center()))`
  before the movement `play`, cleared after. The one-shot `frame.animate.move_to(...)`
  form (see moving-camera) pans once and then sits still — a follow shot that never
  follows renders exit 0, so this corner is invisible to a render gate.'
paper: ''
supporting_passage: manim 0.20.1 renders a MovingCameraScene whose camera.frame carries
  a follow updater across a full traverse, exit 0.
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
  artifact: manim-fixtures/camera-follow/green
grounding: {}
judgment: {}
---

A camera that continuously tracks a moving mobject is an updater on `self.camera.frame` in a `MovingCameraScene`: `self.camera.frame.add_updater(lambda f: f.move_to(runner.get_center()))` before the movement `play`, cleared after. The one-shot `frame.animate.move_to(...)` form (see moving-camera) pans once and then sits still — a follow shot that never follows renders exit 0, so this corner is invisible to a render gate.

> manim 0.20.1 renders a MovingCameraScene whose camera.frame carries a follow updater across a full traverse, exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
