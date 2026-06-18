---
id: structure-5
statement: Give each element that is on screen at the same time as another a DISTINCT
  data-track-index; two clips on the same track must never overlap in time. Same-track
  overlap violates the render contract (StaticGuard rejects it) and makes `inspect`
  fail to build the timeline, so content silently breaks.
paper: ''
supporting_passage: "<div class=\"clip\" id=\"bg\" data-start=\"0\" data-duration=\"\
  5\" data-track-index=\"0\"></div>\n      <div class=\"clip\" id=\"card\" data-start=\"\
  0.5\" data-duration=\"4\" data-track-index=\"1\">"
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: lint
  canonical_title: ''
  match_score: 0.0
  evidence: lint:overlapping_clips_same_track cleared
  checked: '2026-06-17'
execution:
  tool: lint
  gate_code: overlapping_clips_same_track
  artifact: hf-kpmodel-fixtures/structure-5
grounding: {}
---

Give each element that is on screen at the same time as another a DISTINCT data-track-index; two clips on the same track must never overlap in time. Same-track overlap violates the render contract (StaticGuard rejects it) and makes `inspect` fail to build the timeline, so content silently breaks.

> <div class="clip" id="bg" data-start="0" data-duration="5" data-track-index="0"></div>
      <div class="clip" id="card" data-start="0.5" data-duration="4" data-track-index="1">

— *execution verified* via lint: lint:overlapping_clips_same_track cleared
