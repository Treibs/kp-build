# Round-4 territories — sui-move

**Seeding rule:** round 4 is gap-seeded from the recorded falsification/remeasure ledgers, same
as rounds 2 and 3 — every territory below traces to a *measured* failure recorded in
`docs/deepening/round-3/remeasure.md`, `docs/experiments/sui-payload-salience/README.md`
(experiment 5's ledger carried there), or `docs/experiments/sui-sheet-confirm/README.md`, not to
encyclopedic coverage instinct. The two payload-form experiments between round 3 and this round
produced no beats but enriched the candidate ledger; the sheet-confirm README's fork
("targeted round 4 on the enriched ledger or strength-training pack") resolves here to round 4.

**Gate-1 approval:** operator approved this list as proposed, 2026-07-09 (interactive session;
option "Approve as proposed" selected at the scope gate). Exclusions below are part of the
approved record.

## Proposed and approved territories

| # | territory | seed (recorded evidence) | why parametric knowledge is suspect |
|---|---|---|---|
| 1 | `sui-import-path` — the `SUI` type reached through the wrong module (`use sui::coin::{Coin, SUI}`) or through no import at all (`Balance<SUI>` written with `use sui::sui::SUI` absent) | ×4+ cumulative events: exp-4 ×3 answers (subscription/kp61, gift-card/kp86, rental/kp61 `sui::option` sibling), round-3 remeasure import-2/sonnet root cause 1, exp-5 ×2 (staking-pot/slim, payment-channel/full — both absent-import shape). Top of every candidate ledger since exp-4 | `SUI` is *used through* `Coin<SUI>`/`Balance<SUI>` everywhere in real code, so the prior for where the type is *declared* is diffuse; Rust re-exports make "import it from the module you use it with" work — Move resolves `sui::sui::SUI` only |
| 2 | `rust-syntax-bleed` — Rust surface syntax at the parse level: return arrow `fun f(...) -> T` (E01002 "Unexpected '->'") and compound assignment `+=`/`-=` | rust-return-arrow ×4 cumulative answers (round-3 remeasure modimp-2, exp-5 allowance-vault/kp86, exp-5-salience grade-book slim+sheet); rust-compound-assign NEW at sheet-confirm (2 answers, 3 sites) | pure Rust muscle memory below the semantic level; Move 2024 declares returns with `: T` and has no compound-assignment operators. Parse errors also truncate recovery (exp-5 showed E06001 fallout from one `->`), so a single habit can sink an otherwise-correct answer |
| 3 | `rust-api-bleed` — Rust std APIs transplanted whole: `.len()`/`.get(i)` on vectors (E04023; Move 2024 methods are `.length()`/`.borrow(i)`), `std::mem::replace` (E03002), tuples as first-class values / type arguments (E04004/E04005) | rust-vector-method NEW at exp-5 (milestone-contract/kp98, ×6 sites one habit); std-mem-replace ×2 (round-3 probe destr-3/sonnet + remeasure, promoted at round-3); rust-tuple-value NEW at exp-5-salience (grade-book full+sheet, 2 answers, 25 sites) | the sibling family one level up from territory 2: not syntax but API surface. Rust's `Vec::len`, `std::mem`, and tuple values have no Move counterparts; the model reaches for them exactly when the task needs indexed iteration, in-place swap, or a compound key |
| 4 | `generic-transfer-key-bound` — `transfer::public_transfer(x, ...)` / `transfer::transfer(x, ...)` where `x: T` with only `T: store` (needs `T: key + store`) | ×3 cumulative (round-2 remeasure optiondrop-1 ×2, round-3 remeasure generic-3/haiku); promoted at round-2 triage, carried through round 3 where the probe recorded the territory clean yet the class fired again in the remeasure | the `store`-implies-transferable intuition is wrong: `key` is what makes an object; a bare `T: store` can only live inside other objects. Round-3 lesson applied: the class fires when the task *leaves the generic bound choice to the model* — this round's probe tasks are designed to leave that choice open, not to name bounds |
| 5 | `object-identity` — Sui's three identity types blurred: a `UID` captured from a deleted/old object and reused in a new one (Sui E01001), the `UID` emitted in an event where the copyable `ID` belongs, an `address` field filled with an `ID` (E04007) | family ×4 cumulative: uid-reuse ×2 (round-3 probe destr-3 + remeasure, promoted at round-3), uid-vs-ID event field NEW at sheet-confirm (full arm), ID-vs-address NEW at exp-5-salience (micro-amm/slim ×3 sites) | Rust has no owned-identity type; Sui has three (`UID` unique and owned by exactly one object, `ID` copyable, `address` a different type again). The model treats them as interchangeable handles; the pack pins `object::new`/`delete` but nothing pins the UID/ID/address boundary |

## Deliberately excluded (with reasons)

Single-answer classes, held by the standing 1-answer deferral rule (the same rule that held
`generic-transfer-key-bound` at round-2 and promoted it on its 2nd occurrence — each is promoted
if it recurs in this round's probe):

- **E07001 referential-transparency borrow shape** (`coin::split(&mut obj.field, obj.field2, ctx)`
  — sheet-confirm, ×1 answer)
- **macro-bang** (`vector::all` without `!` / lambda outside a macro — exp-5-salience
  rosca-circle/slim, ×1)
- **reserved-name `freeze`** (compliance-coin/sheet, ×1; the *task-authoring* side is already
  covered by the round-3 reserved-word check)
- **turbofish/annotation on `dynamic_field::remove`** (compliance-coin/sheet, ×1)
- **api-arity-missing-ctx** (E04016, `coin::zero()` without `ctx` — round-3 remeasure, ×1)
- **assert-abort-code** (E04035 — exp-4 rental/kp61, ×1 answer; deferred since round-3 scope)
- **hash corner** (sha3 wrong module ×1 base arm + api-byref-arg ×1 kp98 — exp-5; two different
  classes with one answer each, split across arms)
- **hallucinated APIs** (`coin::freeze_currency_metadata` exp-5-salience ×1;
  test-only `coin::burn_for_testing` sheet-confirm base arm ×1) — one answer each AND not a
  stable rule-teachable class (each hallucination is a different invented name; a beat pins a
  rule, not a blocklist). Recorded; if a *specific* invented API recurs it can be taught as
  "the real API for X is Y".

Excluded on standing negative results:

- **W99003 Balance-vs-Coin / coin-field warning class** (8 sites at exp-5, base included):
  warning-tier grounding beats have shown no attributable held-out effect across two
  experiments (W99001 0/18 including base at exp-4; the loaded W99001 class *regressed* in
  exp-5). The round-3 exclusion reasoning stands — no third data point before the warning-tier
  mechanism is rethought.
- **Any payload-form work** (sheet/slim/emit-sheet): form manipulation is double-dead per the
  sheet-confirm verdict; not a deepening concern.
- **Ignored-while-loaded** (4 consecutive experiments, both payload forms): a model-behavior
  constraint, not missing knowledge — restating a loaded rule is not a new rule. Not a beat by
  the standing triage rule.

## Probe shape

15 fresh authoring tasks (3 per territory), dual model (`claude-haiku-4-5` primary,
`claude-sonnet-4-6` secondary), **current 98-claim pack loaded** in every run (this is
deepening — residual gaps are what matter), pinned `sui 1.74.1-8fc60f1fa966` gate. Task
freshness audited against: all 45 round-1/2/3 probe tasks, the experiment 1–5 and sheet-confirm
task lists (34 tasks), and the pack's fixture zones as of master `a8cb8fc`. Elicitation design
per territory 4's seed note: tasks *invite* the corner (SUI-typed coins, indexed iteration,
in-place swaps, generic containers, object lifecycle events) without naming the defect or the
rule. Mechanical repair rule pre-declared in `probe/README.md` before any answer is collected.
