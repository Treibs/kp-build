# Round-5 probe — protocol and layout

**Arm: current pack loaded** (deepening probes measure *residual* gaps). This file is written
and committed **before any answer is collected**.

## Protocol

- 15 tasks (3 per approved territory — [`../territories.md`](../territories.md)), each in
  `<territory>-<k>/task.md`. **All incidental-shaped** per the elicitation experiment's
  branch-1 directive: each territory's corner is a side requirement of a non-focal core.
- **Held-out check:** every task was checked against the **122** prior tasks (60 round-1..4
  probe tasks, 34 experiment tasks across experiments 1–6, 6 payload-salience, 6
  sheet-confirm, 16 elicitation) and the 39 fixture zones at `1a1067a`.
- **Elicitation-replication sweep:** 9 tasks carry an incidental SUI-payment element
  (vcp-1..3, vde-1, uid-1..3, api-2, api-3). Every answer runs through the committed import
  checker (`docs/experiments/sui-import-elicitation/check_import.py`); per-answer verdicts
  land in `results.txt` as the elicitation experiment's named replication measure
  (observational — the SUI-import beat is pre-decided from the experiment's own REDs).
- Dual model, fresh context per task per model, pinned IDs: `claude-haiku-4-5` (primary),
  `claude-sonnet-4-6` (secondary). Prompt = task text + the standard instruction (verbatim,
  unchanged) + `--- Reference pack (verified) ---` + the kp110 payload (assembled from
  `1a1067a` inputs by the standard rule; byte-identical to the experiment-6/elicitation
  payload, sha `92756d2d…`, claims unchanged since `0cdb536`).
- Mechanical extraction, arm-neutral scaffold repair, gate on pinned
  `sui 1.74.1-8fc60f1fa966` — all identical to rounds 1–4. Buildlogs committed ANSI-stripped
  and home-redacted; verdicts `PASS CLEAN` / `PASS WARN<n>` / `FAIL <first error line>`;
  summary + import sweep in `results.txt`.

## Pre-freeze audit review (ran before this freeze; the round's new standing step)

The adversarial reviewer pass over the DRAFT list returned **REVISE**: one restatement-tier
collision, one borderline, six disclosure misses, one wrong differs-clause, and a wrong
audit-scope denominator ("82" — the true prior-task count is 122; the elicitation file's own
"66" carried the same species of miscount). All actions were applied before this freeze:

- **Replaced on the reviewer's findings:** the cooking-class draft (restated the
  sheet-confirm tournament-prize spine — fixed-fee enrollment, the same 3-entrant threshold,
  cap-gated run-or-cancel, per-entrant refunds) → **vcp-3 barber shop** (the
  payment-returned-on-a-branch corner via service availability, no enrollment threshold);
  the spice-rack draft (named-object store/retrieve = round-1 dynfields-1's core) → **ns-2
  book wishlist** (Table-of-vectors, no object custody); the water-cooler draft (shared its
  entire spine with api-2 AND exp-6 book-club) → **api-3 envelope budget** (coin
  splitting/arity corner; adjacency to elicitation F7 exact-change disclosed: denominations
  vending fee vs named allocations with leftover return).
- **Adjacencies disclosed** (differs-clause per entry): vcp-1 food-truck ≈ round-2 coinlint-2
  vending machine (adds the loyalty counter and the every-5th-free path returning the
  presented Coin unconsumed — the vcp corner); vcp-2 parking-garage ≈ round-3 import-1
  parking meter AND elicitation I3 pet-daycare (the rate×epochs exit settlement is
  pet-daycare's shape; the fresh part is the validator-waiver branch returning the payment
  whole); vde-1 mailroom ≈ round-4 gen-3 gift pool (batch drain-to-empty to per-object
  recorded addressees vs one-at-a-time indexed handout) and, farther, exp-2 object-mailbox;
  vde-2 card-deck ≈ round-4 gen-2 send_batch / round-2 letmut-1 (round-robin
  drain-until-empty is the fresh corner); uid-1 gym-locker ≈ round-4 oid-1 member-card
  (same-number rekey driven by loss + fee, no tier progression); uid-2 museum-loan ≈ round-4
  oid-2 pet registry (identity-keyed registry re-probed incidental-shaped BY DESIGN; adds
  loan/return lifecycle, deposit escrow, due epoch) and exp-4 rental-agreement (custody
  against deposit); uid-3 star-registry ≈ oid-2 (weaker tier: append-only provenance on open
  gifting) with the mint leg being the round's deliberate incidental-payment boilerplate;
  ns-1 attendance ≈ round-4 rsyn-1 scoreboard AND round-2 modform-1 rate limiter (the
  per-epoch dedup is modform-1's mechanic; fresh: distinct-students view, no coin);
  ns-3 medicine-cabinet ≈ round-3 time-1 faucet cooldown (ms-clock minimum-interval on an
  owned object).
- Reserved-word check PASS; the 9-task import sweep spans four territories (3/1/3/2);
  no fixture zone restated.

## Task index

| territory | tasks |
|---|---|
| 1 value-consumption-paths | vcp-1 (food-truck loyalty), vcp-2 (parking garage), vcp-3 (barber shop) |
| 2 vector-destroy-empty | vde-1 (mailroom), vde-2 (card deck), vde-3 (firework show) |
| 3 uid-vs-ID | uid-1 (gym locker rekey), uid-2 (museum loan), uid-3 (star registry) |
| 4 namespace-paths | ns-1 (attendance sheet), ns-2 (book wishlist), ns-3 (medicine cabinet) |
| 5 api-argument-shapes | api-1 (party door list), api-2 (club badges), api-3 (envelope budget) |
