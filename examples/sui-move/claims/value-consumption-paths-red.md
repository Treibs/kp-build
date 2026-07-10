---
id: value-consumption-paths-red
statement: 'Consuming a `Coin` parameter on only one branch of an `if` fails: sui
  1.74.1 rejects it with error[E06001] — "The parameter ''payment'' might still contain
  a value. The value does not have the ''drop'' ability and must be consumed before
  the function returns". The same class fires with no branches at all (a parameter
  that is simply never consumed).'
paper: ''
supporting_passage: 'sui 1.74.1 rejects a play function consuming payment only in
  the winning branch, exit 1, error[E06001]: unused value without ''drop'', must be
  consumed before the function returns.'
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
  checked: '2026-07-10'
execution:
  tool: sui-move-build
  gate_code: red_violation
  artifact: sui-move-fixtures/value-consumption-paths-red
grounding: {}
judgment: {}
---

Consuming a `Coin` parameter on only one branch of an `if` fails: sui 1.74.1 rejects it with error[E06001] — "The parameter 'payment' might still contain a value. The value does not have the 'drop' ability and must be consumed before the function returns". The same class fires with no branches at all (a parameter that is simply never consumed).

> sui 1.74.1 rejects a play function consuming payment only in the winning branch, exit 1, error[E06001]: unused value without 'drop', must be consumed before the function returns.

— *execution verified* via sui-move-build: sui-move-build:red_violation cleared
