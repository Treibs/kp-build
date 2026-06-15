---
cite_key: xiong2024
title: 'DySpec: Faster Speculative Decoding with Dynamic Token Tree Structure'
authors:
- Yunfan Xiong
- Ruoyu Zhang
- Yanzeng Li
- Tianhao Wu
- Lei Zou
year: 2024
venue: ''
arxiv_id: '2410.11744'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2410.11744
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: 'DySpec: Faster Speculative Decoding with Dynamic Token Tree Structure'
  match_score: 1.0
  checked: '2026-06-15'
key_contributions:
- Argues that organizing predicted tokens as independent chains or fixed token trees
  fails to generalize to diverse query distributions
- Proposes DySpec, a speculative decoding algorithm with a novel dynamic token tree
  structure built via a greedy expansion strategy at run time
- Shows draft distribution and acceptance rate are strongly correlated, with theoretical
  optimality under mild assumptions
- Reports up to 9.1x throughput improvement and 9.4x latency reduction on Llama2-70B
  under low temperature, outperforming SpecInfer and Sequoia
---

## Key contributions

- Argues that organizing predicted tokens as independent chains or fixed token trees fails to generalize to diverse query distributions
- Proposes DySpec, a speculative decoding algorithm with a novel dynamic token tree structure built via a greedy expansion strategy at run time
- Shows draft distribution and acceptance rate are strongly correlated, with theoretical optimality under mild assumptions
- Reports up to 9.1x throughput improvement and 9.4x latency reduction on Llama2-70B under low temperature, outperforming SpecInfer and Sequoia
