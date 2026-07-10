---
id: scene-anatomy-green
statement: 'Scene anatomy: one `Scene` subclass with a single `construct` method;
  `self.add` displays without animating, `self.play(mobject.animate...)` animates,
  `self.wait(...)` holds the frame.'
paper: ''
supporting_passage: manim 0.20.1 renders a single-construct Scene using add/play/wait
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
  checked: '2026-07-10'
execution:
  tool: manim-render
  gate_code: render_error
  artifact: manim-fixtures/scene-anatomy/green
grounding: {}
judgment: {}
---

Scene anatomy: one `Scene` subclass with a single `construct` method; `self.add` displays without animating, `self.play(mobject.animate...)` animates, `self.wait(...)` holds the frame.

> manim 0.20.1 renders a single-construct Scene using add/play/wait with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
