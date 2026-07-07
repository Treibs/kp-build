---
id: class-shadowing-green
statement: Name Scene subclasses after the content (`class GreetingScene(Scene)`),
  never after a manim class — `from manim import *` makes name collisions fatal at
  first use.
paper: ''
supporting_passage: manim 0.20.1 renders a content-named Scene subclass constructing
  Text(...) with exit 0.
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
  artifact: manim-fixtures/class-shadowing/green
grounding: {}
judgment: {}
---

Name Scene subclasses after the content (`class GreetingScene(Scene)`), never after a manim class — `from manim import *` makes name collisions fatal at first use.

> manim 0.20.1 renders a content-named Scene subclass constructing Text(...) with exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
