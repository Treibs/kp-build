---
id: rate-func-names-red
statement: 'There is no bare `ease_out`: `rate_func=ease_out` fails on manim 0.20.1
  with NameError: name ''ease_out'' is not defined. The easing family is suffixed
  (`ease_out_sine`, `ease_out_quad`, …).'
paper: ''
supporting_passage: 'manim 0.20.1 rejects rate_func=ease_out with exit 1, NameError:
  name ''ease_out'' is not defined.'
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
  artifact: manim-fixtures/rate-func-names/red
grounding: {}
judgment: {}
---

There is no bare `ease_out`: `rate_func=ease_out` fails on manim 0.20.1 with NameError: name 'ease_out' is not defined. The easing family is suffixed (`ease_out_sine`, `ease_out_quad`, …).

> manim 0.20.1 rejects rate_func=ease_out with exit 1, NameError: name 'ease_out' is not defined.

— *execution verified* via manim-render: manim-render:red_violation cleared
