---
id: method-syntax-red
statement: 'The legacy declaration `friend method_syntax_red::admin;` does not compile
  in edition 2024: sui 1.74.1 fails with error[E13002] feature is deprecated in specified
  edition — "''friend''s are deprecated. Remove and replace ''public(friend)'' with
  ''public(package)''".'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a `friend` declaration with exit 1, error[E13002]:
  feature is deprecated in specified edition, telling the author to replace ''public(friend)''
  with ''public(package)''.'
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
  checked: '2026-07-06'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/method-syntax-red
grounding: {}
judgment: {}
---

The legacy declaration `friend method_syntax_red::admin;` does not compile in edition 2024: sui 1.74.1 fails with error[E13002] feature is deprecated in specified edition — "'friend's are deprecated. Remove and replace 'public(friend)' with 'public(package)'".

> sui 1.74.1 rejects a `friend` declaration with exit 1, error[E13002]: feature is deprecated in specified edition, telling the author to replace 'public(friend)' with 'public(package)'.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
