---
id: structure-3
statement: Clip timing must be expressed with data-duration, not the deprecated data-end
  attribute.
paper: ''
supporting_passage: Use `data-layer` (use `data-track-index`) or `data-end` (use `data-duration`)
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
  evidence: lint:deprecated_data_end cleared
  checked: '2026-06-17'
execution:
  tool: lint
  gate_code: deprecated_data_end
  artifact: hf-kpmodel-fixtures/structure-3
grounding: {}
---

Clip timing must be expressed with data-duration, not the deprecated data-end attribute.

> Use `data-layer` (use `data-track-index`) or `data-end` (use `data-duration`)

— *execution verified* via lint: lint:deprecated_data_end cleared
