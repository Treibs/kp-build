# Held-out tasks — sui-move falsification, experiment 5 (pre-registered, deepening round-3 delta)

Deepening round 3 (`docs/deepening/round-3/`, merged PR #16) grew the pack 86 → 98 claims.
Its tier-1 remeasure numbers are tainted by construction (the failed tasks selected the beats).
This is the pre-registered tier-2 run: **does round 3 measurably improve the pack on fresh
held-out tasks?** **This file is committed before any answer is collected** — the commit
timestamp is the pre-registration. Operator sign-off for a fifth experiment: explicit request
2026-07-08 ("run the pre-registered tier-2 experiment before any more pack work").

## Question and arms

Three arms, identical prompts except the reference material:

- **base** — fresh context, ONLY the task text + the standard instruction. No pack, no docs, no tools.
- **kp86** — task text + instruction + the pre-round-3 pack payload, assembled from the pack as of
  master `86989a1` (the PR #14 merge — byte-identical to experiment 4's kp86 arm): `CONTEXT.md` +
  a `## Pack claims (all)` section listing every claim statement from
  `examples/sui-move.research.json` at that commit, sorted (Python `sorted()`, byte order), one
  `- ` bullet each.
- **kp98** — same assembly rule applied to the round-3 pack at master `17f3210` (the PR #16 merge).

**The headline comparison is kp98 vs kp86** (the round-3 delta). The base arm is contextual —
reported, not part of the ship rule.

- Model, all arms: `claude-haiku-4-5` — the pack's falsification primary and the model whose
  compile-tier gaps round 3 targeted (sonnet-4-6 probed 13/15 with the pack loaded in round 3;
  its two valid failures were one task).
- Fresh context per task per arm; headless, no tools.
- Instruction (verbatim, same as experiments 3–4 and all probes): *"Answer with the complete Sui
  Move source only (edition 2024), in a single ```move code block. No explanations, no tools. If
  the task asks for two modules, put both in the same code block."*
- Prompt assembly for the pack arms (same as the round-1/2/3 probes): task text, then the
  instruction, then a line `--- Reference pack (verified) ---`, then the payload.
- **Protocol fix carried from experiment 4's disclosure:** the headless CLI is invoked from a
  neutral scratch working directory (not the repo), so no arm can inherit repo-name vocabulary
  from the process environment. Environment identical for all three arms.

## Tasks

Six contract-authoring tasks, module naming left free (as in experiments 3–4; no pinned
identifiers, so the round-3 reserved-word check is trivially satisfied). Held-out audit run
**before** drafting was frozen — each task was checked against: the experiment 1 task list
(shared-counter, capped-token, soulbound-badge, escrow-swap, guestbook-clock), experiment 2
(flash-loan, object-mailbox, generic-vault, nft-display, kiosk-listing), experiment 3
(escrow-swap, english-auction, multisig-treasury, loyalty-points, epoch-vesting, crowdfund),
experiment 4 (rental-agreement, wager-arbiter, subscription-service, gift-card, crafting-forge,
dead-man-switch), all 45 round-1/2/3 probe tasks, and the 35 fixture zones as of `17f3210`.
Four draft candidates were **dropped by that audit**: a rate-limited faucet (restates round-3
probe time-1 `faucet::drip` and round-2 modform-1's per-address rate limiter), a donor
matching-fund (restates round-3 probe import-3's `MatchPool`), a pawn-shop collateral loan
(adjacent to experiment 4's rental-agreement: item escrowed against SUI with an epoch deadline
and two terminal paths), and a revenue splitter (restates round-2 coinlint-3's `RoyaltyPool`
and modform-3's fee split). Multi-concept difficulty calibrated to the probe band.

1. **ballot-box** — Write a module implementing an on-chain ballot. A creator opens a shared
   ballot with a question and a fixed list of option labels (strings), and receives a closing
   capability. Any address can vote exactly once, for one option by index; double voting and
   out-of-range indices must abort. The capability holder can close the ballot, after which
   voting aborts. Provide read functions for the vote count of an option and for the index of
   the currently leading option.
2. **insurance-pool** — Write a module implementing a simple insurance pool. An operator creates
   the shared pool and receives an adjuster capability. Anyone can buy a policy by paying a
   premium in SUI (the premium joins the pool's reserves) and stating a coverage amount, subject
   to a pool-defined minimum premium; the buyer receives a policy object recording the holder
   address and coverage. Only the adjuster (via the capability) can approve a claim: the policy
   is consumed and destroyed, and a payout of at most the recorded coverage is paid from
   reserves to the recorded holder. The operator can withdraw reserves in excess of a stated
   float.
3. **hash-riddle** — Write a module implementing a hash-locked riddle bounty. A poser creates a
   shared riddle escrowing a SUI prize and storing the 32-byte hash digest of the secret answer.
   Anyone can attempt to solve by submitting answer bytes: if hashing the submission matches the
   stored digest, the solver receives the full prize and the riddle object is destroyed;
   otherwise the attempt aborts. If the riddle has gone unsolved for more than a stated number
   of epochs since creation, the poser (and only the poser) can reclaim the prize, also
   destroying the riddle.
4. **allowance-vault** — Write a module implementing a vault with a delegated spending allowance.
   An owner creates a shared vault funded with SUI and receives an owner capability. The owner
   can set (or replace) at most one active allowance naming a spender address and a per-epoch
   spending limit, and can clear it. The named spender can withdraw SUI from the vault subject
   to the limit: withdrawals within one epoch accumulate against the limit, and the spent
   counter resets when the epoch advances. The owner can withdraw any amount at any time,
   independent of the allowance.
5. **milestone-contract** — Write a module implementing milestone-based work payments. A client
   creates a contract naming a worker address and a list of milestone amounts, funding the full
   total in SUI up front. The client (and only the client) approves milestones strictly in
   order; each approval immediately pays that milestone's amount to the worker. After the final
   milestone is approved, the contract object must be cleaned up. The client can cancel at any
   point before completion: all not-yet-approved funds return to the client and the contract is
   cleaned up (already-approved payments stay with the worker).
6. **oracle-feed** — Write a module implementing a published price feed. A publisher creates the
   shared feed and receives a publisher capability. Only the capability holder can post a price
   update; the feed records the latest price and the epoch it was posted in, and emits an event
   for every update. Provide a read function taking a maximum acceptable age in epochs that
   returns the price but aborts if the latest update is older than that bound, and a second read
   function returning the raw (price, posted-epoch) pair without any staleness check.

## Scoring protocol (identical to experiments 3–4)

- **Mechanical extraction (arm-neutral):** the first fenced code block is the source (whole answer
  if unfenced). No edits.
- **Scaffold repair (arm-neutral, pre-declared):** minimal `Move.toml` (edition 2024) binding every
  address name declared by the answer's own `module X::Y` lines to `0x0`; multi-module answers are
  gated as ONE package; answers declaring only bare `module name {` forms (no address name to bind)
  get an inert `probe = "0x0"` binding. No source is ever touched.
- Gate: plain `sui move build` with the pinned binary (`sui 1.74.1-8fc60f1fa966`). Committed
  buildlogs are ANSI-stripped and home-directory-redacted; verdicts computed from the stripped text.
- Layout: `answers/<task>/<arm>.answer` (raw), `<arm>-src.move`, `<arm>-pkg/` (scaffold),
  `<arm>.buildlog`, `<arm>.result`; summary in `results.txt`.

## Pre-registered metrics and ship rule

- **Primary — compile-pass:** the build exits 0. Count per arm over the 6 tasks.
- **Secondary — clean-compile:** the build exits 0 AND zero `warning[` lines.

**Ship rule for the round-3 headline (decided before data):**

1. If kp98 compile-pass > kp86 compile-pass → **round 3 improves the pack** (headline).
2. If primary ties and kp98 clean-compile > kp86 clean-compile → round 3 improves the pack on the
   cleanliness axis (headline scoped to the secondary metric).
3. Anything else → no round-3 headline on this evidence; the result is recorded as-is. If kp98 is
   BELOW kp86 on the primary, that is a regression and must be reported prominently, not buried.

No post-hoc metric may be substituted. Base-arm numbers are reported for context in all cases and
carry no ship-rule weight. Failure detail (error codes, whether any taught beat's error class —
from the original pack, round 1, round 2, OR round 3 — appears in any arm) is recorded for every
failing task.

## Pre-registered observational analysis — vocabulary induction (no ship-rule weight)

Experiment 4 recorded a hypothesis it was not designed to test: the pack's idiom vocabulary
(Table, events, Balance, Clock, dynamic fields) prompts more ambitious designs whose extra API
surface creates failure opportunities the base answers never encounter (it fit 3 of 6 failing
pack-arm rows there). This experiment pre-registers the analysis method so it cannot be shaped
post hoc; it remains observational and carries no ship-rule weight:

- For every task × arm, record the answer's line count and its used-API-surface set: which of
  {`sui::table`, `sui::event`, `sui::balance`, `sui::clock`, `sui::dynamic_field` /
  `sui::dynamic_object_field`, `sui::package`/OTW display} the extracted source references.
- For every **failing pack-arm row**, record (a) whether the root-cause error sits on API surface
  in that set, and (b) whether the base answer for the same task used that surface at all.
  A row supports the hypothesis iff the root cause is on pack-named surface the base answer
  avoided while base passed.
- Report the counts (rows fitting / not fitting) in the README next to the failure detail, for
  both pack arms, alongside the same census for base failures (which the hypothesis predicts
  should not show the pattern).
