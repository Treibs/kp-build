---
id: image-group-red
statement: '`VGroup` is vector-only — putting an `ImageMobject` in one fails on manim
  0.20.1 with TypeError: Only values of type VMobject can be added as submobjects
  of VGroup. (The pack pins a second rule under this same message: table-labels, where
  the fix is wrapping strings in `Text`. Here the fix is using `Group`.)'
paper: ''
supporting_passage: 'manim 0.20.1 rejects VGroup(ImageMobject(arr), ImageMobject(arr))
  with exit 1, TypeError: Only values of type VMobject can be added as submobjects
  of VGroup.'
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
  artifact: manim-fixtures/image-group/red
grounding: {}
judgment: {}
---

`VGroup` is vector-only — putting an `ImageMobject` in one fails on manim 0.20.1 with TypeError: Only values of type VMobject can be added as submobjects of VGroup. (The pack pins a second rule under this same message: table-labels, where the fix is wrapping strings in `Text`. Here the fix is using `Group`.)

> manim 0.20.1 rejects VGroup(ImageMobject(arr), ImageMobject(arr)) with exit 1, TypeError: Only values of type VMobject can be added as submobjects of VGroup.

— *execution verified* via manim-render: manim-render:red_violation cleared
