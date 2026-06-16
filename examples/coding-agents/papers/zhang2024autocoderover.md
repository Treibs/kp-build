---
cite_key: zhang2024autocoderover
title: 'AutoCodeRover: Autonomous Program Improvement'
authors:
- Yuntong Zhang
- Haifeng Ruan
- Zhiyu Fan
- Abhik Roychoudhury
year: 2024
venue: ISSTA 2024
arxiv_id: '2404.05427'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2404.05427
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: 'AutoCodeRover: Autonomous Program Improvement'
  match_score: 1.0
  checked: '2026-06-15'
key_contributions:
- Program-structure-aware code search over classes/methods (AST) rather than plain
  string matching for repo-level context retrieval
- Adds spectrum-based fault localization from tests to sharpen repair context when
  a test suite is available
- Solves 19% of SWE-bench-lite at low cost (~$0.43/issue), arguing structured retrieval
  beats brute-force agent exploration
---

## Key contributions

- Program-structure-aware code search over classes/methods (AST) rather than plain string matching for repo-level context retrieval
- Adds spectrum-based fault localization from tests to sharpen repair context when a test suite is available
- Solves 19% of SWE-bench-lite at low cost (~$0.43/issue), arguing structured retrieval beats brute-force agent exploration
