# SUI-import elicitation experiment (pre-registered)

**This file is committed BEFORE any answer is collected.** Operator authorization 2026-07-10
(gate-1 approval of round 5 including this experiment, "approve + run to merge").

## Question

The `SUI`-import class (`SUI` reached through the wrong module or no import at all;
E03003/E03006) has fired **×5 cumulative in held-out experiment draws** (exp-4 ×2, exp-5 ×2
counting the salience draw, exp-6 ×1) yet came back **clean 6/6** under round-4's targeted
probe. Two live explanations: **elicitation shape** (targeted probe tasks make coin mechanics
focal, which keeps the import salient; held-out failures all occurred where payment was
incidental to some other core mechanic) or **draw variance** (a low per-answer rate that a
6-run probe misses: at p≈0.3, P(0 fails in 6) ≈ 0.12). This experiment separates them.

## Design

**The pack is held constant; only the task shape varies.** One model, one payload, two arms
of 8 tasks each:

- **Arm F (focal):** coin mechanics ARE the task — paying, pooling, sweeping is the point.
  The shape of round-4's suimport probe tasks (which elicited 6/6 correct imports).
- **Arm I (incidental):** the task's core is a non-coin mechanic (registries, custody,
  ladders, lifecycles) and a SUI payment appears as a side requirement. The shape of all five
  recorded held-out failures (arcade-crown, staking-pot, payment-channel, subscription,
  gift-card).

Every task in both arms requires `Coin<SUI>`/`Balance<SUI>` somewhere, so all 16 answers
exercise the corner. Model: `claude-haiku-4-5` (the falsification primary). Payload: kp110,
assembled from master `0cdb536` by the standard rule — **51,799 bytes, sha256
`92756d2d7532318ffd16be0b87794141c185336ce6c324a1e0937b6602cfb812`** (byte-identical to
experiment 6's kp110 arm). Fresh context per task; headless, no tools; neutral scratch
working directory; the standard instruction and prompt assembly (task text, instruction,
`--- Reference pack (verified) ---`, payload); the standard mechanical extraction + scaffold
repair; gate on pinned `sui 1.74.1-8fc60f1fa966` (compile outcome recorded as context, not
the metric).

## Metric (mechanical, frozen)

Per answer, **import-correct** iff the extracted source satisfies: every use of the `SUI`
type token is covered by `use sui::sui::SUI` (plain or in a group import from `sui::sui`) or
written fully qualified as `sui::sui::SUI`. **Import-fail** otherwise — including the
wrong-module form (`use sui::coin::{..., SUI}`) and the absent-import form. Checked by
script (committed with the answers); the buildlog's E03003 "Unbound member 'SUI'" /
E03006-on-`SUI` lines recorded as corroboration. An answer that avoids the `SUI` token
entirely (e.g. generic-only coin handling) is recorded **n/a** and excluded from both
denominators (disclosed if it occurs).

## Ship rule and action map (frozen)

Let `fail_F`, `fail_I` = import-fail counts per arm (of 8, less any n/a).

- **Branch 1 — elicitation confirmed:** `fail_I ≥ fail_F + 2`. Round-4's clean probe was an
  elicitation artifact. Actions: round-5's probe tasks adopt the incidental shape for every
  territory, and the SUI-import beat is taught in round 5 (the experiment's own failing
  answers supply the observed RED evidence).
- **Branch 2 — rare-per-answer:** `fail_F + fail_I ≤ 1`. Targeted probes at n≈6 cannot see a
  class this rare; the held-out ×5 accumulated across ~30 pack-arm answers. Actions: the
  beat is still taught in round 5 (five held-out occurrences is coverage evidence enough —
  the question was probe design, not whether the gap exists), but probe shape is recorded as
  non-diagnostic for rare classes and future clean-territory claims carry a rate ceiling
  (clean at n=6 bounds p at roughly < 0.3, nothing stronger).
- **Branch 3 — shape-independent:** anything else (failures in both arms, gap < 2). The
  class fires regardless of shape once drawn; coverage gap plain and simple. Actions: teach
  the beat in round 5; probe shape unchanged.

n = 8 per arm; every number with its denominator; the branch actions are design decisions
for round 5, not headline claims about the pack.

## Tasks

Held-out audit run before this freeze — checked against the 66 prior probe/experiment tasks
(rounds 1–4, experiments 1–6, salience + sheet-confirm) and the 39 fixture zones at
`68e487d`. Disclosed adjacencies (mechanics differ, named per the standing standard):
F4 wishing-well ≈ round-3 tip jar (adds max-single-wish tracking + drain-all); F1 laundromat
≈ round-4 toll booth (adds machine busy/free state machine); I1 chess-ladder ≈ round-4 duel
record (adds stakes + rating updates vs bare win counts); I4 quest-board ≈ round-3 bounty
board (XP rewards, not coin rewards; the fee is the only coin); I6 lost-pet-poster ≈ round-3
lost-and-found (notice + escrowed reward vs deposit-item-reclaim); I2 community-garden ≈
round-3 farm harvest (plot registry vs harvest cooldown). Dropped drafts: cover-charge
(restates round-4 paywall's pay-for-access-object), guild-armory deposit lending (restates
experiment 4 rental-agreement — the same adjacency that killed tool-lending in experiment 6),
tip-splitter (restates round-2 modform-3 fee splitting), science-fair prize pot (the pot
made coin focal, breaking the arm's design).

### Arm F (focal — coin mechanics are the task)

1. **laundromat** — A coin-op laundromat: a shared `Washer` charges a fixed price per cycle
   in SUI (exact payment, abort otherwise). Starting a cycle marks the washer busy and
   records the current epoch; it can be started again only after the epoch advances. Payments
   pool in the washer; the owner (capability) sweeps them.
2. **photo-booth** — A photo booth: pay the fixed fee in SUI (exact), receive a numbered
   `PhotoStrip` object (sequential numbering), fees accumulate, the operator sweeps.
3. **jukebox** — A jukebox: pay the fee in SUI for one play credit (credits tracked per
   payer), spend a credit to queue a song title, owner sweeps the pool.
4. **wishing-well** — A wishing well: toss any positive amount of SUI in; the well tracks the
   total collected and the largest single wish; the keeper (capability) drains the entire
   pool.
5. **bus-fare** — A bus fare box: pay the fixed fare in SUI (exact), receive a `DayTicket`
   valid through the current epoch (a view reports whether a ticket is still valid); fares
   pool for the transit operator to sweep.
6. **car-wash** — A prepaid wash card: load SUI value onto an owned `WashCard`; each wash
   deducts the fixed price from the card's stored balance (abort if insufficient); the
   station owner sweeps the deducted value from the station's pool.
7. **exact-change** — An exact-change machine: feed it one SUI coin and a denomination; it
   returns a vector of coins of that denomination (as many as fit), keeps the remainder as
   its fee, and the owner sweeps accumulated fees.
8. **karma-boost** — A pay-to-boost board: anyone pays a fixed SUI fee to add one boost to a
   post (posts tracked by id with boost counts); each post's author can withdraw the boosts
   collected for their post.

### Arm I (incidental — the core mechanic is elsewhere; SUI payment is a side requirement)

1. **chess-ladder** — A club ladder: players hold `Rating` objects; a challenge pits two
   players, the reporter (capability) records the result, winner gains 10 rating and loser
   drops 10 (floor 0). Issuing a challenge requires a small fixed SUI stake from the
   challenger, which the winner collects with the result.
2. **community-garden** — A garden plot registry: a shared garden of numbered plots;
   gardeners claim a free plot (one each), record plantings (a crop name per epoch), and
   release plots. Claiming requires the season's fee in SUI, pooled for the garden
   association to sweep.
3. **pet-daycare** — A daycare: owners check their `Pet` objects in (custody moves to the
   shared daycare, a tag records the owner) and check them out again (custody returns).
   Checkout requires paying the day rate in SUI per epoch elapsed, pooled for the operator.
4. **quest-board** — A guild quest board: the guildmaster (capability) posts quests with XP
   rewards; adventurers accept (one active quest each) and the guildmaster marks completions,
   crediting XP to the adventurer's `Adventurer` object. Posting a quest costs the guild a
   flat SUI listing fee into the board's coffer.
5. **recipe-book** — A community cookbook: chefs submit recipes (title + ingredient count),
   readers rate them 1–5 (one rating per reader per recipe, running average kept). Submitting
   a recipe requires a small anti-spam fee in SUI, pooled for the maintainer.
6. **lost-pet-poster** — A lost-pet notice board: an owner posts a notice describing the pet
   and escrows a SUI reward with it; a finder registers a claim; the owner confirms one claim,
   which releases the reward to the finder and closes the notice (or the owner cancels,
   reclaiming the reward).
7. **marathon** — A race registration: runners register and receive sequential bib numbers;
   the organizer (capability) closes registration, after which the finish line records
   finishers in order; the first three finishers receive `Medal` objects. Registration
   requires the entry fee in SUI, pooled for the organizer.
8. **carpool-log** — A carpool ledger: members log rides (driver, date-epoch, rider list);
   the ledger tracks per-member rides-driven counts; monthly (per epoch) the member with the
   most rides driven is paid the pool. Logging a ride requires each rider's gas-share
   micro-payment in SUI into the pool.

## Layout

`answers/<arm>-<task>/{answer, -src.move, -pkg/, .buildlog, .result, .import}` where
`.import` is `CORRECT` / `FAIL <shape>` / `NA` from the committed checker script
(`check_import.py` alongside this file); summary in `answers/results.txt`; verdict in
`README.md` (post-gate).
