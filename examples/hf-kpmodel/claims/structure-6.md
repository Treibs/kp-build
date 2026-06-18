---
id: structure-6
statement: The ROOT composition <div> must carry data-duration (the total video length,
  in seconds). Without it the runtime has no totalDuration, so `inspect` fails to
  build the timeline and the render is unreliable — and crucially `lint` does NOT
  flag its absence, so this only surfaces as an inspect failure.
paper: ''
supporting_passage: <div data-composition-id="main" data-start="0" data-duration="5"
  data-width="1920" data-height="1080">
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
  evidence: inspect:inspect_error cleared
  checked: '2026-06-17'
execution:
  tool: inspect
  gate_code: inspect_error
  artifact: hf-kpmodel-fixtures/structure-6
grounding: {}
---

The ROOT composition <div> must carry data-duration (the total video length, in seconds). Without it the runtime has no totalDuration, so `inspect` fails to build the timeline and the render is unreliable — and crucially `lint` does NOT flag its absence, so this only surfaces as an inspect failure.

> <div data-composition-id="main" data-start="0" data-duration="5" data-width="1920" data-height="1080">

— *execution verified* via inspect: inspect:inspect_error cleared
