# Held-out tasks — sui-move falsification, experiment 2 (pre-registered)

Experiment 1 (`../sui-compile-pass/`) hit a ceiling: base 5/5 vs kp 5/5 compile-pass.
This is the pre-registered second run: harder tasks, dual metric. **This file is
committed before any answer is collected** — the commit timestamp is the
pre-registration.

## Tasks

Five contract-authoring tasks, harder than experiment 1, none appearing as a pack
fixture (fixture zones: struct visibility, method syntax, friend, implicit imports,
key/UID, let-mut, object::new, transfer/store, entry-vs-public, OTW init, capability,
coin currency, dynamic fields, events, clock, test_scenario, test_only, macros):

1. **flash-loan** — A flash-loan pool for SUI: `borrow` hands out a `Coin<SUI>`
   together with a hot-potato receipt (a struct with no abilities) that forces
   `repay` (principal + fee) in the same transaction.
2. **object-mailbox** — A mailbox that accepts objects sent directly to its address:
   an `open` function that takes a `Receiving<T>` ticket and uses
   `transfer::receive` to extract the sent object, gated by an owner capability.
3. **generic-vault** — A generic vault `Vault<phantom T>` that stores `Balance<T>`,
   supports deposit of `Coin<T>` and withdrawal by an admin capability, using
   `coin::into_balance` / `coin::from_balance`.
4. **nft-display** — An NFT collection with off-chain Display metadata: claim the
   `Publisher` in `init` with a one-time witness, create a `Display<Nft>` with
   name/image_url fields, and a mint function.
5. **kiosk-listing** — A function set that places an item into a `Kiosk` and lists
   it for a fixed price, plus a purchase flow that resolves the `TransferPolicy`
   hot potato.

## Protocol (identical to experiment 1 except where stated)

- **base** arm: fresh agent context, ONLY the task text. No pack, no docs, no
  compiler, no tools.
- **kp** arm: identical prompt PLUS the pack (CONTEXT.md + all claims, the same
  assembled text used in experiment 1). Fresh context per task.
- Model both arms: claude-sonnet-4-6. Answer = one Move module, source only.
- Scaffold: minimal `Move.toml` (edition 2024) **including the arm-neutral address
  repair from experiment 1, now part of the scaffold from the start**: the declared
  address name in the answer's `module X::Y` line is mechanically bound to `0x0`.
  No module source is ever touched.
- Score with the pinned binary (`sui 1.74.1-8fc60f1fa966`), `sui move build`.

## Pre-registered metrics and ship rule

- **Primary — compile-pass:** the build exits 0.
- **Secondary — clean-compile:** the build exits 0 AND emits zero compiler warnings
  (count of `warning[` lines in the build output is 0, lints included).

**Ship rule (decided before data):**
1. If kp compile-pass > base compile-pass → pack ships.
2. If compile-pass ties, and kp clean-compile > base clean-compile → pack ships
   (cleanliness axis, pre-registered this time).
3. Anything else (kp below base on primary, or tie on both) → pack does not ship
   on this evidence. No third experiment without operator sign-off; no post-hoc
   metric may be substituted.
