# Round-4 triage — sui-move

Probe: 15 tasks × 2 models, pack-loaded (98 claims, payload sha `4a53c7df…`), pinned
`sui 1.74.1-8fc60f1fa966`. **haiku 11/15, sonnet 14/15.** Full per-run verdicts in
[`probe/results.txt`](probe/results.txt). Every failing buildlog was root-caused in full
(round-3 rule: classify the whole log, not the first error); the five failing runs carry seven
distinct root causes.

## Failures

| task / model | observed error | verdict | reason |
|---|---|---|---|
| suimport-2 / haiku | E07001 ×1 — `let prize = split(&mut raffle.pot, value(&raffle.pot), ctx);` ("Field 'pot' is still being mutably borrowed") | **beat-worthy** | the sheet-confirm E07001 borrow-alias class recurring in a fresh draw — **×2 answers cumulative → promoted**, exactly the promotion the territories.md exclusion pre-declared. Encodes a Rust intuition: NLL two-phase borrows let `f(&mut x, x.g())` compile in Rust; Move holds the mutable borrow across the argument list. Fix shape: hoist the read to a `let` before the call. Note: fired under a territory-1 task; the territory-1 corner itself (the SUI import) was handled correctly in this same answer |
| rsyn-3 / haiku (root cause a) | E01002 — `character.experience += amount;` ("Unexpected '='") | **beat-worthy** | `rust-compound-assign`, territory 2's invited corner, **×3 answers cumulative** (sheet-confirm ×2 + this). Move has no compound-assignment operators; the fix is `x = x + amount` |
| rsyn-3 / haiku (root cause b) | E01002 — `while character.experience >= … {` ("Expected '('") | **beat-worthy** | NEW shape inside approved territory 2 (parse-level Rust bleed): Rust writes `while cond {`, Move 2024 requires `while (cond) {`. Probe-elicited inside an approved territory — taught on the same standing as any territory hit |
| rapi-3 / sonnet | E03002 — `std::mem::swap(&mut robot.battery, &mut depleted);` ("Unbound module 'std::mem'") | **beat-worthy** | the `std-mem-replace` family (promoted at round 3, ×2 then) now **×3 cumulative** in its `swap` variant, territory 3's invited corner. There is no `std::mem` in Move; in-place replacement of a non-`copy` struct field needs a different idiom (see beat) |
| gen-2 / haiku (root cause a) | E04024 ×2 — `vector::pop_back(&mut boxes)` / `(&mut recipients)` on parameters not declared `mut` | **not beat-worthy** | the round-3 taught `param-mut` rule **ignored while loaded** — same pinned rule and fix, message identical modulo identifiers. Recorded as an ignored-while-loaded event (the standing model-behavior constraint); a rule restated is not a new rule |
| gen-2 / haiku (root cause b) | E06001 — the drained `vector<CareBox<T>>` parameter "still contains a value … must be consumed" | **not beat-worthy (deferred)** | NEW class `vector-destroy-empty` ×1: a `vector<T>` where `T` lacks `drop` must be consumed with `vector::destroy_empty` even after it is emptied — Rust drops an empty `Vec` silently. One answer → held by the standing 1-answer deferral rule; round-5 ledger |
| gen-3 / haiku | E04010 — `gifts: vector[]` in a generic struct literal ("Could not infer this type") | **not beat-worthy (deferred)** | NEW class `vector-literal-annotation` ×1: the empty `vector[]` literal does not take its element type from later `push_back`es. Distinct fix from the sheet-confirm `dynamic_field::remove` annotation case (different rule/fix = not a recurrence, exp-5 standard). One answer → deferred; round-5 ledger |

## Clean territories (corner exercised, no failure — findings, not omissions)

- **Territory 1 `sui-import-path` — clean under targeted elicitation.** All six answers wrote
  `use sui::sui::SUI;` with `Coin<SUI>`/`Balance<SUI>` in active use. The ×4-cumulative top
  ledger class did not reproduce in a 3-task targeted probe under the loaded pack. (Its four
  recorded events all came from held-out *experiment* draws; whether the difference is draw
  variance or elicitation shape is not measurable from n=6.)
- **Territory 4 `generic-transfer-key-bound` — clean on the invited corner, second consecutive
  probe.** All six answers chose sound bounds: `T: key + store` where the bare item is
  transferred (gen-1 both models), or a `key + store` wrapper over `T: store` (gen-2/gen-3) —
  the two failing gen runs failed on *other* classes (above). The class's three recorded events
  all come from remeasure/experiment runs, never from its own territory probe — recorded as-is.
- **Territory 5 `object-identity` — clean, corners engaged.** `object::delete` ×4, event fields
  typed `ID` (via `object::id`/`uid_to_inner`), registries keyed by identity (one answer used
  the object's address form — semantically defensible, compiles). No UID reuse, no UID-in-event.
- Territory 2's return-arrow shape (×4 on the ledger) also did **not** fire: all six
  constructors used `: T` returns, including a tuple return. The two territory-2 hits were the
  *other* invited shape (compound-assign) and a new sibling (while-parens).
- Territory 3's tuple-key and vector-method shapes did not fire either: rapi-1 both models
  encoded pair keys as `copy+drop+store` structs (`Pair`/`DuelKey`); on rapi-2, sonnet used
  the method forms `.length()`/`.borrow()` and haiku the function forms
  `vector::length`/`vector::borrow` — neither reached for Rust's `.len()`/`.get()`. The one
  T3 hit was the `std::mem` family.

## Warnings on passing runs (recorded, not beats)

- **W99001 non-composable-transfer ×3** (suimport-1/haiku, suimport-3/haiku, suimport-2/sonnet)
  — the loaded round-2 grounding rule ignored again, consistent with the standing
  ignored-while-loaded phenomenon (warning-tier).
- **W99003 coin-field ×1 on passing runs** (suimport-1/haiku, `proceeds: Coin<SUI>`); the
  failing suimport-2/haiku log carries a second (`pot: Coin<SUI>`) — two data points for the
  excluded class this round; the exclusion reasoning stands.
- **W04037 deprecated ×1** (oid-3/haiku, `*string::bytes(&street)`).

## Notes

- rapi-3/haiku avoided the swap corner legally: it gave `Battery` `copy, drop, store`, making
  `let old = robot.battery; robot.battery = fresh;` a copy-then-overwrite. Compiles clean;
  semantically loose (serial numbers are copyable); recorded as a dodge, not a failure.
- **Beat list for this round: 4** — `borrow-arg-alias` (E07001), `compound-assignment`
  (E01002 `+=`), `while-condition-parens` (E01002), `std-mem-swap` (E03002). All four proceed
  to corpus research and RED/GREEN fixtures.
