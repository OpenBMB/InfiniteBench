<div align="center">

# InfiniteBench: 128k Long-Context Benchmark for Language Models

<p align="center">
  <a href="./README_ZH.md">中文</a> •
  <a href="./README.md">English</a> •
  <a href="">Paper (upcoming)</a>
</p>

</div>

## 简介

理解、处理长文本，是大模型迈向更深层次理解与交互阶段必备的能力。现已有大模型声称可以处理100k+的长序列，但是对应的标准评测集却是空缺的。为此，我们构建了一个面向 100k+ 的评测集，InfiniteBench。该评测集针对大模型在长文本方面的五项能力而设计：检索、数学、代码、问答、和摘要。

## 特点

- **长上下文:** InfiniteBench 测试数据的平均上下文长度为195k，远超现有评测数据。
- **多领域多语言:** InfiniteBench 评测集包含12个任务，包括中英双语，涵盖了检索、数学、代码、问答、和摘要等5个领域。
- **前瞻性挑战性:** InfiniteBench 测试任务，对标当前最强的模型如 GPT-4, Claude 2 等。
- **真实场景与合成场景:** InfiniteBench 既包含真实场景数据，探测大模型在处理实际问题的能力；也包含合成数据，为测试数据拓展上下文窗口提供了便捷。

## 任务构成

| 任务             | 内容          | 样本数量 | 平均上下文 token 数量 | 平均输出 token 数量 | 任务描述                                                               |
| ---------------- | ------------- | -------- | --------------------- | ------------------- | ---------------------------------------------------------------------- |
| 摘要(英)         | Fake Book     | 148      | 131.7k                | 1.1k                | Summarization of a fake book created through key entity substitution.  |
| En.QA            | Fake Book     | 466      | 155.3k                | 4.9                 | Question Answering based on the fake book.                             |
| En.MC            | Fake Book     | 322      | 142.4k                | 5.3                 | Multiple choice questions derived from the fake book.                  |
| En.Dia           | Script        | 200      | 103.6k                | 3.4                 | Identification of talkers in partially anonymized scripts.             |
| Zh.QA            | New Book      | 189      | 1918.1k               | 6.2                 | Question answering on a set of newly collected books.                  |
| Code.Debug       | Code Document | 394      | 114.7k                | 4.8                 | Multiple choice, choose the function that contains errors within code. |
| Code.Run         | Synthetic     | 400      | 75.2k                 | 1.3                 | Simulated Execution of functions from a simple collection.             |
| Math.Calc        | Synthetic     | 50       | 43.9k                 | 43.9k               | Calculations involving super-long equations.                           |
| Math.Find        | Synthetic     | 350      | 87.9k                 | 1.3                 | Finding special values in a lengthy list.                              |
| Retrieve.PassKey[^1] | Synthetic     | 590      | 122.4k                | 2.0                 | Retrieving hidden keys amidst noisy context.                           |
| Retrieve.Number  | Synthetic     | 590      | 122.4k                | 4.0                 | Locating repeated hidden numbers in extensive context.                 |
| Retrieve.KV[^2]      | Synthetic     | 500      | 89.9k                 | 22.7                | Matching values from a key-value list given a key.                     |

## 评测结果

我们在 SOTA 模型上评测了 InfiniteBench 结果如下：

| Task Name        | GPT-4       | Yarn-Mistral-7B | Kimi-Chat | Claude 2    | RWKV-4-World-7B |
| ---------------- | ----------- | --------------- | --------- | ----------- | --------------- |
| Retrieve.PassKey | 100%        | 92.71%          | 98.14%    | coming      | < 5%            |
| Retrieve.Number  | 100%        | 56.61%          | 95.42%    | 67.12%      | -               |
| Retrieve.KV      | 89.00%      | < 5%            | 40.40%    | 67.00%      | -               |
| En.Sum           | 8.76%  | 7.73%            | 18.02%    | 15.13%   | -               |
| En.QA            | 21.45% | 10.49%          | 14.98%    | coming   | -               |
| En.MC            | 69.88% | 30.43%          | 71.74%    | coming   | -               |
| En.Dia           | 8.50%       | 7.50%           | 11.50%    | 46.50%     | -               |
| Zh.QA            | 24.80%      | 14.25%          | 17.63%    | coming      | -               |
| Code.Debug       | 39.59%      | < 5%            | 18.02%    | < 5%        | -               |
| Code.Run         | 23.25%      | < 5%            | < 5%      | < 5%        | -               |
| Math.Calc        | < 5%        | < 5%            | < 5%      | < 5%        | -               |
| Math.Find        | 60.00%      | 17.14%          | 12.57%    | 32.29%      | -               |

注： 

1. YaRN-Mistral-7B 和 RWKV-4-World-7B 实现代码已开源在仓库，请大家批评指正；Kimi-Chat 和 Claude 2 使用用户界面评测，GPT-4 使用 API 评测，均使用官方默认配置。
2. 

> 由于 RWKV-World-4-7B 没有在 Retrieve.PassKey 上的任何正确的例子，因此我们没有考虑在其他更具有挑战性的任务上测试它。但是我们强调 RWKV-World-4-7b 似乎从来没有在 128k 长度的上下文上训练，并且没有被宣传能够处理这样长度的上下文，所以这个结果不能证明 RWKV 架构不能扩展到 128k 长度的上下文。

## 评测

## 获取数据集

从 <https://huggingface.co/datasets/xinrongzhang2022/InfiniteBench> 下载数据集到 `infinitebench/data` 路径下（我们将评测数据集放在 InfiniteBench 目录下），得到文件如下：

```
InfiniteBench
├── data
│   ├── code_debug.jsonl
│   ├── code_run.jsonl
│   ├── kv_retrieval.jsonl
│   ├── longbook_choice_eng.jsonl
│   ├── longbook_qa_chn.jsonl
│   ├── longbook_qa_eng.jsonl
│   ├── longbook_sum_eng.jsonl
│   ├── longdialogue_qa_eng.jsonl
│   ├── math_calc.jsonl
│   ├── math_find.jsonl
│   ├── number_string.jsonl
│   ├── passkey.jsonl
│   └── construct_synthetic_dataset.py
...
```

或者使用 Datasets 下载：

```python
from datasets import load_dataset
dataset = load_dataset("xinrongzhang2022/InfiniteBench")
```

### 安装依赖

```shell
pip install -r requiremnets.txt
```

### 推理

比如，评测 GPT-4 在 Retrieve.PassKey 任务上的表现：

```shell
cd src
python eval_gpt4.py --task passkey
```

可以选择的 `--task` 有：

- `passkey`
- `number_string`
- `kv_retrieval`
- `longbook_sum_eng`
- `longbook_qa_eng`
- `longbook_qa_chn`
- `longbook_choice_eng`
- `longdialogue_qa_eng`
- `math_calc`
- `math_find`
- `code_debug`
- `code_run`

#### 计算分数

```shell
python compute_scores.py
```

## 引用

> This will be updated when our preprint paper is released.

```bibtex
@misc{zhang2023infinitebench,
  title  = {InfiniteBench: 128k Long-Context Benchmark for Language Models},
  author = {Zhang, Xinrong and Chen, Yingfa and Hu, Shengding and Wu, Qihao and Chen, Junhao and Xu, Zihang and Dai, Zhenning and Han, Xu and Wang, Shuo and Liu, Zhiyuan and Sun, Maosong},
  year   = {2023}
}
```

## 参考文献
[^1]: Mohtashami, Amirkeivan and Martin Jaggi. “Landmark Attention: Random-Access Infinite Context Length for Transformers.” ArXiv abs/2305.16300 (2023): n. pag.
[^2]: Liu, Nelson F. et al. “Lost in the Middle: How Language Models Use Long Contexts.” ArXiv abs/2307.03172 (2023): n. pag.
