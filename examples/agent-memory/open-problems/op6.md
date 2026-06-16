---
id: op6
statement: Selective forgetting / memory consolidation lacks principled, evaluated
  mechanisms; existing approaches range from Ebbinghaus-style decay to LLM-driven
  ADD/UPDATE/DELETE operators, but no consensus on when and what to forget.
flagged_by:
- zhong2023memorybank
- chhikara2025mem0
- du2025rethinkingmemory
- hu2025memoryagentbench
status: open
why_it_matters: Unbounded memory growth causes cost explosion and retrieval noise;
  wrong forgetting loses critical facts or fails to update superseded ones. Forgetting
  and consolidation are listed as core operations yet are the least benchmarked, making
  this a high-value gap for deployable agents.
flagged_by_ids:
- arXiv:2305.10250
- arXiv:2504.19413
- arXiv:2505.00675
- arXiv:2507.05257
---

Selective forgetting / memory consolidation lacks principled, evaluated mechanisms; existing approaches range from Ebbinghaus-style decay to LLM-driven ADD/UPDATE/DELETE operators, but no consensus on when and what to forget.

**Why it matters:** Unbounded memory growth causes cost explosion and retrieval noise; wrong forgetting loses critical facts or fails to update superseded ones. Forgetting and consolidation are listed as core operations yet are the least benchmarked, making this a high-value gap for deployable agents.

**Flagged by:** [[papers/zhong2023memorybank]] (arXiv:2305.10250), [[papers/chhikara2025mem0]] (arXiv:2504.19413), [[papers/du2025rethinkingmemory]] (arXiv:2505.00675), [[papers/hu2025memoryagentbench]] (arXiv:2507.05257)
