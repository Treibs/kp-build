# Round-7 triage — sui-move

Inputs: `probe/results.txt` (haiku **10/15**, sonnet **15/15**; verdicts regenerated from
`.result` files, FAIL codes from committed buildlogs). Import sweep (8 SUI carriers, both
models): **16/16 CORRECT, 0 wrong-module, 0 absent** — the taught SUI-import beat holds through a
second consecutive clean replication draw (correction, review round 1: round 5's sweep
recorded 1/9 haiku import-FAIL and its probe arm predates the beat — rounds 6 and 7 are
the clean pair).

**Teach rule reminder (frozen at scope):** beats this round are ledger-selected; a clean
probe territory does NOT decline its beat. Probe evidence below is recorded per class as
fresh-elicitation confirmation or as a finding — the five beats ship either way.

## Failure verdicts (every FAIL, whole-log)

| task | model | observed error | verdict | reason |
|---|---|---|---|---|
| tb-2 | haiku | error[E04004] ×3 — `Option<(u64, u64)>` return: "Expected a single non-reference type, but found: '(u64, u64)'" | **ledger class fires live** | The round's top class (`tuple-bleed`, ×3 → now ×4 cumulative) elicited exactly as it fired in exp-8: a paired-data view pushed a tuple into a type argument. The `tuple-bleed` beat's RED pins this precise shape and fragment. |
| sop-2 | haiku | error[E06002] — `option::fill(&mut to_tank.exhibit, exhibit)` after `exhibit` moved: "The value of 'exhibit' was previously moved here." | **ledger class fires live, cross-territory** | The `moved-value-arg-order` class (×2 → now ×3 cumulative) fired in an sop task — the move-then-read slip under multi-concern load, exactly the draw-sensitivity the frequency method predicts (round 6's mva probes gated clean; the class fires where it likes). Covered by this round's `moved-value-arg-order` beat (E06002, hoist-the-read). |
| tb-1 | haiku | error[E06001] — `let _entry = vector::remove(...)`: WaitlistEntry has no `drop`; `_entry` unconsumed | loaded-class-adjacent (vcp family), recorded | The tuple corner was AVOIDED — the answer used a named `WaitlistEntry` struct (the tuple-bleed green idiom, via the loaded doc-tier rule or draw). The failure is the round-5-taught `value-consumption-paths` family in a new sub-shape: an underscore-prefixed binding read as a discard (the Rust habit) — in Move `_entry` still holds the non-drop value. Shape recorded on the ledger as `underscore-discard` ×1; not taught (adjacent to a loaded class, single firing). |
| mva-1 | haiku | error[E03006] ×7 — `use sui::coin::Coin;` then `coin::value(...)`: "Could not resolve the name 'coin'" | **ignored-while-loaded** (missing-module-import) | The pack's `missing-module-import` beat pins exactly this (alias must be bound by `use`; type-only import binds no module alias). Rule loaded, not applied — ledger event, a rule restated is not a new rule. |
| mva-3 | haiku | error[E04007] — event field declared `volume_id: address`, fed `object::uid_to_inner(&volume.id)` (returns `ID`) | ignored-while-loaded at doc tier (uid-vs-id) | The loaded `uid-vs-id-doc` claim says verbatim "the identity carried in events and tables is the copyable `ID`" — the answer declared the event field as `address` and then correctly produced an `ID` value: self-inconsistent under a loaded rule. Ledger event (uid-vs-id application ×1); the mva class itself did not fire in this task. |

## Clean territories (recorded, per the frequency rule — beats ship anyway)

- **stp (std-table-path):** all six answers imported `sui::table` correctly (haiku's two
  WARN1s are unused-variable W09002, unrelated). The class's evidence remains the ledger's
  two held-out firings (exp-6 book-club, exp-8 plant-clinic/kp128).
- **bac (balance-api-on-coin):** the round's cleanest finding — all six answers stored the
  pool as `Balance<SUI>` AND consumed the low-level API exclusively
  (`balance::split`/`join`/`zero` + `coin::from_balance`/`into_balance`; zero
  `coin::take`/`put` call sites in any answer), so the class had no site to fire. The beat
  ships on the exp-6 recorded firing; the finding says the convenience surface — not the
  Balance concept — is where the class lives.
- **sop (std-option-path) on its own class:** every Option use resolved to implicit
  `std::option` — zero `use sui::option` in 30 answers. Ledger evidence (×3 held-out,
  including round-6's own remeasure) carries the beat, per the frozen rule.
- **mva (moved-value-arg-order) on its own tasks:** mva-1/mva-3 haiku failed on OTHER
  loaded classes (above); no E06002 in the mva trio — but the class fired cross-territory
  in sop-2 the same draw. Elicitation is draw-sensitive; frequency selection exists
  precisely because of this.

## Beats shipped this round (5, all pre-decided at scope; +15 claims → 149)

| beat | claims | evidence (ledger + this probe) |
|---|---|---|
| tuple-bleed | green + red + doc | exp-8 ×2 (one loaded-rule-ignored at doc tier) + round-6 opt-1 + **tb-2 live ×3 sites** — doc-tier→execution-tier escalation, adjacency to `reference-type-argument-red` (same E04004 family, distinct fragments) disclosed in the red claim |
| std-table-path | green + red + doc | exp-6 book-club + exp-8 plant-clinic/kp128 (probe clean) |
| balance-api-on-coin | green + red + doc | exp-6 coin::put-on-Coin + exp-8 ferry-manifest coin::take-on-Coin, E04007 (citation corrected in review round 1; the frozen territories.md cited an exp-7 `Balance::zero()` family shape that belongs to the api-arity-ctx family — the ×2 count stands on the exp-6+exp-8 events) (probe clean — take/put never touched) |
| std-option-path | green + red + doc | exp-4 + exp-7 + round-6 remeasure opt-1 (probe clean) |
| moved-value-arg-order | green + red + doc | round-5 vde-1 + round-6 remeasure mva-3 + **sop-2 live** (cross-territory) |

All ten fixtures proven through the pinned oracle before commit; RED fragments pasted from
observed output of the minimized fixtures (`expected_error.txt` per zone); corpus +1 excerpt
(move-book `reference/variables.md` Move-and-Copy section, same pinned commit `8ce4dcb9`)
grounding the mva doc claim.

## Ledger updates (for round 8 / next falsification)

- `tuple-bleed` ×4 (taught — watch the next held-out draw), `moved-value-arg-order` ×3
  (taught), `std-option-path` ×3 (taught), `std-table-path` ×2 (taught),
  `balance-api-on-coin` ×2 (taught).
- NEW: `underscore-discard` ×1 (vcp-family sub-shape, tb-1).
- Ignored-while-loaded events: `missing-module-import` ×1 (mva-1, ×7 sites),
  `uid-vs-id` doc-tier ×1 (mva-3). The application ledger (`use-self` ~12 + these) remains
  beat-unaddressable.
- Import sweep: two consecutive clean replications (round 6, round 7) — corrected in
  review round 1 (round 5's sweep was 1/9 import-FAIL, pre-beat).
