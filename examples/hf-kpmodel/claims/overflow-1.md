---
id: overflow-1
statement: Text must not extend beyond its nearest visual container box; constrain
  dynamic copy with padding/max-width (or fitTextFontSize) so it wraps inside the
  box rather than spilling out a fixed-size container.
paper: ''
supporting_passage: Failures usually mean text is spilling out of a bubble/card, a
  fixed-size label is clipping dynamic copy, or text has moved off the canvas. Fix
  by increasing container size or padding, reducing font size or letter spacing, adding
  a real `max-width` so text wraps inside the container, or using `window.__hyperframes.fitTextFontSize(...)`
  for dynamic copy.
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: inspect
  canonical_title: ''
  match_score: 0.0
  evidence: inspect:text_box_overflow cleared
  checked: '2026-06-17'
execution:
  tool: inspect
  gate_code: text_box_overflow
  artifact: hf-kpmodel-fixtures/overflow-1
grounding: {}
---

Text must not extend beyond its nearest visual container box; constrain dynamic copy with padding/max-width (or fitTextFontSize) so it wraps inside the box rather than spilling out a fixed-size container.

> Failures usually mean text is spilling out of a bubble/card, a fixed-size label is clipping dynamic copy, or text has moved off the canvas. Fix by increasing container size or padding, reducing font size or letter spacing, adding a real `max-width` so text wraps inside the container, or using `window.__hyperframes.fitTextFontSize(...)` for dynamic copy.

— *execution verified* via inspect: inspect:text_box_overflow cleared
