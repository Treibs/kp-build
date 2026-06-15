# Examples

Real packages built by `kp-build`, kept as reference output and regression fixtures.

Three packages, three regimes — together they show what the `probe` pre-screen and the falsification
gate actually discriminate (and the blind spot one of them drove a fix for):

| package | topic regime | `probe` | falsification verdict |
|---|---|---|---|
| [`discrete-diffusion-llms/`](#discrete-diffusion-llms) | model-**weak**, model *fabricates* | BUILD | **KP HELPS** — wins on *precision* (kills mislabeled cites) **and** recall |
| [`speculative-decoding-llms/`](#speculative-decoding-llms) | model-**known** | SKIP | **KP HELPS on coverage only** — precision already 1.0; the win is pure recall |
| [`rubric-based-rl-nonverifiable/`](#rubric-based-rl-nonverifiable) | model-**weak**, model *hedges* (post-cutoff 2026) | BUILD† | **KP HELPS hugely** — recall 0.07→1.00 |

† **This package exposed a probe blind spot and drove a fix.** The probe was originally *precision-only* — it
greenlit a build only when the unaided model *fabricated* citations. A well-calibrated model that *hedges*
(cites a few real foundational papers but writes a placeholder like `arXiv:2510.xxxxx` for the frontier it
can't recall) cleared the "enough real cites" floor and wrongly read as **SKIP**, even while covering almost
none of the actual frontier. The probe now also **counts hedges** — a masked id is proof the model knows the
frontier holds work it cannot name — and greenlights on them, so it correctly **BUILD**s this topic. (The
full, recall-aware falsification was the backstop that caught the value the old probe missed.)

## `discrete-diffusion-llms/`

A wikillm knowledge package on **discrete / masked diffusion language models for text generation**
— deliberately a *model-weak* frontier topic (roughly half the citation spine is post-training-cutoff:
e.g. `2511.19152`, `2512.10858`, `2512.15745`, `2602.15014`, `2603.01367`).

Built end-to-end by the `/kp-build` skill: a multi-agent research wave found real papers per
sub-question, then the engine **verified every citation live against arXiv/Crossref** before
assembling. It is a valid [0xLT/kpm](https://github.com/0xLT/kpm) package (`knowledge.json` +
wiki-linked notes) — `kpm doctor` / `kpm pack` accept it as-is.

| | value |
|---|---|
| citations verified | **19 / 19** (live, `match_score` 1.0) |
| claims / open problems / debates / benchmarks | 37 / 8 / 3 / 13 |
| `CONTEXT.md` (agent payload) | ~6k tokens |

### Reproduce

```bash
kp-build build -i examples/discrete-diffusion-llms.research.json -o /tmp/ddl --no-verify   # offline
# or, with the real citation gate (hits arXiv/Crossref):
kp-build build -i examples/discrete-diffusion-llms.research.json -o /tmp/ddl
```

### Falsification — does the package actually help?

Held-out task: *write a related-work section on the 2024–2026 diffusion-LLM frontier, with arXiv
citations.* A **base** agent (unaided recall) vs a **KP-loaded** agent (given `CONTEXT.md`), scored on
citation precision (does each cited id resolve **and** match the paper named?) and spine recall:

| | base (memory) | KP-loaded |
|---|---|---|
| precision | 0.62 | **1.00** |
| recall (spine coverage) | 0.26 (5/19) | **0.84 (16/19)** |
| **f1** | **0.37** | **0.91** |

**Verdict: KP HELPS.** Unaided, the base agent recalled only ~5 of the 19 frontier papers and
**mislabeled 3 citations** — it swapped the titles of `2406.04329` (MD4) ↔ `2406.07524` (MDLM) and
cited `2410.17891` (DiffuLLaMA) for "Scaling up Masked Diffusion Models on Text" (really `2410.18514`).
These are *real-id-wrong-paper* errors the package eliminates. The two answers
(`*.base-answer.txt`, `*.kp-answer.txt`) and the verdict (in the package's `wikillm.json`) are kept
for audit. Re-score with:

```bash
kp-build falsify examples/discrete-diffusion-llms \
  --question "2024-2026 frontier of discrete/masked diffusion LMs" \
  --base examples/discrete-diffusion-llms.base-answer.txt \
  --kp   examples/discrete-diffusion-llms.kp-answer.txt
```

## `speculative-decoding-llms/`

A wikillm knowledge package on **speculative decoding for fast LLM inference** (draft-then-verify
acceleration: EAGLE-1/2/3, Medusa, Lookahead/Jacobi, SpecInfer-style tree verification, and the
2024–2026 serving-regime frontier — `2509.04474`, `2505.13204`, `2603.12617`, `2605.08632`).

This one is the deliberate **counterpoint** to the diffusion example: a topic the model already
**knows**. The `probe` pre-screen said so before any build —

```
$ kp-build probe --answer examples/speculative-decoding-llms.base-answer.txt --question "Speculative decoding ..."
topic pre-screen: SKIP — the model already knows this (a package adds ~0 value)
  unaided base agent: 9 cited · 9 real · 0 fabricated/mislabeled · hallucination 0%
```

We built it anyway as a fixture, to show what the falsification gate honestly reports when the
model *isn't* weak. Every citation was verified live and **every claim passage was machine-grounded**
against its paper's abstract (the grounding gate, abstract-level):

| | value |
|---|---|
| citations verified | **17 / 17** (live) |
| claims grounded | **37 / 37** (`--ground`, 0 unconfirmed, 0 ungrounded) |
| claims / open problems / debates / benchmarks | 37 / 6 / 2 / 17 |
| `CONTEXT.md` (agent payload) | ~5.9k tokens |

### Reproduce

```bash
kp-build build -i examples/speculative-decoding-llms.research.json -o /tmp/spec --no-verify   # offline
# or, with the live citation gate + passage grounding:
kp-build build -i examples/speculative-decoding-llms.research.json -o /tmp/spec --ground
```

### Falsification — what "helps" means when the model already knows the field

Held-out task: *write a related-work section on the 2024–2026 speculative-decoding frontier, with
arXiv citations.* Base (unaided recall) vs KP-loaded (given `CONTEXT.md`):

| | base (memory) | KP-loaded |
|---|---|---|
| precision | **1.00** | **1.00** |
| recall (spine coverage) | 0.47 (8/17) | **1.00 (17/17)** |
| **f1** | **0.64** | **1.00** |

**Verdict: KP HELPS — but on *coverage*, not accuracy.** Unaided, the model cites cleanly (0%
hallucination — it knows the seminal and mid-frontier papers), so the package buys **no precision**.
What it buys is **recall**: the base agent recalled only 8 of the 17 spine papers and named none of
the post-cutoff 2025–2026 frontier (`2509.04474`, `2505.13204`, `2603.12617`, `2605.08632`); the
KP-loaded agent covers the whole spine. This is exactly the honest distinction the `probe` flagged up
front — on a model-known topic the value is traceability and completeness, not fewer fabrications.
Re-score with:

```bash
kp-build falsify examples/speculative-decoding-llms \
  --question "2024-2026 frontier of speculative decoding for LLM inference" \
  --base examples/speculative-decoding-llms.base-answer.txt \
  --kp   examples/speculative-decoding-llms.kp-answer.txt
```

## `rubric-based-rl-nonverifiable/`

A wikillm knowledge package on **rubrics-as-rewards: LLM-graded structured rubrics as the RL reward
signal for post-training in non-verifiable/open-ended domains** — a genuinely **2026-emergent** subfield
(RaR was coined mid-2025; the named-method wave — QUBRIC, RUBRIC-ARROW, EvoRubric, OpenRS, SRaR, RLCER,
AMARIS — and its reward-hacking failure literature crystallized in 2026). **14 of 15 spine papers carry
2026 arXiv ids** (`2602.*`–`2606.*`), i.e. post the model's training cutoff.

This is the case that **exposed — and fixed — a probe blind spot** (read the `†` note at the top first).
The topic was found by *browsing arXiv for what's new since the cutoff* — exactly because a model can't
name from memory what it was never trained on.

| | value |
|---|---|
| citations verified | **15 / 15** (live, 14 of them 2026 ids) |
| claims grounded | **42 / 43** (`--ground`; 1 unconfirmed, 0 ungrounded) |
| claims / open problems / debates / benchmarks | 43 / 7 / 2 / 13 |
| `CONTEXT.md` (agent payload) | ~6k tokens |

### The probe blind spot this example fixed

The unaided model cited **3 real papers** (the 2025 seeds) and *hedged* on the 2026 frontier — it wrote a
placeholder `arXiv:2510.xxxxx` rather than inventing an id. The **original** probe measured only fabrication,
so zero fabrication + 3 real cites read as SKIP — wrong, since the model covered just **1 of 15** spine
papers. That false-SKIP motivated **hedge detection**: a masked id is the model admitting it can't name a
paper it knows exists. The probe now counts hedges and greenlights:

```
# before the fix (precision-only):
topic pre-screen: SKIP — the model already knows this (a package adds ~0 value)
  unaided base agent: 3 cited · 3 real · 0 fabricated/mislabeled · hallucination 0%

# now (hedge-aware):
$ kp-build probe --answer examples/rubric-based-rl-nonverifiable.base-answer.txt --question "Rubrics-as-Rewards ..."
topic pre-screen: BUILD — the topic is model-weak (worth packaging)
  unaided base agent: 3 cited · 3 real · 0 fabricated/mislabeled · 2 hedged · hallucination 0%
  -> the unaided model hedged on 2 citation(s) it could not recall ... it knows the frontier holds work it cannot name
```

The full falsification — which measures **recall**, not just precision — confirms the call.

### Reproduce

```bash
kp-build build -i examples/rubric-based-rl-nonverifiable.research.json -o /tmp/rubric --no-verify   # offline
# or, with the live citation gate + passage grounding:
kp-build build -i examples/rubric-based-rl-nonverifiable.research.json -o /tmp/rubric --ground
```

### Falsification — the recall-aware gate catches what the probe missed

Held-out task: *write the related-work section for a 2026 self-evolving rubric-RL paper, citing the named
2026 systems and the reward-hacking literature.* Base (unaided recall) vs KP-loaded (given `CONTEXT.md`):

| | base (memory) | KP-loaded |
|---|---|---|
| precision | **1.00** | **1.00** |
| recall (spine coverage) | **0.07 (1/15)** | **1.00 (15/15)** |
| **f1** | **0.12** | **1.00** |

**Verdict: KP HELPS — massively, on recall.** The base agent, hedging honestly, engaged just **one** of the
15 frontier papers; the KP-loaded agent covered the whole spine including the post-cutoff named methods
(`2606.03968` QUBRIC, `2605.29847` EvoRubric, `2602.10885` RLCER, `2606.04923` reward-hacking, …). Precision
ties at 1.0 (the model never fabricated — it just didn't *know*), so the entire f1 jump 0.12→1.00 is
coverage the package supplied. This is the value the `probe` could not detect and the falsification could.
Re-score with:

```bash
kp-build falsify examples/rubric-based-rl-nonverifiable \
  --question "2026 frontier of rubric-based RL for non-verifiable domains" \
  --base examples/rubric-based-rl-nonverifiable.base-answer.txt \
  --kp   examples/rubric-based-rl-nonverifiable.kp-answer.txt
```
