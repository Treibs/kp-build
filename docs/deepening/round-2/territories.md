# Round 2 — territories (step 1: Scope)

Pack: `examples/sui-move/` (61 claims at master `da895f5`) · Oracle: pinned
`sui 1.74.1-8fc60f1fa966`, plain `sui move build`.

**Seeding rule for this round (differs from round 1):** territories are seeded from **recorded
falsification gaps** — the round-2 candidates written down in experiment 3's ledger
(`docs/experiments/sui-compile-pass-3/README.md`) and round 1's deferrals — not from a fresh
unprobed-territory brainstorm. This is the skill's core thesis applied recursively: depth follows
measured failures, and experiment 3 measured exactly where the deepened pack still fails.

**Approval (human gate 1):** operator explicitly requested this deepening round (2026-07-07),
in direct response to the experiment-3 report that named these candidates. Recorded here as the
approval of the list below.

## Approved territories

| # | territory | seed | why parametric knowledge is likely wrong here |
|---|---|---|---|
| 1 | **module-declaration address form** (E02004) | exp-3 candidate 1 — 3 hits, pack arms only, both pack arms; counterfactual-proven a model defect, not a scaffold artifact | pre-2024 Move sources and older tutorials use `address 0x0 { module name { } }` blocks or bare `module name {`; Move 2024 requires `module <address>::name`. The pack teaches no module-declaration claim at all |
| 2 | **Option-field `drop` discipline** (E05001 mutation + ignore shapes) | exp-3 candidate 2 — 7 errors across 4 logs, the largest residual class by raw count; ignore shape = round-1 remeasure's "drop on discard" residual | models habitually overwrite (`s.f = option::some(x)`) or discard (`f: _`) `Option<T>` fields where `T` lacks `drop`; the correct idioms are `option::fill`/`swap`/`extract`. Ability-constraint reasoning is a known parametric weak spot |
| 3 | **`let mut` borrow shape** (E04024 mutable borrow of an immutable binding) | exp-3 nuance candidate — english-auction/kp47 | the pack's let-mut claims cover the *reassignment* shape only; `&mut x` of a non-`mut` binding is the same 2024 rule surfacing through a different syntactic path, untaught |
| 4 | **Coin/Balance field idiom + transfer composability** (Lint W99003, W99001) | exp-3 candidate 3 — 4 warning rows; the natural target while the secondary (clean-compile) metric is tied | storing `Coin<T>` in struct fields instead of `Balance<T>`, and `transfer::public_transfer(.., ctx.sender())` instead of returning, are pervasive in pre-lint example code; the 1.74-era linter flags both |
| 5 | **deprecated stdlib collection constructors** (W04037 `vector::empty` → `vector[]`) | recorded deferral from round 1, re-observed in exp-3 (multisig base + kp47) | `vector::empty<T>()` is the dominant form in older corpus/tutorials; the edition-2024 idiom is the `vector[]` literal — classic edition drift |

## Deliberately excluded

- **Fresh unprobed territories** (PTB construction depth, upgrade policies, test-scenario
  patterns beyond the disclosed gate exception) — this round is gap-seeded by design; fresh
  territory scans return in a later round.
- **E03006 "unexpected name in this position" cascade** (12 hits in crowdfund/kp47) — secondary
  damage from the broken `use`-import, not an independent knowledge gap; closing use-self
  (already taught) removes it.
- **Sui E01001 invalid object construction** (loyalty-points/base) — single hit, base arm only;
  monitor, revisit if it recurs in this round's probe.
- **W04037 `exists_` rename** — already taught (round-1 `dynamic-field-exists` beat).

## Probe shape (step 2 parameters)

~3 concrete authoring tasks per territory (15 total), none restating a pack fixture, a round-1
probe task, or an experiment-1/2/3 task (checked against all four lists before collection —
lesson from exp-3's held-out defect). Dual model on every task: `claude-haiku-4-5` (falsification
primary) + `claude-sonnet-4-6` (secondary). Arm: current 61-claim pack loaded. Same mechanical
repair rule as round 1, pre-declared in `probe/README.md` before any answer is collected.
