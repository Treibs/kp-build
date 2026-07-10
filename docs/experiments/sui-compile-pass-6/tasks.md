# Experiment 6 — held-out falsification of deepening round 4 (pre-registered)

**This file is committed BEFORE any answer is collected.** The commit that introduces it is
the pre-registration point; answers, results, and the verdict land in later commits. Operator
instruction 2026-07-09: "run the tier-2 falsifications for both packs" — the tier-2 run the
round-4 ledger recorded as due.

## Question and arms

Does deepening round 4 (pack 98 → 110 claims, PR #21) improve held-out contract authoring on
the pinned toolchain? Three arms, identical prompts except the reference material:

- **base** — task text + the standard instruction only. No pack. Contextual anchor for draw
  difficulty; **no ship-rule weight**.
- **kp98** — task text + instruction + the pre-round-4 payload, **reused byte-identical**
  from the committed artifact `docs/experiments/sui-payload-salience/payloads/payload-full.md`
  (49,656 bytes, sha256 `4a53c7dfeb198aaca6df579c39be2adb697e01d40eeb0ff89ea6e000d39fbc4b`) —
  the same bytes every prior kp98 arm used. Validity: the sui pack's payload inputs were
  unchanged from `04d7cba` through `a8cb8fc`; round 4 (merge `0cdb536`) is exactly what
  changed them, which is the delta under test.
- **kp110** — the post-round-4 payload, assembled from master `0cdb536`
  (`examples/sui-move/CONTEXT.md` + `## Pack claims (all)` + the `statement` strings from
  `examples/sui-move.research.json`, Python `sorted()` code-point order, one `- ` bullet
  each, trailing newline — the rule that reproduces the kp98 artifact byte-identically from
  its own inputs): **51,799 bytes, sha256
  `92756d2d7532318ffd16be0b87794141c185336ce6c324a1e0937b6602cfb812`**.

**The headline comparison is kp110 vs kp98** (the round-4 delta).

- Model, all arms: `claude-haiku-4-5` — the pack's falsification primary, continuous with
  experiments 3–5 and both payload draws. (An opus-tier arm was considered and deliberately
  deferred: it would break cross-experiment comparability mid-series and the recorded sonnet
  ceiling makes a stronger-model compile-pass ceiling likely; candidate for a separate
  experiment if the operator wants the top-model question answered.)
- Fresh context per task per arm; headless, no tools; collection from a neutral scratch
  working directory. Instruction (verbatim, same as experiments 2–5 and all probes): *"Answer
  with the complete Sui Move source only (edition 2024), in a single ```move code block. No
  explanations, no tools. If the task asks for two modules, put both in the same code
  block."*
- Prompt assembly for pack arms: task text, then the instruction, then a line
  `--- Reference pack (verified) ---`, then the payload.
- Gate: mechanical extraction (first fenced block), arm-neutral scaffold repair (minimal
  `Move.toml`, edition 2024, answer-declared address names bound to `0x0`, multi-module
  answers gated as ONE package), plain `sui move build` on the pinned binary
  (`sui 1.74.1-8fc60f1fa966`). Buildlogs committed ANSI-stripped and home-redacted.

## Metrics and ship rule (frozen)

- **Primary: compile-pass** (exit 0).
- **Secondary: clean-compile** (exit 0 with zero `warning[` lines).
- **Branch 1** — kp110 > kp98 on the primary → round-4 deepening improves held-out
  compile-pass; ships as the headline.
- **Branch 2** — primary tied AND kp110 > kp98 on the secondary → cleanliness improvement
  only; scoped headline.
- **Branch 3** — anything else → **no headline**; failure composition reported as
  observational only.
- n = 6; every number reported with its denominator; absolute numbers are not comparable
  across experiments (draw difficulty varies — recorded lesson of the salience/confirm pair).
- **Mechanism analysis (pre-registered):** taught-class recurrence under the strict
  experiment-5 standard — recurrence = same pinned rule and fix, message identical modulo
  identifiers; template-match with different rule/fix = loaded-rule-adjacent. Applied
  symmetrically across arms. Round-4 taught classes of special interest: E07001
  borrow-arg-alias, `+=`/`while`-parens E01002 shapes, `std::mem` E03002.

## Tasks

Six contract-authoring tasks, module naming left free (no pinned identifiers; the round-3
reserved-word check applies to any names the tasks do mention). Held-out audit run **before**
this freeze — each task was checked against: experiment 1 (shared-counter, capped-token,
soulbound-badge, escrow-swap, guestbook-clock), experiment 2 (flash-loan, object-mailbox,
generic-vault, nft-display, kiosk-listing), experiment 3 (escrow-swap, english-auction,
multisig-treasury, loyalty-points, epoch-vesting, crowdfund), experiment 4 (rental-agreement,
wager-arbiter, subscription-service, gift-card, crafting-forge, dead-man-switch), experiment
5 (allowance-vault, ballot-box, hash-riddle, insurance-pool, milestone-contract,
oracle-feed), the payload-salience draw (compliance-coin, grade-book, micro-amm,
payment-channel, rosca-circle, staking-pot), the sheet-confirm draw (bottle-deposit,
tournament-prize, freelance-invoice, layaway-plan, penalty-jar, warranty-registry), all 60
round-1/2/3/4 probe tasks, and the 39 fixture zones at `0cdb536`. **Six draft candidates were
dropped by that audit** (adjacency named): karaoke-queue (restates round-3 import-2's
deposit-waitlist), tool-lending (restates experiment 4's rental-agreement), split-bill
(restates experiment 3's crowdfund funding-goal-then-payout), quiz-bounty (restates
experiment 5's hash-riddle), frequent-flyer-miles (restates experiment 3's loyalty-points),
recycling-center (restates the sheet-confirm draw's bottle-deposit). One kept task carries a
disclosed adjacency: digest-notary shares "record an entry with a timestamp" with experiment
1's guestbook-clock and round-2's name registry, but differs in mechanics (fee-gated,
content-addressed dedup with abort, lookup by digest).

1. **book-club** — A shared book club: members join by paying one epoch's dues in SUI (a
   fixed amount), and must top up each epoch to stay current. Pooled dues accumulate in the
   club. The librarian (capability issued at creation) spends from the pool to acquire a
   `Book` (title, cost) which joins the club's shared shelf. Views: a member's paid-through
   epoch, the shelf size, and the pool balance.
2. **carbon-retire** — A carbon-credit registry: an issuer capability mints `CarbonCredit`
   objects carrying tonnage; credits transfer freely between holders. Any holder can
   permanently retire a credit they own: the credit is destroyed, a `RetirementReceipt`
   object goes to the retirer recording the tonnage and the credit's identity, an event is
   emitted, and a shared registry's running total of retired tonnage increases.
3. **passport-stamps** — An event passport: attendees mint themselves an empty `Passport`.
   Each venue holds a `VenueCap` (issued by the organizer) and stamps a passport presented to
   it — a passport can hold at most one stamp per venue (abort on a repeat). Once a passport
   carries 5 distinct stamps its holder redeems it for a `Badge` object; redemption consumes
   the passport.
4. **water-rights** — A reservoir ledger: a shared `Reservoir` holds an acre-feet balance,
   refilled by the commissioner (capability). Rights holders own `WaterRight` objects (issued
   by the commissioner) carrying a per-epoch allocation; a holder draws water against their
   right — total draws per right per epoch cannot exceed the allocation (abort), and the
   reservoir balance decreases by the draw (abort if insufficient).
5. **arcade-crown** — An arcade high-score game: players pay a fixed fee in SUI per play
   (fees pool for the operator to sweep). A player submits a score with their play; if it
   beats the standing record, the shared machine records the new champion and the `Crown`
   object passes to them — taken from the previous champion's custody in the machine and
   delivered to the new one (the crown lives in the machine between reigns, so it is always
   transferable).
6. **digest-notary** — A notary service: anyone pays a fixed fee to record a 32-byte document
   digest; the shared notary stores, per digest, who recorded it and the timestamp
   (milliseconds from the on-chain clock). Recording an already-recorded digest aborts.
   Views: the recorder and time for a digest (abort if absent), and the total number of
   recorded digests. The operator sweeps accumulated fees.

## Layout

`answers/<task>/{base,kp98,kp110}.answer` (verbatim), `-src.move` (first fenced block,
unedited), `-pkg/` (scaffold), `.buildlog` (stripped), `.result`
(`PASS CLEAN` / `PASS WARN<n>` / `FAIL <first error line>`); summary in `answers/results.txt`;
verdict + analysis in `README.md` (written after gating).
