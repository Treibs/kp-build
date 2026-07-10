---
id: camera-follow-green
statement: 'A camera that continuously tracks a moving mobject is an updater on `self.camera.frame`
  in a `MovingCameraScene` — AND the frame must be added to the scene first, or its
  updaters never run during `play`: `self.add(self.camera.frame)`, then `self.camera.frame.add_updater(lambda
  f: f.move_to(runner.get_center()))` before the movement `play`, cleared after. Without
  the `self.add` step the scene renders exit 0 and the camera silently never moves
  (this pack''s own first GREEN omitted it and was caught by hand-checking the video
  — a render gate cannot see it). The one-shot `frame.animate.move_to(...)` form (see
  moving-camera) pans once and then sits still.'
paper: ''
supporting_passage: manim 0.20.1 renders a MovingCameraScene whose camera.frame is
  added to the scene and carries a follow updater across a full traverse, exit 0;
  the follow was verified on the output video (marks scroll, runner centered).
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

A camera that continuously tracks a moving mobject is an updater on `self.camera.frame` in a `MovingCameraScene` — AND the frame must be added to the scene first, or its updaters never run during `play`: `self.add(self.camera.frame)`, then `self.camera.frame.add_updater(lambda f: f.move_to(runner.get_center()))` before the movement `play`, cleared after. Without the `self.add` step the scene renders exit 0 and the camera silently never moves (this pack's own first GREEN omitted it and was caught by hand-checking the video — a render gate cannot see it). The one-shot `frame.animate.move_to(...)` form (see moving-camera) pans once and then sits still.

> manim 0.20.1 renders a MovingCameraScene whose camera.frame is added to the scene and carries a follow updater across a full traverse, exit 0; the follow was verified on the output video (marks scroll, runner centered).

— *execution verified* via manim-render: manim-render:render_error cleared
