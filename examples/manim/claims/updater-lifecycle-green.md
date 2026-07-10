---
id: updater-lifecycle-green
statement: 'dt-updater lifecycle: `square.add_updater(spin)` where `spin(mob, dt)`
  uses the frame delta, `self.wait(...)` to run it, then `square.remove_updater(spin)`
  before `self.play(square.animate...)`.'
paper: ''
supporting_passage: manim 0.20.1 renders add_updater(dt updater) -> wait -> remove_updater
  -> animate with exit 0.
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
  artifact: manim-fixtures/updater-lifecycle/green
grounding: {}
judgment: {}
---

dt-updater lifecycle: `square.add_updater(spin)` where `spin(mob, dt)` uses the frame delta, `self.wait(...)` to run it, then `square.remove_updater(spin)` before `self.play(square.animate...)`.

> manim 0.20.1 renders add_updater(dt updater) -> wait -> remove_updater -> animate with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
