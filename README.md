# Does the grader change the winner?

Qwen finished ahead of Llama under both automatic graders on 96 matched WebArena tasks. The functional check put Qwen ahead by 9.4 percentage points. GPT-4o mini put it ahead by 15.6 points. The published expert labels put the gap at 10.4 points.

| Successful runs | Qwen2.5-VL-72B | Llama-3.3-70B |
| --- | ---: | ---: |
| WebArena functional check | 26 | 17 |
| GPT-4o mini, accessibility tree without screenshots | 53 | 38 |
| Expert judgment | 32 | 22 |

The automatic graders disagreed on 62 of 192 runs. On those 62, the experts sided with the functional check 38 times and the language grader 24 times. Over all runs, agreement with experts was 157/192 and 143/192 respectively. Paired task bootstrap 95% intervals for the Qwen lead were [1.0, 17.7], [3.1, 28.1], and [2.1, 19.8] percentage points, respectively. These exploratory intervals describe variation across sampled task IDs. Related task templates may make them optimistic.

## Inspect one decision

The first disagreement in numeric task order was Qwen on WebArena 15. The goal asked how many store reviews mentioned a particular word. The final grid showed one customer's reviews. The agent entered the word in the page banner and the grid's review filter remained empty. GPT-4o mini accepted the answer. The functional check and expert marked it unsuccessful. A separate model reviewer given only goal and trajectory evidence, with agent identity and verdicts withheld, also judged it unsuccessful. This is one illustrative audit of a selected disagreement. Blinding of the original expert annotators is unverified.

## Reproduce and explore

Run `python3 study.py` with Python 3.9+ and curl. The script downloads published annotations and archived judgments at a fixed dataset revision, caches them locally, and regenerates decisions.csv. No model API or keys are needed. To switch graders and inspect any trace, run `python3 -m http.server 8080 --bind 127.0.0.1` in this directory and open http://localhost:8080. Each evidence link contains the goal, agent actions and recorded grader response.

We included the two open-weight agent configurations available for WebArena. Of 98 jointly annotated task IDs, 96 had a definitive, internally consistent expert success label for both agents. Repeated agreeing annotations count once. Both automatic verdicts come from the same saved trajectory record. Each task contributes equal weight. The bootstrap resamples the paired outcomes 10,000 times at seed 42. The reference measures expert-rated completion and can itself be fallible. This reanalysis does not establish a universal grader ranking, a causal effect, or a new benchmark.

Source: [AgentRewardBench, Lu et al.](https://arxiv.org/abs/2504.08942) and its [versioned data and terms](https://huggingface.co/datasets/McGill-NLP/agent-reward-bench/tree/b6d17e646009d6cb63d5dd7be78807b680693f61). The researchers produced the underlying trajectories, judgments and annotations. The comparison, interface and single-case adjudication are new to this reanalysis.
