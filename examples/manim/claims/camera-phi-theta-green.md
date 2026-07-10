---
id: camera-phi-theta-green
statement: 'Animate a top-down→side-on 3D view by moving the polar angle: open with
  `set_camera_orientation(phi=0, …)` (straight down), then `self.move_camera(phi=90
  * DEGREES, run_time=…)`.'
paper: ''
supporting_passage: manim 0.20.1 renders set_camera_orientation(phi=0, ...) followed
  by move_camera(phi=90 * DEGREES) with exit 0.
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
  artifact: manim-fixtures/camera-phi-theta/green
grounding: {}
judgment: {}
---

Animate a top-down→side-on 3D view by moving the polar angle: open with `set_camera_orientation(phi=0, …)` (straight down), then `self.move_camera(phi=90 * DEGREES, run_time=…)`.

> manim 0.20.1 renders set_camera_orientation(phi=0, ...) followed by move_camera(phi=90 * DEGREES) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
