# sui-move deepening — round 1 — territories

**Date:** 2026-07-07 · **Pack at round start:** 47 claims (30 execution = 17 GREEN + 13 RED,
17 grounding) · **Oracle:** pinned `sui 1.74.1-8fc60f1fa966`, plain `sui move build`
· **Design:** `docs/specs/2026-07-07-kp-deepen-design.md`

## Gate 1 — approval

The five territories below were named in the approved design spec (pilot row of the
decisions table); per the skill, an approved spec naming the territories counts as
owner approval. No changes were made to the approved list.

## Approved territories

| # | territory | why it's a candidate (unprobed + stale-knowledge-prone) |
|---|---|---|
| 1 | **PTB composition** | Entry-function argument/return restrictions and PTB-chainable designs (`public fun` returning objects) are enforced by the compiler and changed across editions; no pack fixture touches entry signatures beyond the entry-vs-public lint. |
| 2 | **Dynamic fields (deep)** | The existing `dynamic-fields` beat only pins the fabricated `object::add_field` → `sui::dynamic_field`. The deeper surface — `dynamic_object_field` vs `dynamic_field`, `&mut UID` receivers, `Table`/`Bag` ability constraints — is unprobed and API-shape-heavy. |
| 3 | **Package upgrades** | Version-gated shared objects, `public(package)` cross-module access, and cross-module object construction rules are the standard upgrade-safety idioms; models trained pre-2024-edition often reach for deprecated `friend` or cross-module struct literals. |
| 4 | **Object-owner patterns** | Wrapping/unwrapping, share-at-creation freshness, and freeze semantics all have compiler/verifier-enforced ability rules (`store` on object fields, `key` vs `key+store` transfer APIs) the pack has not probed beyond single-object transfer. |
| 5 | **Security idioms** | Witness-gated generic registration, two-step ownership transfer, and `Balance`/`Coin` accounting APIs (`coin::take`, `balance::split`) are idiom-dense and frequently confabulated; the pack covers capability *storage* but not these composition patterns. |

## Deliberately excluded

- **Kiosk / TransferPolicy** — probed by experiment 2 task 5 (compiles, warning-tier
  weakness already recorded there).
- **Receiving\<T\>** — was the experiment-2 gap; now a shipped fixture (`receiving` beat,
  PR #11). Probing it again would restate a fixture.
- **Hot potato / flash loan** — probed by experiment 2 task 1 (both arms clean).
- **Publisher / Display** — probed by experiment 2 task 4.
- **`#[test]` / test_scenario depth** — the pack's oracle gate is plain `sui move build`,
  which does not compile test code on 1.74.1 (beat-log surprise #1); failures there would
  be invisible to the gate.
- **Clock-based logic as a primary target** — the `clock` fixture already pins the
  fabricated-timestamp failure; tasks avoid requiring `Clock` so failures stay attributable
  to the territory under probe.

## Probe plan

3 concrete authoring tasks per territory (15 total), fresh context per task,
**current 47-claim pack loaded** (CONTEXT.md + all claim statements — the same assembled
payload family as `docs/experiments/sui-compile-pass-2/`), dual model:
`claude-haiku-4-5` (falsification primary) and `claude-sonnet-4-6` (secondary).
Every answer is gated by the pinned binary with the arm-neutral scaffold repair
(declared address names bound to `0x0`; first-defined-module rule for multi-module
answers). Tasks and per-task results live under `probe/`.
