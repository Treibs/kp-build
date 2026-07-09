# Sheet-vs-full confirmation draw — sui-move pack (pre-registered)

The payload-salience experiment (`docs/experiments/sui-payload-salience/`, merged `d908cca`)
adopted the **sheet** form as the recommended answer-time load format under its pre-registered
branch 1 — but the bar was met **exactly** (sheet 3/6 vs full 1/6, ≥ full + 2 with zero margin,
n = 6, two disclosed treatment comparisons), and its README recorded a required follow-up:
*"one fresh draw, sheet vs full only, before any `kp-build` emit-sheet feature is built."*
This experiment is that confirmation draw. **This file is committed before any answer is
collected** — the commit timestamp is the pre-registration. Operator sign-off: explicit
selection 2026-07-09 (chose "confirmation draw, sheet vs full" from the recorded open forks,
over a content round 4).

## Question and arms

One treatment comparison: **sheet vs full**, fresh tasks, same model, same oracle. Three arms:

- **base** — task text + the standard instruction only. No pack. Contextual anchor for draw
  difficulty (the salience draw's base went 0/6, the hardest of the series, which was essential
  for reading full's 1/6); **no ship-rule weight** — including it does not add a treatment
  comparison.
- **full** — the standard payload: `CONTEXT.md` + a `## Pack claims (all)` section with every
  claim statement, sorted, one bullet each. **Reused byte-identical** from the salience
  experiment's committed artifact `docs/experiments/sui-payload-salience/payloads/payload-full.md`,
  49,656 bytes, sha256 `4a53c7dfeb198aaca6df579c39be2adb697e01d40eeb0ff89ea6e000d39fbc4b`
  (re-verified at freeze time).
- **sheet** — the 35-line imperative cheat sheet, one rule per line derived 1:1 from the pack's
  claims. **Reused byte-identical** from
  `docs/experiments/sui-payload-salience/payloads/payload-sheet.md`, 5,887 bytes,
  sha256 `19a42c4dccc5a4454c9503f7da4ce8f9b8e123d317685c922b63d6d28cfd8bd0` (re-verified at
  freeze time).

Payload validity: both pack arms carry the same 98 claims. Since the salience payloads were
assembled (pack state `04d7cba`), the only pack files that changed are `README.md` and
`wikillm.json` (recording the salience verdict itself) — **neither is a payload input**
(`CONTEXT.md` and `claims/` are byte-unchanged, checked by `git diff` at freeze time), so the
committed payload files remain exact views of the current pack. No payload is re-committed
here; the SHA pins above are the reference.

- Model, all arms: `claude-haiku-4-5` — the pack's falsification primary, same as all prior
  experiments in this series.
- Fresh context per task per arm; headless, no tools; neutral scratch working directory;
  environment identical across arms.
- Instruction (verbatim, same as experiments 3–5 and the salience draw): *"Answer with the
  complete Sui Move source only (edition 2024), in a single ```move code block. No
  explanations, no tools. If the task asks for two modules, put both in the same code block."*
- Prompt assembly for pack arms (same as experiments 3–5 and the salience draw): task text,
  then the instruction, then a line `--- Reference pack (verified) ---`, then the payload.

## Tasks

Six contract-authoring tasks, module naming left free (no pinned identifiers; the round-3
reserved-word check is trivially satisfied). Held-out audit run **before** this file was
frozen — each task was checked against the experiment 1–5 task lists (28 tasks), the salience
draw's 6 tasks, all 45 round-1/2/3 probe tasks, and the fixture zones as of `c036839`. The
audit killed **five draft candidates**: a vending machine (restates round-2 probe coinlint-2's
`VendingMachine`; the same collision exp-4's audit caught as a ticket vendor), a revenue/royalty
splitter (restates round-2 probe coinlint-3's `RoyaltyPool`; same collision exp-5's audit
caught), a bounty board (restates round-3 probe destr-2's `board::bounty`), a desk-booking
calendar (adjacent to round-3 probe import-2's pay-deposit-to-reserve restaurant waitlist),
and a parking permit (restates round-3 probe import-1's `park::meter`, which issues `Permit`
objects). Disclosed adjacencies that were kept (mechanism judged distinct): tournament-prize
vs exp-4 wager-arbiter (declared-winner payout, but open multi-entrant enrollment + fee pool +
ranked three-way split vs a two-party stake); freelance-invoice vs exp-5 milestone-contract
(payment-for-work, but billing direction with no escrowed funds); penalty-jar vs round-3 probe
modimp-3's tip jar (a jar swept by an owner, but staked members + referee-deducted fines vs
open voluntary tips); layaway-plan vs exp-4 rental-agreement (item held by a contract object +
epoch deadline, but installment purchase-to-own vs rent + recoverable deposit);
warranty-registry vs exp-5 insurance-pool (claims paid from a reserve, but per-item issued
warranties with a repair/reject flow vs premium-priced coverage policies). Multi-concept
difficulty calibrated to the experiment 4–5 band.

1. **warranty-registry** — Write a module implementing a merchant warranty program. A merchant
   creates a shared registry, funding a repair reserve with SUI, and receives a merchant
   capability. The capability holder issues a warranty to a buyer, recording a product name and
   a validity period in epochs; the buyer receives the warranty as an owned object. The
   warranty holder can file a claim against the registry before the warranty expires; filing on
   an expired warranty aborts, and filing a second claim on the same warranty aborts. The
   capability holder resolves a filed claim either by approving it — paying a stated repair
   reimbursement from the reserve to the warranty holder and emitting an event carrying the
   warranty's id and the amount — or by rejecting it; either resolution closes the warranty for
   good. The merchant can top up the reserve at any time. Provide a read function returning
   whether a warranty is still valid (unexpired, no claim filed).
2. **layaway-plan** — Write a module implementing a layaway purchase of a generic item. A
   seller opens a layaway plan naming a buyer, stating a total price in SUI, a fixed
   cancellation fee, and a payment deadline interval in epochs; the item is held by the plan
   while it is open. Only the named buyer pays installments, of any size; when accumulated
   payments reach the total price, any overpayment in the final installment is returned to the
   buyer, the item is released to the buyer, the accumulated funds go to the seller, and the
   plan is cleaned up. Before completion the buyer can cancel: the cancellation fee goes to the
   seller, the rest of the accumulated payments are refunded to the buyer, and the item returns
   to the seller. If more than the deadline interval has elapsed since the last payment (or
   since opening, if none), the seller can cancel with the same split. Both cancellation paths
   clean up the plan. Provide a read function returning the remaining amount owed.
3. **freelance-invoice** — Write a module implementing contractor invoicing. A contractor
   issues an invoice as a shared object naming a client, an amount in SUI, a fixed late fee,
   and a due epoch. Only the named client can pay: past the due epoch the amount owed is the
   invoice amount plus the late fee, otherwise just the amount; payment must cover the amount
   owed, with any overpayment returned. On payment the funds go to the contractor, the client
   receives an owned receipt recording the invoice's id and the amount paid, an event carrying
   the same two values is emitted, and the invoice is cleaned up. The contractor (and only the
   contractor) can void an unpaid invoice, cleaning it up. Provide a read function returning
   the amount currently owed on an invoice.
4. **tournament-prize** — Write a module implementing a tournament prize pool. An organizer
   creates a shared tournament with an entry fee and a start epoch, and receives an organizer
   capability. Anyone can enter before the start epoch by paying exactly the entry fee;
   entering twice aborts; entering at or after the start epoch aborts. From the start epoch on,
   the capability holder either declares a result — three distinct entrants ranked first,
   second, third, paying first 50%, second 30%, and third 20% of the pool (any remainder from
   integer division goes to first), aborting if any declared address never entered — or, if
   fewer than three players entered, cancels the tournament, refunding every entrant their
   entry fee. Both paths clean up the tournament object. Provide read functions returning the
   current pool amount and the entrant count.
5. **bottle-deposit** — Write a module implementing a bottle deposit scheme. A distributor
   creates a shared scheme with a fixed per-bottle deposit amount and receives a distributor
   capability. The capability holder sells a bottle to a recipient: the sale payment must cover
   exactly the deposit amount, the payment joins the scheme's refund reservoir, and the
   recipient receives an owned bottle object recording the scheme it belongs to. Anyone holding
   a bottle can return it: a bottle from a different scheme aborts; otherwise the bottle is
   destroyed, the deposit amount is refunded from the reservoir, and a running count of
   returned bottles is incremented. The distributor can top up the reservoir, and can withdraw
   from it only what exceeds the scheme's outstanding liability (unreturned bottles × deposit
   amount). Provide read functions returning the outstanding (sold, unreturned) bottle count
   and the reservoir balance.
6. **penalty-jar** — Write a module implementing a team penalty jar. A referee creates the
   shared jar naming a beneficiary address, a fixed fine amount, and a minimum stake, and
   receives a referee capability. Anyone can join as a member by staking SUI of at least the
   minimum; joining twice aborts. The capability holder records an infraction against a member:
   the fine amount moves from that member's stake into the jar's pot; if the member's remaining
   stake is smaller than the fine, the entire remaining stake moves instead and the member is
   removed. A member can top up their stake at any time. A member can leave, recovering their
   remaining stake; a non-member leaving aborts. The capability holder can sweep the pot to the
   beneficiary, emitting an event carrying the swept amount. Provide a read function returning
   a member's current stake.

## Scoring protocol (identical to experiments 3–5 and the salience draw)

- **Mechanical extraction (arm-neutral):** the first fenced code block is the source (whole
  answer if unfenced). No edits.
- **Scaffold repair (arm-neutral, pre-declared):** minimal `Move.toml` (edition 2024) binding
  every address name declared by the answer's own `module X::Y` lines to `0x0`; multi-module
  answers are gated as ONE package; answers declaring only bare `module name {` forms get an
  inert `probe = "0x0"` binding. No source is ever touched.
- Gate: plain `sui move build` with the pinned binary (`sui 1.74.1-8fc60f1fa966`). Committed
  buildlogs are ANSI-stripped and home-directory-redacted; verdicts computed from the stripped
  text.
- Layout: `answers/<task>/<arm>.answer`, `<arm>-src.move`, `<arm>-pkg/`, `<arm>.buildlog`,
  `<arm>.result`; summary in `results.txt`.

## Pre-registered metrics and ship rule

- **Primary — compile-pass:** the build exits 0. Count per arm over the 6 tasks.
- **Secondary — clean-compile:** the build exits 0 AND zero `warning[` lines. **Observational
  this draw — no ship-rule weight.** (Design change from the salience experiment, disclosed:
  the adoption being confirmed was made on the primary axis, and this draw's single-comparison
  design deliberately carries exactly one decision.)

**Ship rule (decided before data; ONE comparison, sheet vs full, n = 6):**

1. **Confirmed** — sheet compile-pass ≥ full compile-pass + 2 → the salience adoption is
   confirmed; the sheet stays the recommended answer-time load format and `emit-sheet` tooling
   is unblocked.
2. **Directional, unconfirmed** — sheet = full + 1 → not confirmed; the sheet's recommendation
   stays provisional, tooling stays blocked, and the next step (a third draw, or accepting the
   pooled evidence) is an operator decision.
3. **Not confirmed** — sheet ≤ full → the "recommended load format" adoption is **withdrawn**:
   the sheet reverts to an experimental view of the pack, the full payload reverts to the
   recommended form, and this outcome is reported as prominently as the original adoption was.

No post-hoc metric may be substituted. Base-arm numbers are reported for context and carry no
ship-rule weight. Failure detail (error codes, root causes) is recorded for every failing task.

**Pooled context (observational, no ship-rule weight):** the combined sheet-vs-full counts over
the 12 tasks of this draw plus the salience draw are reported next to the verdict, labeled as
pooled-across-draws context. The decision above is taken on this draw alone.

## Pre-registered mechanism analysis — loaded-rule application (no ship-rule weight)

Same standard as the salience experiment, verbatim (experiment 5's recurrence standard: a hit
counts against a rule when the answer's defect is the rule a claim pins — same defect shape,
same fix, message matching up to answer-specific identifiers; template-match with a different
pinned rule and fix = loaded-rule-adjacent, counted separately):

- For every failing **pack-arm** row, classify each independent root cause as:
  loaded-rule-ignored (the rule is in that arm's payload), loaded-rule-adjacent, or untaught.
  Both pack payloads carry the same rule set, so denominators are comparable by construction;
  for the sheet arm, "in the payload" means the rule's sheet line.
- Independently, count `Lint W99001` occurrences per arm across ALL logs.
- Report both counts per arm in the README next to the failure detail. These are observational;
  they carry no ship-rule weight in either direction.
