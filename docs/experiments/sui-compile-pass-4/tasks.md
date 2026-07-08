# Held-out tasks — sui-move falsification, experiment 4 (pre-registered, deepening round-2 delta)

Deepening round 2 (`docs/deepening/round-2/`, merged PR #14) grew the pack 61 → 86 claims.
Its tier-1 remeasure numbers are tainted by construction (the failed tasks selected the beats).
This is the pre-registered tier-2 run: **does round 2 measurably improve the pack on fresh
held-out tasks?** **This file is committed before any answer is collected** — the commit
timestamp is the pre-registration. Operator sign-off for a fourth experiment: explicit blanket
authorization 2026-07-08 ("continue with merging 14 and all the way through a next round …
make sure to ralph loop review when you hit milestones").

## Question and arms

Three arms, identical prompts except the reference material:

- **base** — fresh context, ONLY the task text + the standard instruction. No pack, no docs, no tools.
- **kp61** — task text + instruction + the pre-round-2 pack payload, assembled from the pack as of
  master `da895f5` (post-PR#13, pre-PR#14): `CONTEXT.md` + a `## Pack claims (all)` section listing
  every claim statement from `examples/sui-move.research.json` at that commit, sorted (Python
  `sorted()`, byte order), one `- ` bullet each.
- **kp86** — same assembly rule applied to the round-2 pack at master `86989a1` (the PR #14 merge).

**The headline comparison is kp86 vs kp61** (the round-2 delta). The base arm is contextual —
reported, not part of the ship rule.

- Model, all arms: `claude-haiku-4-5` — the pack's falsification primary and the model whose
  compile-tier gaps round 2 targeted (sonnet-4-6 probed 15/15 compile-pass with the pack loaded
  in round 2; a sonnet compile-pass metric would ceiling as experiment 1 did).
- Fresh context per task per arm; headless, no tools.
- Instruction (verbatim, same as the round-1/round-2 probes and experiment 3): *"Answer with the
  complete Sui Move source only (edition 2024), in a single ```move code block. No explanations,
  no tools. If the task asks for two modules, put both in the same code block."*

## Tasks

Six contract-authoring tasks, module naming left free (as in experiment 3). Held-out audit run
**before** drafting was frozen — each task was checked against: the experiment 1 task list
(shared-counter, capped-token, soulbound-badge, escrow-swap, guestbook-clock), experiment 2
(flash-loan, object-mailbox, generic-vault, nft-display, kiosk-listing), experiment 3
(escrow-swap, english-auction, multisig-treasury, loyalty-points, epoch-vesting, crowdfund),
all 30 round-1/round-2 probe tasks, and the 31 fixture zones as of `86989a1`. Two draft
candidates were **dropped by that audit**: an on-chain name registry (restates probe task
modform-2) and a ticket vendor (restates probe task coinlint-2's vending machine). Multi-concept
difficulty calibrated to the probe band.

1. **rental-agreement** — Write a module implementing an object rental agreement. An owner lists
   a generic item for rent with a per-epoch price and a required deposit (both in SUI). A renter
   takes the rental by paying the deposit plus rent for a stated number of epochs up front; the
   item is held by the agreement while rented. The renter can return the item on time and recover
   the deposit (rent goes to the owner); if the rental period has elapsed without a return, the
   owner can reclaim the item AND keep the deposit. The agreement object must be cleaned up on
   both terminal paths.
2. **wager-arbiter** — Write a module implementing a two-party wager with a neutral arbiter. A
   creator opens the wager by staking `Coin<SUI>` and naming an opponent and an arbiter; the
   opponent joins by matching the stake exactly. Only the arbiter (via an arbiter capability
   issued at creation) can resolve the wager, sending the whole pot to the declared winner. If
   the opponent has not joined yet, the creator can cancel and recover the stake.
3. **subscription-service** — Write a module implementing a paid subscription registry. A service
   operator creates the shared registry with a price per period (in SUI) and a period length in
   epochs (use the transaction context's epoch, not the Clock object). Anyone can subscribe or
   extend an existing subscription by paying for one or more whole periods; the registry tracks
   each subscriber's paid-through epoch. Provide a read function reporting whether an address is
   currently active, and an operator-only withdrawal of accumulated fees.
4. **gift-card** — Write a module implementing merchant gift cards. A merchant issues a gift card
   object funded with SUI, locked to that merchant, and gives it to a customer. The customer can
   spend any partial amount at the issuing merchant (the spent amount goes to the merchant; the
   remainder stays on the card), top the card up with more SUI, or cash out the full remaining
   balance back to themselves, destroying the card. Spending at any other merchant address must
   be impossible by construction.
5. **crafting-forge** — Write a module implementing item crafting. The module declares two
   component object types (e.g. `Blade` and `Hilt`) with public mint functions, and a `Sword`
   crafted object. A `forge` function consumes exactly one of each component (destroying both)
   and produces a `Sword` recording how many total components were consumed to make it. Provide
   a `smelt` function that destroys a `Sword` and mints back both fresh components.
6. **dead-man-switch** — Write a module implementing an inactivity-triggered vault. An owner
   creates the vault with a SUI balance, a beneficiary address, and a timeout in epochs. The
   owner can check in at any time (resetting the inactivity clock), deposit more SUI, or withdraw
   any amount while active. Once more than the timeout number of epochs has passed since the last
   check-in, the beneficiary can claim the entire vault balance, closing the vault.

## Scoring protocol (identical to experiment 3)

- **Mechanical extraction (arm-neutral):** the first fenced code block is the source (whole answer
  if unfenced). No edits.
- **Scaffold repair (arm-neutral, pre-declared):** minimal `Move.toml` (edition 2024) binding every
  address name declared by the answer's own `module X::Y` lines to `0x0`; multi-module answers are
  gated as ONE package; answers declaring only bare `module name {` forms (no address name to bind)
  get an inert `probe = "0x0"` binding (the experiment-3 disclosed fallback, now pre-declared). No
  source is ever touched.
- Gate: plain `sui move build` with the pinned binary (`sui 1.74.1-8fc60f1fa966`). Committed
  buildlogs are ANSI-stripped and home-directory-redacted; verdicts computed from the stripped text.
- Layout: `answers/<task>/<arm>.answer` (raw), `<arm>-src.move`, `<arm>-pkg/` (scaffold),
  `<arm>.buildlog`, `<arm>.result`; summary in `results.txt`.

## Pre-registered metrics and ship rule

- **Primary — compile-pass:** the build exits 0. Count per arm over the 6 tasks.
- **Secondary — clean-compile:** the build exits 0 AND zero `warning[` lines.

**Ship rule for the round-2 headline (decided before data):**

1. If kp86 compile-pass > kp61 compile-pass → **round 2 improves the pack** (headline).
2. If primary ties and kp86 clean-compile > kp61 clean-compile → round 2 improves the pack on the
   cleanliness axis (headline scoped to the secondary metric).
3. Anything else → no round-2 headline on this evidence; the result is recorded as-is. If kp86 is
   BELOW kp61 on the primary, that is a regression and must be reported prominently, not buried.

No post-hoc metric may be substituted. Base-arm numbers are reported for context in all cases and
carry no ship-rule weight. Failure detail (error codes, whether any taught beat's error class —
from round 1 OR round 2 — appears in any arm) is recorded for every failing task.
