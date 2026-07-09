---
id: capability-green
statement: 'Access-control idiom: declare `public struct AdminCap has key, store {
  id: UID }`, transfer it to the publisher in `init`, and gate privileged functions
  by taking `_cap: &AdminCap` as the first parameter — possession of the capability
  IS the authorization.'
paper: ''
supporting_passage: 'sui 1.74.1 builds the capability pattern (AdminCap created in
  `init`, privileged function gated on `_cap: &AdminCap`) with exit 0.'
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
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/capability-green
grounding: {}
judgment: {}
---

Access-control idiom: declare `public struct AdminCap has key, store { id: UID }`, transfer it to the publisher in `init`, and gate privileged functions by taking `_cap: &AdminCap` as the first parameter — possession of the capability IS the authorization.

> sui 1.74.1 builds the capability pattern (AdminCap created in `init`, privileged function gated on `_cap: &AdminCap`) with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
