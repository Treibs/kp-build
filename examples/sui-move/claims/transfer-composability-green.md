---
id: transfer-composability-green
statement: 'Public functions that create or extract an object compose better when
  they RETURN the object instead of `transfer::public_transfer(obj, ctx.sender())`:
  the 1.74 linter flags transfer-to-sender with warning[Lint W99001] "non-composable
  transfer to sender" and suggests returning the object so a caller (e.g. a PTB) can
  use it in subsequent commands. Returning the object compiles with zero warnings.'
paper: ''
supporting_passage: sui 1.74.1 (edition 2024) builds a module whose public function
  returns the created object (instead of transferring it to the sender) with exit
  0 and zero warnings.
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
  checked: '2026-07-07'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/transfer-composability-green
grounding: {}
judgment: {}
---

Public functions that create or extract an object compose better when they RETURN the object instead of `transfer::public_transfer(obj, ctx.sender())`: the 1.74 linter flags transfer-to-sender with warning[Lint W99001] "non-composable transfer to sender" and suggests returning the object so a caller (e.g. a PTB) can use it in subsequent commands. Returning the object compiles with zero warnings.

> sui 1.74.1 (edition 2024) builds a module whose public function returns the created object (instead of transferring it to the sender) with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
