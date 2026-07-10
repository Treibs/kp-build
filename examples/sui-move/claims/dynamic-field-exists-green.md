---
id: dynamic-field-exists-green
statement: Check for a dynamic field with `dynamic_field::exists(&obj.id, name)` —
  on sui 1.74.1 the old `exists_` still compiles but warns W04037 deprecated usage
  ("Renamed to `exists`"); `exists` builds clean.
paper: ''
supporting_passage: sui 1.74.1 (edition 2024) builds a module calling `dynamic_field::exists(&profile.id,
  b"bio")` with exit 0 and zero warnings.
claim_type: method
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: execution
  via: sui-move-build
  canonical_title: ''
  match_score: 0.0
  evidence: sui-move-build:build_error cleared
  checked: '2026-07-10'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/dynamic-field-exists-green
grounding: {}
judgment: {}
---

Check for a dynamic field with `dynamic_field::exists(&obj.id, name)` — on sui 1.74.1 the old `exists_` still compiles but warns W04037 deprecated usage ("Renamed to `exists`"); `exists` builds clean.

> sui 1.74.1 (edition 2024) builds a module calling `dynamic_field::exists(&profile.id, b"bio")` with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
