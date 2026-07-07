---
id: capability-doc
statement: 'Capabilities are objects: a function taking `&AdminCap` can only be called
  by whoever owns that object, and strict typing guarantees only the correct capability
  satisfies the parameter. This is a design rule, not a compiler rule — a naive hardcoded
  sender check like `assert!(ctx.sender() == @0xCAFE)` compiles clean on sui 1.74.1
  (triage-observed on sui 1.74.1-8fc60f1fa966; see examples/sui-move-fixtures/beat-log.md),
  so prefer the capability pattern for access control.'
paper: ''
supporting_passage: 'In the [Sui Object Model](./../object/), capabilities are represented
  as objects. An owner of an

  object can pass this object to a function to prove that they have the right to perform
  a specific

  action. Due to strict typing, the function taking a capability as an argument can
  only be called

  with the correct capability.'
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
  evidence: 'In the [Sui Object Model](./../object/), capabilities are represented
    as objects. An owner of an

    object can pass this object to a function to prove that they ha'
  checked: '2026-07-07'
execution: {}
grounding:
  source: sui-move-book
  supporting_passage: 'In the [Sui Object Model](./../object/), capabilities are represented
    as objects. An owner of an

    object can pass this object to a function to prove that they have the right to
    perform a specific

    action. Due to strict typing, the function taking a capability as an argument
    can only be called

    with the correct capability.'
judgment: {}
---

Capabilities are objects: a function taking `&AdminCap` can only be called by whoever owns that object, and strict typing guarantees only the correct capability satisfies the parameter. This is a design rule, not a compiler rule — a naive hardcoded sender check like `assert!(ctx.sender() == @0xCAFE)` compiles clean on sui 1.74.1 (triage-observed on sui 1.74.1-8fc60f1fa966; see examples/sui-move-fixtures/beat-log.md), so prefer the capability pattern for access control.

> In the [Sui Object Model](./../object/), capabilities are represented as objects. An owner of an
object can pass this object to a function to prove that they have the right to perform a specific
action. Due to strict typing, the function taking a capability as an argument can only be called
with the correct capability.

— *grounding verified* via doc-corpus: In the [Sui Object Model](./../object/), capabilities are represented as objects. An owner of an
object can pass this object to a function to prove that they ha
