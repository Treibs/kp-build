---
id: coin-currency-green
statement: 'Create a currency in `init` with the module''s one-time witness: `let
  (treasury, metadata) = coin::create_currency(witness, 9, b"MYC", b"My Coin", b"Example
  coin", option::none(), ctx);` then freeze the metadata and transfer the treasury.
  This compiles on sui 1.74.1 but with a deprecation warning (W04037); the newer API
  is `coin_registry::new_currency_with_otw`.'
paper: ''
supporting_passage: sui 1.74.1 builds `coin::create_currency` called with a one-time
  witness with exit 0, emitting warning[W04037] deprecated usage which recommends
  `coin_registry::new_currency_with_otw` instead.
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
  checked: '2026-07-06'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/coin-currency-green
grounding: {}
judgment: {}
---

Create a currency in `init` with the module's one-time witness: `let (treasury, metadata) = coin::create_currency(witness, 9, b"MYC", b"My Coin", b"Example coin", option::none(), ctx);` then freeze the metadata and transfer the treasury. This compiles on sui 1.74.1 but with a deprecation warning (W04037); the newer API is `coin_registry::new_currency_with_otw`.

> sui 1.74.1 builds `coin::create_currency` called with a one-time witness with exit 0, emitting warning[W04037] deprecated usage which recommends `coin_registry::new_currency_with_otw` instead.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
