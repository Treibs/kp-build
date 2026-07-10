# Round-6 tier-1 remeasure — sui-move

*Tier-1 numbers are tainted — these tasks selected the beats. Trend signal only; headline
numbers come from pre-registered held-out falsification (tier 2).*

Exactly the eight failed probe runs, fresh answers, deepened **134-claim** payload (56,464
bytes, sha256 `9d4e6fe8a69abf15…`, assembled from teach commit `2911da4` by the standard
rule). Artifacts in `remeasure/`; every attribution grep-verified.

## Flip table

| task / model | probe | remeasure | attribution (grep-verified) |
|---|---|---|---|
| opt-1 / haiku | FAIL E03003 (use-self) | **FAIL E03002** | the probe's `self` casing is gone, but the residual is `use sui::option` — **the `std-option-path` class this round's frozen design declined to teach, firing in its own remeasure** (×3 cumulative) |
| opt-3 / haiku | FAIL E03003 (use-self) | **FAIL E03003** | `use std::option::{self, …}` — `use-self` ignored AGAIN (series event ~9) |
| brm-1 / haiku | FAIL E03006 (missing-module-import ignored) | **PASS WARN1** | no round-6 beat involved; the previously ignored rule applied this draw |
| brm-2 / haiku | FAIL E04004 (reference-type-argument) | **FAIL E03003** | **corner avoided, no credit** (correction, review round 1: the first version claimed the taught `Option<ID>` fix was applied "grep-confirmed" — the committed source contains neither `Option<ID>` nor `object::id`; it takes `Option<Stamp>` by value, a different design). The taught class does not recur. Residual: `use sui::coin::{self, …}` — `use-self` ignored (event ~10) |
| brm-3 / haiku | FAIL E04024 (param-mut destructure, ignored) | **FAIL E01002** | `module @0x1::grading {` — an `@`-literal module declaration, a new *shape* under the taught `module-address-form` class (loaded-rule-adjacent) |
| csp-2 / haiku | FAIL E04024 (param-mut, ignored) | **PASS CLEAN** | no round-6 beat involved; rule applied this draw |
| mva-3 / haiku | FAIL E04007 (contains-by-value) | **FAIL E06002** | **corner avoided, no credit** (correction, review round 1: the first version claimed the taught contains fix was applied — the committed source switched containers to `Table<address,bool>` and passes the key by value; the earlier grep matched the *container* borrow, not the element). The taught class does not recur. Residual: `transfer::public_transfer(letter, letter.sender)` — **the `moved-value-arg-order` class this round declined to teach, firing in its own remeasure** (×2 → promoted) |
| ctx-3 / haiku | FAIL E03003 (use-self) | **FAIL E03003** | `use sui::coin::{Coin, self}` — `use-self` ignored (event ~11) |

## Reading (trend only — see taint label above)

- **Flips: 2/8 — the weakest remeasure of the six sui rounds** (r1 4/8, r2 6/8, r3 1/6,
  r4 4/5, r5 5/8). Zero round-6 taught-class recurrence — but taught-fix visibility is
  **0/2**, not 2/2 as first written (review round 1's catch, the same defect family as
  rounds 4 and 5's corrections): both runs avoided their corners by redesign rather than
  applying the taught shapes. The beats' effect is therefore unmeasured even at tier-1;
  the residuals belong to classes the round declined to teach.
- **The old-way design's cost, measured same-day:** the two strongest ledger classes it
  declined to teach (`std-option-path` ×2 held-out, `moved-value-arg-order` ×1 carried) BOTH
  fired in this remeasure — now ×3 and ×2 respectively. The controlled comparison is intact
  (that was the point), and its price is now quantified on this round's own runs.
- **`use-self` ignored three more times** (~events 9–11; probe+remeasure of this round alone
  account for six). The rule-application constraint dominates every surface the pack has.
- **Round-7 ledger:** `std-option-path` (×3), `moved-value-arg-order` (×2), the
  `@`-literal module-declaration shape (×1, adjacent), plus the carried singles.
- **Post-measure claim freeze:** claims frozen at `2911da4`; nothing here altered a claim.
  Round 6's held-out effect is unmeasured until experiment 8 — which now reads as the formal
  comparison of the two selection methods, with this remeasure as its foreshadowing.
