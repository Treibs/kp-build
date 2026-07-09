# Round-4 tier-1 remeasure — sui-move

*Tier-1 numbers are tainted — these tasks selected the beats. Trend signal only; headline
numbers come from pre-registered held-out falsification (tier 2).*

Protocol: the exact five failed probe runs re-collected fresh (same models, pinned IDs, same
oracle `sui 1.74.1-8fc60f1fa966`, same neutral scratch working directory), with the deepened
**110-claim** pack loaded. Payload assembled by the standard rule (`CONTEXT.md` +
`## Pack claims (all)`, sorted statements, one bullet each) — the assembly script first
reproduced the canonical 98-claim artifact byte-identically from the `a8cb8fc` inputs
(sha `4a53c7df…`) before assembling the 110-claim payload: **51,799 bytes, sha256
`92756d2d7532318ffd16be0b87794141c185336ce6c324a1e0937b6602cfb812`**. Artifacts per run in
`remeasure/<task>/`.

## Flip table

| task / model | probe (98-claim pack) | remeasure (110-claim pack) | taught fix applied? |
|---|---|---|---|
| suimport-2 / haiku | FAIL E07001 (`split(&mut raffle.pot, value(&raffle.pot), ctx)`) | **PASS CLEAN** | **no — corner avoided by restructuring** (correction: the first version of this row and the `ededeef` commit message claimed the taught hoist "appears verbatim"; the committed artifact contradicts that). The answer redesigned the pot as a dynamic field (`dynamic_field::remove` of the whole coin, then re-`add` of `coin::zero`) — no hoisted-read-fed-into-`&mut`-call site exists in the source. The flip is real; taught-cause attribution is not demonstrable, so by the same standard as gen-3 no credit is claimed |
| rsyn-3 / haiku | FAIL E01002 ×2 (`experience += amount`; `while … {` paren-free) | **PASS CLEAN** | **yes ×2** — written-out accumulation and parenthesized `while (…)`; both taught shapes applied |
| rapi-3 / sonnet | FAIL E03002 (`std::mem::swap(&mut robot.battery, &mut old)`) | **PASS CLEAN** | **yes** — the answer holds the battery in an `Option` slot and swaps with `option::swap`, the `std-mem-swap` GREEN idiom |
| gen-2 / haiku | FAIL E04024 ×2 (params not `mut`) + E06001 (drained vector not consumed) | **FAIL E06001 only** | **partially** — n/a for the beats (no round-4 beat targeted this run's causes): the loaded round-3 `param-mut` rule, *ignored* in the probe draw, was **applied** this draw (`mut boxes`, `mut recipients`); the residual is the **deferred `vector-destroy-empty` class** (missing `vector::destroy_empty(boxes)`) — **now ×2 answers cumulative → promoted round-5 candidate** per the standing rule |
| gen-3 / haiku | FAIL E04010 (`gifts: vector[]` uninferable) | **PASS CLEAN** | n/a — no beat targeted this class (deferred ×1); this draw the answer resolves inference with an explicit type argument on the struct instantiation (`GiftPool<T> { … }`), not an annotation on the literal itself. Recorded as a flip without a taught cause: draw variance, no credit claimed |

## Reading (trend only — see taint label above)

- **Compile-pass: 4/5 flipped** on the exact previously-failed runs — the strongest tier-1
  flip of the four sui rounds (round 1: 4/8; round 2: 6/8; round 3: 1/6). Reported as-is,
  tainted label unchanged: the same caution as every round applies, and one of the four flips
  (gen-3) has no taught cause and gets no credit.
- **Round-4 taught-fix visibility: 3/4** (corrected from an initial 4/4 — the suimport-2
  attribution did not survive adversarial review; see the flip-table row). Three taught GREEN
  shapes appear verbatim in their remeasure answers (written-out accumulation, parenthesized
  `while`, `Option`+`option::swap`); suimport-2 avoided its corner by restructuring. Zero
  round-4 taught-class recurrence in any remeasure log.
- **Ignored-while-loaded, both directions in one round:** the round-3 `param-mut` rule was
  ignored in the probe draw and applied in the remeasure draw by the same model on the same
  task — consistent with the standing observation that rule application is draw-variable, not
  payload-determined (four experiments, both payload forms).
- **Round-5 candidate ledger after this remeasure:** `vector-destroy-empty` (E06001, ×2 —
  **promoted**), `vector-literal-annotation` (E04010, ×1 — deferred, and its one recurrence
  opportunity this round resolved itself), plus the carried single-answer classes from
  `territories.md` (E07001 is now taught; the rest stand as recorded).
- **Post-measure claim freeze:** the pack's 110 claims are frozen for this round as of the
  teach commit (`362ca84`); nothing in this file altered a claim. The round-4 held-out effect
  is unmeasured until the next pre-registered tier-2 falsification.
