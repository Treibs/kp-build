---
id: create-rename-red
statement: '`ShowCreation` — the manimgl name for the drawing-on animation — is not
  defined under `from manim import *`: manim 0.20.1 fails with NameError: name ''ShowCreation''
  is not defined. The CE animation is `Create`.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: name ''ShowCreation'' is
  not defined.'
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
  checked: '2026-07-07'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/create-rename/red
grounding: {}
judgment: {}
---

`ShowCreation` — the manimgl name for the drawing-on animation — is not defined under `from manim import *`: manim 0.20.1 fails with NameError: name 'ShowCreation' is not defined. The CE animation is `Create`.

> manim 0.20.1 fails the render with: name 'ShowCreation' is not defined.

— *execution verified* via manim-render: manim-render:red_violation cleared
