# Experiment 9 — held-out falsification of deepening round 7

**Verdict: ROUND 7 SHIPS (ship-rule branch 1) — kp149 4/6 vs kp134 3/6 compile-pass** (base
anchor 2/6). Secondary (observational once the primary decides): clean-compile kp149 3/6 vs
kp134 2/6 vs base 1/6. n = 6; a +1 margin is the series' narrowest shipping branch-1 —
reported as measured, and the mechanism section below is blunt about how little of the
margin the round-7 beats can claim.

Pre-registered at `5a0f286` before any answer (arms, payload SHAs, frozen 3-branch rule,
dual metric, per-class carrier map, import sweep; six tasks through a two-round pre-freeze
review — round 1 replaced two drafts that restated a beat's own eliciting story and a
round-7 probe fusion, and removed an arm-asymmetric noun). Model: claude-haiku-4-5, all
arms. Gate: pinned `sui 1.74.1-8fc60f1fa966`. Per-run verdicts + import sweep:
[answers/results.txt](answers/results.txt).

## Results

| task | base | kp134 | kp149 |
|---|---|---|---|
| left-luggage | FAIL E03003 — `use sui::coin::{Coin, self}` (lowercase group-`self`, the `use-self` shape unaided) +cascades | **PASS CLEAN** | FAIL Sui E02003 — `init(_witness: OFFICE, …)` in module `luggage_office`: OTW misnamed (rule "named after the module in all uppercase" is loaded verbatim in this arm — **ignored-while-loaded**), plus an independent E06001: the bag is removed and its fields read into the `Forwarded` event but the delivery to the recorded address is never written (the pre-registered mva bait site was never authored; vcp rule loaded — ignored) |
| drying-room | FAIL E01003 ×2 (bare `struct`, edition-2024 visibility) + **E04004 `Table<(u32, u32), Slot>` — the tuple-bleed composite-key shape, unaided** | PASS CLEAN | PASS CLEAN |
| repair-cafe | PASS CLEAN | FAIL E06001 — `option::extract` then event emit; the delivery to the recorded owner never written (vcp rule loaded — ignored) | **PASS CLEAN** |
| barn-dance | FAIL E01003 ×3 (bare `struct`) | PASS WARN1 — stores a named `Couple has copy, drop, store` struct (the tuple-bleed GREEN idiom, on the doc-tier rule alone) | FAIL E04004 ×2 authored sites (+8 cascades; count corrected in review round 1), one rule — `couples: vector<(address, address)>`: **`tuple-bleed`, the round-7 top beat's exact pinned storage shape, firing in the arm that carries the execution-tier beat — first post-teach recurrence, ignored-while-loaded** |
| cheese-cave | PASS WARN2 | FAIL E03003 — `use sui::table::{self, Table}` (lowercase group-`self`; `use-self` application ledger; note `sui::table` itself is CORRECT — `std-table-path` did not fire) | PASS WARN1 |
| community-sauna | FAIL E01002 — `+=` (the taught `compound-assignment` class, unaided) + an invented `coin::burn_for_fees` | FAIL E01002 — `module @0x0::sauna`: the `@`-literal module-declaration shape (**×2 cumulative** with round-6 remeasure brm-3; adjacent to taught `module-address-form`, whose pin is the missing-address message, not this) | **PASS CLEAN** |

## Mechanism analysis (pre-registered, strict experiment-5 standard)

- **The ship-rule margin is NOT carried by round-7 taught-class flips.** The three tasks
  kp149 wins over kp134 (repair-cafe, cheese-cave, community-sauna) all fail in kp134 on
  loaded-rule-application events of OLDER rounds' classes (vcp non-consumption, `use-self`,
  the `@`-literal module shape) — none of the five round-7 classes. Zero round-7
  taught-class recurrence in kp134.
- **Round 7's top class fired in the arm carrying its beat.** barn-dance/kp149 stored
  `vector<(address, address)>` — the exact `tuple-bleed` storage shape whose RED the round-7
  beat pins (message identical modulo identifiers) — while kp134, carrying only the
  doc-tier "(and tuples)" rule, wrote the named-struct GREEN idiom and passed. One draw
  cannot rank tiers, but this is the class's first post-teach recurrence and it lands on
  the application ledger: the execution-tier escalation did not prevent the event that the
  doc-tier arm happened to avoid. The exp-8 steering question (does tuple guidance
  redirect answers?) stays open in both directions.
- **The pack-vs-base signature is intact** (both pack arms, symmetric): base fails on
  classic taught classes — bare-`struct` visibility ×2 tasks, `use-self` ×1,
  `compound-assignment` ×1, and the tuple-bleed composite key ×1 — all absent from BOTH
  pack arms (drying-room: both pack arms keyed the table with a named struct, the GREEN
  idiom, where base wrote `Table<(u32, u32), …>`).
- **`balance-api-on-coin` had live sites and fired nowhere:** four answers across arms
  call `coin::take`/`coin::put`, every receiver correctly `Balance<SUI>` — including
  kp134's. The class's convenience surface was exercised this draw (round 7's probe saw it
  avoided); zero firings in any arm.
- **A cross-arm application sub-shape appeared twice:** left-luggage/kp149 and
  repair-cafe/kp134 both removed/extracted the custody object, emitted the event reading
  its fields, and never wrote the delivery — E06001 with the vcp rule loaded in both arms.
  Recorded on the application ledger as sub-shape `event-emission-not-consumption` ×2
  (round-8 scope may judge whether "emitting an event does not consume the object" is a
  distinct teachable rule or a vcp restatement — the strict standard here scores both
  events ignored-while-loaded).
- **Other ledger events:** `otw-misnaming` ignored-while-loaded ×1 (left-luggage/kp149;
  the naming rule is verbatim in the payload); `@`-literal module declaration ×2 cumulative
  (community-sauna/kp134 + round-6 brm-3) — an untaught sub-shape (the taught
  `module-address-form` pin is a different message), now at the promotion threshold's
  edge; `std-option-path`, `std-table-path`, `moved-value-arg-order` (E06002),
  `branch-type-mismatch` (E04007), `underscore-discard`: **zero events in any arm** —
  though note the mva carriers were under-exercised (left-luggage/kp149 omitted the
  delivery leg entirely; the bait site was never written).
- **Import sweep (point #5): 0 fails — 12/12 CORRECT** across the four SUI carriers × 3
  arms (base correct unaided in all four, consistent with exp-8's base-correct draw).
  Third consecutive clean replication for the pack arms (rounds 6, 7, this).

## Reading

The frozen rule ships round 7 on the primary metric, and the honest gloss is: the margin
this draw is application-variance-shaped, not teaching-shaped. What the round-7 delta
demonstrably did NOT do is stop its own top class from firing once in the deepened arm —
`tuple-bleed` joins the ignored-while-loaded ledger at execution tier on its first held-out
test, the sharpest data point this experiment produced. Meanwhile the older beats' value
shows where it always has: the base arm keeps failing on classes no pack arm fails on. n =
6 everywhere; absolute numbers not cross-comparable across experiments.

**Round-8 ledger updates from this draw:** `tuple-bleed` post-teach recurrence ×1
(application ledger, execution tier); `event-emission-not-consumption` ×2 (vcp application
sub-shape, cross-arm); `otw-misnaming` ×1 (application); `@`-literal module declaration ×2
cumulative (untaught — promotion candidate); `use-self` +1 application event (~13 —
cheese-cave/kp134; left-luggage/base's `{Coin, self}` is the same SHAPE but unaided, so it
is not an ignored-rule event and is recorded here as base composition only; convention
point settled in review round 1); base-only: bare-`struct` visibility ×2,
`compound-assignment` ×1, tuple composite key ×1.
