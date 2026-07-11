# Round-7 probe — protocol and layout

**Arm: current pack loaded.** This file is written and committed **before any answer is
collected.**

## Protocol

- 15 incidental-shaped tasks (3 per territory — [`../territories.md`](../territories.md)),
  `<territory>-<k>/task.md`. Dual model, fresh context, pinned IDs (`claude-haiku-4-5`
  primary, `claude-sonnet-4-6` secondary). Prompt = task text + the standard instruction +
  `--- Reference pack (verified) ---` + the kp134 payload (56,464 bytes, sha
  `9d4e6fe8a69abf15453a940455ce0616f78beea84dfbf368bbf3905859c89bff` — byte-identical to
  exp-8's pinned artifact; sui claims unchanged since round-6 teach).
- **Mechanical repair rule (arm-neutral, pre-declared):** the answer is saved unchanged and
  gated as ONE package; the scaffold (Move.toml manifest, named-address binding) is derived
  mechanically from the answer's own module declarations; no source edit of any kind.
  Multi-module answers stay in one gated package so a failure in ANY module is observed.
- Pinned `sui 1.74.1-8fc60f1fa966` gate (env-injected binary path; placeholder here per the
  standing leak rule), committed import checker
  (`docs/experiments/sui-import-elicitation/check_import.py`) on every answer — the sweep
  is replication measurement for the elicitation experiment's finding. Buildlogs
  ANSI-stripped + home-redacted; verdict format and layout as prior rounds; summary + import
  sweep in `results.txt`.
- **Frequency selection (binding, per territories.md):** beats this round come from the
  ledger's recorded evidence; the probe adds fresh elicitation and RED material but a clean
  territory does NOT decline its beat.

## Pre-freeze audit review (ran before this freeze; the standing step)

The reviewer pass on the draft returned **REVISE**: 3 REPLACE, 4 story re-skins (one
optional, taken), one denominator unit error, and eight required disclosures. All applied
before this freeze:

- **Replaced:** orchard plots (restated elicitation I-2 community-garden — numbered plots,
  grant/surrender, per-plot harvest logs; also adjacent to exp-7 stall-rental's numbered
  board) → **stp-3 apiary hive stands** (same keyed re-grantable registry elicitor, no SUI);
  gallery wall (triple ground: its swap-in-receive-back mechanic IS the `std-mem-swap`
  fixture's — and swap-focal sop tasks steer the model into the one payload claim that
  names `std::option::swap`, answering the class instead of eliciting it; restated round-2
  optiondrop-1 + round-6 opt-3; thinnest sui:: import crowd) → **sop-2 aquarium tank hall**
  (stock/retire/move between numbered optional tanks, clock-stamped + event — no
  swap-return; recorded design rule: **sop tasks must not make swap focal**); arcade prize
  machine (story = exp-6 arcade-crown, mechanic = round-5 vcp-1 every-Nth counter) →
  **bac-2 carnival dunk tank** (operator-recorded hit pays from pool; keeps all three
  territory loads incl. the owner top-up-IN, the strongest `coin::put` bait).
- **Re-skinned (mechanics unchanged):** kennel → **stp-1 campground** (pet-boarding spine
  collided with elicitation I-3 pet-daycare); ferry till → **bac-1 cinema** (story family
  with exp-8 ferry-manifest — the corpus kp134 was just measured on — and a same-round
  transit twin with stp-2); tip jar → **bac-3 fishing-boat catch-money box** (noun-identical
  to round-3 modimp-3 `pool::tipjar`; equal-split-with-remainder mechanic kept); plant
  sitter → **mva-1 ski-valet desk** (optional re-skin taken: exp-8 plant-clinic is
  same-pack immediately-preceding corpus).
- **Disclosures (differs-clause per entry):** tb-1 marina ≈ round-3 import-2 popup-waitlist
  (differs: ordered multi-entry list scanned for first fit + per-berth deposits vs single
  next-up slot with forfeit); stp-2 transit passes ≈ exp-4 subscription-service (differs:
  per-ride counter + capability void vs paid-through-epoch; keyed registry vs owned ticket
  objects) + elicitation F-5 bus-fare (story family only); sop-1 lighthouse ≈ round-6 opt-2
  mentorship (same territory, mechanic adjacency near-inevitable; differs: single-station
  slot, clock-stamped handover + event, vacancy changes who may install); sop-3 pharmacy ≈
  round-6 opt-2 (one-liner: slot + roster economics + event-that-vacates); mva-1 ski valet
  ≈ elicitation I-3 custody spine + round-6 mva-2 (differs: deposit held INSIDE the moved
  object, fee split out before the send-home); mva-2 consignment ≈ round-6 mva-1 trophy
  desk (closest call in the round; the saving delta the clause must carry: the event adds a
  SECOND derived field — the unmet reserve — widening the read-after-move surface from
  recipient-only to recipient + event-data, which round-6's clean-gating probe lacked);
  mva-3 interloan ≈ round-6 mva-2 courier (differs: per-recipient keyed count with an
  acknowledge/decrement round-trip vs a running sum) + round-5 uid-2 museum loan (story).
  **Wholesale disclosure:** the mva trio is family-adjacent to round-6's mva trio by
  territory inheritance — the class fired in round-6's remeasure, so round 7 re-elicits the
  same family with widened read-after-move surfaces (deposit-split / second event field /
  keyed count).
- **Denominator correction:** the fixture denominator is **47 zones** (87 directories = 40
  red/green pairs + 7 green-only); the draft said 87 zones. Task denominator 164 and all
  five ledger seed citations reviewer-verified against the exp-8 README, round-6
  triage/remeasure, and the exp-4/6/7 experiment records.
- Same-round checks after revision: no internal spine clones (bac payout surfaces differ:
  fixed payroll + sweep / triggered prize + top-up-in / equal division with remainder; tb
  surfaces differ: Option-view / Option-view+scan / event+last-element); nautical crowding
  resolved (bac-1 off ferry); no reserved-word hazards in derivable type names.

## Task index

| territory | tasks |
|---|---|
| 1 tuple-bleed | tb-1 (marina waitlist), tb-2 (seed vault), tb-3 (tram depot) |
| 2 std-table-path | stp-1 (campground), stp-2 (transit passes), stp-3 (apiary hive stands) |
| 3 balance-api-on-coin | bac-1 (cinema till), bac-2 (dunk tank), bac-3 (catch-money box) |
| 4 std-option-path | sop-1 (lighthouse log), sop-2 (aquarium tank hall), sop-3 (night pharmacy) |
| 5 moved-value-arg-order | mva-1 (ski-valet desk), mva-2 (auction consignment), mva-3 (interlibrary loan) |

SUI-payment carriers (8 of 15): tb-1, stp-1, stp-2, bac-1, bac-2, bac-3, sop-3, mva-1.

## Layout

`<territory>-<k>/{task.md, <model>.answer, <model>.buildlog, <model>.result, <model>.import}`
