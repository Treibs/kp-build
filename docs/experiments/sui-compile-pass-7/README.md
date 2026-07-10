# Experiment 7 — held-out falsification of deepening round 5

**Verdict: ROUND 5 SHIPS (ship-rule branch 1) — kp128 5/6 vs kp110 2/6 compile-pass** (base
anchor 2/6), the largest pack-delta margin in the series and the sui pack's first branch-1
since experiment 3. Secondary (observational once the primary decides): clean-compile kp128
4/6 vs kp110 1/6 vs base 1/6. n = 6; the +3 margin is the series' widest but still small-n —
reported as measured, not extrapolated.

Pre-registered at `850e895` before any answer (arms, payload SHAs, dual metric, frozen
3-branch rule, import sweep; six tasks that survived TWO pre-freeze reviewer passes — the
first replaced three drafts that restated round-5's own probe tasks, closing the story-replay
channel that would have let kp128 win by reciting its teaching material; the second added
three differs-clauses). Model: claude-haiku-4-5, all arms. Gate: pinned
`sui 1.74.1-8fc60f1fa966`. Per-run verdicts + import sweep:
[answers/results.txt](answers/results.txt).

## Results

| task | base | kp110 | kp128 |
|---|---|---|---|
| escape-room | FAIL E03006 (`Coin` instantiated directly — "can only be instantiated within its defining module") | FAIL E03003 — `use sui::coin::{Self, Coin, SUI}`: **the round-5 taught `sui-import` class, exact pinned message, in the arm without the beat**; the import sweep flags the same run | **PASS CLEAN** |
| stall-rental | FAIL E05001 ×2 (+2 cascades) | PASS WARN2 | FAIL E03002 — `use sui::option`: `Option` lives in `std::option` (untaught `std-option-path`, ×2 cumulative with experiment 4's rental answer) |
| community-fridge | FAIL E05001 ×2 (+2) | FAIL E01002 "Expected ';'" — round-2 taught `block-statement-semicolon` **ignored while loaded** | **PASS CLEAN** |
| service-log | FAIL E03002 — `use sui::vector` (std/sui namespace confusion, the round-5 territory-4 family) + 6 cascades | PASS CLEAN | **PASS CLEAN** |
| card-merge | PASS CLEAN | FAIL E05001 — `object::id(&card1.id)` on a raw `UID`: **the round-5 taught `uid-vs-id` class in the arm without the beat** | **PASS CLEAN** |
| charging-station | PASS WARN1 | FAIL E03006 — `coin::zero(ctx)` with only `use sui::coin::Coin` bound: round-3 taught `missing-module-import` **ignored while loaded** (+8 cascades) | PASS WARN2 |

## Mechanism analysis (pre-registered, strict experiment-5 standard)

- **Two round-5 taught classes fired in the beat-less kp110 arm and nowhere in kp128:**
  `sui-import` (escape-room, exact pinned message; the import sweep independently flags it —
  replication data point #3: kp110 1/3 coin-bearing fail, kp128 0/3, base 0/3) and
  `uid-vs-id` (card-merge, the exact `object::id`-on-UID shape). Both tasks **pass clean
  under kp128**. This is the compositional signature every round has shown — but for the
  first time since experiment 3, the primary moved with it.
- **Zero round-5 taught-class recurrence in kp128** (grep across all six kp128 buildlogs for
  every taught fragment: empty).
- **kp128's single failure is untaught:** `use sui::option` — the reverse-direction namespace
  confusion (`std` module imported from `sui`), sibling of round-5's territory-4 but a
  different pinned path; ×2 cumulative (experiment 4 rental/kp61) → **round-6 candidate
  `std-option-path`, promoted on recurrence.**
- **Two loaded-rule-ignored events in kp110** (block-statement-semicolon, missing-module-
  import) — the standing phenomenon, present as always; kp128's draw happened not to ignore
  any loaded rule, which at n=6 is within the draw variance the round-5 remeasure documented
  (rule application remains draw-variable; this experiment does not claim otherwise).
- **Base-arm composition:** the classic unaided classes (E05001 ability discipline ×2 tasks,
  direct `Coin` instantiation, `use sui::vector`) — consistent with the series.

## Reading

Round 5 is the first deepening round whose tier-2 delta ships since round 1 — and it is also
the round whose beats were chosen by measured held-out frequency (two beats taught from
held-out REDs after clean probes) and whose probe design came from a mechanism experiment.
The obvious next question — was the difference the *selection method* rather than the round
size — is a one-experiment question (a round-6 designed the old way would test it) and is
recorded, not answered here. The import-sweep replication point (kp110 1/3, third data
point) keeps the elicitation mechanism unestablished; what is now measured twice is the
*beat's* effect, which is the thing the pack can actually ship.

Absolute numbers are not comparable across experiments (draw difficulty varies); within this
draw, both anchor arms tied at 2/6 while kp128 reached 5/6, and the two tasks that flipped
against kp110's taught-class failures are the two whose classes round 5 taught. Round-6
ledger: `std-option-path` (×2, promoted), plus the round-5 carried singles
(`split-by-value` + split-returns-pair, `branch-type-mismatch`, `moved-value-arg-order`).
