# Rubrics-as-Rewards: LLM-graded structured rubrics as the RL reward signal for post-training in non-verifiable, open-ended domains

*wikillm knowledge package (`@kp/rubrics-as-rewards-llm-graded-structured-rubrics-as`) — a research-landscape foundation.*

**Scope:** In scope: reinforcement learning methods that replace or augment verifiable rewards (RLVR) with structured, multi-criterion rubrics graded by an LLM judge as the dense reward for open-ended/subjective tasks (writing, dialogue, medicine, reasoning quality) — covering the original "Rubrics as Rewards (RaR)" formulation, its 2026 named descendants (e.g. self-evolving/auto-generated rubric systems, rubric-anchored policy optimization variants, rubric ensembling and EM-style judge training), the training recipes (GRPO/PPO with rubric aggregation), and the emerging rubric-reward-hacking / judge-gaming failure-mode literature with its mitigations. Out of scope: classic RLHF with a single scalar Bradley-Terry preference reward model; pure RLVR on math/code with programmatic checkers; LLM-as-a-judge purely for offline evaluation/benchmarking (not as an RL training signal); and general constitutional-AI / preference-optimization (DPO/RLAIF) methods that do not use explicit structured rubrics as the reward.

- 15/15 citations verified (arXiv/Crossref); source years 2025–2026
- 43 claims · 7 open problems · 2 debates · 13 benchmarks
- dropped (unverified-anchored): {'claims': 0, 'open_problems': 0, 'debates': 0, 'benchmarks': 0, 'positions': 0}

**Load `CONTEXT.md` into your agent** to inherit this field without re-running the research. `index.json` is the machine-readable graph (nodes + edges); the subdirectories hold the notes.

## Distribution

This is a [0xLT/kpm](https://github.com/0xLT/kpm) knowledge package (`knowledge.json`). Publish it as a tagged GitHub repo, then any consumer installs it with kpm — no re-research:

```bash
kpm add github:<owner>/<repo>#v0.1.0
kpm compose            # composes into a vault; load CONTEXT.md into your agent
```

Confidence is corpus-relative (conditional on the cited sources). Built 2026-06-15.
