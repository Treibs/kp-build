---
id: implicit-imports-doc
statement: Framework staples like `sui::transfer` are implicitly imported in every
  package that depends on the Sui Framework and need no `use` statement. The legacy
  `use sui::object::{Self, UID}; use sui::transfer; use sui::tx_context::TxContext;`
  block still compiles silently on sui 1.74.1 (no warning), but it is dead weight
  — omit it (triage-observed on sui 1.74.1-8fc60f1fa966; see examples/sui-move-fixtures/beat-log.md).
paper: ''
supporting_passage: 'The module that defines main storage operations is `sui::transfer`.
  It is implicitly imported in all

  packages that depend on the [Sui Framework](./../programmability/sui-framework),
  so, like other

  implicitly imported modules (e.g. `std::option` or `std::vector`), it does not require
  adding a use

  statement.'
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
  evidence: 'The module that defines main storage operations is `sui::transfer`. It
    is implicitly imported in all

    packages that depend on the [Sui Framework](./../programmab'
  checked: '2026-07-09'
execution: {}
grounding:
  source: sui-move-book
  supporting_passage: 'The module that defines main storage operations is `sui::transfer`.
    It is implicitly imported in all

    packages that depend on the [Sui Framework](./../programmability/sui-framework),
    so, like other

    implicitly imported modules (e.g. `std::option` or `std::vector`), it does not
    require adding a use

    statement.'
judgment: {}
---

Framework staples like `sui::transfer` are implicitly imported in every package that depends on the Sui Framework and need no `use` statement. The legacy `use sui::object::{Self, UID}; use sui::transfer; use sui::tx_context::TxContext;` block still compiles silently on sui 1.74.1 (no warning), but it is dead weight — omit it (triage-observed on sui 1.74.1-8fc60f1fa966; see examples/sui-move-fixtures/beat-log.md).

> The module that defines main storage operations is `sui::transfer`. It is implicitly imported in all
packages that depend on the [Sui Framework](./../programmability/sui-framework), so, like other
implicitly imported modules (e.g. `std::option` or `std::vector`), it does not require adding a use
statement.

— *grounding verified* via doc-corpus: The module that defines main storage operations is `sui::transfer`. It is implicitly imported in all
packages that depend on the [Sui Framework](./../programmab
