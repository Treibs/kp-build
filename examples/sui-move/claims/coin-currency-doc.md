---
id: coin-currency-doc
statement: '`coin::create_currency<T: drop>` creates a new currency type `T` and returns
  the `TreasuryCap` (plus `CoinMetadata`) to the caller; it can only be called with
  a one-time witness, ensuring there is only one `TreasuryCap` per `T`.'
paper: ''
supporting_passage: 'Create a new currency type <code>T</code> as and return the <code><a
  href="../sui/coin.md#sui_coin_TreasuryCap">TreasuryCap</a></code> for

  <code>T</code> to the caller. Can only be called with a <code>one-time-witness</code>

  type, ensuring that there''s only one <code><a href="../sui/coin.md#sui_coin_TreasuryCap">TreasuryCap</a></code>
  per <code>T</code>.'
claim_type: method
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
  evidence: 'Create a new currency type <code>T</code> as and return the <code><a
    href="../sui/coin.md#sui_coin_TreasuryCap">TreasuryCap</a></code> for

    <code>T</code> to the'
  checked: '2026-07-09'
execution: {}
grounding:
  source: sui-framework-docs
  supporting_passage: 'Create a new currency type <code>T</code> as and return the
    <code><a href="../sui/coin.md#sui_coin_TreasuryCap">TreasuryCap</a></code> for

    <code>T</code> to the caller. Can only be called with a <code>one-time-witness</code>

    type, ensuring that there''s only one <code><a href="../sui/coin.md#sui_coin_TreasuryCap">TreasuryCap</a></code>
    per <code>T</code>.'
judgment: {}
---

`coin::create_currency<T: drop>` creates a new currency type `T` and returns the `TreasuryCap` (plus `CoinMetadata`) to the caller; it can only be called with a one-time witness, ensuring there is only one `TreasuryCap` per `T`.

> Create a new currency type <code>T</code> as and return the <code><a href="../sui/coin.md#sui_coin_TreasuryCap">TreasuryCap</a></code> for
<code>T</code> to the caller. Can only be called with a <code>one-time-witness</code>
type, ensuring that there's only one <code><a href="../sui/coin.md#sui_coin_TreasuryCap">TreasuryCap</a></code> per <code>T</code>.

— *grounding verified* via doc-corpus: Create a new currency type <code>T</code> as and return the <code><a href="../sui/coin.md#sui_coin_TreasuryCap">TreasuryCap</a></code> for
<code>T</code> to the
