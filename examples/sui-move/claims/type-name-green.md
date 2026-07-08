---
id: type-name-green
statement: 'Runtime type reflection returns `TypeName` values, not strings: store
  them as `vector<TypeName>` or convert with `.into_string()`, which yields `std::ascii::String`
  (not `std::string::String`). On sui 1.74.1 use `type_name::with_defining_ids<T>()`
  — `type_name::get` is deprecated ("Renamed to `with_defining_ids`").'
paper: ''
supporting_passage: sui 1.74.1 (edition 2024) builds a module storing `type_name::with_defining_ids<T>()`
  in a `vector<TypeName>` and converting via `.into_string()` to `std::ascii::String`
  with exit 0 and zero warnings.
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
  artifact: sui-move-fixtures/type-name-green
grounding: {}
judgment: {}
---

Runtime type reflection returns `TypeName` values, not strings: store them as `vector<TypeName>` or convert with `.into_string()`, which yields `std::ascii::String` (not `std::string::String`). On sui 1.74.1 use `type_name::with_defining_ids<T>()` — `type_name::get` is deprecated ("Renamed to `with_defining_ids`").

> sui 1.74.1 (edition 2024) builds a module storing `type_name::with_defining_ids<T>()` in a `vector<TypeName>` and converting via `.into_string()` to `std::ascii::String` with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
