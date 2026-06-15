---
cite_key: tyagi2026
title: 'Not Every Rubric Teaches Equally: Policy-Aware Rubric Rewards for RLVR'
authors:
- Utkarsh Tyagi
- Xingang Guo
- MohammadHossein Rezaei
- Daniel George
- Anas Mahmoud
- Jackson Lee
- Bing Liu
- Yunzhong He
year: 2026
venue: ''
arxiv_id: '2605.20164'
arxiv_version: ''
doi: ''
url: https://arxiv.org/abs/2605.20164
verified:
  exists: true
  status: verified
  via: arxiv
  canonical_title: 'Not Every Rubric Teaches Equally: Policy-Aware Rubric Rewards
    for RLVR'
  match_score: 1.0
  checked: '2026-06-15'
key_contributions:
- Shows static rubric aggregation conflates a criterion's human-assigned importance
  with its current usefulness as a training signal
- Documents that many important rubric criteria are already saturated or currently
  unreachable while discriminative criteria need not carry the largest human weights
- Introduces POW3R, which preserves human weights/category balance while adapting
  criterion-level reward weights via rollout-level contrast; wins 24 of 30 base-policy/metric
  comparisons and reaches the same plateau in 2.5-4x fewer training steps
---

## Key contributions

- Shows static rubric aggregation conflates a criterion's human-assigned importance with its current usefulness as a training signal
- Documents that many important rubric criteria are already saturated or currently unreachable while discriminative criteria need not carry the largest human weights
- Introduces POW3R, which preserves human weights/category balance while adapting criterion-level reward weights via rollout-level contrast; wins 24 of 30 base-policy/metric comparisons and reaches the same plateau in 2.5-4x fewer training steps
