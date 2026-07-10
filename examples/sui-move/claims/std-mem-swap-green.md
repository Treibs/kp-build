---
id: std-mem-swap-green
statement: 'In-place replacement of a non-copy struct field uses an `Option` slot
  with `std::option::swap`, which installs the new value and returns the old one:
  `option::swap(&mut d.slot, fresh)` builds green.'
paper: ''
supporting_passage: sui 1.74.1 builds a module replacing a non-copy field held in
  an `Option` slot via `option::swap(&mut d.slot, fresh)`, with exit 0 and zero warnings.
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
  artifact: sui-move-fixtures/std-mem-swap-green
grounding: {}
judgment: {}
---

In-place replacement of a non-copy struct field uses an `Option` slot with `std::option::swap`, which installs the new value and returns the old one: `option::swap(&mut d.slot, fresh)` builds green.

> sui 1.74.1 builds a module replacing a non-copy field held in an `Option` slot via `option::swap(&mut d.slot, fresh)`, with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
