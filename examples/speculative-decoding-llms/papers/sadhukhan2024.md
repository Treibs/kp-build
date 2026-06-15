---
cite_key: sadhukhan2024
title: 'MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation
  with Speculative Decoding'
authors:
- Ranajoy Sadhukhan
- Jian Chen
- Zhuoming Chen
- Vashisth Tiwari
- Ruihang Lai
- Jinyuan Shi
- Ian En-Hsu Yen
- Avner May
- Tianqi Chen
- Beidi Chen
year: 2024
venue: ''
arxiv_id: '2408.11049'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2408.11049
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: 'MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context
    Generation with Speculative Decoding'
  match_score: 1.0
  checked: '2026-06-15'
key_contributions:
- Challenges the conventional wisdom that speculative decoding only helps at small
  batch sizes, showing speedups in high-throughput regimes for moderate-to-long sequences
- Analyzes how the bottleneck shifts with batch size and sequence length, and uses
  a draft model with sparse KV cache to address the KV bottleneck that scales with
  both sequence length and batch size
- Demonstrates up to 2.51x speedup for Llama3.1-8B at batch sizes from 32 to 256
---

## Key contributions

- Challenges the conventional wisdom that speculative decoding only helps at small batch sizes, showing speedups in high-throughput regimes for moderate-to-long sequences
- Analyzes how the bottleneck shifts with batch size and sequence length, and uses a draft model with sparse KV cache to address the KV bottleneck that scales with both sequence length and batch size
- Demonstrates up to 2.51x speedup for Llama3.1-8B at batch sizes from 32 to 256
