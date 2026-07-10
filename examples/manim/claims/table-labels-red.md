---
id: table-labels-red
statement: '`Table(row_labels=["R1", "R2"], col_labels=["C1", "C2"])` with plain strings
  — the naive form a probe model wrote — does not render: manim 0.20.1 fails with
  TypeError: Only values of type VMobject can be added as submobjects of VGroup. Wrap
  labels in `Text(...)`.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: Only values of type VMobject
  can be added as submobjects of VGroup.'
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
  artifact: manim-fixtures/table-labels/red
grounding: {}
judgment: {}
---

`Table(row_labels=["R1", "R2"], col_labels=["C1", "C2"])` with plain strings — the naive form a probe model wrote — does not render: manim 0.20.1 fails with TypeError: Only values of type VMobject can be added as submobjects of VGroup. Wrap labels in `Text(...)`.

> manim 0.20.1 fails the render with: Only values of type VMobject can be added as submobjects of VGroup.

— *execution verified* via manim-render: manim-render:red_violation cleared
