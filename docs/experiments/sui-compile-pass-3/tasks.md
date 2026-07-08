# Held-out tasks — sui-move falsification, experiment 3 (pre-registered, deepening delta)

Deepening round 1 (`docs/deepening/round-1/`, merged PR #12) grew the pack 47 → 61 claims.
Its tier-1 remeasure numbers are tainted by construction (the failed tasks selected the beats).
This is the pre-registered tier-2 run: **does the deepening measurably improve the pack on fresh
held-out tasks?** **This file is committed before any answer is collected** — the commit
timestamp is the pre-registration. Operator sign-off for a third experiment: explicit request
2026-07-07 ("run the tier-2 falsification on the deepened pack").

## Question and arms

Three arms, identical prompts except the reference material:

- **base** — fresh context, ONLY the task text + the standard instruction. No pack, no docs, no tools.
- **kp47** — task text + instruction + the PRE-deepening pack payload, assembled from the pack as of
  master `82d55df` (pre-PR#12): `CONTEXT.md` + a `## Pack claims (all)` section listing every claim
  statement from `examples/sui-move.research.json` at that commit, sorted, one `- ` bullet each.
- **kp61** — same assembly rule applied to the current (deepened) pack at master `8c1a2e5`.

**The headline comparison is kp61 vs kp47** (the deepening delta). The base arm is contextual —
reported, not part of the ship rule — it keeps the base-vs-pack picture current for the probe model.

- Model, all arms: `claude-haiku-4-5` — the pack's falsification primary and the model whose
  compile-tier gaps round 1 targeted. (sonnet-4-6 probed 15/15 compile-pass with the pack loaded in
  round 1; a sonnet compile-pass metric would ceiling exactly as experiment 1 did.)
- Fresh context per task per arm; headless, no tools.
- Instruction (verbatim, same as the round-1 probe): *"Answer with the complete Sui Move source only
  (edition 2024), in a single ```move code block. No explanations, no tools. If the task asks for two
  modules, put both in the same code block."*

## Tasks

Six contract-authoring tasks. None appears as a pack fixture (fixture zones as of `8c1a2e5`:
struct visibility, method syntax, friend, implicit imports, key/UID, let-mut, object::new,
transfer/store, entry-vs-public, OTW init, capability, coin currency, dynamic fields, events, clock,
test_scenario, test_only, macros, receiving, abilities, use-Self, type-name, witness-naming,
key-field-store, dynamic-field-exists) and none restates a round-1 probe task or an experiment-1/2
task. Multi-concept difficulty calibrated to the round-1 probe band (where haiku passed 7/15).

1. **escrow-swap** — Write a module implementing a two-party atomic swap escrow. Party A creates an
   escrow offering a generic item (any object type with appropriate abilities) and naming a
   counterparty and the exact object type it wants in return is out of scope — instead: the escrow
   holds A's item, the counterparty deposits their item, and a `swap` function completes the
   exchange (each party receives the other's item). Either party can cancel before the swap
   completes and recover whatever they deposited. The escrow object itself must be cleaned up on
   both paths.
2. **english-auction** — Write a module implementing an English auction for a single item (declare a
   simple `Artifact` object type in the same module). Sellers start an auction as a shared object
   with a minimum bid in SUI. Bidders bid with `Coin<SUI>`; a higher bid refunds the previous
   highest bidder immediately. A `settle` function (callable by anyone after the seller closes
   bidding, or by the seller at any time) sends the item to the winner and the proceeds to the
   seller; if there were no bids the seller gets the item back.
3. **multisig-treasury** — Write a module implementing an M-of-N treasury: created with a fixed set
   of N owner addresses and a threshold M. Any owner can propose a withdrawal (amount + recipient);
   owners approve by address; once M distinct owners have approved, anyone can execute the
   withdrawal, which pays out from the treasury's SUI holdings. Proposals must be trackable while
   pending and unexecutable twice.
4. **loyalty-points** — Write a module implementing a closed-loop loyalty program: only the program
   operator (holder of an operator capability) can issue points to users; points must NOT be
   transferable between users (a user cannot send their points object to someone else); users redeem
   a fixed number of points for a `Reward` object, burning the points. Include issue, redeem, and a
   balance-merge convenience for a user holding two of their own point objects.
5. **epoch-vesting** — Write a module implementing a linear vesting wallet paid in SUI and measured
   in epochs (use the transaction context's epoch, not the Clock object): created with a
   beneficiary, a start epoch, and a duration in epochs; the beneficiary can claim at any time and
   receives the vested-so-far amount minus what was already claimed; after start+duration the full
   remainder is claimable.
6. **crowdfund** — Write a module implementing a crowdfunding campaign: a creator opens a campaign
   with a funding goal (in SUI) and a deadline epoch. Anyone contributes `Coin<SUI>` before the
   deadline; contributions are tracked per contributor. After the deadline: if the goal was met the
   creator claims the total once; if not, each contributor can reclaim exactly their contribution.

## Scoring protocol (identical to the round-1 probe)

- **Mechanical extraction (arm-neutral):** the first fenced code block is the source (whole answer
  if unfenced). No edits.
- **Scaffold repair (arm-neutral, pre-declared):** minimal `Move.toml` (edition 2024) binding every
  address name declared by the answer's own `module X::Y` lines to `0x0`; multi-module answers are
  gated as ONE package. No source is ever touched.
- Gate: plain `sui move build` with the pinned binary (`sui 1.74.1-8fc60f1fa966`). Committed
  buildlogs are ANSI-stripped and home-directory-redacted; verdicts computed from the stripped text.
- Layout: `answers/<task>/<arm>.answer` (raw), `<arm>-src.move`, `<arm>-pkg/` (scaffold),
  `<arm>.buildlog`, `<arm>.result`; summary in `results.txt`.

## Pre-registered metrics and ship rule

- **Primary — compile-pass:** the build exits 0. Count per arm over the 6 tasks.
- **Secondary — clean-compile:** the build exits 0 AND zero `warning[` lines.

**Ship rule for the deepening headline (decided before data):**

1. If kp61 compile-pass > kp47 compile-pass → **deepening improves the pack** (headline).
2. If primary ties and kp61 clean-compile > kp47 clean-compile → deepening improves the pack on the
   cleanliness axis (headline scoped to the secondary metric).
3. Anything else → no deepening headline on this evidence; the result is recorded as-is. If kp61 is
   BELOW kp47 on the primary, that is a regression and must be reported prominently, not buried.

No post-hoc metric may be substituted. Base-arm numbers are reported for context in all cases and
carry no ship-rule weight. Failure detail (error codes, whether any taught beat's error class
appears in any arm) is recorded for every failing task.
