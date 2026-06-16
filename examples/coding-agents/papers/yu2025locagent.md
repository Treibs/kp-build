---
cite_key: yu2025locagent
title: 'LocAgent: Graph-Guided LLM Agents for Code Localization'
authors:
- Zhaoling Chen
- Xiangru Tang
- Gangda Deng
- Fang Wu
- Jialong Wu
- Zhiwei Jiang
- Viktor Prasanna
- Arman Cohan
- Xingyao Wang
year: 2025
venue: ACL 2025
arxiv_id: '2503.09089'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2503.09089
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: 'LocAgent: Graph-Guided LLM Agents for Code Localization'
  match_score: 1.0
  checked: '2026-06-15'
key_contributions:
- Parses repos into directed heterogeneous graphs (files/classes/functions + import/invocation/inheritance
  edges) for multi-hop localization reasoning
- Fine-tuned Qwen-2.5-Coder-32B reaches 92.7% file-level localization accuracy at
  ~86% lower cost than proprietary SOTA
- Lifts downstream issue-resolution success (Pass@10) by 12%
---

## Key contributions

- Parses repos into directed heterogeneous graphs (files/classes/functions + import/invocation/inheritance edges) for multi-hop localization reasoning
- Fine-tuned Qwen-2.5-Coder-32B reaches 92.7% file-level localization accuracy at ~86% lower cost than proprietary SOTA
- Lifts downstream issue-resolution success (Pass@10) by 12%
