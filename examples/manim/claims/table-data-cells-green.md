---
id: table-data-cells-green
statement: 'Mobject cells belong in `MobjectTable`: `MobjectTable([[Text("1"), Text("2")],
  [Text("3"), Text("4")]], row_labels=[Text("R1"), Text("R2")], col_labels=[Text("C1"),
  Text("C2")])` renders — plain `Table` data cells stay strings.'
paper: ''
supporting_passage: manim 0.20.1 renders MobjectTable([[Text(...), ...], ...], row_labels=[Text(...),
  ...], col_labels=[Text(...), ...]) with exit 0.
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
  artifact: manim-fixtures/table-data-cells/green
grounding: {}
judgment: {}
---

Mobject cells belong in `MobjectTable`: `MobjectTable([[Text("1"), Text("2")], [Text("3"), Text("4")]], row_labels=[Text("R1"), Text("R2")], col_labels=[Text("C1"), Text("C2")])` renders — plain `Table` data cells stay strings.

> manim 0.20.1 renders MobjectTable([[Text(...), ...], ...], row_labels=[Text(...), ...], col_labels=[Text(...), ...]) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
