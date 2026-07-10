# Round-5 tier-1 remeasure — sui-move

*Tier-1 numbers are tainted — these tasks selected the beats. Trend signal only; headline
numbers come from pre-registered held-out falsification (tier 2).*

Exactly the eight failed probe runs, fresh answers, same models, deepened **128-claim**
payload (55,374 bytes, sha256 `d9e414e7…`, assembled from teach commit `1b85d58` by the
standard rule). Artifacts in `remeasure/`. Every attribution below was grep-verified against
the committed source before this file was written.

## Flip table

| task / model | probe | remeasure | taught fix applied? |
|---|---|---|---|
| vcp-1 / haiku | FAIL E04024 (param-mut ignored) | **FAIL E03003** | n/a for round-5 beats — the probe's ignored `param-mut` is gone, but the residual is `use sui::balance::{Balance, self}` — **round-1 `use-self` ignored while loaded**, the rule's third recorded ignore in two days (probe vcp-2, elicitation recipe-book, here). Import sweep: CORRECT (the taught `sui-import` shape present) |
| vcp-2 / haiku | FAIL E03003 ×2 (use-self ignored + SUI absent) | **FAIL E04007** | **yes for the taught class** — the SUI import is now correct (checker: CORRECT) and no `use-self` shape remains; the residual is NEW: `coin::split(payment, fee, ctx)` passing the `Coin` **by value** (`split` takes `&mut self`) — `split-by-value`, api-argument family, **round-6 candidate** |
| vde-1 / haiku | FAIL E06002 (moved-value-arg-order) | **PASS CLEAN** | no round-5 beat targeted its class (deferred ×1) — the answer self-corrects with the exact hoist (`let addressee = package.addressee;` before the move). Flip real, no credit claimed. The vde corner is avoided by design change: the intake vector lives in the struct and is drained in place, so no `destroy_empty` site exists |
| uid-3 / haiku | FAIL E04010 (unannotated `vector::empty()`) | **PASS CLEAN** | **partially** — no unannotated empty vector remains; the answer seeds the literal with its first element (`vector[sender]`), satisfying the taught rule's inference-evidence requirement, though not via the GREEN's explicit-annotation spelling. Partial attribution, so stated |
| ns-2 / haiku | FAIL E01002 + E04024 (two loaded rules ignored) | **PASS CLEAN** | n/a — no round-5 beat involved; the previously ignored `block-statement-semicolon` and `mut` rules are applied this draw (rule application remains draw-variable) |
| api-1 / haiku | FAIL E04007 (`id_to_address(&uid)`) | **FAIL E05001** | **yes for the taught class** — the answer now uses `uid_to_address`/`id_address` (grep-confirmed) and the taught E04007 shape is gone; the residual is `CheckInRecord has copy, drop` inside a `key` struct's vector field — **round-1 `key-field-store` ignored while loaded** |
| api-3 / haiku | FAIL E06001 (envelope vector unconsumed) | **PASS WARN2** | **corner avoided** — `Envelope has copy, drop` makes the vector freely droppable (the round-4 `Battery has copy` dodge pattern). Flip real; no credit for the consumption beats |
| vcp-3 / sonnet | FAIL E04007 (branch-type-mismatch) | **PASS WARN2** | n/a — deferred ×1 class, no beat; the answer self-fixes the branch typing. No credit |

## Reading (trend only — see taint label above)

- **Flips: 5/8.** Attribution is thin and stated per-row: one partial taught-fix flip (uid-3),
  two runs where the taught class died but a *different loaded rule was ignored* (vcp-1,
  api-1 — both still FAIL), one dodge (api-3), and two self-fixes on deferred classes.
- **Taught-class recurrence: ZERO.** No round-5 taught class appears in any remeasure log,
  and the applicable taught shapes are visibly applied (SUI imports correct in all four
  coin-bearing runs — remeasure import sweep 0 fails; `uid_to_address` in api-1).
- **The remeasure's real signal is the ignored-rules ledger:** this round's probe+remeasure
  recorded SIX loaded-rule-ignored events (`param-mut` ×2, `use-self` ×2, `block-statement-
  semicolon`, `key-field-store`) — `use-self` is now the most-ignored rule in the record
  (5 events across draws). Rule application, not rule coverage, remains the pack's binding
  constraint — consistent with four experiments of payload-form results.
- **Round-6 candidate ledger:** `split-by-value` (×1, NEW — api-argument family),
  `branch-type-mismatch` (×1 carried), `moved-value-arg-order` (×1 carried, self-fixed once),
  plus the standing deferred singles. The value-consumption and destroy-empty corners were
  avoided rather than exercised in their remeasure runs — their taught effect is a tier-2
  question.
- **Post-measure claim freeze:** claims frozen at `1b85d58`; nothing here altered a claim.
  Round 5's held-out effect is unmeasured until the next pre-registered tier-2 falsification.
