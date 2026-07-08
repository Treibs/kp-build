# Payload-salience experiment — sui-move pack (pre-registered)

Experiments 4 and 5 recorded two consecutive no-headline results for pack growth (61 → 86 → 98
claims), and experiment 5's sharpest finding was that **8 pack-arm defect events were rules
literally present in the loaded payload** (3 loaded-rule-ignored classes in kp86; W99001 ×3 plus
2 loaded-rule-adjacent events in kp98). The recorded diagnosis: the binding constraint is rule
**salience** at answer time, not rule **coverage**. This experiment tests that diagnosis
directly: same 98 claims, same tasks, same model — only the **form of the loaded payload**
varies. **This file is committed before any answer is collected** — the commit timestamp is the
pre-registration. Operator sign-off: explicit request 2026-07-08 ("run the payload-salience
experiment"), choosing the salience fork recorded in the experiment-5 README over a content
round 4.

## Question and arms

Four arms, identical prompts except the reference material. All pack arms load the SAME
98-claim pack (master `04d7cba`; claims unchanged since `17f3210`) — the arms differ only in
payload form. The payload files are committed under `payloads/` at pre-registration time and
pinned by SHA-256:

- **base** — task text + the standard instruction only. No pack. Contextual anchor for draw
  difficulty; no ship-rule weight.
- **full** — the standard payload assembly used by experiments 3–5 and all probes: `CONTEXT.md`
  + a `## Pack claims (all)` section with every claim statement, sorted, one bullet each.
  **Byte-identical to experiment 5's kp98 payload** (verified by diff at assembly time).
  `payloads/payload-full.md`, 49,656 bytes,
  sha256 `4a53c7dfeb198aaca6df579c39be2adb697e01d40eeb0ff89ea6e000d39fbc4b`.
- **slim** — mechanical redundancy removal, zero editorial judgment: the SAME sorted claim
  statements, one bullet each, once — the `CONTEXT.md` briefing (which restates most claims a
  second time in prose + a third time in blockquotes, plus pins/refresh material irrelevant at
  answer time) is dropped, replaced by a two-line header. Every statement in slim appears
  verbatim in full. `payloads/payload-slim.md`, 24,519 bytes,
  sha256 `9cf4a06cc55d55f954d9276d096ac7bee25f4fb9a506f5681f0f6ef546a8dd90`.
- **sheet** — hand-compressed cheat sheet: one imperative line per fixture rule (37 lines,
  grouped by category), each line derived 1:1 from pack claims with the broken form and the
  observed error code; **no fact appears on the sheet that is not in the pack's claims**
  (auditable line-by-line against the claim statements). This arm intentionally confounds two
  things — imperative form AND content compression (verbatim message fragments and doc-claim
  nuance are dropped) — so a sheet win alone cannot separate form from brevity; the slim arm is
  the control that isolates pure redundancy removal. `payloads/payload-sheet.md`, 5,887 bytes,
  sha256 `19a42c4dccc5a4454c9503f7da4ce8f9b8e123d317685c922b63d6d28cfd8bd0`.

**The headline comparisons are slim vs full and sheet vs full** (two comparisons — disclosed
multiplicity; with n=6 per arm the ≥+2 threshold below is the guard against celebrating draw
noise across two chances).

- Model, all arms: `claude-haiku-4-5` — the pack's falsification primary, the model whose
  loaded-rule-ignored events motivated this experiment.
- Fresh context per task per arm; headless, no tools; neutral scratch working directory
  (experiment-4 protocol fix); environment identical across arms.
- Instruction (verbatim, same as experiments 3–5 and all probes): *"Answer with the complete Sui
  Move source only (edition 2024), in a single ```move code block. No explanations, no tools. If
  the task asks for two modules, put both in the same code block."*
- Prompt assembly for pack arms (same as experiments 3–5): task text, then the instruction, then
  a line `--- Reference pack (verified) ---`, then the payload.

## Tasks

Six contract-authoring tasks, module naming left free (no pinned identifiers; the round-3
reserved-word check is trivially satisfied). Held-out audit run **before** this file was
frozen — each task was checked against the experiment 1–5 task lists (28 tasks), all 45
round-1/2/3 probe tasks, and the fixture zones as of `04d7cba`. Two draft candidates were
**dropped by that audit**: a name registry with fees and expiry (restates round-2 probe
modform-2's name registry) and a custody/handoff chain (restates round-3 probe generic-3's
relay-baton). Multi-concept difficulty calibrated to the experiment 4–5 band.

1. **micro-amm** — Write a module implementing a minimal two-asset swap pool. Anyone can create
   a shared pool for a pair of coin types by depositing initial reserves of both assets and
   fixing a swap fee in basis points; the creator receives a pool capability. Anyone can swap
   one asset for the other at the constant-product price, with the fee retained in the pool's
   reserves; a swap whose computed output is zero must abort. The capability holder can add to
   the reserves at any time, and can close the pool, receiving both remaining reserves; the pool
   object must be cleaned up on close. Provide a read function returning the two current reserve
   amounts.
2. **staking-pot** — Write a module implementing single-asset staking with per-epoch rewards. An
   operator creates a shared pot, funding a reward reservoir with SUI and fixing a per-epoch
   reward rate in basis points. Anyone can stake SUI; the staker receives an owned position
   object recording the staked amount and the epoch the stake began. Unstaking consumes the
   position and pays out the principal plus a reward of amount × rate × full-epochs-elapsed /
   10_000, drawn from the reservoir; unstaking aborts if the reservoir cannot cover the reward.
   The operator can top up the reservoir at any time. Provide a read function for the current
   reservoir balance.
3. **rosca-circle** — Write a module implementing a rotating savings circle. A coordinator
   creates a shared circle with a fixed ordered list of member addresses and a fixed per-round
   contribution amount in SUI. In each round, every member must contribute exactly the
   contribution amount; contributing twice in the same round aborts, and non-members cannot
   contribute. Once all members have contributed, anyone can trigger the payout: the entire pot
   is paid to the member whose turn it is, rotating through the list in order, and the next
   round begins. After every member has received exactly one payout, the circle is complete and
   the circle object must be cleaned up.
4. **compliance-coin** — Write a module implementing a regulated token. In the module
   initializer, create a new currency with 9 decimals and symbol "REG"; the publisher receives
   the treasury and a separate compliance capability. The compliance capability holder can
   freeze and unfreeze addresses, and freeze status must be queryable. The treasury holder mints
   tokens to a recipient, aborting if the recipient is frozen. Provide a guarded transfer entry
   function that sends a REG coin to a recipient, aborting if either the sender or the recipient
   is frozen.
5. **grade-book** — Write a module implementing an instructor's grade book. An instructor
   creates a shared grade book for a course and receives an instructor capability. The
   capability holder registers assignments, each with a name and a maximum score. Only the
   capability holder can record a student's score for an assignment: recording aborts if the
   score exceeds the assignment's maximum or if that student already has a score for that
   assignment. Corrections go through a separate amend function (capability-gated) that replaces
   an existing score and must emit an event carrying the student address, the assignment index,
   and the old and new scores. Provide read functions for a student's total across all
   assignments and for whether a student has a recorded score for a given assignment.
6. **payment-channel** — Write a module implementing a two-party payment channel. An opener
   creates a channel naming a counterparty and depositing SUI; the counterparty joins by adding
   their own deposit. Before the counterparty joins, the opener can cancel and recover the
   deposit. Once joined, either party can propose a cooperative close as a split of the total
   between the two parties (the two amounts must sum to the total); the other party accepts the
   proposal, funds are paid out per the split, and the channel is cleaned up. A pending proposal
   can be withdrawn by its proposer. Independently, once more than a stated number of epochs
   have passed since the channel opened, either party can force a close that refunds each party
   exactly their own deposit.

## Scoring protocol (identical to experiments 3–5)

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
- **Secondary — clean-compile:** the build exits 0 AND zero `warning[` lines.

**Ship rule for the salience headline (decided before data):**

1. If slim or sheet compile-pass ≥ full compile-pass + 2 → **payload form matters** (salience
   headline); adopt the winning form as the recommended load format. If both clear the bar, the
   higher count wins; on a tie between them, the shorter payload (sheet) wins on cost.
2. If neither clears branch 1, and a treatment arm is ≥ full on the primary AND ≥ full + 2 on
   the secondary → headline scoped to the cleanliness axis (salience moves warning-tier rule
   application).
3. Anything else → no salience headline on this evidence; the result is recorded as-is. If a
   treatment arm is ≤ full − 2 on the primary, that is evidence AGAINST payload slimming (the
   redundancy may be load-bearing) and must be reported prominently, not buried.

No post-hoc metric may be substituted. Base-arm numbers are reported for context and carry no
ship-rule weight. Failure detail (error codes, root causes) is recorded for every failing task.

## Pre-registered mechanism analysis — loaded-rule application (no ship-rule weight)

The salience hypothesis predicts the treatment arms show **fewer loaded-rule-ignored events**
than full, not merely more passes. Using experiment 5's recurrence standard verbatim (a hit
counts against a rule when the answer's defect is the rule a claim pins — same defect shape,
same fix, message matching up to answer-specific identifiers; template-match with a different
pinned rule and fix = loaded-rule-adjacent, counted separately):

- For every failing **pack-arm** row, classify each independent root cause as: loaded-rule-ignored
  (the rule is in that arm's payload), loaded-rule-adjacent, or untaught. Note: all three pack
  payloads carry the same rule set, so the denominators are comparable by construction; for the
  sheet arm, "in the payload" means the rule's sheet line (the sheet carries every fixture rule).
- Independently, count `Lint W99001` occurrences per arm across ALL logs (experiment 5's
  regression class — the sharpest known ignored-while-loaded rule).
- Report both counts per arm in the README next to the failure detail. These are observational;
  they carry no ship-rule weight in either direction.
