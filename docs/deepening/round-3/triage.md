# Round-3 triage

30 runs (15 tasks × 2 models, 86-claim pack loaded): **haiku 9/15, sonnet 13/15**. 8 failing
runs; two of them (import-3, both models) are void — see the task-defect note below. Every
verdict traces to the committed buildlog for that run.

## Task-authoring defect (reported, not counted)

**import-3 is VOID for both models.** The task itself pinned `module match::donation`, and
`match` is a **reserved keyword** in Move 2024 — both models followed the pinned path verbatim
(as the elicitation design required) and failed at line 1 with E01002 `Unexpected 'match'`.
This measures nothing about parametric knowledge; the defect is in the task, not the answers.
Both runs are excluded from territory scoring. (The task freshness audit checked for overlap
with prior tasks; it did not check pinned identifiers against the reserved-word list — that
check is now part of the task-design step.)

## Failure table

| task / model | observed error (first line + shape) | verdict | reason |
|---|---|---|---|
| modimp-2 / haiku | E03006 ×3 — `event::emit(...)`: "Could not resolve the name 'event'"; no `use sui::event` anywhere in the answer | **beat-worthy** | Territory-1 on-target. The alias-binding rule is untaught: the pack's `events` claim states the copy+drop ability rule and *shows* a fully-qualified `sui::event::emit(...)` call, but no claim states that a `module::fn` alias call requires `use sui::module`. Adjacency disclosed: copying the loaded claim's fully-qualified form would have avoided the error, but a form shown in passing is not a rule stated |
| destr-2 / haiku | E05001 ×2 — `let Bounty { id, task: _, reward: _ } = bounty;` with `reward: Option<Coin<SUI>>`: Option can only have `drop` if the type argument does, and `Coin` does not | **beat-worthy** | Territory-2 on-target: `field: _` ignore of a non-`drop` field. The answer even extracted the coin first — the leftover *empty* `Option<Coin<SUI>>` still cannot be `_`-ignored; it needs `option::destroy_none` (or `destroy_some`) |
| destr-3 / haiku | (a) E05001 ×2 — `let Snake { id: _, .. }` / `let Skin { id: _, .. }`: "The type 'sui::object::UID' does not have the ability 'drop'" | **beat-worthy** | Territory-2 on-target, second independent answer: `id: _` ignore of `UID`; the correct dismantle is `let ... { id, .. }` + `object::delete(id)` |
| destr-3 / haiku | (b) Sui E01001 — `Snake { id: snake_id, .. }` reusing a UID unpacked from another object: "The UID must come directly from `sui::object::new`" | recorded, deferred | New class (`uid-reuse`), **1 answer** — same deferral rule that held `generic-transfer-key-bound` at round-2 triage and `assert-abort-code` at exp-4. Promoted if it recurs |
| destr-3 / sonnet | E03002 — `use std::mem;` then `mem::replace(&mut snake.skin, ...)`: "Unbound module: 'std::mem'" (+ downstream E03006 / Sui E02009) | recorded, deferred | New class (`std-mem-replace`, direct Rust bleed — Move has no `std::mem`), **1 answer** → same deferral rule. Notable as the round's only non-void sonnet failure |
| import-2 / haiku | (a) E05001 ×2 — `let deposit = reservation.deposit;`: "'sui::coin::Coin<sui::sui::SUI>' does not have the ability 'copy'" | **beat-worthy** | **Promoted on recurrence** per the rule recorded in `territories.md`: exp-4 rental/kp61 hit the same class ×2 ("Invalid implicit copy of field 'item' without the 'copy' ability" — same E05001 field-access-copies shape, different message wording). Field access copies; moving a field out requires destructuring (or borrowing). 2 answers across the record |
| import-2 / haiku | (b) E06001 ×2 — the extracted `Reservation` value left unused without `drop` | downstream of (a) | Same root cause: `let Reservation { reservee, deposit } = extract(...)` fixes (a) and (b) at once. Not counted separately |
| import-2 / haiku | (c) E01002 — `while (...) { ... }` followed by `total` with no `;` after the block | loaded rule ignored | This is the round-2 **taught** class `block-statement-semicolon` (E01002, braced statement mid-sequence needs `;`). A rule restated is not a new rule — recorded, not taught |
| import-3 / both | E01002 line 1 — `module match::donation` | **VOID** | Task-authoring defect (see above) |
| generic-3 / haiku | E04024 — `public fun pass<T: store>(relay: Relay<T>, ...)` then `relay.legs = ...`: "To use the variable mutably, it must be declared 'mut', e.g. 'mut relay'" | **beat-worthy** | **Promoted on recurrence**: exp-3's recorded falsification gaps included the E04024 mut-declaration class (it seeded round-2's `letmut` territory, which came up clean in 6 runs). Round-3 observed the *parameter* shape (exp-3's was the `let` shape); promoted as one mut-declaration family, fixtures pin the observed parameter shape |

## Territory verdicts

| # | territory | verdict |
|---|---|---|
| 1 | missing-module-import | **1 on-target hit** (modimp-2/haiku, `event::emit`) → beat |
| 2 | destructure-ignore | **2 on-target answers** (destr-2/haiku, destr-3/haiku) → beat |
| 3 | wrong-module-import | **inconclusive** — import-3 void (task defect), import-1 passed both models, import-2 failed off-target. 0 on-target hits in the 4 valid runs; NOT recorded clean (one third of the territory's evidence was voided) |
| 4 | generic-transfer-key-bound | **model already strong — no beats** (with pack loaded): generic-1/2/3 sonnet + generic-1/2 haiku all compiled; generic-3/haiku failed off-target (E04024). 0 on-target hits in 6 valid runs. The round-2 remeasure occurrences did not reproduce |
| 5 | clock-epoch-confusion | **model already strong — no beats**: 6/6 runs passed, including time-2 (ms timelock) and time-3 (epoch farm) which pull in opposite time-API directions |

## Beats to teach (4 — each needs GREEN+RED proven on the pinned oracle before commit)

1. **`missing-module-import`** — calling `module::fn` requires `use sui::module` (E03006
   "Could not resolve the name"). RED: `event::emit` with no `use sui::event`.
2. **`destructure-ignore`** — `field: _` in a destructure cannot ignore a non-`drop` value
   (E05001); `UID` fields need `object::delete`, empty `Option<T>` (non-drop `T`) needs
   `option::destroy_none`. RED: `id: _`.
3. **`implicit-field-copy`** — `let x = s.field;` copies, so non-`copy` fields cannot be read
   out by field access (E05001); move them out by destructuring the struct. RED: field access
   on a `Coin` field.
4. **`param-mut`** — assigning through a by-value function parameter requires `mut` in the
   signature (E04024). RED: `fun f(x: S)` with `x.n = 1`.

Deferred this round (promoted if they recur): `uid-reuse` (Sui E01001, 1 answer),
`std-mem-replace` (E03002, 1 answer), `assert-abort-code` (E04035 — 0 hits this round, stays
deferred), `implicit-field-copy`'s E06001 companion shape (downstream, not independent).
