# Experiment 8 — held-out falsification of deepening round 6

**Verdict: NO HEADLINE (ship-rule branch 3).** kp134 3/6 vs kp128 5/6 compile-pass (base
4/6); clean-compile tied 2/6 = 2/6 = 2/6. Branch 1 does not fire; the pack arm sits *below*
its predecessor this draw — attributed below to untaught-class draw variance, not to the
round-6 beats.

Pre-registered at `4247c97` before any answer (arms, full payload SHAs, frozen rule, the
declined-class observational analysis, the per-class carrier map; six tasks through a
two-pass pre-freeze review — the first pass replaced an escrow-swap restatement and a
restatement of round-6's own opt-2). Model: claude-haiku-4-5, all arms. Per-run verdicts:
[answers/results.txt](answers/results.txt).

## The selection-method comparison (this experiment's purpose)

| round | selection method | tier-2 verdict | margin |
|---|---|---|---|
| round 5 (exp-7) | frequency-promoted ledger classes; two beats from held-out REDs | **branch 1 — ships** | **+3** (5/6 vs 2/6) |
| round 6 (exp-8) | old-way: probe-elicited beats only | **branch 3 — no headline** | −2 (3/6 vs 5/6) |

Under identical protocols, adjacent rounds, same model and gate: **the frequency-selected
round shipped and the old-way round did not.** Two rounds cannot prove a mechanism, but every
recorded observable lines up: round 6's own probe found all five seeded territories clean
(the old-way well dry), its remeasure watched the declined classes fire same-day, and this
falsification's pack-arm failures land on classes the old way could not or did not teach.
The working conclusion for round 7: **beat selection by measured held-out frequency is the
program's method of record**; probe elicitation remains the fixture-evidence source where it
fires, not the selection criterion.

## Results

| task | base | kp128 | kp134 |
|---|---|---|---|
| wine-cellar | PASS WARN3 | PASS CLEAN | PASS CLEAN |
| plant-clinic | PASS CLEAN | FAIL E03002 — `use std::table` (**`std-table-path`, ×2 cumulative → promoted round-7 candidate**) +11 cascades | FAIL E04004 — `Option<(vector<u8>, vector<u8>)>`: a TUPLE as a type argument — **`tuple-bleed`, the class round 6's review flagged as a missed beat, firing through its pre-registered carrier** |
| ferry-manifest | FAIL E01002 (parse at the capacity `if`) +7 | PASS WARN2 | FAIL E04007 — `coin::take(&mut toll_payment, …)` on a `Coin` (take operates on `Balance`) — the api-argument family round 5 seeded and round 6 probed clean |
| quilt-bee | PASS WARN5 | PASS WARN1 | FAIL E04004 ×2 (+21 cascades) — `vector<(address, Square)>`: **`tuple-bleed` again, the second pre-registered carrier** |
| tide-tables | PASS CLEAN | PASS CLEAN | PASS CLEAN |
| apple-press | FAIL E05001 (vector-field ability) | PASS WARN1 | PASS WARN1 |

## Mechanism analysis (pre-registered standard)

- **Round-6 taught classes: zero recurrence in any arm.** No `Option<&T>`/reference-in-type-
  arg shape and no contains-by-value anywhere — both E04004s in kp134 are the **tuple**
  shape, a different pinned rule (tuples are not single types) from the taught
  reference-type-argument (references are not types). The taught beats neither fired nor
  were exercised — their carrier baits elicited the *tuple* sibling instead.
- **The declined/missed classes did the damage, exactly as the observational pre-registration
  anticipated:** `tuple-bleed` ×2 (kp134's plant-clinic and quilt-bee — the round-6 review's
  missed-beat catch, now with held-out teeth), `std-table-path` ×1 more (kp128's
  plant-clinic — ×2 cumulative, promoted), and ferry/kp134's `coin::take`-on-Coin extends the
  api-argument family (×2 with exp-6's `coin::put` shape → promoted as
  `balance-api-on-coin`). **Attribution note:** tuple-bleed is untaught in BOTH pack arms and
  in base; its two kp134 firings against zero kp128 firings on the same tasks is draw
  variance in design choice (kp128's answers happened not to reach for tuples), so the
  3-vs-5 gap is NOT evidence that round 6's beats harmed the pack — the honest statement is
  that round 6 added nothing measurable here, while the classes it left untaught were
  decisive.
- **Import sweep (point #5): 0 fails** (only ferry-manifest bears SUI; CORRECT in all three
  arms — the taught beat loaded in both pack arms, base correct by draw).
- **Round-7 ledger (now rich):** `tuple-bleed` (×3 cumulative counting round-6's opt-1 —
  top candidate), `std-table-path` (×2, promoted), `balance-api-on-coin` (`coin::take`/`put`
  on `Coin`, ×2, promoted), `std-option-path` (×3, carried), `moved-value-arg-order` (×2,
  carried), `branch-type-mismatch` (×2, carried), plus the ignored-rule ledger (`use-self`
  ~11 events) which no beat can address.

## Reading

Round 7, when it runs, should teach from the frequency ledger — it now holds three promoted
classes with held-out evidence — and the tuple-bleed episode becomes the program's cleanest
cautionary tale: a reviewer caught the class, the old-way rule declined it, and the very next
falsification paid for it twice. n = 6 everywhere; absolute numbers not cross-comparable;
the selection-method conclusion rests on the exp-7/exp-8 verdict pair plus the round-6
probe/remeasure record, all pre-registered, none individually decisive.
