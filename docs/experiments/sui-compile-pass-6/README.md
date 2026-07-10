# Experiment 6 — held-out falsification of deepening round 4

**Verdict: NO HEADLINE (ship-rule branch 3).** kp110 tied kp98 on the primary (compile-pass
**2/6 = 2/6**) and on the secondary (clean-compile **2/6 = 2/6**), and the base arm beat both
pack arms on the primary (**3/6**) — the second experiment in the series where base wins the
draw (experiment 4 was the first). Round 4's held-out delta does not ship a headline.

Pre-registered at `7cf9e58` before any answer (arms, payload SHAs, six tasks with the
held-out audit, dual metric, 3-branch rule — see [tasks.md](tasks.md)). Model:
claude-haiku-4-5, all arms. Gate: pinned `sui 1.74.1-8fc60f1fa966`. Full per-run verdicts in
[answers/results.txt](answers/results.txt); every failing log root-caused below.

## Results

| task | base | kp98 | kp110 |
|---|---|---|---|
| book-club | FAIL E01003 ×3 + E05001 ×1 (`struct` without `public` — the original edition class — plus one bound-and-dropped split; corrected count, review round 1) | FAIL E06001 (`let _balance = balance::split(...)` — split proceeds never consumed) | FAIL E03002 +15 cascades (`use std::table` — wrong path for `sui::table`) |
| carbon-retire | PASS CLEAN | FAIL E05001 (`object::id(&id)` on a `UID` — `'key' constraint not satisfied`; the uid-vs-ID ledger family) | FAIL E04007 (`object::id_to_address` fed a non-`ID` argument) |
| passport-stamps | PASS WARN2 | PASS CLEAN | PASS CLEAN |
| water-rights | PASS WARN1 | PASS CLEAN | PASS CLEAN |
| arcade-crown | FAIL E04024 ×2 (params not `mut` — the class round 3 taught the pack, firing untaught in the pack-less arm) | FAIL E03003 +cascades (`use sui::coin::{...SUI...}` — **the SUI-import class, ×5 cumulative**) | FAIL E06001 ×2 (`payment: Coin<SUI>` never consumed — once in `init_champion`, which has no branches at all, and once in `play`, where **neither** branch of the high-score `if` consumes it; correction, review round 1: the first version said "not consumed on the losing branch") |
| digest-notary | FAIL E03006 + **E01002 `+=`** | FAIL **E01002 `+=`** (`notary.total_digests += 1;` — exact pinned message `Unexpected '='`) + E04007 (`coin::put` on a `Coin` field) | FAIL E06001 (`mut payment` "might still contain a value" — conditional path) |

- **Compile-pass: base 3/6, kp98 2/6, kp110 2/6** → primary tied, branch 1 does not fire.
- **Clean-compile: base 1/6 (carbon-retire), kp98 2/6, kp110 2/6** (both pack arms:
  passport-stamps + water-rights) → secondary tied, branch 2 does not fire. **Branch 3.**

## Mechanism analysis (pre-registered, strict experiment-5 standard)

- **Round-4 taught-class recurrence in kp110: ZERO.** No E07001, no `+=`/paren-free `while`,
  no `std::mem` anywhere in the kp110 logs.
- **The round-4 taught `compound-assignment` class fired in BOTH arms that lack the beat:**
  digest-notary/base and digest-notary/kp98 each wrote `+= 1` (exact pinned message,
  `Unexpected '='`), and the kp110 answer on the same task wrote the taught written-out form.
  The same compositional signature experiment 4 recorded for round-2's beats: the taught
  class stops appearing in the arm that carries it, but the pack arm loses the gains to
  *other* classes, so the primary does not move.
- **The SUI-import ledger class hit kp98** (arcade-crown, `Unbound member 'SUI' in module
  'sui::coin'` — **×5 cumulative**, still the top uncovered class); both kp110 answers checked
  for the corner import `use sui::sui::SUI` correctly. Observational: with round 4's probe
  recording this territory clean under targeted elicitation, the class keeps firing only in
  held-out draws — elicitation shape, not coverage, remains the open question.
- **kp110's failure signature is one untaught discipline: unconsumed `Coin` parameters**
  (E06001) — **3 sites across 2 answers** in one draw (corrected description, review round 1:
  the first version said "×3 answers" and framed all three as conditional): arcade-crown's
  `init_champion` never consumes `payment` (no branches involved), arcade-crown's `play`
  consumes it on *neither* branch of its `if`, and digest-notary's is the genuinely
  conditional shape (consumed only when residual value > 0 — "might still contain a value").
  One unifying fix — a non-`drop` parameter must be consumed on **every** path, including the
  no-op path — distinct from the promoted `vector-destroy-empty` rule. **Round-5 candidate
  `value-consumption-paths`, promoted on frequency (3 sites / 2 answers).** kp98's book-club
  E06001 (`let _balance = balance::split(...)` bound-and-dropped) is the same error code with
  a different fix (consume the split proceeds) — counted separately, ×1. Plus two ×1 classes
  for the ledger: `std-table-path` (`use std::table`) and `id-to-address-arg` (E04007).
- **kp98's uid-vs-ID family event** (carbon-retire, `object::id(&id)` on a raw `UID`): the
  round-4 territory-5 corner firing held-out in the pre-round-4 arm — ×2 cumulative for
  uid-vs-ID (sheet-confirm + here).

## Reading

Round 4 behaves like rounds 2 and 3 before it: the taught classes demonstrably stop firing in
the arm that carries them, and the pack arm's failures migrate to adjacent untaught classes —
value-discipline shapes this draw — leaving the primary flat. Three consecutive no-headline
deepening deltas (rounds 2, 3, 4) against one shipped headline (round 1) is now the recorded
shape of this pack's deepening curve at n=6 per draw; the standing candidates for what moves
the number are (a) the value-consumption-paths family (3 sites / 2 answers in one draw — the largest
single-draw untaught cluster since the E05001 family), and (b) the elicitation question on
SUI-import. Both are round-5 material; nothing here revises round 4's fixtures, which all
still gate green.

Base beating both pack arms (3/6 vs 2/6) is reported with the same prominence as in
experiment 4 and remains within draw variance at n=6 (base's three passes carry 3 warnings
across 2 tasks; the pack arms' passes are clean).


## Audit erratum (review round 1)

The frozen tasks.md's held-out audit disclosed one adjacency (digest-notary) and missed two
that the branch review surfaced — on exactly the two tasks both pack arms passed:
**water-rights** shares experiment 5 allowance-vault's per-epoch capped-draw mechanic, and
**book-club** shares experiment 4 subscription-service's paid-through-epoch dues shape. Per
the standing erratum rule the frozen file is untouched; the adjacencies are disclosed here.
No arm's prompt carries any prior experiment text, and both adjacent tasks were passed (or
failed) identically enough to leave the tie verdict unaffected — what this corrects is the
audit's completeness claim, and the round-5 protocol inherits the stricter check.
