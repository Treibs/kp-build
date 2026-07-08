# Experiment 4 — held-out falsification of deepening round 2 (sui-move)

**Result up front: no round-2 headline.** Primary metric tied (kp86 3/6 = kp61 3/6) and the
secondary tied (2/6 = 2/6), so the pre-registered ship rule lands on branch 3. **The base arm
beat both pack arms on the primary (5/6 vs 3/6)** — on this task draw, loading the pack made
claude-haiku-4-5 *worse* at compile-pass, and that is reported here as prominently as a win
would have been. The failure composition still moved the way round 2 intended (detail below):
the round-2 taught `option-field-fill` class fired only in the kp61 arm (3 hits across 2 tasks)
and never in kp86, and both those tasks flipped to PASS under kp86 — though each of those kp61
failures also carried untaught defects, so the flips are not attributable to the round-2 beats
alone. No taught error class from any round recurred in the kp86 arm; kp86 gave the two wins
back on new, previously unrecorded classes.

## Setup

- Pre-registration: [`tasks.md`](tasks.md), committed at `d5947f6` **before any answer was
  collected** — arms, tasks (held-out audit run before drafting froze; two candidates dropped
  by it, disclosed there), metrics, and the three-branch ship rule.
- Arms: **base** (task + instruction only), **kp61** (pack payload as of master `da895f5`,
  61 claims — pre-round-2), **kp86** (pack payload as of master `86989a1`, 86 claims —
  post-round-2). Payloads assembled by the arm-neutral rule in tasks.md (`CONTEXT.md` +
  all claim statements, sorted).
- Model: `claude-haiku-4-5`, fresh context per task per arm, headless, no tools.
- Gate: mechanical first-fenced-block extraction, arm-neutral scaffold (`Move.toml` binding the
  answer's own module address names to `0x0`), plain `sui move build` on the pinned
  `sui 1.74.1-8fc60f1fa966`. Committed buildlogs are ANSI-stripped and home-directory-redacted.
- Layout: `answers/<task>/<arm>.answer|-src.move|-pkg/|.buildlog|.result`; summary in
  [`answers/results.txt`](answers/results.txt).
- The assembled payloads themselves are not committed; they are mechanically reproducible from
  the assembly rule in tasks.md (the pinned commits + `sorted()` claim statements).
- **Disclosed protocol inexactness:** the headless CLI runs inherited the harness working
  directory, and one base-arm answer's module address name reflects the repo name
  (`dead-man-switch/base.answer`, `module kp_build::inactivity_vault`). The environment was
  identical for all three arms (arm-neutral) and no task text or payload was affected, but
  tasks.md's "ONLY the task text + the standard instruction" is literally inexact for the
  process environment; disclosed here rather than editing the pre-registration.

## Results

| task | base | kp61 | kp86 |
|---|---|---|---|
| rental-agreement | PASS WARN2 | FAIL E03002 | PASS WARN2 |
| wager-arbiter | FAIL E03003 | FAIL E03006 | **PASS CLEAN** |
| subscription-service | PASS CLEAN | FAIL E03003 | FAIL E03006 |
| gift-card | PASS CLEAN | PASS CLEAN | FAIL E03003 |
| crafting-forge | PASS CLEAN | PASS CLEAN | PASS CLEAN |
| dead-man-switch | PASS WARN1 | PASS WARN1 | FAIL E04023 |
| **primary — compile-pass** | **5/6** | **3/6** | **3/6** |
| **secondary — clean-compile** | **3/6** | **2/6** | **2/6** |

## Verdict (pre-registered ship rule)

- Branch 1 (kp86 > kp61 primary): **no** — tie.
- Branch 2 (primary tie AND kp86 > kp61 secondary): **no** — tie.
- **Branch 3: no round-2 headline on this evidence; recorded as-is.** kp86 is not below kp61 on
  either metric, so this is not a round-2 regression under the rule — but the base arm
  outperforming both pack arms on the primary is the headline *of the experiment* and appears
  in every summary of it.

Two honest context notes, neither of which changes the verdict:

1. **This draw left little headroom.** Base solved 5/6 unaided (exp-3's base was 2/6 on its
   draw — task sets are not comparable across experiments). With base near ceiling, the pack
   could mostly only lose, and it did: both pack arms underperformed base.
2. **The per-task flips are informative even though the topline ties.** kp61→kp86:
   rental-agreement FAIL→PASS and wager-arbiter FAIL→PASS (both kp61 failures hit the round-2
   taught `option-field-fill` class — the beat kp61 lacks), against gift-card PASS→FAIL and
   dead-man-switch PASS→FAIL (both new classes). The taught class disappeared in kp86 as
   intended; but since both kp61 failures also carried untaught defects (rental: wrong-module
   import, string abort codes, destructure-ignore, implicit field copy; wager: missing
   `sui::event` import), the flips are consistent with round 2's beats, not proof of them.

## Failure detail (every failing row; subsequent-error census, all `error[` lines classified)

| task/arm | errors in log | root cause | class |
|---|---|---|---|
| wager-arbiter/base | E03003 ×2, E03006 ×11, E01003 ×2 | `use sui::coin::{Coin, self}` — lowercase `self` in group import (E03003), leaving `coin::`/`balance::` unresolved (all 11 E03006 are downstream of this one defect); plus `struct WagerCap has key` without `public` (E01003) | **round-1 taught `use-self` class** + **original `visibility-modifiers` class** — both fired only in the no-pack arm |
| rental-agreement/kp61 | E03002 ×1, E04035 ×7, E05001 ×10 | `use sui::option;` (Option lives in `std::option`); `assert!(cond, "string")` — string literal as abort code; the 10 E05001 split three ways: ×2 `Option<Coin<SUI>>` field overwrite ("Invalid mutation. Mutation requires the 'drop' ability"), ×6 `deposit: _`-style unpacking of non-`drop` fields ("Cannot ignore values without the 'drop' ability"), ×2 `let item = agreement.item` ("Invalid implicit copy of field" — moving a field out of a borrowed generic struct) | wrong-module import (new); assert-abort-code (new); **round-2 taught `option-field-fill` class ×2 — the beat kp61 lacks; kp86 passed this task**; **destructure-ignore sibling ×6** (already in the round-2 remeasure ledger; 6 fresh hits here); implicit-field-copy ×2 (new) |
| wager-arbiter/kp61 | E03006 ×3, E05001 ×1 | `event::emit(...)` with no `use sui::event` ("Could not resolve the name 'event'"); `wager.opponent_stake = option::some(stake)` | missing-module-import (new); **round-2 taught `option-field-fill` class again — kp86 passed this task** |
| subscription-service/kp61 | E03003 ×1, E03006 ×4 | `use sui::coin::{Self, Coin, SUI}` — `SUI` is not in `sui::coin` (it is `sui::sui::SUI`); the E03006s are downstream uses | SUI-import-path (new) |
| subscription-service/kp86 | E03006 ×14 | `use sui::table::{Table}` / `use sui::balance::{Balance}` / `use sui::coin::{Coin}` — only the *types* imported, then `table::new`, `balance::zero`, `coin::split`, `table::contains` called by module path ("Could not resolve the name 'table'/'balance'/'coin'") | missing-module-import (new — the `{Self, Type}` sibling of the taught `use-self` beat: omitting `Self` entirely instead of writing it lowercase) |
| gift-card/kp86 | E03003 ×1, E03006 ×6 | two independent import defects in `use sui::coin::{Coin, SUI}`: `SUI` is not in `sui::coin` (E03003, plus ×3 downstream E03006 on `SUI` uses), and `Self` is not bound, so `coin::` module-path calls fail (×3 E03006 "Could not resolve the name 'coin'") | SUI-import-path (new) + missing-module-import (new) |
| dead-man-switch/kp86 | E04023 ×5 | `clock.epoch()` — `sui::clock::Clock` has no `epoch` method (`timestamp_ms` only; epochs come from `ctx.epoch()`); the task is epoch-denominated and never needed Clock | clock-epoch-confusion (new) |

**Taught-beat recurrence (pre-registered check, rounds 1 AND 2):** every taught *error class*
hit occurred in an arm whose payload lacked that rule — round-1 `use-self` and the original
`visibility-modifiers` class in **base**; round-2 `option-field-fill` (×3) in **kp61**.
**Zero taught error classes recurred in kp86**; all three kp86 failures are new classes. One
qualifier that cuts the other way: the missing-module-import failures (subscription/kp86,
gift-card/kp86) produce an *untaught* error class, but the loaded `use-self` claims literally
show the correct `{Self, Type}` form that would have prevented them — by the project's round-1
vocabulary this is adjacent to "a loaded rule ignored", and it is recorded as such rather than
counted as a pure knowledge gap.

## Why did the pack arms lose to base? (observation, not a measured claim)

Per-task API-surface counts on the failing tasks show the pack-loaded answers reaching for
richer Sui API surface than the base answers for the same tasks:

- subscription-service: kp86 used `Table` (8 module-path call sites; failed on its imports) —
  base used a plain approach with no Table and passed clean.
- dead-man-switch: kp86 pulled in `Clock` + events + `Balance` (112 lines; failed on
  `clock.epoch()`) — base used neither, 72 lines, passed.
- wager-arbiter: kp61 added events (157 lines; failed partly on the missing `sui::event`
  import) — kp86, 87 lines without events, passed clean. (Base also failed this task, so it
  is not a pack-arm-only failure; the within-task contrast is still the same shape.)

The pack's claims name these idioms (Table, events, Balance, Clock), and the plausible
mechanism is that the payload prompts more ambitious designs whose extra API surface creates
failure opportunities the base answers never encounter. Scored against all six pack-arm
failing rows: the pattern fits subscription/kp86, dead-man/kp86, and wager/kp61; it does
**not** explain rental/kp61, subscription/kp61, or gift-card/kp86 (plain import-path and
ability defects at ordinary API surface — **gift-card/kp86 is the sharpest counterexample**,
the shortest answer of its row at 55 lines failing on two independent import slips). A
hypothesis fitting 3 of 6 failing pack-arm rows, recorded for round-3 design, not a mechanism
this experiment was designed to test.

## Warning detail

- `Lint W99003` (Coin field where Balance fits): 9 hits — the only warning class in any green
  log (rental base ×2, rental kp86 ×2, dead-man base ×1, dead-man kp61 ×1; 3 more in failing
  logs). It did not reproduce in the round-2 probe but is now the dominant residual lint.
- `Lint W99001` (non-composable transfer): **0 hits in all 18 logs, including base** — the
  round-2 grounding beat targeted it, but with base also at zero, nothing here is attributable
  to the pack.
- `W04039` ×7 (all in rental/kp61, downstream of its errors); `W09002` unused-variable ×21
  (failing logs only).

## Round-3 candidates recorded by this experiment

1. **missing-module-import** — module functions called with only the type imported
   (`use sui::table::{Table}` then `table::new`); 3 tasks (wager/kp61 `event`,
   subscription/kp86 `table`+`balance`+`coin`, gift-card/kp86 `coin`). Sibling of the taught
   `use-self` beat: the fix is the same `{Self, Type}` form; the defect shape (omit vs
   lowercase) is different.
2. **destructure-ignore** — `field: _` unpacking of non-`drop` fields ("Cannot ignore values
   without the 'drop' ability"); ×6 in rental/kp61 here, on top of the round-2 remeasure
   occurrence — the ledger-recorded sibling is now the single most frequent untaught error
   in the combined record.
3. **SUI-import-path** — `SUI` imported from `sui::coin` instead of `sui::sui`; 2 tasks
   (subscription/kp61, gift-card/kp86), plus the same wrong-module habit as rental/kp61's
   `use sui::option`.
4. **clock-epoch-confusion** — `clock.epoch()` invented on `Clock`; epochs are
   `ctx.epoch()`; 1 task ×5 call sites.
5. **assert-abort-code** — string literal as `assert!` abort code (E04035); 1 answer ×7 sites.
6. **implicit-field-copy** — `let x = obj.field` moving a field out of a generic struct
   ("Invalid implicit copy of field"); ×2 in rental/kp61.
7. Carried from the round-2 remeasure ledger: `generic-transfer-key-bound` (E05001, ×2 there).

## Combined record (experiments 1–4)

| | exp 1 (sonnet, representative) | exp 2 (sonnet, harder, pre-reg) | exp 3 (haiku, round-1 delta, pre-reg) | exp 4 (haiku, round-2 delta, pre-reg) |
|---|---|---|---|---|
| compile-pass | base 5/5 = kp 5/5 (ceiling) | base 4/5 = kp 4/5 (tie) | base 2/6, kp47 2/6, **kp61 4/6 → shipped branch 1** | **base 5/6, kp61 3/6, kp86 3/6 → branch 3, no headline; base beat both pack arms** |
| clean-compile | post-hoc only | **kp 3/5 > base 2/5 → shipped branch 2** | 1/6 all arms | base 3/6, kp61 2/6 = kp86 2/6 |

The honest cumulative reading: the pack's held-out wins are exp 2's cleanliness claim (sonnet)
and exp 3's compile-pass doubling (haiku, round-1 delta). Round 2's taught class fired only in
the arm without its beats (3 `option-field-fill` hits, all kp61) and never with them, but the
86-claim pack did not raise — and on this draw sat below base on — overall held-out
compile-pass. The dominant
residual failure mode is no longer stale edition knowledge; it is import-path and API-existence
slips, several of them plausibly *induced* by the pack's own idiom vocabulary. That reframes
round 3: teach the import/API corners the pack's vocabulary invites, or stop growing the pack
and test payload slimming.
