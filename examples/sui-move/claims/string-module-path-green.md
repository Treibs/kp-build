---
id: string-module-path-green
statement: '`std::string::String` values are created with the lowercase module-path
  call `string::utf8(b"...")` (import `use std::string::{Self, String};`). Function
  calls in Move go through the module path, not the type name.'
paper: ''
supporting_passage: sui 1.74.1 builds a module calling `string::utf8(b"hello")` via
  `use std::string::{Self, String};` with exit 0 and zero warnings.
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
  checked: '2026-07-08'
execution:
  tool: sui-move-build
  gate_code: build_error
  artifact: sui-move-fixtures/string-module-path-green
grounding: {}
judgment: {}
---

`std::string::String` values are created with the lowercase module-path call `string::utf8(b"...")` (import `use std::string::{Self, String};`). Function calls in Move go through the module path, not the type name.

> sui 1.74.1 builds a module calling `string::utf8(b"hello")` via `use std::string::{Self, String};` with exit 0 and zero warnings.

— *execution verified* via sui-move-build: sui-move-build:build_error cleared
