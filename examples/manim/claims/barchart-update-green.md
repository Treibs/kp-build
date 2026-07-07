---
id: barchart-update-green
statement: Update an existing BarChart in place with `chart.animate.change_bar_values([...])`
  — no need to rebuild the chart to change bar heights.
paper: ''
supporting_passage: manim 0.20.1 renders BarChart(values=[2, 4, 3], ...) animated
  via chart.animate.change_bar_values([5, 1, 4]) with exit 0.
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
  checked: '2026-07-06'
execution:
  tool: manim-render
  gate_code: render_error
  artifact: manim-fixtures/barchart-update/green
grounding: {}
judgment: {}
---

Update an existing BarChart in place with `chart.animate.change_bar_values([...])` — no need to rebuild the chart to change bar heights.

> manim 0.20.1 renders BarChart(values=[2, 4, 3], ...) animated via chart.animate.change_bar_values([5, 1, 4]) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
