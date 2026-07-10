# SUI-import elicitation experiment — verdict

**Verdict: ELICITATION CONFIRMED (frozen-rule branch 1, bar met exactly).** Import-fail
**incidental 3/8 vs focal 1/8** — `fail_I ≥ fail_F + 2` at zero margin (the salience draw's
recorded lesson on exactly-met bars applies and is carried here: n=8 per arm, one flipped
answer changes the branch). All four failures are the **wrong-module shape**
(`use sui::coin::{..., SUI}`), each corroborated by the exact
`E03003: Unbound member 'SUI' in module 'sui::coin'` buildlog line; zero absent-import
failures; zero n/a answers (all 16 used the `SUI` token; both denominators are 8).

Pre-registered at `72dfce6` before any answer (design, 16 audited tasks, the committed
mechanical checker `check_import.py`, the 3-branch rule with its round-5 action map:
[tasks.md](tasks.md)). Pack constant across arms: kp110 (sha `92756d2d…`, byte-identical to
experiment 6's arm). Model: claude-haiku-4-5. Per-run verdicts: [answers/results.txt](answers/results.txt).

## What this selects (correction, review round 1: this section originally said "settles")

Round 4's targeted probe recorded the SUI-import territory **clean 6/6** while the class kept
firing in held-out draws (×5 cumulative). In this draw, focal tasks (the round-4 probe's
shape — payment IS the task) elicited 1/8 failures and incidental tasks (the held-out
failures' shape) elicited 3/8 — the pre-registered branch-1 condition, so the elicitation
action branch is selected. **What the data does not do is establish the mechanism as fact:**
one-sided Fisher exact p ≈ 0.29 at n=8 per arm — under a no-shape-effect null this asymmetry
arises roughly 28% of the time, and the pre-registration's draw-variance alternative is not
strongly excluded. The consistent *direction* (this draw + all five held-out occurrences
being incidental-shaped) is why the branch design put the decision threshold where it did;
the round-5 probe running incidental-shaped is itself the replication test — if SUI-import
and its territory-mates fire there at held-out-like rates, the salience reading gains real
support; if not, this was noise and the record will say so.

## Actions (per the frozen map)

1. **Round-5 probe tasks adopt the incidental shape for every territory** — the corner under
   test is made a side requirement of a non-focal core, not the task's headline.
2. **The SUI-import beat is taught in round 5**, with this experiment's failing answers as
   the observed RED evidence (wrong-module shape; the exact E03003 fragment above).
3. Standing correction to clean-territory claims: a clean probe at n≈6 bounds a class's
   per-answer rate at roughly p < 0.3, nothing stronger — and says nothing at all about
   differently-shaped elicitation. (Attribution note, review round 2: this bound is frozen
   as branch 2's action text; it is branch-independent arithmetic and is adopted here as a
   standing caution alongside branch 1's two actions.)

## Context (observational, outside the metric)

- Overall compile-pass differed sharply by arm — **focal 7/8 vs incidental 2/8** — but this
  is confounded by design: incidental tasks are inherently multi-concept and harder. The
  import metric is the controlled comparison; the compile-pass gap is reported as context
  only.
- **One loaded-rule-ignored event:** I-recipe-book's gate failure is
  `use sui::balance::{self, Balance}` — lowercase `self` in a group import, the round-1
  taught `use-self` class firing with the rule in context (exact pinned class; the answer's
  SUI import itself was correct). Recorded, not re-taught, per the standing rule.
- Other incidental-arm gate failures for the round-5 ledger: I-pet-daycare E05001
  (ability constraint), I-carpool-log E04007 (incompatible types) — root-caused during the
  round-5 probe triage if their classes recur.


## Audit erratum + apparatus notes (review round 1)

- **Missed adjacencies, disclosed here** (frozen tasks.md untouched, standing erratum rule):
  I7 marathon ≈ sheet-confirm tournament-prize (enrollment + exact fee + organizer cap +
  close boundary + ranked top-three — the strongest miss, and one of the three I-arm fails);
  F5 bus-fare ≈ round-4 suimport-1 paywall (pay-exact → access object → pool → sweep; the
  audit dropped the cover-charge draft for this same spine yet kept bus-fare — the sole
  F-arm fail); F6 car-wash ≈ experiment-4 gift-card (stored-value card); F2 photo-booth and
  F3 jukebox ≈ round-2 coinlint-2 vending machine (pay → minted object → cap collects);
  I3 pet-daycare ≈ round-4 oid-2 pet registry (weaker tier, same tier as the disclosed
  I2/I6). Interpretation note: arms run fresh-context, so no prior task text reaches any
  answer — adjacency bears on the audit-hygiene claim and on how novel each arm's shapes
  are, not on information leakage. The F arm skews closer to previously-probed shapes than
  disclosed; on a bar-met-exactly result that asymmetry belongs in the record. Third audit
  miss in the series (experiment 6 had two) — the round-5 audit adds a reviewer pass BEFORE
  freeze.
- **Layout deviation:** the frozen layout named `{answer, -src.move, -pkg/, .buildlog,
  .result, .import}`; the committed files are `answer, src.move, pkg/, gate.buildlog,
  gate.result, import.result` (+ untracked `run.stderr`). Naming only; the metric and rule
  text are unchanged.
- **Checker holes, none exercised** (verified over all 16 sources by the branch review): a
  both-imports source would score FAIL wrong-module (defensible, diverges from the frozen
  "every use covered" phrasing); nested `use sui::{...}` groups, block comments, and `as`
  aliases are invisible to it. No source in this corpus hits any of these; the holes are
  recorded for reuse of the checker.

## Replication outcome pointer (added with round 5)

The named replication test ran in round 5's probe: import-fail **1/9** (haiku) against this
experiment's incidental arm 3/8 — recorded as **non-replication** per the commitment above;
the salience mechanism stays unestablished. Full record: `docs/deepening/round-5/triage.md`.
