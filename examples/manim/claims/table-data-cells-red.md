---
id: table-data-cells-red
statement: '`Table` with `Text(...)` mobjects in the DATA cells — over-applying the
  labels-are-mobjects rule — does not render: manim 0.20.1 fails with TypeError: sequence
  item 0: expected str instance, Text found (the default `element_to_mobject`, Paragraph,
  joins cell content as strings). Labels are mobjects; data cells are strings.'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: sequence item 0: expected
  str instance, Text found.'
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
  artifact: manim-fixtures/table-data-cells/red
grounding: {}
judgment: {}
---

`Table` with `Text(...)` mobjects in the DATA cells — over-applying the labels-are-mobjects rule — does not render: manim 0.20.1 fails with TypeError: sequence item 0: expected str instance, Text found (the default `element_to_mobject`, Paragraph, joins cell content as strings). Labels are mobjects; data cells are strings.

> manim 0.20.1 fails the render with: sequence item 0: expected str instance, Text found.

— *execution verified* via manim-render: manim-render:red_violation cleared
