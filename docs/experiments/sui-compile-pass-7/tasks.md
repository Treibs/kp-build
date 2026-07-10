# Experiment 7 — held-out falsification of deepening round 5 (pre-registered)

**This file is committed BEFORE any answer is collected.** Operator instruction 2026-07-10:
"run the tier-2 falsification for round 5."

## Question and arms

Does deepening round 5 (pack 110 → 128 claims, PR #25 — six beats including the
experiment-derived `sui-import`) improve held-out contract authoring on the pinned toolchain?
Three arms:

- **base** — task text + the standard instruction only. Contextual anchor; no ship-rule
  weight.
- **kp110** — the pre-round-5 payload, byte-identical to the experiment-6/elicitation/round-5
  arm: **51,799 bytes, sha256
  `92756d2d7532318ffd16be0b87794141c185336ce6c324a1e0937b6602cfb812`**.
- **kp128** — the post-round-5 payload from master `ea3e3af` (assembly rule unchanged;
  verified byte-identical to the round-5 remeasure payload since the post-teach commits
  touched no claim input): **55,374 bytes, sha256
  `d9e414e76b9b3033424546e44991b68ad7ba83cb3e648ae061ed8723b8757245`**.

**The headline comparison is kp128 vs kp110.** Model, all arms: `claude-haiku-4-5`. Fresh
context per task per arm; headless, no tools; neutral scratch directory; the standard
instruction, prompt assembly, mechanical extraction, arm-neutral scaffold repair, and pinned
`sui 1.74.1-8fc60f1fa966` gate — all unchanged from experiments 3–6.

## Metrics and ship rule (frozen)

- **Primary: compile-pass.** **Secondary: zero-warning clean-compile.**
- **Branch 1** — kp128 > kp110 on the primary → round 5 improves held-out compile-pass.
- **Branch 2** — primary tied AND kp128 > kp110 on the secondary → cleanliness headline only.
- **Branch 3** — anything else → no headline; composition observational.
- n = 6; denominators everywhere; absolute numbers not cross-comparable between experiments.
- **Mechanism analysis (pre-registered, strict exp-5 recurrence standard).** Round-5 taught
  classes of special interest: SUI-import (either shape), `id_to_address`-arg, E06001
  consumption shapes (branch-path and drained-vector), `object::id`-on-UID, unannotated
  empty vectors.
- **Import sweep (observational):** the committed checker
  (`docs/experiments/sui-import-elicitation/check_import.py`) runs on every answer —
  replication data point #3 for the elicitation record.

## Tasks

Six contract-authoring tasks, incidental-multi-concept in the recent style. Held-out audit
run before this freeze against the **137** prior tasks (60 round-1..4 probes + 15 round-5
probes + 34 experiment tasks + 6 salience + 6 sheet-confirm + 16 elicitation) and the 45
fixture zones at `ea3e3af` — **with the standing pre-freeze adversarial reviewer pass**; its
findings and the applied actions are recorded below, before any answer was collected.

1. **escape-room** — An escape-room booking desk: teams book a named room for a future epoch
   by paying the fee in SUI. A team that finishes under the room's target time (the operator
   records finish times) gets half the fee back (rounded down; the kept half pools); an
   over-target finish forfeits the whole fee to the pool; a booked slot whose epoch passes
   unplayed forfeits likewise. Views: a room's bookings and the pool total.
2. **stall-rental** — A farmers-market stall board: vendors rent numbered stalls for the
   current market day (one epoch) with the rent plus a cleaning deposit in SUI. After the
   market, the inspector (capability) marks each stall clean or dirty: clean vendors reclaim
   their deposit, dirty stalls forfeit it to the market's pool. Rent always pools. Views:
   stalls rented today and the pool total.
3. **community-fridge** — A community fridge: donors stock `Meal` objects (label + the epoch
   stocked); anyone takes at most one meal per epoch. At any time the coordinator
   (capability) runs a spoilage sweep: every meal stocked BEFORE the current epoch is
   discarded (each discard emits an event recording that meal object's identity and label)
   while meals stocked this epoch stay in the fridge — an in-place cull, not a full clear.
4. **service-log** — An appliance repair shop: a shared service history, keyed by each
   appliance's on-chain identity, records every service visit (epoch + note) the mechanic
   (capability) logs against the owner's presented appliance. Views: an appliance's visit
   count and the shop's total visits. When an owner scraps their appliance (destroys it), a
   `Scrapped` event carries its identity and its final visit count, and the history entry is
   removed.
5. **card-merge** — A loyalty desk: shoppers hold `PointsCard` objects (points balance). The
   desk (capability) consolidates two cards into one: both old cards are retired, a single
   new card carrying the summed points goes to the shopper, and a `Merged` event records both
   retired cards' identities, the successor's identity, and the combined balance.
6. **charging-station** — An EV charging post: a driver plugs in escrowing an upfront SUI
   payment (any positive amount); on unplug the station keeps cost-per-epoch × epochs
   connected and returns the unused remainder to the driver — a session whose measured cost
   equals or exceeds the escrow keeps it all and must still settle cleanly (zero-coin
   return path). Proceeds pool for the operator.

## Pre-freeze audit review (ran before this freeze; the standing step)

The reviewer pass on the first draft returned **REVISE** with the series' most consequential
catch yet: three of six drafts — the three carrying round-5's taught classes — were
restatement-tier collisions with **round-5's own probe tasks** (bike-share ≈ uid-2
museum-loan point-for-point; report-card ≈ oid-1/uid-1 succession schema verbatim;
community-fridge's clear ≈ vde-3 drain-and-destroy-with-events wrapped in vde-1's daily
reset). Since kp128 was taught from those probes, a kp128 win on them would have measured
story-replay, not generalization. Actions applied before this freeze:

- **bike-share → replaced by service-log** (identity-keyed history with NO custody and NO
  deposit; scrap event carries identity + final count — disclosed adjacent to exp-6
  carbon-retire's destroy+event at the weaker tier: no receipt object, no running total;
  second-pass disclosures: ≈ round-5 uid-3 star provenance — the identity-keyed-table spine
  any fair uid-class task must carry; differs: cap-gated logging vs open gifting, epoch+note
  payload, no transfer chain, no fee, terminal destroy with entry removal — and ≈ round-5
  uid-2 at the negation level, entry-removal-at-lifecycle-end on destroy rather than return).
- **report-card → replaced by card-merge** (merge-two-into-one succession: both retired
  identities + successor in one event — a succession shape no probe or fixture pins;
  disclosed adjacent to exp-3 loyalty-points at the payload level, and — second-pass
  disclosure — to exp-4 crafting-forge at the mechanic level: consume-two-produce-one with
  an aggregate; differs: homogeneous type, cap gating, the identity-bearing Merged event,
  delivery to the shopper).
- **community-fridge → reworked to a selective cull** (destroy only meals stocked before the
  current epoch, retain the rest — an in-place filter of non-`drop` objects, a consumption
  shape no vde probe or fixture exercises; the take-≤1-per-epoch path is disclosed adjacent
  to round-2 modform-1's rate limiter; second-pass disclosure: the sweep's retained skeleton
  — cap-gated destroy with a per-object event — is round-5 vde-3's run_show, and the event
  payload matches round-4 oid-3's identity+attribute schema; differs: retained-subset
  partition vs consume-all).
- **Differs-clauses added for the three keepers:** escape-room ≈ round-3 import-2 deposit
  waitlist (refund-or-forfeit adjudication; fresh: future-epoch booking, recorded finish
  times, HALF-refund partial consumption) and ≈ the value-consumption-paths fixture's cover
  story (performance-threshold deciding a payment's fate — story-level only, mechanics and
  code shapes differ) and dodges the tournament-prize spine (no enrollment threshold, no
  run-or-cancel); stall-rental ≈ exp-4 rental-agreement (deposit split; fresh: NO item
  custody, inspector-verdict trigger) and ≈ elicitation I-2 community-garden (numbered-slot
  claim + pooled fee; fresh: deposit + inspection) and ≈ import-2 (adjudicated forfeit);
  charging-station ≈ round-3 import-1 parking meter / round-5 vcp-2 garage / elicitation I-3
  pet-daycare (the rate×epochs settlement family, fourth lap — fresh: escrow-at-plug-in
  settled by measured epochs, and the zero-coin-return edge no prior task pins).
- **Composition note:** three of six tasks remain in the settlement family by design — they
  are the value-consumption class's carriers (three carriers per class, the probe convention);
  the other three are non-settlement.
- Ambiguities tightened arm-neutrally (odd-fee half rounded down; forfeits pool; any positive
  escrow). Reserved-word check trivially satisfied (no pinned module names; `Meal`, `Bike`→
  gone, `PointsCard`, `Scrapped`, `Merged` not reserved). Denominator 137 verified by the
  reviewer (60+15+34+6+6+16) along with the 45 fixture zones and both payload SHAs.
- **Second pass on the replacements** ran before the freeze (round-5 precedent) — see below.

## Layout

`answers/<task>/{base,kp110,kp128}.{answer,-src.move,-pkg/,buildlog,result,import}`; summary
+ import sweep in `answers/results.txt`; verdict in `README.md` (post-gate).
