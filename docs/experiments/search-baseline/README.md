# Experiment: does a package beat an agent with a search engine?

**Date:** 2026-07-06 · **Package:** [`examples/rubric-based-rl-nonverifiable`](../../../examples/rubric-based-rl-nonverifiable)
· **Result: no — and the tool said so itself.** The blind quality panel preferred the search-armed
baseline **6–0**, which vetoed the mechanical win (exit 1, `KP DID NOT HELP`).

## Why this experiment

Every shipped falsification compares a KP-loaded agent against **unaided recall** — the model answering
from memory. That is the honest baseline for the question kp-build asks ("is the model weak here?"),
but it is not the strongest competitor: real agents have web search. And the two mechanical axes can't
referee this match-up fairly — the KP side's precision ≈ 1.0 is instruction-following, and recall is
graded against the package's own spine (see the *honest limit* in the main README). This run was the
first test of the **blind quality panel** as the non-circular axis, against the strongest cheap
baseline we can field.

## Method

Same held-out question the package's shipped falsification used (the full related-work task for
self-evolving rubric-based RL). Two answer agents, same model:

- **base** — `WebSearch`/`WebFetch` allowed (it made 10 searches), no package.
- **kp** — no search; the package's `CONTEXT.md` briefing injected via `make_prompts`.

Scored with `kp-build falsify <pkg> --no-record ...` (live citation checks), then a 6-round blind
panel: `--emit-judge-prompts 6` → each prompt to a **fresh** judge subagent (no shared context) →
recorded slot verdicts fed back via `--judge-rounds`. Answers are committed here as
`base-search-answer.txt` / `kp-answer.txt`; the tally is `result.json`.

## Results

| axis | base (search) | kp (package) |
|---|---|---|
| citations real / checked | **12 / 12** | 12 / 12 (+3 transient) |
| precision | 1.00 | 1.00 |
| spine adoption (recall) | 0.27 | 1.00 |
| f1 | 0.42 | 1.00 |
| **blind panel** | **preferred, 6–0** | — |

- **Mechanically, "KP HELPS — f1 0.42 → 1.00"** — but the entire margin is spine adoption, the circular
  axis: the KP agent cited the paper set it was handed. Search killed the fabrication problem outright
  (12/12 real cites), so precision — the axis that made the unaided baseline lose on this same package —
  contributed nothing.
- **The blind panel preferred the search answer in all 6 rounds.** The recorded verdicts alternate
  `b,a,b,a,b,a` — every judge tracked the same underlying answer through the slot swap, so this is a
  genuine preference, not position bias. Both answers cited only real papers, but they surveyed
  substantially different 2026 papers; the judges found the search agent's framing and critical
  engagement stronger.
- **The veto fired:** `judged-worse` overturned the mechanical win → `KP DID NOT HELP — ... whatever
  the spine numbers say`, exit 1.

## What this means (and doesn't)

1. **The panel does its job.** Without it, this run would have been recorded as a 0.42 → 1.00 win. The
   non-circular axis caught what the spine numbers structurally cannot: against a searching agent, this
   package did not make the *answer* better.
2. **The value claim sharpens.** A package's measured edge is over **unaided recall** — fabrication and
   blind spots — plus what search can't give you: verified-by-construction citations, a reusable asset
   with zero per-query latency/cost, and offline determinism. Where live search is available, cheap, and
   the topic is searchable, the quality edge shrinks — and kp-build now measures that instead of
   asserting around it.
3. **Honest limits of this run:** one topic, one search-agent sample (n=1); judges share a model family
   with both authors; the search agent spent ~10 live searches the KP agent didn't need; and the KP
   answer's 3 unresolved cites were index transients, not fakes.

## Reproduce

```bash
Q="$(python3 -c "import json;print(json.load(open('examples/rubric-based-rl-nonverifiable/wikillm.json'))['falsification']['question'])")"
kp-build falsify examples/rubric-based-rl-nonverifiable --no-record --question "$Q" \
  --base docs/experiments/search-baseline/base-search-answer.txt \
  --kp   docs/experiments/search-baseline/kp-answer.txt \
  --judge-rounds b,a,b,a,b,a          # the recorded 6-round panel (result.json)
```
