---
id: type-name-red
statement: 'Type reflection does not return `std::string::String`: pushing `type_name::with_defining_ids<T>()`
  into a `vector<String>` fails on sui 1.74.1 with error[E04007] incompatible types
  — Expected: ''std::string::String'', "Given: ''std::type_name::TypeName''".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects storing a type_name reflection result in a
  vector<std::string::String> with exit 1, error[E04007]: incompatible types — Given:
  ''std::type_name::TypeName''.'
claim_type: finding
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
  evidence: sui-move-build:red_violation cleared
  checked: '2026-07-07'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/type-name-red
grounding: {}
judgment: {}
---

Type reflection does not return `std::string::String`: pushing `type_name::with_defining_ids<T>()` into a `vector<String>` fails on sui 1.74.1 with error[E04007] incompatible types — Expected: 'std::string::String', "Given: 'std::type_name::TypeName'".

> sui 1.74.1 rejects storing a type_name reflection result in a vector<std::string::String> with exit 1, error[E04007]: incompatible types — Given: 'std::type_name::TypeName'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
