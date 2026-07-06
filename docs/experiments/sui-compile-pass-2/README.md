# sui-move falsification — experiment 2 (pre-registered, harder tasks, dual metric)

**Pre-registration:** [`tasks.md`](tasks.md), committed at `443981c` **before any
answer was collected**. Experiment 1 (`../sui-compile-pass/`) had hit a ceiling
(base 5/5 vs kp 5/5 compile-pass); this run used 5 harder held-out tasks and two
pre-registered metrics with an explicit ship rule.

## Results

| Task | base | kp |
|---|---|---|
| 1 flash-loan (hot potato) | PASS clean | PASS clean |
| 2 object-mailbox (Receiving\<T\>) | **FAIL** | **FAIL** |
| 3 generic-vault (phantom) | PASS 1 warning | PASS clean |
| 4 nft-display (Publisher/Display) | PASS 1 warning | PASS clean |
| 5 kiosk-listing (TransferPolicy) | PASS clean | PASS 3 warnings |
| **compile-pass (primary)** | **4/5** | **4/5** |
| **clean-compile (secondary)** | **2/5** | **3/5** |

Raw log: [`results.txt`](results.txt).

**Verdict under the pre-registered ship rule:** primary ties (4/5 vs 4/5); secondary
kp 3/5 > base 2/5 → **rule branch 2 → the pack ships.** The pack does not make
sonnet compile more of these harder contracts, but it measurably shifts output
toward the modern idiom set the toolchain's linter enforces.

## Failure detail (both arms, task 2)

Both arms failed **identically** on the same error — `Sui E02009: invalid private
transfer call`: calling `transfer::receive<T>` with a generic `T` not declared in
the current module (the correct call for foreign `store` types is
`transfer::public_receive` with `T: key + store`). Notably the kp answer's own
comments *describe* this exact caveat and then the code uses `transfer::receive`
anyway. The pack has no Receiving/`transfer::receive` beat — this is an honest,
actionable gap for a future pack revision, recorded here rather than patched
post-hoc.

## Warning detail

- base task-3, task-4: `Lint W99010` (unnecessary `entry` on a `public` function) —
  a weakness the pack explicitly targets (entry-vs-public beat); kp produced zero.
- kp task-5: `Lint W99000` (possible owned object share) + 2× `Lint W99001`
  (non-composable transfer to sender) — composability lints on the kiosk wrapper
  functions, a zone the pack does not cover.

## Combined record (experiments 1 + 2)

| | exp 1 (easy tasks) | exp 2 (hard tasks) |
|---|---|---|
| compile-pass | base 5/5 = kp 5/5 (ceiling) | base 4/5 = kp 4/5 (tie) |
| clean-compile | post-hoc only: base ~6 warnings vs kp ~2 | **pre-registered: base 2/5 vs kp 3/5, kp wins** |

The exp-1 post-hoc warning observation predicted the exp-2 pre-registered result.
Scope of the shipping claim: **the pack improves output cleanliness/modern-idiom
compliance on the pinned toolchain; it does not raise raw compile-pass rate for
claude-sonnet-4-6 on tasks of this difficulty.**
