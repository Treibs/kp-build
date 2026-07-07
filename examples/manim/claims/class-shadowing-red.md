---
id: class-shadowing-red
statement: '`class Text(Scene)` shadows `manim.Text` under `from manim import *`,
  so the inner `Text("hello", font_size=40)` recursively constructs the Scene subclass:
  manim 0.20.1 fails with TypeError: Scene.__init__() got an unexpected keyword argument
  ''font_size''. A strong probe model made exactly this mistake (naming its scene
  MarkupText).'
paper: ''
supporting_passage: 'manim 0.20.1 fails the render with: TypeError: Scene.__init__()
  got an unexpected keyword argument ''font_size''.'
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
  checked: '2026-07-06'
execution:
  tool: manim-render
  gate_code: red_violation
  artifact: manim-fixtures/class-shadowing/red
grounding: {}
judgment: {}
---

`class Text(Scene)` shadows `manim.Text` under `from manim import *`, so the inner `Text("hello", font_size=40)` recursively constructs the Scene subclass: manim 0.20.1 fails with TypeError: Scene.__init__() got an unexpected keyword argument 'font_size'. A strong probe model made exactly this mistake (naming its scene MarkupText).

> manim 0.20.1 fails the render with: TypeError: Scene.__init__() got an unexpected keyword argument 'font_size'.

— *execution verified* via manim-render: manim-render:red_violation cleared
