# kp-build — the wikillm Knowledge Package format

**One line:** a portable, citation-verified, agent-loadable knowledge package that gives an
LLM the research-landscape knowledge a human needs to *begin* a PhD-level paper on a narrow
topic — built once, shared, so nobody's agent has to re-spend the compute to reconstruct the field.

## Why this exists (and how it differs from kpm-build)
The Memory Doctrine's `kpm-build` distils *settled, consensus* knowledge into axioms. That is
exactly the knowledge an LLM already has in its weights, so the artifact added little. `kp-build`
inverts the target: it captures the **frontier** — the recent, specific, contested literature an
LLM is *worst* at (it hallucinates citations, is stale, and averages conflicting results to mush).

Differentiation from one-shot "deep research" reports: a wikillm package is **persistent**,
**citation-verified** (no hallucinated papers — every cite checked against arXiv/Crossref),
**structured for reuse** (a standard portable schema), and **agent-loadable** (a token-bounded
digest plus a machine index). It is a reusable knowledge *asset*, not a report.

## What is load-bearing (priority order)
1. **Verified citation spine** — real, existing papers (arXiv id / DOI checked), organized by
   sub-problem. A fake or wrong citation is fatal for a paper foundation, so verification is a
   hard gate, not a nicety.
2. **Open-problems register** — the gaps: what's unsolved, what authors explicitly flag as
   future work / limitations, where the field is stuck. *This is where a paper's contribution
   lives — the single most valuable section, and the hardest to fabricate.*
3. **Debate map** — contested points: competing positions and which papers hold them. (This is
   the doctrine's "value lives in the connections," finally pointed at something real.)
4. **Claims** — grounded findings/results/methods, each anchored to a verified paper + verbatim
   passage + confidence. (Like axioms, but paper-anchored and confidence-labelled.)
5. **Concepts** — definition/taxonomy scaffolding (least valuable; the model mostly has this).

## Package schema (v1) — a portable directory
```
<topic-slug>/
  wikillm.json            # manifest: schema_version, topic, scope, built, stats, falsification result
  CONTEXT.md              # THE agent-loadable digest — token-bounded field briefing
  README.md               # human entry point
  papers/<cite_key>.md    # one verified citation object per source paper
  claims/<id>.md          # grounded, paper-anchored claims
  open-problems/<id>.md   # the gaps register
  debates/<id>.md         # contested points
  index.json              # machine-readable graph: nodes + edges (paper↔claim↔problem↔debate)
```

### Citation object (`papers/<cite_key>.md` frontmatter)
`cite_key, title, authors, year, venue, arxiv_id?, doi?, url, verified{exists, via, canonical_title, checked}, key_contributions[]`
A paper with `verified.exists == false` MUST NOT anchor any shipped claim (validate fails).

### Claim object (`claims/<id>.md`)
`statement, paper (cite_key), supporting_passage, claim_type{result|method|finding|definition},
confidence{high|medium|low}, corroborated_by[cite_key]`. Confidence is corpus-relative.

### Open-problem object (`open-problems/<id>.md`)
`statement (the gap), flagged_by[cite_key] (papers that explicitly call it open/future-work),
status{open|partially-addressed}, why_it_matters`. Must be flagged by ≥1 verified paper.

### Debate object (`debates/<id>.md`)
`question, positions[{stance, papers[cite_key], summary}], resolved{bool}`.

### CONTEXT.md (the agent payload)
A token-bounded (default ~6k tokens) briefing an agent loads to inherit the field: scope, the
verified paper list (with ids), key claims by sub-area, the open-problems register, the debates.
This is what makes the package "compute-amortizing" — load it, skip the research.

## Pipeline (the skill orchestrates; the engine assembles)
1. **Scope** — a narrow research area + the sub-questions a paper's related-work must answer.
2. **Survey** — find core papers by search AND citation-graph expansion (follow the references /
   citations of seed papers), not keyword search alone — to fight the "missed the seminal paper" failure.
3. **Extract** — per paper, grounded claims (verbatim passage), its stated open problems /
   limitations / future work, and its position on any debate.
4. **Verify citations** — every paper checked against arXiv/Crossref; unverifiable papers are
   dropped (and logged, never silently).
5. **Synthesize** — cluster claims by sub-problem; build the open-problems register and debate map.
6. **Assemble + validate** — write the package; lint (cites resolve to verified papers, problems
   flagged, no orphans).
7. **Falsify (acceptance gate)** — a KP-loaded agent vs a base agent on a held-out task
   ("write the related-work + name 3 real open problems"), judged for correctness and ZERO
   hallucinated citations. A package that doesn't beat base+sources is not shipped as useful.

## Non-negotiables
- No hallucinated citations (hard gate).
- Coverage is scope-relative and can be too shallow — citation-graph expansion mitigates; the
  manifest records what was searched so the gap is honest.
- The package is stale the day a field moves; the manifest carries `built` + a re-run is a diff.
