# Examples

Real packages built by `kp-build`, kept as reference output and regression fixtures.

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
