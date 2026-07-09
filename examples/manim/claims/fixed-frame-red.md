---
id: fixed-frame-red
statement: '`title.fix_in_frame()` is manimgl, not Manim CE — manim 0.20.1 fails with
  AttributeError: Text object has no attribute ''fix_in_frame''. The CE mechanism
  is the scene method `self.add_fixed_in_frame_mobjects(...)`.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: AttributeError: Text object
  has no attribute ''fix_in_frame''.'
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
  checked: '2026-07-09'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/fixed-frame/red
grounding: {}
judgment: {}
---

`title.fix_in_frame()` is manimgl, not Manim CE — manim 0.20.1 fails with AttributeError: Text object has no attribute 'fix_in_frame'. The CE mechanism is the scene method `self.add_fixed_in_frame_mobjects(...)`.

> manim 0.20.1 fails the render with: AttributeError: Text object has no attribute 'fix_in_frame'.

— *execution verified* via manim-render: manim-render:red_violation cleared
