# Round-7 territories — sui-move

**Seeding rule:** frequency-ledger selection — **the method of record** per the exp-7/exp-8
verdict pair (`docs/experiments/sui-compile-pass-7/`, `docs/experiments/sui-compile-pass-8/`,
merged `e5496b7` / `2b3d909`): round 5 (frequency-selected) shipped on branch 1 while round 6
(old-way, probe-elicited-only) recorded branch 3 with its two declined classes firing in its
own remeasure. The ledger below is copied from the exp-8 README's "Round-7 ledger" section
and the round-6 remeasure ledger; every count is a recorded, committed observation. Pack at
round start: **134 claims** (master `cf492b1`; sui claims unchanged since round-6 teach
`2911d…`; the kp134 payload is byte-identical to exp-8's pinned artifact, sha
`9d4e6fe8a69abf15453a940455ce0616f78beea84dfbf368bbf3905859c89bff`, 56,464 bytes).

**Gate-1 approval:** operator directive 2026-07-10: "run sui round 7 from the frequency
ledger" — the directive names the seeding rule; the territories below follow from it
mechanically (the five ledger classes with the highest recorded frequency, all ×2 or more).
Run-to-merge authorization per the round-5/6 precedent.

**Teach rule (binding, the frequency method):** beats this round are selected by the ledger,
not by what this probe elicits. Every class below already has observed oracle failures in
committed artifacts (cited per row); a clean probe on a territory does NOT decline its beat —
that is exp-8's core finding (round 6 probed `std-option-path` and `moved-value-arg-order`
clean, declined both, and both fired in its own remeasure). The probe's roles: fresh
elicitation evidence, RED-fragment material, remeasure baselines, and the import-checker
replication sweep.

**Probe-shape directive (binding, carried from the elicitation experiment):** every task is
incidental-shaped — the territory's corner is a side requirement of a non-focal core
mechanic, never the task's headline. 8 of the 15 tasks carry an incidental SUI-payment
element; every answer runs through the committed import checker
(`docs/experiments/sui-import-elicitation/check_import.py`).

## Approved territories

| # | territory | seed (recorded evidence) | why parametric knowledge is suspect |
|---|---|---|---|
| 1 | `tuple-bleed` (`tb`) — tuples pushed into type-argument or storage positions (`Option<(A, B)>`, `vector<(A, B)>`, tuple struct fields), E04004 "expected a single non-reference type" | ×3 cumulative, TOP: round-6 review's missed-beat class fired exp-8 plant-clinic/kp134 (`Option<(vector<u8>, vector<u8>)>` return-position type argument) + exp-8 quilt-bee/kp134 (`vector<(address, Square)>` storage, ×2 in one answer) | Rust tuples are first-class storable values; Move tuples exist only as expression/return conveniences — they cannot be type arguments or stored. The pack carries the DOC-tier rule ("References (and tuples) are the only types that cannot be stored as struct field values") and quilt-bee fired THROUGH it (loaded-rule-ignored at doc tier) — this round escalates the class to an execution beat with a RED pin, disclosed as a tier escalation, not a new rule |
| 2 | `std-table-path` (`stp`) — `use std::table`; `Table` lives at `sui::table`, E03002 unbound module | ×2, promoted: exp-6 book-club/kp110 (16-error cascade) + exp-8 plant-clinic/kp128 (10 cascades) | the std-vs-sui split is memorized per-module, not derived (`std::string` is real, `std::table` is not); family sibling of the taught `string-module-path` beat — the sui-side mirror is unpinned |
| 3 | `balance-api-on-coin` (`bac`) — `coin::take`/`coin::put` invoked on `Coin`-typed values or fields; both operate on `&mut Balance` | ×2, promoted: exp-6 (coin::put on a `Coin` field) + exp-7 family firing (`Balance::zero()` shape adjacent); named and promoted in the exp-8 README **[CORRECTION, post-freeze review round 1: the second recorded event is exp-8 ferry-manifest's `coin::take` on a `Coin` (E04007, the exact class); exp-7's `Balance::zero()` is an E03006 base-arm shape already filed under api-arity-ctx and records no balance-api event — the ×2 count stands on exp-6 + exp-8. The task designs are unaffected; frozen text preserved above.]** | signature-level knowledge decays fastest; the model knows take/put exist and guesses the receiver type from the "wallet" intuition — the Coin-vs-Balance split (store `Balance`, wrap to `Coin` at the boundary) has no Rust analogue |
| 4 | `std-option-path` (`sop`) — `use sui::option`; `Option` lives at `std::option`, E03002 | ×3: exp-4 rental/kp61 + exp-7 stall-rental/kp128 + round-6 remeasure opt-1 (the class round 6's frozen design declined, firing in its own remeasure) | mirror image of the taught `sui-import` beat: std modules pulled under the `sui::` prefix when the import block is crowded with genuine `sui::` imports; the loaded payload *implies* the right path (`std::option::swap` appears in claim text) but never pins it |
| 5 | `moved-value-arg-order` (`mva`) — a value moved as an earlier call argument then read in a later argument (`transfer(obj, obj.recipient)`), E06002 | ×2, promoted: round-5 probe vde-1 + round-6 remeasure mva-3 (`transfer::public_transfer(letter, letter.sender)` — the second class round 6 declined that fired in its own remeasure) | argument evaluation order × linearity: the read must be hoisted before the move; both Rust and Move reject it, but the model writes it under multi-concern load — round-6's probe gated clean while the remeasure fired it, so elicitation is draw-sensitive and the beat must come from the ledger |

## Deliberately excluded

- **`branch-type-mismatch`** (×2, carried not promoted) — round-6 probed the territory clean
  on its class and it has not fired since exp-7; it stays on the ledger at carried tier. If
  it reaches ×3 it promotes next round.
- **`use-self` ignored-rule ledger** (~12 events) — rule APPLICATION, not coverage, is the
  binding constraint; no beat can address it (the rule is already loaded and ignored).
  Recorded, not taught.
- **W-tier warning beats** — the standing negative result stands.
- **`split-by-value`/pair classes at ×1** — below the frequency threshold; carried.

## Probe shape

15 fresh authoring tasks (3 per territory), ALL incidental-shaped, dual model
(`claude-haiku-4-5` primary, `claude-sonnet-4-6` secondary), current 134-claim pack loaded,
pinned `sui 1.74.1-8fc60f1fa966` gate, committed import checker on every answer. Task
freshness audited against the **164 prior probe/experiment tasks** (143 at the round-6
audit + round-6's 15 probes + exp-8's 6) and the **47 committed fixture zones (87 fixture
directories — 40 red/green pairs + 7 green-only)** — **with a
pre-freeze adversarial reviewer pass on the audit** (the standing step since the elicitation
erratum; the author does not freeze an audit alone). The reviewer's verdict and every
applied revision are recorded in `probe/README.md` before the freeze. Mechanical repair
rule pre-declared in `probe/README.md` before any answer.
