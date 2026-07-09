---
id: receiving-green
statement: 'Receive an object that was sent to another object with `transfer::public_receive(&mut
  parent.id, ticket)`, where the ticket parameter has type `transfer::Receiving<T>`
  and `T has key + store`: `public fun redeem(mailbox: &mut Mailbox, ticket: transfer::Receiving<Parcel>):
  Parcel { transfer::public_receive(&mut mailbox.id, ticket) }`.'
paper: ''
supporting_passage: sui 1.74.1 (edition 2024) builds a module that unwraps a transfer::Receiving<Parcel>
  ticket via transfer::public_receive(&mut mailbox.id, ticket) with exit 0.
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
  checked: '2026-07-09'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/receiving-green
grounding: {}
judgment: {}
---

Receive an object that was sent to another object with `transfer::public_receive(&mut parent.id, ticket)`, where the ticket parameter has type `transfer::Receiving<T>` and `T has key + store`: `public fun redeem(mailbox: &mut Mailbox, ticket: transfer::Receiving<Parcel>): Parcel { transfer::public_receive(&mut mailbox.id, ticket) }`.

> sui 1.74.1 (edition 2024) builds a module that unwraps a transfer::Receiving<Parcel> ticket via transfer::public_receive(&mut mailbox.id, ticket) with exit 0.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
