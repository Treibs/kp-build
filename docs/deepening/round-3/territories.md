# Round-3 territories — sui-move

**Seeding rule:** round 3 is gap-seeded from the recorded falsification/remeasure ledgers, same
as round 2 — every territory below traces to a *measured* failure in `docs/deepening/round-2/`
or `docs/experiments/sui-compile-pass-4/`, not to encyclopedic coverage instinct.

**Gate-1 approval:** operator blanket authorization 2026-07-08 ("continue with merging 14 and
all the way through a next round, in whatever order and following whatever process you wish,
just make sure to ralph loop review when you hit milestones"). The territory list is the
recorded round-3 candidate list from the exp-4 README plus the two carried round-2 remeasure
deferrals; exclusions below.

## Proposed and approved territories

| # | territory | seed (recorded evidence) | why parametric knowledge is suspect |
|---|---|---|---|
| 1 | `missing-module-import` — module functions called with the module alias never bound (`use sui::table::{Table}` then `table::new`, or no `use sui::event` at all before `event::emit`) | exp-4: 3 tasks (wager/kp61, subscription/kp86 ×14 errors, gift-card/kp86); untaught error shape E03006 "Could not resolve the name '<module>'" | Rust's paths resolve `crate::mod::fn` without a per-module import; Move 2024 requires the alias bound. Sibling of the taught round-1 `use-self` beat (lowercase-self shape) — the *omission* shape has no beat |
| 2 | `destructure-ignore` — `field: _` unpacking of non-`drop` fields ("Cannot ignore values without the 'drop' ability") | exp-4 rental/kp61 ×6; round-2 remeasure optiondrop-3; first recorded as the exp-3 sibling | Rust `_` drops any value; Move requires explicit consumption of non-`drop` values. Ledger-recorded in two rounds, never taught — now the most frequent untaught error in the combined record |
| 3 | `wrong-module-import` — well-known types imported from the wrong module (`use sui::coin::{Coin, SUI}`; `use sui::option`) | exp-4: subscription/kp61, gift-card/kp86 (`SUI` is `sui::sui::SUI`), rental/kp61 (`Option` is `std::option`) | The types are used *through* `sui::coin`/everywhere, so the model's prior for "where it lives" is diffuse; 3 answers hit it in one experiment |
| 4 | `generic-transfer-key-bound` — `transfer::public_transfer(x)` where `x: T` with only `T: store` (needs `T: key + store`) | round-2 remeasure optiondrop-1 (×2 across probe+remeasure); deferred at round-2 triage with 1 answer, promoted after the 2nd occurrence | The `store`-implies-transferable intuition is wrong: `key` is what makes an object; a bare `T: store` can only live inside other objects |
| 5 | `clock-epoch-confusion` — `clock.epoch()` invented on `sui::clock::Clock` (E04023); epochs come from `ctx.epoch()`, Clock carries `timestamp_ms` only | exp-4 dead-man-switch/kp86 ×5 call sites | Two time APIs with disjoint units invite blending; the pack teaches `clock.timestamp_ms()` but nothing pins the epoch/Clock boundary |

## Deliberately excluded (with reasons)

- **`assert-abort-code`** (E04035, string literal as abort code — exp-4 rental/kp61 ×7): one
  answer only so far; same deferral rule that held `generic-transfer-key-bound` back at round-2
  triage. Promoted if it recurs in this round's probe.
- **`implicit-field-copy`** (E05001 "Invalid implicit copy of field" — exp-4 rental/kp61 ×2):
  one answer; same rule.
- **W99003 Balance-vs-Coin grounding beat:** now the dominant residual lint (9 exp-4 hits), but
  exp-4 also measured W99001 — the round-2 grounding-only lint beat — at 0/18 *including base*:
  grounding-only warning beats have shown no attributable held-out effect. Not worth a third
  data point before rethinking the warning-tier mechanism.
- **Payload-slimming experiment** (the exp-4 README's alternative reading — base 5/6 beat both
  pack arms; the 86-claim payload may induce failures via idiom ambition): this is a *tier-2
  experiment design question*, not a deepening beat; recorded here as the leading candidate for
  the next pre-registered experiment rather than smuggled into a round.

## Probe shape

15 fresh authoring tasks (3 per territory), dual model (`claude-haiku-4-5` primary,
`claude-sonnet-4-6` secondary), **current 86-claim pack loaded** in every run (this is
deepening — residual gaps are what matter), pinned `sui 1.74.1-8fc60f1fa966` gate. Task
freshness audited against: all 30 round-1/round-2 probe tasks, exp-1/2/3/4 task lists, and the
31 fixture zones. Mechanical repair rule pre-declared in `probe/README.md` before any answer.
