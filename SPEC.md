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
4. **Claims** — findings/results/methods, each anchored to a verified paper + a supporting passage +
   confidence. (Like axioms, but paper-anchored.) *The passage can be machine-grounded: `kp-build build
   --ground` confirms it actually appears in the paper (the arXiv abstract for free, or ar5iv fulltext),
   marking each claim `grounded` (✓, confirmed), `unconfirmed` (not in the abstract — may be in the
   body), or `ungrounded` (checked the fulltext, not there → capped + flagged). Confidence stays
   corpus-relative. Fuzzy matching accepts on the single longest contiguous block covering ≥60% of the
   passage — which alone would let a long quote with one tampered number (year/percentage/measurement)
   near an end still verify. A digit guard closes this: on the fuzzy path every number token in the
   passage must also appear in the text, else the verdict downgrades to `unconfirmed` (abstain, not
   `ungrounded` — number formatting legitimately varies). Exact substring matches are exempt.*
5. **Concepts** — definition/taxonomy scaffolding (least valuable; the model mostly has this).

## Package schema (v1) — a portable directory (and a valid 0xLT/kpm package)
```
<topic-slug>/
  knowledge.json          # the 0xLT/kpm package CONTRACT — the distribution envelope (see below)
  wikillm.json            # wikillm manifest: schema_version, topic, scope, built, stats, falsification
  CONTEXT.md              # THE agent-loadable digest — token-bounded field briefing (the payload)
  README.md               # human entry point + kpm install snippet (kpm entrypoint)
  papers/<cite_key>.md    # one verified citation object per source paper
  claims/<id>.md          # grounded, paper-anchored claims
  open-problems/<id>.md   # the gaps register
  debates/<id>.md         # contested points
  benchmarks/<id>.md      # reported SOTA results (method/dataset/metric/value)
  index.json              # machine-readable graph: nodes + edges (paper↔claim↔problem↔debate)
```
Every note's `[[wikilink]]` is path-qualified (`[[papers/<cite_key>]]`) so kpm resolves it by exact
package path — collision-proof, and `kpm doctor`/`kpm pack` accept it as-is.

## Distribution — kp-build builds, 0xLT/kpm distributes (no reinvention)
kp-build owns the **content** (research + verification + authoring); [`0xLT/kpm`](https://github.com/0xLT/kpm)
owns **distribution** (install / lock / compose / pack / share). The seam is `knowledge.json`: by
emitting the kpm package contract, a wikillm package *is* a first-class kpm package, so "build once,
share" is the existing kpm CLI — there is no separate distribution layer to build.

`knowledge.json` is the protocol's CLOSED field set (kpm rejects unknown keys):
```json
{ "name": "@kp/<topic-slug>", "version": "0.1.0", "description": "<scope>", "license": "CC-BY-4.0",
  "type": "knowledge-package", "files": ["**/*.md", "wikillm.json", "index.json"], "entrypoint": "README.md" }
```
- `name`/`version`/`license` are **publisher-overridable** (`--name/--version/--license`); whoever
  publishes the package tags it however they like. Default name is `@kp/<topic-slug>`, version `0.1.0`.
- The wikillm-specific richness (verified-spine stats, coverage, falsification, the graph) can't live
  in `knowledge.json` (closed set), so it rides alongside in `wikillm.json`/`index.json`, carried into
  the package by the `files` glob.

**The shareable lifecycle (all existing kpm commands):**
```bash
kp-build build -i research.json -o ./pkg     # produces a valid kpm package
cd ./pkg && kpm doctor && kpm pack           # validates + writes a shareable .tgz
# publish ./pkg as a tagged GitHub repo, then any consumer:
kpm add github:<owner>/<repo>#v0.1.0 && kpm compose   # inherits CONTEXT.md — no re-research
```
Verified end-to-end against the real kpm CLI (doctor ok → pack → consumer add/compose).

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
7. **Falsify (acceptance gate)** — `kp-build falsify <dir> --question … --base … --kp …` scores a
   KP-loaded agent vs a base agent on a held-out task, on **precision** (cited papers that actually
   exist) AND **recall** (spine adoption), records the f1 verdict into the manifest (atomically —
   write-then-rename; `--no-record` to score without touching it), and tells you honestly if the
   package does not beat base (e.g. on a topic the model already knows). **Honest limit:** both
   mechanical axes favor the KP side by construction — the KP agent is instructed to cite the spine
   it was handed, and recall is graded against that same spine. The optional **blind quality panel**
   (`--emit-judge-prompts N` → fresh judges → `--judge-rounds a,b,…`) is the non-circular axis: it
   replays recorded slot-alternated A/B verdicts through the same JudgeVerifier the build uses
   (even-length panels only), and a judged-worse panel *vetoes* a mechanical win. Without a panel,
   the verdict discloses what it does not certify.

## Non-negotiables
- **No hallucinated citations (hard gate).** A citation is `verified` only when an explicit arXiv id
  or DOI resolves AND its canonical title strictly matches; title-only cites are `unconfirmed` and
  cannot anchor a shipped claim. The gate never rescues a mismatched id via a title search.
- Coverage is scope-relative and can be too shallow — citation-graph expansion mitigates; the
  manifest records what was searched so the gap is honest.
- The package is stale the day a field moves; the manifest carries `built`, and `kp-build refresh <dir>`
  reports age + post-build citation-graph candidates + a re-probe prompt (exit 0 fresh / 1 stale /
  3 inconclusive).
