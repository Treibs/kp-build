---
cite_key: nguyentri2025
title: Attention Is All You Need for KV Cache in Diffusion LLMs
authors:
- Quan Nguyen-Tri
- Mukul Ranjan
- Zhiqiang Shen
year: 2025
venue: ''
arxiv_id: '2510.14973'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2510.14973
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: Attention Is All You Need for KV Cache in Diffusion LLMs
  match_score: 1.0
  checked: '2026-06-14'
key_contributions:
- Identifies that prior diffusion-LLM decoders recompute QKV for all tokens at every
  denoising step and layer, despite KV states changing little across most steps
- Adaptive, layer-aware selective KV refresh (starting from deeper layers) to cut
  redundant computation
- 8.7x speedup on GSM8K (256 tokens) and 45.1x on longer sequences; 6.8x higher throughput
  than confidence-based approaches while preserving quality
---

## Key contributions

- Identifies that prior diffusion-LLM decoders recompute QKV for all tokens at every denoising step and layer, despite KV states changing little across most steps
- Adaptive, layer-aware selective KV refresh (starting from deeper layers) to cut redundant computation
- 8.7x speedup on GSM8K (256 tokens) and 45.1x on longer sequences; 6.8x higher throughput than confidence-based approaches while preserving quality
