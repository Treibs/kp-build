# Experiment 9 — held-out falsification of deepening round 7 (pre-registered)

**This file is committed BEFORE any answer is collected.** The commit that introduces it is
the pre-registration point; answers, results, and the verdict land in later commits.
Operator delegation 2026-07-11 (rounds 8–11 + the tier-2 cadence the skill mandates); this
is the tier-2 the round-7 ledger recorded as owed. **Round 7 is the first
frequency-method-of-record round** (beats selected from the cumulative held-out ledger per
the exp-7/exp-8 verdict pair, not from its own probe) — this experiment is that method's
first post-adoption falsification.

## Question and arms

Does deepening round 7 (pack 134 → 149 claims, PR #30, merge `bad7b96`) improve held-out
contract authoring on the pinned toolchain? Three arms, identical prompts except the
reference material:

- **base** — task text + the standard instruction only. No pack. Contextual anchor for draw
  difficulty; **no ship-rule weight**.
- **kp134** — the pre-round-7 payload, regenerated from the canonical rule at master
  `cf492b1` and verified byte-identical to exp-8's pinned artifact: **56,464 bytes, sha256
  `9d4e6fe8a69abf15453a940455ce0616f78beea84dfbf368bbf3905859c89bff`**.
- **kp149** — the post-round-7 payload, assembled from master `bad7b96` by the canonical
  series rule (`examples/sui-move/CONTEXT.md` + `\n## Pack claims (all)\n` + the
  `statement` strings from `examples/sui-move.research.json`, Python `sorted()` code-point
  order, one `- ` bullet each, trailing newline): **59,916 bytes, sha256
  `d138fae7ea00283c04d822926017a1ac852b3bd52cc4b82f0584a0fb1711bfc0`**. Disclosure: the
  round-7 tier-1 remeasure used a one-newline assembly variant (sha `6c3f3bc2…`, same
  bytes otherwise — diffed and documented in that remeasure); this experiment uses the
  canonical rule, whose sha is recorded there.

**The headline comparison is kp149 vs kp134** (the round-7 delta).

- Model, all arms: `claude-haiku-4-5` — the pack's falsification primary, continuous with
  experiments 3–8 and all probe rounds.
- Fresh context per task per arm; headless, no tools; collection from a neutral scratch
  working directory. Instruction (verbatim, same as experiments 2–8 and all probes):
  *"Answer with the complete Sui Move source only (edition 2024), in a single ```move code
  block. No explanations, no tools. If the task asks for two modules, put both in the same
  code block."*
- Prompt assembly for pack arms: task text, then the instruction, then a line
  `--- Reference pack (verified) ---`, then the payload.
- Gate: mechanical extraction (first fenced block), arm-neutral scaffold repair (minimal
  `Move.toml`, edition 2024, answer-declared address names bound to `0x0`, multi-module
  answers gated as ONE package), plain `sui move build` on the pinned binary
  (`sui 1.74.1-8fc60f1fa966`). Buildlogs committed ANSI-stripped and home-redacted.
  Import sweep (point #5): the committed checker
  (`docs/experiments/sui-import-elicitation/check_import.py`) on every answer.

## Metrics and ship rule (frozen)

- **Primary: compile-pass** (exit 0).
- **Secondary: clean-compile** (exit 0 with zero `warning[` lines).
- **Branch 1** — kp149 > kp134 on the primary → round-7 deepening improves held-out
  compile-pass; ships as the headline.
- **Branch 2** — primary tied AND kp149 > kp134 on the secondary → cleanliness improvement
  only; scoped headline.
- **Branch 3** — anything else → **no headline**; failure composition reported as
  observational only.
- n = 6; every number reported with its denominator; absolute numbers are not comparable
  across experiments (draw difficulty varies).
- **Mechanism analysis (pre-registered, strict experiment-5 standard):** taught-class
  recurrence — recurrence = same pinned rule and fix, message identical modulo identifiers;
  template-match with different rule/fix = loaded-rule-adjacent; applied symmetrically
  across arms. Round-7 taught classes of special interest: `tuple-bleed` (E04004 tuple
  shapes in type-argument/storage position), `std-table-path` (E03002 `use std::table`),
  `balance-api-on-coin` (E04007 `coin::take`/`coin::put` on a `Coin`), `std-option-path`
  (E03002 `use sui::option`), `moved-value-arg-order` (E06002 move-then-read across
  argument positions). Also pre-registered as observational: `underscore-discard` (the
  round-7 ledger's new vcp sub-shape), `branch-type-mismatch` (×2, carried unpromoted),
  the ignored-while-loaded application ledger (`use-self` et al.), and the import sweep.

## Tasks

Six fresh contract-authoring tasks, audited against the **179** prior tasks (164 at the
round-7 audit + round-7's 15 probes) and the **52** fixture zones at `bad7b96` (97 fixture
directories = 45 red/green pairs + 7 green-only), with the standing pre-freeze reviewer
pass (record below, before any answer).

1. **left-luggage** — A station's left-luggage office: travelers deposit bags free of
   charge — each bag records a label and the traveler's forwarding address. The office
   keeps a courier fund in SUI; anyone may top the fund up at any time. The clerk
   (capability) forwards bags one at a time, in any order the clerk picks: the bag is
   delivered to the forwarding address recorded on it, the posted courier fee (fixed at
   creation) is paid out of the fund to a courier address the clerk names per forwarding,
   and a `Forwarded` event carries the bag's label and its forwarding address. Forwarding
   when the fund holds less than the fee aborts. Views: bags held; whether the fund covers
   at least one more forwarding.
2. **drying-room** — A pottery studio's drying room: a wall of shelf slots identified by
   bay number and shelf number together. A member sets a greenware record at an empty slot
   — the slot records the piece's title and the member; setting at an occupied slot
   aborts. A member may move their own record to a different empty slot, and may take it
   down at any time (only the member who set a record may move or take it down).
   Views: the title and owner together of the piece drying at a given bay and shelf
   (aborts for an empty slot); how many pieces are drying.
3. **repair-cafe** — A repair café: a visitor drops off a broken item (description
   recorded, owner recorded), paying the posted diagnosis fee in SUI (the exact amount;
   anything else aborts) into the café's fund. Each registered fixer has a workbench that
   holds at most one item at a time — vacant between jobs; the floor manager (capability)
   registers fixers, moves a dropped-off item onto an idle fixer's bench (an occupied
   bench aborts), and marks a bench's job finished: the finished item is delivered back to
   the owner recorded on it and the bench goes vacant. Views: whether a fixer's bench is
   occupied and the item's description when it is; the café fund balance.
4. **barn-dance** — A barn-dance contest: couples enter as a pair of dancer addresses,
   paying one fixed entry fee in SUI per couple (the exact
   amount; anything else aborts) into the purse; a dancer may appear in at most one
   standing couple (a duplicate aborts). The caller (capability) eliminates couples one at
   a time (eliminating when one or no couples remain aborts); when exactly one couple
   remains the caller closes the contest: the prize amount posted at creation is paid out
   of the purse to each member of the winning couple (two payments; a purse that cannot
   cover both aborts), and whatever remains stays in the purse for the hall. Closing while
   more than one couple still stands aborts; entering after the close aborts. A sponsor
   may top the purse up at any time. Views: couples still standing; purse balance.
5. **cheese-cave** — A co-op cheese cave: makers shelve wheels (label + ready epoch; the
   wheel records its maker) at no charge. At or after a wheel's ready epoch, the affineur
   (capability) releases it: the wheel is delivered back to the maker recorded on it and a
   `Ripened` event carries the maker and the label; releasing early aborts. The cave also
   tracks, per maker, how many wheels they currently have resting. Views: a maker's
   resting count; the label and ready epoch together of the oldest wheel still resting (by
   earliest ready epoch), when the cave is not empty.
6. **community-sauna** — A community sauna: bathers pay for a session in SUI — the posted
   price or more; any overpayment above the price returns to the bather as change in the
   same call, and the price portion joins the sauna's takings. The stove watch is
   optionally staffed: the owner (capability) seats a watcher (address) or ends the watch,
   and the slot is vacant between watches; a session bought while the watch is vacant
   aborts. The owner may sweep the whole takings at any time. Views: the current watcher
   when one is seated; sessions sold; takings balance.

## Per-class carrier map (pre-registered so fragility is visible)

- `tuple-bleed` E04004 → **barn-dance** (the couples themselves — pair-of-addresses
  storage), **drying-room** (the bay/shelf composite key in type-argument position is the
  real bait; the title/owner pair view is weak — it aborts on empty, so a bare tuple
  return is legal there).
- `std-table-path` E03002 → **drying-room** (the slot registry), **cheese-cave** (per-maker
  resting counts), **left-luggage** (weak — held bags may be keyed or held as a
  collection).
- `balance-api-on-coin` E04007 → **left-luggage** (top-up IN + per-forwarding fee draw
  OUT — the put and take baits), **barn-dance** (sponsor top-up + posted prize paid out of
  the purse ×2).
- `std-option-path` E03002 → **repair-cafe** (vacant-between-jobs bench, sui::-crowded
  imports), **community-sauna** (vacant-between-watches slot, sui::-crowded imports).
- `moved-value-arg-order` E06002 → **left-luggage** (deliver bag to the forwarding address
  recorded on it + `Forwarded` event reading the bag's fields), **cheese-cave** (deliver
  wheel to the maker recorded on it + `Ripened` event), **repair-cafe** (weaker — deliver
  item to recorded owner, no event required).
- Observational: `branch-type-mismatch` → community-sauna (exact-or-change branch);
  `underscore-discard` → left-luggage (removing the forwarded bag from the held
  collection); import sweep SUI carriers: left-luggage, repair-cafe, barn-dance,
  community-sauna (4 of 6; drying-room and cheese-cave are coin-free).

## Held-out audit (run before the freeze)

Reserved-word check on every pinned identifier (`Forwarded`, `Ripened`): none reserved,
none prelude-colliding. Adjacency disclosures (differs-clause each):

- left-luggage ≈ round-5 vde-1 mailroom / exp-8 ferry-manifest disembark on the
  deliver-to-recorded-address leg — this is the pre-registered `moved-value-arg-order`
  carrier, so class adjacency is by design; the spine differs on every other axis: deposit
  is free (no fee-per-item into a pool), delivery is single-item on the clerk's pick
  (never a batch drain), and the money flow is OUTBOUND per delivery (a courier fee from a
  communal fund to a third address named per call, plus open top-ups) rather than inbound
  fees swept. Also ≈ round-6 mva-1/mva-2 on the single-item forwarding spine and the
  `Forwarded` event schema (kept per the exp-8 wine-cellar precedent — the round-under-
  test's own eliciting family is re-elicited by design under the frequency method; differs:
  per-forwarding fee payout from the fund, open top-ups, the covers-one-more view; no
  manifest total, no blocklist). The fund mechanics are nearest round-5 api-2's engraver
  treasury (differs: the paid third party is named per call, not a fixed engraver;
  the paid-for act is forwarding custody out, not minting). Views: "bags held" is vde-1's
  waiting-count shape (disclosed); the fund-covers-one-more boolean is fresh. Story tier
  only: ≈ round-3 generic-2 lost-and-found office (differs: bags forward OUT to the
  recorded address; no receipt object, no claim-retrieval leg).
- drying-room ≈ round-7 sop-2 aquarium at the slotted-wall tier (differs: slots are
  member-self-managed — set, move-own, take-down-own — with NO capability and no
  stock/retire/storage custody; lookups abort on empty rather than answer optionally; the
  key is a two-part coordinate, the tuple carrier) and ≈ round-4 rapi-1 at the
  ordered-pair-keying tier (the composite-key precedent; differs: coordinates key slot
  records, not a relation between two parties) and ≈ elicitation I-2
  community-garden / round-7 stp-1 campground / exp-7 stall-rental at the
  numbered-public-slots tier (differs: no tenure, no fee, no booking economics — the
  record is per-piece data, placed and removed by its own author) and ≈ round-6 opt-2 at
  the negation tier only (no assignment by capability).
- repair-cafe ≈ round-7 mva-1 ski-valet (item custody + delivery home to the recorded
  owner; differs: the settlement economics are gone entirely — a flat exact diagnosis fee
  is paid at drop-off into the fund, no deposit rides with the item, nothing is split or
  refunded at delivery) and ≈ round-5 vde-1 on the reworked drop-off leg (flat exact fee
  per drop-off into a pool + an item carrying its recorded recipient; differs: delivery is
  bench-mediated by a manager-finish, never a batch drain, and the fee is for a service,
  not postage held against dispatch) and ≈ round-7 sop-2 aquarium (occupied/vacant slots under a
  capability; differs: benches are keyed by fixer address not numbered, the occupant
  arrives from a public drop-off queue and leaves the system to its owner — never moved
  slot-to-slot or to storage) and ≈ round-6 opt-2 / exp-8 plant-clinic at the
  optional-record tier (differs: object custody on the bench, not a data record) and ≈
  elicitation I-3 pet-daycare on the check-in-custody-with-owner-tag leg (differs: fee at
  drop-off not exit; a third-party fixer works the item; manager-mediated placement).
- barn-dance ≈ round-7 bac-2 dunk-tank (pool + payout-from-pool + top-up-in; differs:
  one-shot close paying a fixed amount to EACH of two winners vs per-hit instant prize;
  pair entries — the tuple carrier — have no dunk-tank analogue) and ≈ sheet-confirm
  tournament-prize (enter-with-exact-fee-before-start + capability-declared outcome +
  pool payout; differs: progressive one-at-a-time elimination of standing couples vs a
  three-way 50/30/20 percentage split declared at once; a fixed posted prize × 2 equal
  payments; remainder stays in the purse; no cancel/refund path; sponsor top-ups) and ≈
  elicitation I-7 marathon (register-with-fee-then-close; differs: pair entries,
  elimination, prize payout).
- cheese-cave ≈ exp-8 wine-cellar (member-stocked custody + oldest-item view; differs:
  epoch-gated release DELIVERED by capability to the recorded maker — the mva carrier —
  vs member unracking their own bottle; per-maker counts — the stp carrier — vs a reserve
  list; no membership economics) and ≈ round-7 mva-2 consignment on the
  return-to-recorded-address-with-event leg (same class by design; differs: the trigger is
  a per-wheel epoch gate with early-abort, not a season's-end return of unsold lots; the
  event carries the item's own label, not an unmet reserve) and ≈ round-7 mva-3 interloan
  at the per-key-count-that-decrements tier (differs: count keyed by maker with no
  acknowledge round-trip) and ≈ round-3 time-3 harvest farm on the epoch-maturation gate
  with early-abort (differs: maturation releases custody to a recorded party, not a
  harvest yield) and ≈ round-7 tb-1 at the pair-if-any view tier (oldest-wheel view;
  disclosed for completeness).
- community-sauna ≈ round-5 vcp-3 barber shop (a staffed/unstaffed state gating the sale
  path; differs: the watch is an `Option`-shaped seat filled/ended by the OWNER's
  capability vs a barber self-marking in/out per epoch; a vacant watch ABORTS the sale vs
  turning the customer away with a refund; exact-or-change payment vs exact-only) and ≈
  round-7 sop-3 night pharmacy (optional duty slot; differs: no retainer economics, no
  dispatch event, the slot gates a SALE path) and ≈ round-7 sop-1 lighthouse (a station
  watch that is vacant between occupants; differs: no clock stamp, no handover event, no
  self-handover — only the owner seats/ends — and the slot's only consequence is gating
  sales) and ≈ round-4 paywall / exp-7 charging-station at the pay-fixed-fee tier
  (differs: the exact-or-change branch and the watch gate).

**Same-round diversity check:** the three custody tasks differ in spine (single-item
forwarding on the clerk's pick / managed bench assignment with drop-off queue /
epoch-triggered release); the three money tasks differ in outflow (per-forwarding fee to a
named third party / fixed prize × 2 at one close / change-making at sale); the two keyed
registries differ in key domain (two-part coordinates / maker addresses) and management
(self-managed records / capability-released custody). No two tasks share a headline
mechanic. Same-round noun check: bench appears only in repair-cafe, purse only in
barn-dance, takings only in community-sauna ("till" was dropped in review round 1 as
arm-asymmetric vocabulary, see below). One shared noun is accepted on genericity (review
round 2): "fund" names the money container in both left-luggage and repair-cafe and occurs
in payload text of both arms — it is corpus-generic across the series (crowdfund, candy
fund) and does not meet the distinctive-noun bar that killed "till" (a kp149-ONLY fixture
module name); recorded rather than renamed.

## Pre-freeze audit review (the standing step; ran before this freeze)

**Round 1 returned REVISE** (independent adversarial reviewer, full checklist: restatement
sweep over all 179 prior tasks + 52 fixture zones, carrier-map soundness, arm-neutrality,
denominators, payload pins, leak scan). Findings and dispositions, all applied before this
freeze:

- **REPLACED: glass-studio** (kiln queue) — spine restated round-5 vde-1 mailroom
  point-for-point (fee-per-deposit into a pool, capability batch-drains every item to its
  recorded address, identical two views) with vde-3's per-item event inside the drain
  loop; disqualifying aggravator: vde-1 is a recorded RED seed of the very
  `moved-value-arg-order` beat under test, so a kp149 win there would measure replay of
  the beat's eliciting story. Replaced by **left-luggage** (free deposit, single-item
  clerk-picked forwarding, outbound per-delivery courier fee from a toppable fund,
  different views).
- **REPLACED: birdhouse-trail** — a fusion re-skin of two round-7 probes (the round under
  test): stp-3 apiary's assign-person-to-numbered-station-who-logs-data spine + tb-2 seed
  vault's best/latest-pair-if-any view with a readings count; the draft's own
  differs-clause against stp-3 was itself tb-2's shape, undisclosed. Replaced by
  **drying-room** (self-managed composite-key slot records, no capability, no
  assignment).
- **RE-SKINNED: repair-cafe** — the settlement leg (fee kept from deposit, rest refunded,
  item home to recorded owner) restated round-7 mva-1 ski-valet's story on the very leg
  the mva class is pre-registered; economics decoupled to a flat exact drop-off fee with
  no deposit and no split. The bench leg's round-7 sop-2 adjacency was undisclosed — now
  disclosed with differs; who-may-finish, fee exactness, occupied-bench abort, and fixer
  registration all tightened.
- **FIXED: community-sauna** — the draft's audit claim "exists in no prior till task" was
  false (round-5 vcp-3 barber shop gates sales on staffing); vcp-3 and sop-1 now
  disclosed. **Arm-asymmetric vocabulary removed:** the draft's headline noun "till"
  appears verbatim in kp149's round-7 `balance-api-on-coin` claim text and fixture module
  and in round-7 probe bac-1, and zero times in kp134's claims — renamed to "takings"
  (fresh across the corpus; "drawer" rejected — round-6 ctx-2 petty-cash `Drawer`).
  Undefined "at close" sweep replaced with "at any time".
- **DISCLOSED + TIGHTENED: barn-dance** — the tournament-prize differs-clause
  mischaracterized that task ("bracket seeding" — it has none; its real mechanics are
  ranked 50/30/20 split with cancel path) — rewritten from the sheet-confirm text; abort
  clauses added (duplicate dancer, eliminate at ≤1, close at >1, purse short of two
  payments, entry after close, exact fee).
- **DISCLOSED: cheese-cave** — round-7 mva-2 (return-to-recorded-address + event; the
  draft's `Released` event echoed mva-2's `Returned` schema — renamed `Ripened`),
  round-7 mva-3 (per-key decrementing count), round-3 time-3 (epoch-maturation gate with
  early-abort), round-7 tb-1 (pair-if-any view) all added with differs.
- **REBUILT: the per-class carrier map** to match the replacements (above); `tuple-bleed`
  regained two carriers (barn-dance storage + drying-room key/view), `std-table-path`
  holds three (drying-room, cheese-cave, left-luggage weak), `underscore-discard`'s
  carrier moved to left-luggage.
- Reviewer confirmations kept: denominators (179 tasks recounted = 105 probes + 46
  experiment + 6 salience + 6 sheet-confirm + 16 elicitation; 52 zones = 97 dirs = 45
  pairs + 7 green-only), both payload pins verified against exp-8 tasks.md and the round-7
  remeasure, instruction continuity with exps 3–8, reserved words clean, leak scan clean.

**Round 2 (on the two replacement tasks + re-skin, before this freeze) returned REVISE at
disclosure/clause tier only** — no REPLACE findings, no protocol-symmetry breakers; the
replacements and the re-skin were judged structurally sound. All eight findings applied
before this freeze:

- left-luggage: round-6 mva-1/mva-2 disclosed (single-item forwarding spine + `Forwarded`
  event schema; kept per the exp-8 wine-cellar precedent — the frequency method re-elicits
  the class family by design); the fund-mechanics comparison corrected from round-3
  import-3 MatchPool to round-5 api-2 engraver treasury (the nearer precedent); the views
  claim fixed ("bags held" IS vde-1's waiting-count shape — only the covers-one-more
  boolean is fresh); round-3 generic-2 lost-and-found disclosed at story tier.
- repair-cafe: the reworked drop-off leg's vde-1 adjacency (flat exact fee + recorded
  recipient) disclosed.
- drying-room: round-4 rapi-1 disclosed as the ordered-pair-keying precedent; "takes it
  down when the piece has dried" tightened to "may take it down at any time"; the carrier
  map corrected — the pair VIEW is weak (aborts on empty make a bare tuple return legal),
  the composite KEY is the real bait.
- barn-dance: the unpinned "before the music starts" entry-close implication deleted
  (entry gating is fully carried by "entering after the close aborts").
- Same-round noun check corrected: the shared generic "fund" (left-luggage, repair-cafe)
  accepted on genericity and recorded above, per the reviewer's judgment that it does not
  meet the distinctive-noun bar that killed "till".
- Reviewer round-2 confirmations: "takings" absent from both payloads' inputs and all 179
  prior tasks; the till-asymmetry record accurate; kp149-only distinctive-vocabulary sweep
  clean over all six task texts; carrier map otherwise sound; round-1 record faithful.

## Layout

`answers/<task>/{base,kp134,kp149}.answer` (verbatim), `-src.move` (first fenced block,
unedited), `-pkg/` (scaffold), `.buildlog` (stripped), `.result`
(`PASS CLEAN` / `PASS WARN<n>` / `FAIL <first error line>`), `.import`; summary in
`answers/results.txt`; verdict + analysis in `README.md` (written after gating).
