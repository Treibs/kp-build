---
name: kp-build
description: >-
  Build a wikillm knowledge package: a portable, citation-verified, agent-loadable research-landscape
  foundation for starting a PhD-level paper on a NARROW topic. You scope it, dispatch survey subagents
  that find real papers (by search AND citation-graph expansion), extract grounded claims + the open
  problems each paper flags + the field's debates, verify every citation against arXiv/Crossref (no
  hallucinated papers), and assemble a package whose CONTEXT.md another agent loads to inherit the field
  without re-running the research. Use when someone wants the literature foundation to begin original
  research — NOT for settled textbook knowledge the model already has (that adds nothing).
---

# kp-build — `/kp-build`

You are the orchestrator. The user gives a narrow research area; you map its frontier into a
**wikillm package** — a reusable, verified, agent-loadable knowledge asset. **You + subagents do the
judgment (find, read, extract, synthesize); the Python engine (`kp_build`) does the mechanical,
deterministic part: verify every citation, assemble, lint.**

**Why this is not kpm-build:** kpm-build distils *settled* knowledge into axioms — which the model
already has. kp-build targets the *frontier*: recent, specific, contested literature the model is
worst at. The value is (1) verified citations (no hallucinations), (2) the open-problems register
(where new work goes), and (3) compute amortization (build once, anyone's agent loads it).

## Non-negotiables
- **No hallucinated citations.** Every paper is checked against a real index; unverifiable papers are
  dropped. The engine enforces this — but draft cites with a real `arxiv_id` or `doi` so they verify.
- **Scope narrow.** One package = one paper-sized research area ("speculative decoding for LLM
  inference"), not a whole field ("LLM inference") and not one paper.
- **The open-problems register is the point.** Mine each paper's *future-work / limitations /
  conclusion* sections for what it says is unsolved. A package with no open problems is a failure.
- **Coverage is scope-relative and can be too shallow.** Fight "missed the seminal paper" with
  citation-graph expansion (step 2), and record what you searched so the gap is honest.

## Setup
```
pip install -e ~/kp-build      # provides the `kp-build` CLI and the kp_build engine
```
Citation verification uses arXiv + Crossref (free, no key, network required).

## Procedure

### 1 — Scope (the one human step)
Confirm with the user: the **narrow research area**, the **sub-questions** a paper's related-work
must answer, and **in/out of scope**. Keep it tight. This defines "done."

### 2 — Survey (find the REAL papers — search + citation graph)
Dispatch survey subagents. Each must return real papers with a verifiable handle:
`{cite_key, title, authors, year, venue, arxiv_id?, doi?, url, key_contributions[]}`.
**Do two passes, not one:**
- (a) **Search** — arXiv, Semantic Scholar, Google Scholar, the venue (NeurIPS/ICML/ACL/...) for the
  seed papers of the area.
- (b) **Citation-graph expansion** — for the seed papers, follow their *references* (what they build
  on) and their *citations* (what builds on them). This is how you catch the seminal paper a keyword
  search misses. Prefer the highly-cited and the most-recent.
Every `cite_key` must carry an `arxiv_id` or `doi` (or an exact title) so the engine can verify it.
If a subagent can't find a real handle for a paper, it does not get cited — drop it, don't invent one.

### 3 — Extract (per paper — grounded, INDEPENDENT of the drafter, like kpm-build)
For each paper, dispatch extraction. Return, each tied to a **verbatim passage** from the paper:
- **Claims** — its key results/methods/findings: `{id, statement, paper, supporting_passage,
  claim_type, confidence}`. Scope each claim to its passage (no over-reach — same discipline as
  kpm-build; over-reaching claims are noise).
- **Open problems** — what THIS paper says is unsolved / future work / a limitation:
  `{id, statement, flagged_by:[cite_key], status, why_it_matters}`. This is the highest-value output.
- **Debate position** — if the paper takes a side on a contested question, note it.
Ground the claims independently (a separate isolated check: does the passage entail the statement?) —
reuse the kpm-build grounding pattern if available.

### 4 — Synthesize
- Merge open problems that multiple papers flag (`flagged_by` grows — corroboration that it's real).
- Build the **debate map**: cluster opposing positions into `{question, positions:[{stance, papers,
  summary}]}`.
- Mark `corroborated_by` on claims that several independent papers support.

### 5 — Assemble (the engine — verifies + lints)
Write the research JSON (shape below) and run:
```
kp-build build --input research.json --out <out_dir>
```
The engine **verifies every citation** (drops unverifiable ones + logs them), assembles the package,
generates `CONTEXT.md` (the agent payload), and lints. Read the output: any UNVERIFIED papers are a
signal a subagent may have hallucinated — investigate, don't ignore.

Research JSON:
```json
{"topic","scope",
 "papers":[{"cite_key","title","authors","year","venue","arxiv_id","doi","url","key_contributions"}],
 "claims":[{"id","statement","paper","supporting_passage","claim_type","confidence","corroborated_by"}],
 "open_problems":[{"id","statement","flagged_by","status","why_it_matters"}],
 "debates":[{"id","question","positions":[{"stance","papers","summary"}],"resolved"}]}
```

### 6 — Falsify (the acceptance gate — does it actually help?)
Run the falsification harness (`eval/falsify.py`): a KP-loaded agent vs a base agent on a held-out
task ("write the related-work paragraph + name 3 *real* open problems for this area"), judged for
correctness, usefulness, and ZERO hallucinated citations. **If the package doesn't beat the base
agent, it is not useful — say so, and either deepen the survey or report the gap honestly.** Record
the result in the manifest.

### 7 — Deliver
Hand over the package directory. Point the user at `CONTEXT.md` (load into an agent) and `README.md`
(human entry). State the citation-verification rate and the falsification result plainly. Confidence
is corpus-relative; the package is a *foundation*, not the paper.

## What this is not
Not a search-result list, not a one-shot report (it is a persistent, verified, reusable asset), and
not an oracle — it is the frontier as the literature states it, with every citation checked to exist.
