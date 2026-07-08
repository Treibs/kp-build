# Payload-salience experiment — same 98 claims, form varies (sui-move)

**Result up front: branch 1 fires — payload form matters.** The hand-compressed cheat sheet
(**sheet**, 5,887 bytes) compile-passed **3/6** against the standard payload's (**full**,
49,656 bytes) **1/6**, meeting the pre-registered ≥ full + 2 bar **exactly** (3 = 1 + 2). Per
the frozen ship rule, the sheet form is adopted as the recommended load format. Two honesty
qualifiers travel with the headline, stated as prominently: **(1)** the bar was met with zero
margin, at n = 6, with two disclosed treatment comparisons — this is minimum-clearance
evidence, not a rout; **(2)** the mechanical control arm (**slim** — same sorted claim
statements, briefing stripped, 24,639 bytes) scored **0/6**, below full, so the win cannot be
attributed to redundancy removal alone — it is the sheet's *imperative form and/or content
compression* (an intentional confound disclosed at pre-registration), and pure mechanical
slimming of the existing payload is, on this evidence, if anything mildly harmful (slim did
not hit the ≤ full − 2 against-slimming threshold, so that clause does not fire; the 0/6 vs
1/6 gap is within draw noise and recorded as-is). On the secondary metric no arm cleared
anything: all three sheet passes carried lint warnings (clean-compile: full 1/6, sheet 0/6,
slim 0/6, base 0/6). This was also the hardest draw of the series — **base went 0/6** (its
prior range: 2/6–5/6) — and full's 1/6 is well below its 3/6 history, so the absolute numbers
are not comparable across experiments; only the within-draw arm gaps are.

## Setup

- Pre-registration: [`tasks.md`](tasks.md), committed at `c170058` **before any answer was
  collected** — arms, payload SHA-256s, tasks (held-out audit run before the freeze; two
  candidates dropped by it, disclosed there), metrics, the three-branch ship rule, and the
  pre-registered mechanism analysis.
  - **Erratum (frozen file not edited):** `tasks.md` states the slim payload is "24,519 bytes"
    and the sheet has "37 lines"; the committed files measure **24,639 bytes** and **35 bullet
    lines** (`wc -c payloads/payload-slim.md`; `grep -c '^- ' payloads/payload-sheet.md`). The
    SHA-256 pins in `tasks.md` are correct and match the committed payloads, so pre-registration
    integrity is intact — the two prose numbers were transcription errors at freeze time.
- Arms (all pack arms carry the SAME 98 claims of master `04d7cba`; only form varies; payloads
  committed under [`payloads/`](payloads/) at pre-registration):
  - **base** — task + instruction only; contextual anchor, no ship-rule weight.
  - **full** — CONTEXT.md + all sorted claim statements; byte-identical to experiment 5's kp98
    payload (verified by diff at assembly time; experiment 5 committed no payload file — its
    assembly rule is deterministic, and `payloads/payload-full.md` here is the committed
    artifact). 49,656 B.
  - **slim** — the same sorted claim statements once, two-line header, briefing dropped;
    mechanical, zero editorial judgment; every statement appears verbatim in full. 24,639 B.
  - **sheet** — 35 imperative rule lines derived 1:1 from the claims, grouped by category, with
    broken form + observed error code per line. Confounds form and compression by design;
    slim is the control isolating pure redundancy removal. 5,887 B.
- Model: `claude-haiku-4-5` (the pack's falsification primary), fresh context per cell,
  headless, no tools, neutral scratch working directory.
- Gate: mechanical first-fenced-block extraction, arm-neutral scaffold (`Move.toml` binding the
  answer's own module address names to `0x0`), plain `sui move build` on the pinned
  `sui 1.74.1-8fc60f1fa966`. Committed buildlogs are ANSI-stripped and home-directory-redacted.
- Layout: `answers/<task>/<arm>.answer|-src.move|-pkg/|.buildlog|.result`; summary in
  [`answers/results.txt`](answers/results.txt).

## Results

| task | base | full | slim | sheet |
|---|---|---|---|---|
| micro-amm | FAIL E01003 | **PASS CLEAN** | FAIL E04007 | **PASS WARN2** |
| staking-pot | FAIL E01003 | FAIL E03003 | FAIL E03006 | **PASS WARN1** |
| rosca-circle | FAIL E03002 | FAIL E06001 | FAIL E04030 | **PASS WARN1** |
| compliance-coin | FAIL Sui E02003 | FAIL Sui E02009 | FAIL E03003 | FAIL E04007 |
| grade-book | FAIL E03002 | FAIL E04004 | FAIL E01002 | FAIL E01002 |
| payment-channel | FAIL E01003 | FAIL E03006 | FAIL E05001 | FAIL E05001 |
| **primary — compile-pass** | **0/6** | **1/6** | **0/6** | **3/6** |
| **secondary — clean-compile** | **0/6** | **1/6** | **0/6** | **0/6** |

## Verdict (pre-registered ship rule, applied literally)

- **Branch 1** — slim (0) ≥ full + 2 (3)? No. **Sheet (3) ≥ full + 2 (3)? Yes — fires.**
  Payload form matters on this evidence; the sheet is adopted as the recommended load format
  for answer-time use. (Only one treatment cleared the bar, so no tie-break was needed.)
- Branch 2 — not reached (branch 1 fired).
- The branch-3 against-slimming clause (treatment ≤ full − 2) did **not** fire for slim
  (0 ≤ −1 is false), but the direction is reported anyway: mechanical redundancy removal did
  not help and may have cost the one task full passed.
- Secondary: no treatment arm was ≥ full + 2 on clean-compile; sheet's three passes all carry
  warnings (W99003 ×2; W99001 ×1; W99003 ×1). **Adopting the sheet buys compile-pass, not
  cleanliness, on this draw.**

The bar was met exactly, at n = 6, under two disclosed comparisons. Treat this as
promising-and-provisional: the recommended next confirmation is a fresh draw with sheet vs
full only (one comparison), before the sheet form is baked into tooling.

## Failure detail (every failing row; root causes regenerated from the committed buildlogs)

Classification per the pre-registered mechanism analysis: **loaded-rule-ignored** (the defect
is a rule in that arm's payload — experiment 5's recurrence standard: same defect shape, same
fix, message matching modulo answer-specific identifiers), **loaded-rule-adjacent** (template
match, different pinned rule or scope), or **untaught**. Base rows are recorded for context
only.

| row | codes | root cause(s) | classification |
|---|---|---|---|
| micro-amm/base | E01003 ×2, Sui E02009 ×3 | bare `struct` (no `public`); `transfer::transfer(coin, sender)` on `Coin` (private transfer of a foreign type) | taught classes fired in the no-pack arm (struct-visibility; private-transfer-foreign) |
| staking-pot/base | E01003 ×2 | bare `struct` ×2 | taught class (struct-visibility), no-pack arm |
| rosca-circle/base | E03002, E01003, E05001 ×2, E03003 ×2 | `use sui::vector` (unbound module); bare `struct`; implicit copy + drop-mutation of a `Bag` field; hallucinated `bag::drop` ×2 sites | taught class (struct-visibility) + untaught (wrong-module vector import; hallucinated API) |
| compliance-coin/base | Sui E02003 | OTW named `REG` ≠ upper-case module name `REG_TOKEN` — invalid `init` witness | taught class (OTW naming), no-pack arm |
| grade-book/base | E03002, E04003, E04007 ×5 | `use sui::vector`; `(addr as u256)` (invalid cast); `table::contains(&key)` — key passed by reference | taught class (table-key-by-value) + untaught ×2 |
| payment-channel/base | E01003, E03003 ×2, E05001 ×2 | bare `struct`; hallucinated `clock::epoch`; drop-mutation + `field: _` ignore of `Balance<SUI>` | taught classes (struct-visibility; option-field-fill shape; destructure-ignore), no-pack arm |
| staking-pot/full | E03003 ×2 (+ E03006 ×11 cascade) | `use sui::balance::{Balance, self}` / `use sui::coin::{Coin, self}` — lowercase `self` in group imports; every E03006 is downstream of the two broken imports | **loaded-rule-ignored** (round-1 `use-self`; exact message) |
| rosca-circle/full | E06001 | destructured `pot: Option<Coin<SUI>>` extracted-if-some but the option itself never `destroy_none`/`destroy_some`d — left unused without `drop` | **loaded-rule-adjacent** — the loaded claims state the rule verbatim, down to the example type `Option<Coin<SUI>>` and the destroy fix, but pin the `field: _` shape / E05001 message; this is the leave-unused shape, E06001 (same standard as experiment 5's let-discard call) |
| compliance-coin/full | Sui E02009 | `transfer::transfer(treasury, ctx.sender())` — `TreasuryCap` is a foreign `key+store` type; needs `public_transfer` | **loaded-rule-ignored** (private-transfer-foreign; message identical modulo type) |
| grade-book/full | E04004 ×10, E04005 ×4 | `Table<(address, u64), u64>` and `let key = (student, i)` — tuples used as first-class values/type arguments (Move has none); one design choice, fourteen sites | untaught (rust-tuple-value; Rust-bleed family) |
| payment-channel/full | E03006 ×4; E04023 ×2; E05001 ×2 | three independent root causes: (1) `SUI` used, `use sui::sui::SUI` absent; (2) `.value()` called on `Option<Balance<SUI>>` (forgot to borrow the inner value); (3) `let _ = option::extract(...)` + `..` rest-pattern ignoring a non-`drop` `Proposal` | untaught (SUI-import, absent-import shape — recorded round-4 candidate) + untaught (option-method confusion) + **loaded-rule-adjacent** (value-level ignore; the loaded doc claim's general wording — "every way of ignoring a value" — covers it verbatim, but the pinned fixture shape is `field: _`; same standard as experiment 5) |
| micro-amm/slim | E04007 ×3 | `pool_id: address` field compared/filled with `object::id(...)` (`ID`) — ID/address type confusion | untaught |
| staking-pot/slim | E03006 ×5 | `SUI` used (`Balance<SUI>`, `Coin<SUI>`), `use sui::sui::SUI` absent | untaught (SUI-import, absent-import shape — second hit this draw, fourth cumulative) |
| rosca-circle/slim | E04029, E04030, E04031 | `vector::all(...)` called without `!` and with a lambda outside a macro call | untaught (macro-bang; Move 2024 macro surface) |
| compliance-coin/slim | E03003 | hallucinated `coin::freeze_currency_metadata` (real API: `transfer::public_freeze_object(metadata)`) | untaught (hallucinated API) |
| grade-book/slim | E01002 | `public fun create(...) -> (InstructorCap, GradeBook)` — Rust return arrow | untaught (rust-return-arrow; ×3 cumulative across experiments) |
| payment-channel/slim | E05001 ×4 | two independent root causes: (1) `channel.counterparty_coin = option::some(deposit)` on `Option<Coin<SUI>>` — mutation destroys a non-`drop` old value; (2) `counterparty_coin: _` in a destructure — `field: _` ignore of a non-`drop` field ×3 sites (the adjacent `proposal: _` ignores are legal — `Proposal` has `copy, drop`) | **loaded-rule-ignored ×2** (round-2 `option-field-fill`, exact "Invalid mutation" message; round-3 `destructure-ignore`, the exact pinned `field: _` shape) |
| compliance-coin/sheet | E04007, E03011, E04010 | three independent root causes: (1) `create_currency(..., string::utf8(b"..."), ...)` — `description` takes `vector<u8>`, the sheet's own line shows byte-string args; (2) `public fun freeze(...)` — `freeze` is a reserved name; (3) `let _ = dynamic_field::remove(...)` — cannot infer the removed type, needs annotation | **loaded-rule-ignored** (create-currency call shape; green-claim scope — no RED fragment is pinned for this class, disclosed) + untaught (reserved-name `freeze`) + untaught (turbofish/annotation on `remove`) |
| grade-book/sheet | E01002; E04004 ×8, E04005 ×3 | two independent root causes: (1) Rust return arrow `-> (GradeBook, InstructorCap)`; (2) tuples as dynamic-field keys / local types | untaught ×2 (rust-return-arrow; rust-tuple-value — the same two habits as the full/slim rows of this task) |
| payment-channel/sheet | E05001 ×7, E06001 ×6 | two independent root causes: (1) `pending_proposal: Option<PendingProposal>` where `PendingProposal` lacks `store` inside a `key` struct; (2) `let x = channel.field` dot-reads of non-`copy` fields (`Coin`, `UID`) — implicit copy, with the never-consumed values cascading to all six E06001 | **loaded-rule-ignored ×2** (struct-field-store, exact "all fields require the ability 'store'" message; round-3 `implicit-field-copy`, exact message modulo field name) |

## Pre-registered mechanism analysis (observational; no ship-rule weight)

Independent root causes in failing pack-arm rows:

| arm | failing rows | root causes | loaded-rule-ignored | loaded-rule-adjacent | untaught |
|---|---|---|---|---|---|
| full | 5 | 7 | 2 | 2 | 3 |
| slim | 6 | 7 | 2 | 0 | 5 |
| sheet | 3 | 7 | 3¹ | 0 | 4 |

¹ Sheet's third ignored event (compliance-coin's `create_currency` call shape) is counted at
green-claim scope — the class has no pinned RED fragment, so the strict experiment-5
message-match standard cannot apply to it; under the strict standard alone, sheet has 2,
tying full and slim. Both readings are shown; the row itself carries the disclosure.

`Lint W99001` across ALL logs (experiment 5's regression class): base 1, full 0, slim 0,
sheet 1 (in a sheet PASS — the sheet's own transfer-to-sender line, ignored at the warning
tier).

**The salience prediction is NOT cleanly supported at the mechanism level.** The hypothesis
predicted fewer loaded-rule-ignored events in the treatment arms; instead the sheet's three
failing rows carry 3 ignored events (2 with exact pinned messages, 1 at green-claim scope —
the most of any arm on the inclusive count, a three-way 2–2–2 tie on the strict count), and
slim's failures still ignored two loaded rules. Two caveats cut in opposite directions:
(1) conditioning on failure biases the count — sheet failed only 3 tasks, so its
ignored-events-per-failing-row (1.0) is the highest, while its ignored events per task (0.5)
is comparable to full's; the pre-registration did not fix a normalization, so both are shown;
(2) at the **warning tier**, full and slim show zero W99001 and zero W99010 across all six
logs each, against base's 1× W99001 + 8× W99010 — the verbose arms *did* apply lint-tier
rules broadly, and W99003 (sub-optimal `Coin` field — a class the pack does not carry) is now
the dominant residual warning in pack arms (slim 3, sheet 4). Honest net: the sheet form
bought three compile-passes, but where it failed it ignored its own lines at the same rate as
the verbose forms — form helps, but it does not solve rule application.

## What this changes

1. **Recommended load format: the sheet** (per the ship rule) — for answer-time loading of
   the sui-move pack, a ~6 KB imperative cheat sheet derived 1:1 from the claims. The full
   payload remains the archival/verification form; the sheet is a *view* of the pack, not a
   replacement (claims, fixtures, and grounding are unchanged).
2. **Confirmation before tooling**: one fresh draw, sheet vs full only, before any `kp-build`
   emit-sheet feature is built. The bar was met with zero margin.
3. **Round-4 ledger updates** (carried classes that fired again this draw): SUI-import
   absent-import shape ×2 (staking-pot/slim, payment-channel/full — now 4 cumulative events);
   rust-return-arrow ×2 (grade-book slim+sheet — ×4 cumulative); NEW rust-tuple-value
   (grade-book full+sheet, 25 sites — tuples as values/keys); NEW macro-bang
   (rosca-circle/slim); NEW reserved-name `freeze` (compliance-coin/sheet); NEW
   coin-field W99003 warning class (8 sites across arms, base included).
4. **The ignored-while-loaded phenomenon stands** across three consecutive experiments and
   all payload forms tested; it is a model-behavior constraint, not a payload-format defect,
   and remains not-a-beat.
