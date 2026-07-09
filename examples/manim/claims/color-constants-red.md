---
id: color-constants-red
statement: 'Bare `BROWN` is not a Manim CE color constant: `Rectangle(color=BROWN)`
  fails on manim 0.20.1 with NameError: name ''BROWN'' is not defined. Reach for `LIGHT_BROWN`/`DARK_BROWN`/`GREY_BROWN`
  instead; the color-constant surface also drifts across releases (0.20 fixed `YELLOW_C`
  and added three `PURE_*` constants).'
paper: ''
supporting_passage: 'manim 0.20.1 rejects Rectangle(color=BROWN) with exit 1, NameError:
  name ''BROWN'' is not defined.'
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
  artifact: manim-fixtures/color-constants/red
grounding: {}
judgment: {}
---

Bare `BROWN` is not a Manim CE color constant: `Rectangle(color=BROWN)` fails on manim 0.20.1 with NameError: name 'BROWN' is not defined. Reach for `LIGHT_BROWN`/`DARK_BROWN`/`GREY_BROWN` instead; the color-constant surface also drifts across releases (0.20 fixed `YELLOW_C` and added three `PURE_*` constants).

> manim 0.20.1 rejects Rectangle(color=BROWN) with exit 1, NameError: name 'BROWN' is not defined.

— *execution verified* via manim-render: manim-render:red_violation cleared
