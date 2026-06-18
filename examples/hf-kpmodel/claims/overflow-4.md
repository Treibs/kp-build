---
id: overflow-4
statement: Content must stay inside the composition canvas; the .scene-content container
  must fill the scene (width/height 100% + padding + box-sizing) so content does not
  bleed off-frame, rather than being pinned past the canvas edge.
paper: ''
supporting_passage: The layout step is about catching **unintentional** overlap —
  two headlines landing on top of each other, a stat covering a label, content bleeding
  off-frame.
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
  evidence: inspect:canvas_overflow cleared
  checked: '2026-06-17'
execution:
  tool: inspect
  gate_code: canvas_overflow
  artifact: hf-kpmodel-fixtures/overflow-4
grounding: {}
judgment: {}
---

Content must stay inside the composition canvas; the .scene-content container must fill the scene (width/height 100% + padding + box-sizing) so content does not bleed off-frame, rather than being pinned past the canvas edge.

> The layout step is about catching **unintentional** overlap — two headlines landing on top of each other, a stat covering a label, content bleeding off-frame.

— *execution verified* via inspect: inspect:canvas_overflow cleared
