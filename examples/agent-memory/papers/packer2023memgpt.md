---
cite_key: packer2023memgpt
title: 'MemGPT: Towards LLMs as Operating Systems'
authors:
- Charles Packer
- Sarah Wooders
- Kevin Lin
- Vivian Fang
- Shishir G. Patil
- Ion Stoica
- Joseph E. Gonzalez
year: 2023
venue: arXiv preprint (became Letta)
arxiv_id: '2310.08560'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2310.08560
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: 'MemGPT: Towards LLMs as Operating Systems'
  match_score: 1.0
  checked: '2026-06-15'
key_contributions:
- 'Virtual context management: an OS-inspired hierarchical memory (main context vs.
  external storage) that gives a finite-context LLM the appearance of unbounded memory
  via data movement between fast and slow tiers'
- LLM-issued function calls and interrupts to page information in and out and manage
  control flow, enabling long document analysis and multi-session chat
- Foundational 'memory as paging' framing; basis for the Letta system
---

## Key contributions

- Virtual context management: an OS-inspired hierarchical memory (main context vs. external storage) that gives a finite-context LLM the appearance of unbounded memory via data movement between fast and slow tiers
- LLM-issued function calls and interrupts to page information in and out and manage control flow, enabling long document analysis and multi-session chat
- Foundational 'memory as paging' framing; basis for the Letta system
