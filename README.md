# When a web agent answers for the wrong page

On WebArena task 229, a shopper asks for the price range of Ugreen products. Llama notes a $24.99 item on the first page of results. It moves to the second page and reports $6.99 to $12.74 for the whole brand. Its own trace is enough to rule out that upper bound.

Qwen makes the same mistake at the other end. It notes a $6.99 item, turns the page, and gives $9.99 as the minimum. GPT-4o mini grades both runs as successful. The WebArena functional check and the published expert judgments mark both as failures. [Llama trace](https://huggingface.co/datasets/McGill-NLP/agent-reward-bench/blob/b6d17e646009d6cb63d5dd7be78807b680693f61/judgments/webarena/GenericAgent-meta-llama_Llama-3.3-70B-Instruct/gpt-4o-mini-noscreen/webarena.229.json) · [Qwen trace](https://huggingface.co/datasets/McGill-NLP/agent-reward-bench/blob/b6d17e646009d6cb63d5dd7be78807b680693f61/judgments/webarena/GenericAgent-Qwen_Qwen2.5-VL-72B-Instruct/gpt-4o-mini-noscreen/webarena.229.json)

## Counting the disagreements

The two agents attempted the same 96 tasks. We reviewed all 62 runs where the functional check and GPT-4o mini disagreed. For each run, two model readers saw the goal and trajectory with the scores withheld. Their question was narrow. Did the agent treat evidence about one page, population, or time window as sufficient to answer a question about another?

Of the 36 disagreements where GPT-4o mini passed the run and both the functional check and the expert marked it unsuccessful, **14 showed this error according to both readers**. Those 14 runs span 13 tasks. We only audited disagreements, so this count tells us little about runs that both graders passed. Across all 62, the readers agreed on 54 classifications. Their reasons, including the eight splits, are available for inspection. [Rubric](AUDIT.md) · [Paired annotations](audit.json)

One borderline case is worth keeping. On task 15, Qwen looked at one customer's reviews while trying to count mentions of a word across the store. It timed out before sending a count. One reader saw a scope error in its reasoning. The other saw an unfinished search. That run is excluded from the 14.

## What changed on the leaderboard?

| Successful runs | Qwen2.5-VL-72B | Llama-3.3-70B |
| --- | ---: | ---: |
| WebArena functional check | 26 | 17 |
| GPT-4o mini, accessibility tree without screenshots | 53 | 38 |
| Expert judgment | 32 | 22 |

All three measures rank Qwen first. Switching from the functional check to the language grader increases its lead from 9.4 to 15.6 percentage points. The expert gap is 10.4 points. The expert labels agree with the functional check on 157 of 192 runs and with the language grader on 143.

## Reproduce the result

Python 3.9+ and curl are sufficient. The recorded grader responses come with the dataset.

```sh
python3 study.py
python3 audit.py
python3 -m http.server 8080 --bind 127.0.0.1
```

Open <http://localhost:8080> to switch graders and inspect the underlying traces. The checked-in scores and annotations are sufficient to use the explorer offline. Trace links open the original records.

Of 98 shared task IDs, 96 had a consistent, definitive expert label for both agents. Each task receives equal weight. The study script also reports paired bootstrap intervals over task IDs. Related task templates can make these intervals too narrow.

Lu et al. released the trajectories, grader outputs and expert annotations in AgentRewardBench. This repository adds the paired comparison, the scope audit and the explorer. [Paper](https://arxiv.org/abs/2504.08942) · [Dataset revision](https://huggingface.co/datasets/McGill-NLP/agent-reward-bench/tree/b6d17e646009d6cb63d5dd7be78807b680693f61) · [Data terms](DATA-TERMS.md)
