---
id: op8
statement: 'The long-context-vs-RAG-vs-explicit-memory choice is not settled: results
  depend on resourcing, question type, and dataset, and dynamic routing (e.g., Self-Route)
  is a heuristic rather than a principled solution.'
flagged_by:
- li2024ragvslongcontext
- li2025longcontextvsrag
- liu2023lostmiddle
status: open
why_it_matters: Practitioners must choose between paying for long context, building
  retrieval, or maintaining explicit memory stores. Because long-context still has
  'lost-in-the-middle' failures and RAG wins on cost and on some query types, there
  is no general rule; a principled cost-aware policy for when to use each remains
  open.
flagged_by_ids:
- arXiv:2407.16833
- arXiv:2501.01880
- arXiv:2307.03172
---

The long-context-vs-RAG-vs-explicit-memory choice is not settled: results depend on resourcing, question type, and dataset, and dynamic routing (e.g., Self-Route) is a heuristic rather than a principled solution.

**Why it matters:** Practitioners must choose between paying for long context, building retrieval, or maintaining explicit memory stores. Because long-context still has 'lost-in-the-middle' failures and RAG wins on cost and on some query types, there is no general rule; a principled cost-aware policy for when to use each remains open.

**Flagged by:** [[papers/li2024ragvslongcontext]] (arXiv:2407.16833), [[papers/li2025longcontextvsrag]] (arXiv:2501.01880), [[papers/liu2023lostmiddle]] (arXiv:2307.03172)
