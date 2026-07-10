# Round-6 triage — sui-move

Probe: 15 incidental-shaped tasks × 2 models, kp128 loaded (sha `d9e414e7…`), pinned
`sui 1.74.1-8fc60f1fa966`, import checker on every answer. **haiku 7/15, sonnet 15/15**
([probe/results.txt](probe/results.txt)). Eight failing runs, all haiku; every log
root-caused in full.

## The round's headline finding (before the table)

**All five seeded territories probed clean on their own classes, with corners demonstrably
exercised** — and six of the eight failures are *loaded rules ignored*. Under this round's
old-way selection rule (probe-elicited beats only), the harvest is **two beats**, both new
single-answer classes. The old-way well is visibly drying: the pack's coverage has moved the
failure frontier into rule application, where beats cannot reach. This is the strongest
single-round evidence yet for the experiment-7 hypothesis that round 5's win owed to its
*frequency-based selection* (which teaches where held-out draws actually fail) rather than
pack size — experiment 8 makes the comparison formally.

## Failures

| task / model | observed | verdict | reason |
|---|---|---|---|
| opt-1 / haiku | E03003 — `use std::option::{self, Option}` lowercase group-`self` | **not beat-worthy** | round-1 `use-self` **ignored while loaded** (event ~6 of the series). NOTE: the std::option *path* is correct — the territory's own class did not fire |
| opt-3 / haiku | E03003 — same lowercase `self` shape in `std::option` | **not beat-worthy** | `use-self` ignored again (event ~7) |
| ctx-3 / haiku | E03003 ×2 + 6 cascades — `use sui::balance::{self, …}` | **not beat-worthy** | `use-self` ignored again (event ~8 — three events in ONE draw) |
| brm-1 / haiku | E03006 ×3 — `coin::value(…)` with only `use sui::coin::Coin` bound | **not beat-worthy** | round-3 `missing-module-import` ignored while loaded |
| brm-3 / haiku | E04024 — `let SubmissionData { candidate, score, fee } = …` then `&mut fee` (binding not `mut`) | **not beat-worthy** | the taught `param-mut` rule's own doc claim names destructuring bindings; ignored while loaded (destructure shape) |
| csp-2 / haiku | E04024 — `deposit: Coin<SUI>` param mutated without `mut` | **not beat-worthy** | `param-mut` ignored while loaded (exact taught shape). NOTE: the split itself is written correctly (`coin::split(&mut deposit, amt, ctx)`) — the territory's misconceptions did not fire |
| brm-2 / haiku | E04004 ×2 — `stamp: Option<&Stamp>` (a reference as a type argument) | **beat-worthy** (`reference-type-argument`) | NEW class, probe-elicited: references are not first-class types — they cannot be type arguments or stored values; the fix is `Option<ID>`/borrowing at use. Old-way rule: probe-elicited in an approved territory's task → taught |
| mva-3 / haiku | E04007 ×2 — `vector::contains(&blocklist, address)` passing the element by value | **beat-worthy** (`vector-contains-by-ref`) | NEW class, probe-elicited: `vector::contains<T>(v: &vector<T>, e: &T)` takes the probe element by reference; Rust's `Vec::contains(&self, x: &T)` actually matches — the slip is not borrowing at the call. Taught under the same rule |

## Clean territories (corners exercised — findings, not omissions)

- **std-option-path: clean.** Every answer that used `Option` imported it from `std::option`
  (both failures in opt were the `self` casing, path correct). The ×2 held-out class did not
  reproduce; under this round's design it is NOT taught (the controlled-comparison cost,
  accepted in the freeze). Rate ceiling applies.
- **branch-type-mismatch: clean on its class** — passing brm answers use statement-form
  branches or matching types; no E04007-branch or abort-semicolon shape anywhere.
- **coin-split-shapes: clean** — every split site in passing (and failing) answers is the
  correct `coin::split(&mut …, amount, ctx)`; neither by-value nor pair-return fired.
- **moved-value-arg-order: clean** — mva-1/mva-2 hoist the recorded address before the move
  (`let winner = trophy.winner;` verbatim in both models).
- **api-arity-ctx: clean-with-avoidance** — every empty-value site used `balance::zero()`
  (correctly nullary, and the pack-idiomatic W99003-avoiding choice); the `coin::zero(ctx)`
  corner was never reached. Recorded as avoidance, not knowledge.

## Import sweep (replication point #4)

**0 fails (18 CORRECT, 12 NA).** Confound noted: kp128 carries the taught `sui-import` beat,
so a zero here is consistent with the beat working rather than evidence about elicitation —
the un-confounded points remain the experiment (3/8, 1/8) and the round-5 sweep (1/9).

## Beat list (old-way selection: probe-elicited only)

| beat | evidence | shape |
|---|---|---|
| `reference-type-argument` | brm-2/haiku ×1 (probe) | RED: `Option<&Stamp>` E04004; GREEN: store `ID`, borrow at use; doc: references cannot be stored |
| `vector-contains-by-ref` | mva-3/haiku ×1 (probe) | RED: `contains(&v, e)` by value E04007; GREEN: `contains(&v, &e)`; doc: the signature |

Deliberately NOT taught this round despite ledger strength (the design's controlled cost):
`std-option-path` (×2 held-out), `branch-type-mismatch` (×2), `split-by-value`/pair (×1/×1),
plus every ignored-rule event above. All carry to the round-7 ledger unchanged.
