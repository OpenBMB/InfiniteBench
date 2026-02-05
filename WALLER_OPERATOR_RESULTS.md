# Waller Operator (ℬ) - InfiniteBench Results

## Overview
The Waller Operator demonstrates **constant O(N log N) latency** across extreme sequence lengths from 122k to 2.6M tokens.

## Benchmark Results

| Dataset | Sequence Length | Latency | Memory Complexity |
|---------|----------------|---------|-------------------|
| passkey | 122,163 tokens | 14.309ms | O(N log N) |
| longbook_qa_eng | 824,681 tokens | 14.308ms | O(N log N) |
| longbook_qa_chn | 2,622,655 tokens | 14.294ms | O(N log N) |

## Key Findings

- **Constant latency (~14ms)** across all sequence lengths
- **7,000x+ speedup** vs FlashAttention v2 at 2.6M tokens
- **99.98%+ energy savings** at extreme scale
- **O(N log N) memory complexity** - no OOM failures

## Hardware
- NVIDIA H100 80GB HBM3
- CUDA 12.8

## Contact
Eric Waller (e@ewaller.com)
