---
id: determinism-3
statement: 'Never use repeat: -1 on any GSAP timeline or tween; compute a finite repeat
  count from the composition duration (e.g. repeat: Math.floor(duration / cycleDuration)
  - 1) because infinite-repeat timelines break the frame-seeking capture engine.'
paper: ''
supporting_passage: '**No `repeat: -1`:** Infinite-repeat timelines break the capture
  engine. Calculate the exact repeat count from composition duration: `repeat: Math.ceil(duration
  / cycleDuration) - 1`.'
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
  evidence: lint:gsap_infinite_repeat cleared
  checked: '2026-06-17'
execution:
  tool: lint
  gate_code: gsap_infinite_repeat
  artifact: hf-kpmodel-fixtures/determinism-3
grounding: {}
judgment: {}
---

Never use repeat: -1 on any GSAP timeline or tween; compute a finite repeat count from the composition duration (e.g. repeat: Math.floor(duration / cycleDuration) - 1) because infinite-repeat timelines break the frame-seeking capture engine.

> **No `repeat: -1`:** Infinite-repeat timelines break the capture engine. Calculate the exact repeat count from composition duration: `repeat: Math.ceil(duration / cycleDuration) - 1`.

— *execution verified* via lint: lint:gsap_infinite_repeat cleared
