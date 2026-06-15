---
cite_key: arriola2025
title: 'Block Diffusion: Interpolating Between Autoregressive and Diffusion Language
  Models'
authors:
- Marianne Arriola
- Aaron Gokaslan
- Justin T. Chiu
- Zhihan Yang
- Zhixuan Qi
- Jiaqi Han
- Subham Sekhar Sahoo
- Volodymyr Kuleshov
year: 2025
venue: ''
arxiv_id: '2503.09573'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2503.09573
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: 'Block Diffusion: Interpolating Between Autoregressive and Diffusion
    Language Models'
  match_score: 1.0
  checked: '2026-06-14'
key_contributions:
- Identifies that diffusion LMs lag in likelihood modeling and are limited to fixed-length
  generation, and that standard diffusion LMs lack KV caching
- Introduces block diffusion interpolating between autoregressive and discrete diffusion
  to recover KV caching, flexible-length generation, and parallel sampling
- Provides estimators of gradient variance and data-driven noise schedules to address
  high training-objective gradient variance
---

## Key contributions

- Identifies that diffusion LMs lag in likelihood modeling and are limited to fixed-length generation, and that standard diffusion LMs lack KV caching
- Introduces block diffusion interpolating between autoregressive and discrete diffusion to recover KV caching, flexible-length generation, and parallel sampling
- Provides estimators of gradient variance and data-driven noise schedules to address high training-objective gradient variance
