---
id: balance-api-on-coin-doc
statement: '`sui::coin::take` takes a `Coin` worth of `value` FROM a `Balance` — its
  receiver parameter is `&mut sui::balance::Balance<T>`, never a `Coin`.'
paper: ''
supporting_passage: Take a <code><a href="../sui/coin.md#sui_coin_Coin">Coin</a></code>
  worth of <code><a href="../sui/coin.md#sui_coin_value">value</a></code> from <code>Balance</code>.
claim_type: definition
confidence: high
corroborated_by: []
survived_refuter: true
grounded: unchecked
verified:
  exists: true
  status: verified
  kind: grounding
  via: doc-corpus
  canonical_title: ''
  match_score: 0.0
  evidence: Take a <code><a href="../sui/coin.md#sui_coin_Coin">Coin</a></code> worth
    of <code><a href="../sui/coin.md#sui_coin_value">value</a></code> from <code>Balance</
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: Take a <code><a href="../sui/coin.md#sui_coin_Coin">Coin</a></code>
    worth of <code><a href="../sui/coin.md#sui_coin_value">value</a></code> from <code>Balance</code>.
judgment: {}
---

`sui::coin::take` takes a `Coin` worth of `value` FROM a `Balance` — its receiver parameter is `&mut sui::balance::Balance<T>`, never a `Coin`.

> Take a <code><a href="../sui/coin.md#sui_coin_Coin">Coin</a></code> worth of <code><a href="../sui/coin.md#sui_coin_value">value</a></code> from <code>Balance</code>.

— *grounding verified* via doc-corpus: Take a <code><a href="../sui/coin.md#sui_coin_Coin">Coin</a></code> worth of <code><a href="../sui/coin.md#sui_coin_value">value</a></code> from <code>Balance</
