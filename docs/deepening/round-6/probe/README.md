# Round-6 probe — protocol and layout

**Arm: current pack loaded.** This file is written and committed **before any answer is
collected.**

## Protocol

- 15 incidental-shaped tasks (3 per territory — [`../territories.md`](../territories.md)),
  `<territory>-<k>/task.md`. Dual model, fresh context, pinned IDs (`claude-haiku-4-5`
  primary, `claude-sonnet-4-6` secondary). Prompt = task text + the standard instruction +
  `--- Reference pack (verified) ---` + the kp128 payload (55,374 bytes, sha `d9e414e7…`,
  assembled from `e5496b7` inputs by the standard rule; claims unchanged since `1b85d58`).
- Mechanical extraction, arm-neutral scaffold repair, pinned `sui 1.74.1-8fc60f1fa966` gate,
  committed import checker on every answer (replication point #4) — all identical to round 5.
  Buildlogs ANSI-stripped + home-redacted; verdict format and layout as prior rounds;
  summary + import sweep in `results.txt`.
- **Old-way selection (binding, per territories.md):** beats this round come ONLY from
  failures this probe elicits.

## Pre-freeze audit review (ran before this freeze; the standing step)

The reviewer pass on the draft returned **REVISE**: four restatements, one arm-mechanic
clone, one same-series metaphor clone, and seven required disclosures. All applied before
this freeze:

- **Replaced:** canteen snack till (restated round-2 coinlint-2 vending machine / round-3
  import-1 — a spine prior audits killed twice) → **csp-1 scholarship tranches** (split one
  presented coin into a held disbursement schedule — a split flow no prior task carries);
  bounty 60/40 split (restated round-2 modform-3 fee splitter — the spine that killed
  tip-splitter at the elicitation audit) → **csp-2 lease closeout** (assessed-damages split
  of a presented deposit coin, pair-wise `let (a, b)` pressure retained; disclosed adjacent
  to exp-7 stall-rental — binary clean/dirty forfeit vs assessed partial split — and to the
  charging-station partial-settlement family); library return cart and valentine mailbag
  (both restated round-5 vde-1 mailroom, the mva class's own seed — valentine included its
  fee and view pair) → **mva-2 insured courier** (read-after-move pressure via the manifest's
  declared-value add after delivery) and **mva-3 moderated post** (blocklist branch chooses
  recipient-or-return-address, both read from the letter being moved).
- **Revised:** brm-3 examiner's fail arm (its half-refund-rounded-down cloned exp-7
  escape-room's exact formula — this round's own seed corpus) → refund is now fee minus a
  fixed grading charge, and an invalid-score reject path adds the if/abort elicitor the
  draft lacked.
- **Re-skinned:** red-envelope prep (metaphor + spine = round-5 api-3 envelope budget, one
  round back in the same series) → **ctx-3 casino chip trays** (prepare-empty → fill-from-
  bankroll → hand lifecycle retained; api-3 disclosed regardless).
- **Disclosures (differs-clause per entry):** opt-1 dental scheduler ≈ elicitation I2
  community-garden + exp-7 stall-rental (numbered-slot claims; differs: no coins,
  cap-cancel, Option-returning holder/next-free views — the territory's load); opt-3 racing
  ghost ≈ exp-6 arcade-crown (champion custody; differs: the run object itself swaps, old
  ghost returned to the PREVIOUS holder, no fees) + round-4 rapi-3 battery swap
  (install-new-return-old; differs: shared/conditional/third-party) + the
  value-consumption-paths-green fixture's losing-path-returns-value teaching moment (story
  distinct; a vcp-class failure here scores as ignored-while-loaded, not opt evidence);
  brm-1 rain insurance ≈ exp-5 insurance-pool + sheet-confirm warranty-registry (kept on the
  same precedent; differs: parametric oracle condition, holder-triggered, double-or-nothing)
  + a note vs exp-5 oracle-feed; brm-2 duty-free ≈ sheet-confirm freelance-invoice
  (conditional owed amount; differs: credential-driven branch, accumulating till; `Stamp`
  name collides with exp-6 passport-stamps in word only); csp-3 returns counter ≈
  sheet-confirm bottle-deposit (differs: 80% of receipt-recorded price, receipt retained;
  class-fit caveat recorded — the float-based refund may elicit `coin::take`, so csp-1/csp-2
  carry the split-from-presented-coin load); mva-1 awards desk ≈ round-5 vde-1 at the
  class-seed level only (per-object recorded address at ship time — the territory's
  definition; differs: no container, no batch, no fee; the `Shipped` event is the
  read-after-move pressure); ctx-1 onboarding kit ≈ elicitation F6 car-wash + round-2
  coinlint-1 savings pot (differs: cap-issued starter object beginning EMPTY — the
  `coin::zero(ctx)` load — no spend/sweep).
- **Recorded intent:** ctx-2 petty-cash drawers deliberately probes the `balance::zero()`
  (correctly nullary) vs `coin::zero(ctx)` confusion wing — the exp-7 `Balance::zero()`
  family shape. opt-2 and ctx-2 passed clean.
- Reserved-word check PASS; 143-task and 45-zone denominators reviewer-verified.

## Task index

| territory | tasks |
|---|---|
| 1 std-option-path | opt-1 (dental slots), opt-2 (mentor match), opt-3 (racing ghost) |
| 2 branch-type-mismatch | brm-1 (rain insurance), brm-2 (duty-free), brm-3 (examiner) |
| 3 coin-split-shapes | csp-1 (scholarship tranches), csp-2 (lease closeout), csp-3 (returns counter) |
| 4 moved-value-arg-order | mva-1 (awards desk), mva-2 (insured courier), mva-3 (moderated post) |
| 5 api-arity-ctx | ctx-1 (onboarding kit), ctx-2 (petty-cash drawers), ctx-3 (chip trays) |
