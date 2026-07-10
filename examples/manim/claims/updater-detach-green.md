---
id: updater-detach-green
statement: 'Drive the ValueTracker, not the carrier: `self.play(tracker.animate.set_value(100))`
  while the updater is live, then `counter.remove_updater(live)` BEFORE animating
  the counter itself.'
paper: ''
supporting_passage: manim 0.20.1 renders tracker-driven updates followed by remove_updater
  then counter.animate with exit 0.
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
  artifact: manim-fixtures/updater-detach/green
grounding: {}
judgment: {}
---

Drive the ValueTracker, not the carrier: `self.play(tracker.animate.set_value(100))` while the updater is live, then `counter.remove_updater(live)` BEFORE animating the counter itself.

> manim 0.20.1 renders tracker-driven updates followed by remove_updater then counter.animate with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
