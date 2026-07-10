---
id: sui-import-doc
statement: 'The official shared-object example opens with the canonical import block:
  `use sui::sui::SUI;` then `use sui::coin::{Self, Coin};` then `use sui::balance::{Self,
  Balance};`.'
paper: ''
supporting_passage: 'use sui::sui::SUI;

  use sui::coin::{Self, Coin};

  use sui::balance::{Self, Balance};'
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
  evidence: 'use sui::sui::SUI;

    use sui::coin::{Self, Coin};

    use sui::balance::{Self, Balance};'
  checked: '2026-07-10'
execution: {}
grounding:
  source: sui-docs-concepts
  supporting_passage: 'use sui::sui::SUI;

    use sui::coin::{Self, Coin};

    use sui::balance::{Self, Balance};'
judgment: {}
---

The official shared-object example opens with the canonical import block: `use sui::sui::SUI;` then `use sui::coin::{Self, Coin};` then `use sui::balance::{Self, Balance};`.

> use sui::sui::SUI;
use sui::coin::{Self, Coin};
use sui::balance::{Self, Balance};

— *grounding verified* via doc-corpus: use sui::sui::SUI;
use sui::coin::{Self, Coin};
use sui::balance::{Self, Balance};
