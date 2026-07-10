---
id: frame-fit-green
statement: Compositions stay on screen by sizing against `config.frame_height`/`config.frame_width`
  (e.g. `scale_to_fit_height(config.frame_height - 1)`) — content past the frame edge
  renders exit 0 and is only caught on video.
paper: ''
supporting_passage: manim 0.20.1 renders a tower scaled to fit inside config.frame_height,
  exit 0.
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
  artifact: manim-fixtures/frame-fit/green
grounding: {}
judgment: {}
---

Compositions stay on screen by sizing against `config.frame_height`/`config.frame_width` (e.g. `scale_to_fit_height(config.frame_height - 1)`) — content past the frame edge renders exit 0 and is only caught on video.

> manim 0.20.1 renders a tower scaled to fit inside config.frame_height, exit 0.

— *execution verified* via manim-render: manim-render:render_error cleared
