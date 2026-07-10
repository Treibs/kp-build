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

## What this settles

Round 4's targeted probe recorded the SUI-import territory **clean 6/6** while the class kept
firing in held-out draws (×5 cumulative). This experiment reproduces both behaviors under one
pack in one draw: focal tasks (the round-4 probe's shape — payment IS the task) elicit 1/8;
incidental tasks (the held-out failures' shape — payment as a side requirement of a
non-coin core) elicit 3/8. **The clean probe was an elicitation artifact, not coverage.**
The mechanism reads as salience: when coin handling is the task's center of attention the
import is written correctly; when it is one concern among many, the model reaches for the
plausible-but-wrong `sui::coin` re-export habit.

## Actions (per the frozen map)

1. **Round-5 probe tasks adopt the incidental shape for every territory** — the corner under
   test is made a side requirement of a non-focal core, not the task's headline.
2. **The SUI-import beat is taught in round 5**, with this experiment's failing answers as
   the observed RED evidence (wrong-module shape; the exact E03003 fragment above).
3. Standing correction to clean-territory claims: a clean probe at n≈6 bounds a class's
   per-answer rate at roughly p < 0.3, nothing stronger — and says nothing at all about
   differently-shaped elicitation.

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
