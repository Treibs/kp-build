---
id: image-group-green
statement: 'Image mobjects are grouped with `Group`, which accepts any mobject: `Group(ImageMobject(arr),
  ImageMobject(arr), Text("x2")).arrange(RIGHT)` renders on manim 0.20.1.'
paper: ''
supporting_passage: manim 0.20.1 renders a Group holding two ImageMobjects and a Text,
  arranged in a row, exit 0.
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
  artifact: manim-fixtures/image-group/green
grounding: {}
judgment: {}
---

Image mobjects are grouped with `Group`, which accepts any mobject: `Group(ImageMobject(arr), ImageMobject(arr), Text("x2")).arrange(RIGHT)` renders on manim 0.20.1.

> manim 0.20.1 renders a Group holding two ImageMobjects and a Text, arranged in a row, exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
