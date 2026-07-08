# Sui Move cheat sheet — Move 2024 edition, verified against sui 1.74.1

One rule per line. Every rule was proven against the pinned compiler; the error code is what the
broken form produces. Apply ALL of these — the most common failures are rules on this sheet
being ignored.

## Module and edition syntax

- Declare modules with an address qualifier: `module my_pkg::name { ... }` — bare `module name {` fails (E02004).
- Declare structs `public struct ...` — bare pre-2024 `struct` fails (E01003).
- Declare reassigned locals `let mut x = ...` — reassigning a plain `let` fails (E04024).
- `mut` is also required on by-value function parameters (and tuple destructures) you mutate: `fun bump(mut c: Counter)` — without it, mutation fails (E04024).
- `friend` is deprecated — use `public(package) fun` instead (E13002).
- A braced `if`/`while` used as a statement mid-sequence needs a `;` after the closing brace, unlike Rust (E01002).
- Call functions on their first argument with dot notation when defined in the type's module: `counter.value()`.
- Create vectors with literals: `vector[]` / `vector[e1, e2]` — `vector::empty()` is deprecated (W04037).
- Never write `public entry fun` — plain `public fun` is PTB-callable already (lint W99010); reserve `entry` for non-public functions.
- Prefer RETURNING created/extracted objects from public functions over `transfer::public_transfer(obj, ctx.sender())` — transfer-to-sender draws lint W99001 "non-composable transfer to sender"; returning compiles with zero warnings.

## Imports

- In group imports the module itself is capital `Self`: `use sui::coin::{Self, Coin};` — lowercase `self` fails (E03003).
- Every `module::fn` alias call needs its module bound by `use`: `event::emit(...)` requires `use sui::event;` first — otherwise "Could not resolve the name" (E03006).
- `sui::transfer`, `object`, `UID`, and `TxContext` are implicitly imported — no `use` needed for them.

## Objects and abilities

- A `key` struct's first field must be `id: UID` (Sui E02007), created only with `object::new(ctx)` — `object::uid_from_bytes` does not exist (E03003).
- Every field of a `key` struct needs `store`, including the element type of a vector field (E05001). Generally: `copy` structs need all-`copy` fields, `drop` needs all-`drop`, `store` needs all-`store`.
- `key + store` types are freely transferable by anyone via `transfer::public_transfer`; calling `public_transfer` on a `key`-only type fails (E05001) — use `transfer::transfer` from the defining module for those.
- `transfer::transfer` is PRIVATE (defining module only): transferring a foreign `store` type such as `Coin<SUI>` needs `transfer::public_transfer` (Sui E02009 otherwise).
- An object sent to another object arrives as `transfer::Receiving<T>`; unwrap it cross-module with `transfer::public_receive(&mut parent.id, ticket)` (needs `store`) — cross-module `transfer::receive` fails (Sui E02009).
- Reading a non-`copy` field with the dot operator is an invalid implicit copy (E05001) — move it out by destructuring: `let Pouch { gem } = p;`.
- Ignoring a non-`drop` value fails — `field: _` in a destructure, `let _ =`, or leaving it unused all require `drop` (E05001). Consume explicitly instead: bind the `UID` and `object::delete(id)`.

## init, one-time witnesses, currencies

- `init` is `fun init(witness: OTW, ctx: &mut TxContext)` or `fun init(ctx: &mut TxContext)` — any other first parameter fails at build (Sui E02003).
- A one-time witness cannot be constructed manually (Sui E02005); a struct named the upper-case of its module name IS treated as an OTW — name plain reusable witnesses differently (e.g. `MinterWitness`).
- Create currencies in `init` with the OTW: `let (treasury, metadata) = coin::create_currency(witness, 9, b"MYC", b"My Coin", ...)` — `coin::mint_new` does not exist (E03003).

## Capabilities

- Access control idiom: `public struct AdminCap has key, store { id: UID }`, transferred to the publisher in `init`; gate privileged functions with a `&AdminCap` parameter.

## Events

- Event structs need `copy` AND `drop`: `public struct ValueSet has copy, drop { ... }`, emitted with `sui::event::emit` (import it) — missing `copy` fails (E05001).

## Time

- On-chain time comes from `sui::clock::Clock` (shared object at 0x6): take `clock: &Clock` and read `clock.timestamp_ms()` — `tx_context::now_ms` does not exist (E03003).

## Dynamic fields

- Dynamic fields live in `sui::dynamic_field`: `dynamic_field::add(&mut obj.id, name, value)` — `object::add_field` does not exist (E03003).
- Check existence with `dynamic_field::exists(&obj.id, name)` — the old `exists_` still compiles but warns (W04037).

## Strings

- Build strings with the lowercase module path: `string::utf8(b"...")` with `use std::string::{Self, String};` — Rust-style `String::utf8` parses as enum construction and fails (E03006).
- Concatenate with `append`: `a.append(b)` (mutates through `&mut`) — `+` is integer-only in Move (E04003).

## Options

- Overwriting an `Option<T>` field by assignment destroys the old value and needs `T: drop` (E05001) — to set a `none` field use `option::fill` (`opt.fill(value)`; aborts if already `some`).

## Tables

- `sui::table` functions take keys BY VALUE: `table.contains(key)` / `table.borrow(key)` — passing `&key` (the Rust habit) fails (E04007).

## Type reflection

- `std::type_name` returns `TypeName`, not `String`: store `vector<TypeName>` or convert with `.into_string()` — and on 1.74.1 use `with_defining_ids` (the old `get` is deprecated) (E04007 if stored as String).

## Tests

- `#[test_only]` members are filtered out of non-test builds — production code calling one is an unbound name (E03005).
- Multi-transaction tests use `sui::test_scenario` (`begin`, `next_tx`, `take_shared` + `return_shared` before the scenario ends).
