---
id: op2
statement: Long-term conversational memory remains substantially below human performance
  on long-range temporal and causal reasoning, even with long-context LLMs or RAG.
flagged_by:
- maharana2024locomo
- wu2024longmemeval
status: open
why_it_matters: Temporal reasoning (what was true when, knowledge updates, abstention)
  is precisely what persistent agents need over months of interaction. The ~30% accuracy
  drop on LongMemEval and the human gap on LoCoMo show neither stuffing context nor
  naive retrieval solves it; temporal modeling of memory is an unsolved core problem.
flagged_by_ids:
- arXiv:2402.17753
- arXiv:2410.10813
---

Long-term conversational memory remains substantially below human performance on long-range temporal and causal reasoning, even with long-context LLMs or RAG.

**Why it matters:** Temporal reasoning (what was true when, knowledge updates, abstention) is precisely what persistent agents need over months of interaction. The ~30% accuracy drop on LongMemEval and the human gap on LoCoMo show neither stuffing context nor naive retrieval solves it; temporal modeling of memory is an unsolved core problem.

**Flagged by:** [[papers/maharana2024locomo]] (arXiv:2402.17753), [[papers/wu2024longmemeval]] (arXiv:2410.10813)
