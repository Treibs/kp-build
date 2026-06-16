---
id: op3
statement: Adding knowledge-graph structure to retrieval improves sense-making and
  associativity but degrades basic factual memory below plain vector RAG — a tension
  no single architecture had resolved before HippoRAG 2, and the general trade-off
  remains active.
flagged_by:
- gutierrez2025hipporag2
- rasmussen2025zep
status: partially-addressed
why_it_matters: Structured memory (KGs, temporal graphs) is the leading direction
  for associative/multi-hop recall, but if it sacrifices simple fact lookup it is
  not a drop-in replacement. Reconciling structured and unstructured memory so both
  factual and associative recall improve is a live design problem.
flagged_by_ids:
- arXiv:2502.14802
- arXiv:2501.13956
---

Adding knowledge-graph structure to retrieval improves sense-making and associativity but degrades basic factual memory below plain vector RAG — a tension no single architecture had resolved before HippoRAG 2, and the general trade-off remains active.

**Why it matters:** Structured memory (KGs, temporal graphs) is the leading direction for associative/multi-hop recall, but if it sacrifices simple fact lookup it is not a drop-in replacement. Reconciling structured and unstructured memory so both factual and associative recall improve is a live design problem.

**Flagged by:** [[papers/gutierrez2025hipporag2]] (arXiv:2502.14802), [[papers/rasmussen2025zep]] (arXiv:2501.13956)
