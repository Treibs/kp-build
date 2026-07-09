# Sheet-vs-full confirmation draw — result

**Result up front: branch 3 fires — the sheet adoption is WITHDRAWN.** On a fresh
pre-registered draw the full payload compile-passed **4/6** against the sheet's **1/6**
(base anchor 0/6). Under the frozen ship rule (sheet ≤ full → not confirmed), the
payload-salience experiment's adoption of the sheet as the recommended answer-time load
format is **withdrawn**: the sheet reverts to an experimental view of the pack, the full
payload reverts to the recommended form, and `emit-sheet` tooling stays blocked. Per the
frozen rule, this outcome is reported as prominently as the original adoption was — every
surface that recorded the adoption now records the withdrawal.

This is the confirmation draw the salience experiment itself required before any tooling
("one fresh draw, sheet vs full only"). The salience result cleared its bar **exactly**
(3/6 vs 1/6, zero margin, n = 6); this draw reversed it decisively. Pooled across both
draws (observational, no ship-rule weight): sheet **4/12** vs full **5/12** — no form
signal survives. The zero-margin qualifier disclosed at adoption time did its job.

## Setup

Protocol, arms, tasks, held-out audit, and the ship rule were frozen in [tasks.md](tasks.md)
at commit `5e605c9` **before any answer was collected**. Summary:

- One treatment comparison: **sheet vs full**. Base arm included only as a difficulty
  anchor (no ship-rule weight). Payloads reused **byte-identical** from the salience
  experiment's committed artifacts (SHA-256 pins re-verified at freeze; the pack's
  `CONTEXT.md` and `claims/` are byte-unchanged since those payloads were assembled).
- Six fresh held-out contract-authoring tasks (audit killed five draft candidates;
  disclosed adjacencies recorded in tasks.md), difficulty in the experiment 4–5 band.
- Model: `claude-haiku-4-5`, fresh context per cell, headless, no tools.
- Gate: identical mechanical protocol to experiments 3–5 and the salience draw —
  first fenced block, arm-neutral scaffold, plain `sui move build` on the pinned
  `sui 1.74.1-8fc60f1fa966`.

## Results

| task | base (anchor) | full | sheet |
|---|---|---|---|
| warranty-registry | FAIL E02004 | FAIL E03003 | **PASS CLEAN** |
| layaway-plan | FAIL E04024 | **PASS CLEAN** | FAIL E01002 |
| freelance-invoice | FAIL E06001 | **PASS** (2 warnings) | FAIL E04024 |
| tournament-prize | FAIL E01003 | **PASS CLEAN** | FAIL E07001 |
| bottle-deposit | FAIL Sui E02009 | FAIL E03003 | FAIL E02004 |
| penalty-jar | FAIL E06001 | **PASS** (1 warning) | FAIL E01002 |
| **primary — compile-pass** | 0/6 | **4/6** | **1/6** |
| secondary — clean-compile (observational this draw) | 0/6 | 2/6 | 1/6 |

## Verdict (frozen ship rule)

- Branch 1 — sheet (1) ≥ full (4) + 2? No.
- Branch 2 — sheet = full + 1? No.
- **Branch 3 — sheet (1) ≤ full (4)? Yes — fires.** The "recommended load format"
  adoption is withdrawn as specified above.

**Pooled context** (pre-registered as observational): over the 12 tasks of this draw plus
the salience draw, sheet 4/12 vs full 5/12. The decision is taken on this draw alone, but
the pooled numbers point the same way: no reliable form advantage.

Base anchor: 0/6 — this draw sits at the same difficulty extreme as the salience draw
(also base 0/6). Absolute numbers are not comparable across experiments; the full arm's
4/6 here vs 1/6 there is draw variance on top of any treatment effect, which is exactly
why the frozen rule compares arms within a draw only.

One-row observation, no weight: the sheet's single pass (warranty-registry) was clean and
came on the one task full failed — the two arms' passes are disjoint on this draw.

## Failure detail — pack arms

Root causes verified against the committed buildlogs; every E03006 in the full-arm rows
points back at a broken import line ("Similarly named defintion found here"), so those are
cascades, not independent causes.

| row | observed errors | independent root causes | classification |
|---|---|---|---|
| warranty-registry/full | E03003 ×4; E03006 ×3 (cascades); E04007 | (1) `use sui::X::{self, …}` on four imports — the use-self form; every E03006 is a cascade of these. (2) destructured the warranty's `UID` into `warranty_id`, `object::delete`d it, then passed it to an event field typed `ID` (E04007; needed `object::uid_to_inner` before the delete — the same answer uses `object::id(warranty)` correctly elsewhere) | **loaded-rule-ignored** (use-self, exact pinned message "Invalid 'use'. Unbound member 'self'") + untaught (uid-vs-ID) |
| bottle-deposit/full | E03003 ×2; E03006 ×12 (cascades) | use-self on two imports; all twelve E03006s cascade from them | **loaded-rule-ignored** (use-self, exact pinned message) |
| layaway-plan/sheet | E01002 | `plan.accumulated_amount += amount` — Rust compound assignment; Move has none ("Unexpected '='. Expected an expression term") | untaught (**NEW** rust-compound-assign) |
| freelance-invoice/sheet | E04024; E01002 | (1) by-value `payment: Coin<SUI>` parameter mutated via `coin::split(&mut payment, …)` without `mut` ("To use the variable mutably, it must be declared 'mut'"); (2) braced `if (paid > owed) { … }` used as a statement with no trailing `;` — parser errors at the next token ("Unexpected 'transfer'. Expected ';'") | **loaded-rule-ignored ×2** (param-mut; block-statement-semicolon — both exact pinned messages) |
| tournament-prize/sheet | E07001 | `coin::split(&mut tournament.pool, tournament.entry_fee, ctx)` — the second argument re-borrows `tournament` while `&mut tournament.pool` is live; the fee must be hoisted to a local first | untaught (**NEW** E07001 borrow shape) |
| bottle-deposit/sheet | E02004; E01002 ×2 | (1) bare `module deposit_scheme {` with no address ("The module does not have a specified address"); (2) `+=` at two sites | **loaded-rule-ignored** (module-address-form, exact pinned message) + untaught (rust-compound-assign) |
| penalty-jar/sheet | E01002 | braced `if (member_removed) { … }` as a statement with no trailing `;` ("Unexpected 'event'. Expected ';'") | **loaded-rule-ignored** (block-statement-semicolon, exact pinned message) |

## Pre-registered mechanism analysis — loaded-rule application (observational)

Experiment 5's strict recurrence standard, applied verbatim (same defect shape, same fix,
message matching up to answer-specific identifiers). Every ignored event below matches its
pinned RED fragment exactly — no green-claim-scope judgment calls were needed this draw,
so the strict and inclusive counts coincide.

| arm | failing rows | independent root causes | loaded-rule-ignored | loaded-rule-adjacent | untaught | W99001 (all 6 logs) |
|---|---|---|---|---|---|---|
| full | 2 | 3 | 2 | 0 | 1 | 3 |
| sheet | 5 | 7 | 4 | 0 | 3 | 2 |
| base (context) | 6 | — | — | — | — | 4 |

The sheet's four ignored events are rules the sheet itself states on single imperative
lines (module-address-form, param-mut, block-statement-semicolon ×2); the full arm's two
are the use-self claim. **The ignored-while-loaded phenomenon now stands in a fourth
consecutive experiment and in both payload forms** — whichever form wins a given draw, the
model still violates rules that are verbatim in its context. Conditioning-on-failure
caveat from the salience analysis still applies: the arm with more failing rows
mechanically gets more classification opportunities.

W99001 (transfer-to-sender lint): base 4, full 3, sheet 2. Experiment 5's observation of
a zero-W99001 full arm did **not** replicate.

## Base-arm detail (difficulty anchor, no ship-rule weight)

| row | independent root causes |
|---|---|
| warranty-registry | bare `module` (E02004) + bare `struct` ×8 (E01003 — pre-2024-edition visibility) |
| layaway-plan | plain `let` locals mutated (E04024 ×6) |
| freelance-invoice | non-`drop` `Invoice` left unconsumed (E06001 ×2) |
| tournament-prize | bare `struct` ×2 (E01003) + hallucinated `coin::burn_for_testing` in non-test code (E03003 ×2 — a test-only API) |
| bottle-deposit | `transfer::transfer` on `Coin<SUI>` (Sui E02009 ×2 — private-transfer rule) |
| penalty-jar | implicit copy of a non-`copy` field (E05001 ×2) + non-`drop` value unused (E06001 ×2) |

## What this changes

1. **Recommended load format: the full payload** (CONTEXT.md + sorted claim statements),
   restored per branch 3. The sheet remains committed as an experimental *view* of the
   pack — a form hypothesis that won one zero-margin draw and lost the confirmation.
2. **`emit-sheet` tooling stays unbuilt.** The gate it needed to clear was this draw.
3. **The salience verdict is superseded, not rewritten**: its README, numbers, and
   qualifiers stand as recorded; a dated note there points here.
4. **Round-4 seed ledger additions** from this draw: **NEW** rust-compound-assign `+=`
   (2 sheet rows, 3 sites — the Rust-bleed family grows); **NEW** E07001
   referential-transparency borrow shape (`coin::split(&mut obj.field, obj.field2, ctx)`);
   **NEW** uid-vs-ID event field (delete the `UID`, emit the `ID` — full arm); hallucinated
   test-only `coin::burn_for_testing` (base arm).
5. **Ignored-while-loaded is form-independent** (four consecutive experiments, every
   payload form tested). Form manipulation has now been tried and did not solve rule
   application; whatever attacks it next has to be a different mechanism, not another
   payload rearrangement.
