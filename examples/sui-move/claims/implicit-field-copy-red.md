---
id: implicit-field-copy-red
statement: Reading a field with the dot operator copies, so `let gem = p.gem;` on
  a non-`copy` field fails in sui 1.74.1 with error[E05001] — "Invalid implicit copy
  of field 'gem' without the 'copy' ability" (and the never-consumed struct then trips
  error[E06001] unused value without 'drop'). Field access never moves; destructure
  (or borrow) instead.
paper: ''
supporting_passage: 'sui 1.74.1 rejects `let gem = p.gem;` where `gem` lacks `copy`,
  with exit 1, error[E05001]: ability constraint not satisfied, Invalid implicit copy
  of field ''gem'' without the ''copy'' ability.'
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
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/implicit-field-copy-red
grounding: {}
judgment: {}
---

Reading a field with the dot operator copies, so `let gem = p.gem;` on a non-`copy` field fails in sui 1.74.1 with error[E05001] — "Invalid implicit copy of field 'gem' without the 'copy' ability" (and the never-consumed struct then trips error[E06001] unused value without 'drop'). Field access never moves; destructure (or borrow) instead.

> sui 1.74.1 rejects `let gem = p.gem;` where `gem` lacks `copy`, with exit 1, error[E05001]: ability constraint not satisfied, Invalid implicit copy of field 'gem' without the 'copy' ability.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
