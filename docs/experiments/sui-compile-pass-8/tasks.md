# Experiment 8 — held-out falsification of deepening round 6 (pre-registered)

**This file is committed BEFORE any answer is collected.** Operator instruction 2026-07-10
("run round 6 … until tonight"). **This experiment is the second arm of the selection-method
comparison:** round 5 (frequency-selected beats, two taught from held-out REDs) shipped its
tier-2 at +3 (experiment 7); round 6 (old-way probe-elicited-only beats, 2 narrow classes)
is measured here under the identical protocol. A branch-3 here alongside experiment 7's
branch-1 is the cleanest evidence two adjacent rounds can give that the selection method,
not pack size, moved round 5's number; a branch-1 here would refute that reading.

## Arms

- **base** — no pack; anchor, no ship-rule weight.
- **kp128** — pre-round-6 payload (55,374 bytes, sha256
  `d9e414e76b9b3033424546e44991b68ad7ba83cb3e648ae061ed8723b8757245` — experiment 7's kp128
  arm byte-identical).
- **kp134** — post-round-6 payload from master `8008a22` (standard rule; 56,464 bytes,
  sha256
  `9d4e6fe8a69abf15453a940455ce0616f78beea84dfbf368bbf3905859c89bff` — as pinned in the round-6 remeasure and
  independently reproduced by its branch review).

Headline comparison **kp134 vs kp128**; `claude-haiku-4-5` all arms; instruction, assembly,
extraction, scaffold, pinned `sui 1.74.1-8fc60f1fa966` gate, import sweep (point #5) — all
unchanged from experiments 6–7.

## Metrics and ship rule (frozen)

Primary compile-pass; secondary zero-warning clean-compile. Branch 1: kp134 > kp128 primary.
Branch 2: primary tied AND kp134 > kp128 secondary. Branch 3: anything else — no headline.
n = 6; denominators everywhere; absolute numbers not cross-comparable. Mechanism analysis
pre-registered at the strict standard; round-6 taught classes of special interest:
`reference-type-argument` (E04004 shapes), `vector-contains-by-ref` (E04007 contains
shapes). Also pre-registered as observational: recurrence of the classes round 6 DECLINED
to teach (`std-option-path`, `moved-value-arg-order`, `branch-type-mismatch`,
`tuple-bleed`) — the selection-method reading depends on where the failures land.

## Tasks

Six fresh contract-authoring tasks, audited against the **158** prior tasks (90 + 40 + 6 +
6 + 16) and the 47 fixture zones at `8008a22`, with the standing pre-freeze reviewer pass
(record below, before any answer).

1. **wine-cellar** — A shared wine cellar: members rack `Bottle` objects (vintage year +
   label). The sommelier (capability) keeps a reserve list of vintage years; a view answers
   whether a given bottle's vintage is on the reserve list. Another view returns the details
   (vintage + label) of the OLDEST bottle currently racked, when the cellar isn't empty.
   Members may unrack their own bottles.
2. **plant-clinic** — A plant clinic: a gardener opens at most one case at a time (species +
   symptom recorded); the clinician (capability) closes cases (the record is removed). Views:
   a gardener's open case details when they have one, and the count of open cases across all
   gardeners.
3. **ferry-manifest** — A car-ferry manifest: vehicles (objects recording plate, deck-space
   units, and owner address) board with a toll in SUI of a fixed rate (set at creation) per
   deck-space unit; boarding closes automatically once cumulative deck space reaches the
   ferry's capacity — a vehicle that would overshoot the remaining space is turned away with
   its toll returned whole, as is any vehicle arriving after close. On arrival the purser
   (capability) disembarks every vehicle to the owner address recorded on it. Views: space
   remaining and tolls collected.
4. **quilt-bee** — A quilting bee: members contribute finished `Square` objects (pattern
   name); contributions beyond the ninth abort. When nine are in, the organizer (capability)
   stitches them — consuming all nine — into a single `Quilt` awarded to a member of the
   organizer's choice (contributor or not), and a single `Stitched` event records each contributor
   with how many of their squares went in. One quilt per bee (a second stitch aborts). A view
   reports squares still needed.
5. **tide-tables** — A harbor tide board: the harbormaster (capability) posts the CURRENT
   epoch's high-tide level (posting twice for one epoch aborts; only the current epoch may be
   posted). Boats hold `Mooring` objects with a draft depth; a view answers whether a given
   mooring can sail THIS epoch — false when this epoch is unposted. Another view returns the
   most recently posted level, when any posting exists.
6. **apple-press** — A community apple press: households deposit apple crates (weight units;
   crates are consumed at pressing). On the single pressing day the keeper (capability)
   presses everything: cider totals deposited-weight × a yield rate fixed at creation; each
   household receives ONE `CiderJug` object holding its integer share (weight × yield ÷
   total-weight of the pool — a household whose share rounds to zero still receives a jug
   marked zero), and the keeper receives one jug holding the undistributed remainder. The
   press is one-shot (a second pressing aborts). Views: weight waiting (before pressing) and
   jugs poured.

## Pre-freeze audit review (ran before this freeze; the standing step)

Round 1 returned **REVISE**: seed-swap-meet restated the escrow-swap spine (run twice in this
experiment series — exp-1 and exp-3) and choir-roster restated round-6's own opt-2
(mentor-match) — a protocol-symmetry breaker for the very comparison this experiment makes.
Both replaced before freeze: **wine-cellar** (membership-check leg = the E04007 carrier;
oldest-bottle-details-if-present view = the E04004 `Option<&T>` bait; no custody swap) and
**plant-clinic** (self-opened single case — not the cap-assigns-slot spine — with the
open-case-details-if-present view carrying both the std-option-path surface and the E04004
bait). quilt-raffle renamed **quilt-bee** (no raffle mechanics existed; word-collision with
round-4 `raffle::pot` removed). All flagged ambiguities tightened arm-neutrally (ferry:
auto-close, overshoot turned away, rate at creation, post-close refund-return; quilt: >9
aborts, awardee unrestricted, one-shot; tide: current-epoch-only posting, unposted → false,
latest = most recent posting; apple: yield at creation, zero-share jug minted, keeper
remainder jug, crates consumed, one-shot).

Disclosures (differs-clause each): ferry-manifest ≈ round-5 vde-1 mailroom skeleton on the
disembark leg — **recorded intent: that leg is the pre-registered `moved-value-arg-order`
observational carrier** — and ≈ elicitation I7 marathon (register-fee-close; differs:
cumulative capacity threshold, the series' first), ≈ round-5 vcp-3 (refund-branch shape — a
vcp-class failure there scores ignored-while-loaded, not new-class), ≈ bus-fare/
charging-station settlement family; quilt-bee ≈ exp-7 card-merge + exp-4 crafting-forge
(consume-N-produce-1 family; differs: nine-way threshold accumulation from many
contributors, per-contributor aggregation event — **recorded intent: the `tuple-bleed`
observational carrier**), ≈ round-5 vde-3 / round-4 gen-3 / exp-6 passport-stamps at the
named tiers; tide-tables ≈ exp-5 oracle-feed (differs: per-epoch keyed history with
dedup-abort, no staleness-abort, consumer-object comparison leg), ≈ round-6 brm-1 (view-only,
no pool), ≈ digest-notary + modform-1 (dedup shapes); apple-press ≈ elicitation I8
carpool-log (pro-rata vs winner-take-all) and the split family at arithmetic level only (no
coin is split; jugs are minted objects), ≈ round-6 csp-1's remainder policy (nearest
precedent, from the round under test — disclosed), second (weaker) mva carrier on the jug
payout; wine-cellar ≈ **round-6 mva-3** (second-pass catch: a capability-curated membership list
with a contains check — the round-under-test's own eliciting probe; differs: query-view on
u64 vintages vs routing decision on addresses, no delivery/bounce legs, fixture vocabulary
avoided) and ≈ elicitation I3 pet-daycare + exp-7 community-fridge on the member-stocked
custody leg (nearer than the originally disclosed anchor; differs: no settlement, no
epoch-take limit, reclaim-own-by-owner), and ≈ round-2 optiondrop-1 shop consignment at the weak tier (racked object
custody; differs: no sale, reserve-list membership, oldest-scan view); plant-clinic ≈
round-6 opt-2 at the negation level (per-member optional record WITHOUT cap-assignment —
self-opened, struct-valued, clinician-closed), ≈ **round-6 opt-1** (second-pass catch: the
self-initiate/capability-clear lifecycle direction and the clinic noun echo; differs: no
scarce numbered slots, no per-epoch limit, struct payload, entry removed vs slot freed),
and ≈ elicitation I4 quest-board (one-active-per-member self-opened cap-resolved; differs:
no catalog, no reward, record removed). Note tier: `Bottle` word-collides with
sheet-confirm's bottle-deposit (mechanics fully disjoint); quilt-bee's one-shot clause
echoes round-4 gen-1's award-once at single-clause level.

Per-class carrier map (pre-registered so fragility is visible): E04004
reference-type-argument → wine-cellar + plant-clinic (the if-present struct views); E04007
contains-by-ref → wine-cellar (reserve list) + quilt-bee (contributor tally) +
ferry-manifest; std-option-path → tide-tables + plant-clinic; moved-value-arg-order →
ferry-manifest (primary) + apple-press (weak); branch-type-mismatch → ferry (refund/board),
tide (posted/unposted), quilt (threshold); tuple-bleed → quilt-bee (single carrier — known
fragility, accepted). Reserved-word check PASS (`Bottle`, `Mooring`, `CiderJug`, `Quilt`,
`Square`, `Stitched` — none reserved, none prelude-colliding). Denominators verified: 158
prior tasks (90 probes + 40 experiment + 6 salience + 6 sheet-confirm + 16 elicitation) and
47 fixture zones. **Second pass on the two replacements ran before the freeze** (record
below).

## Layout

Standard: `answers/<task>/{base,kp128,kp134}.*` + import files; results.txt; README post-gate.
