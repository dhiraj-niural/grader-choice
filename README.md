# Two agents gave different price ranges. The grader passed both.

A WebArena shopper asked for one brand’s price range. In its reasoning, Llama had already recorded a $24.99 item, then reported **$6.99–$12.74**. Qwen had recorded a $6.99 item, then reported **$9.99–$38.99**. Both used prices from the second page to answer for the whole brand. GPT-4o mini passed both runs. The functional check and the published expert labels marked both unsuccessful. Each answer contradicts a price in its own trace. The true endpoints are unnecessary to spot either inconsistency. [Llama trace](https://huggingface.co/datasets/McGill-NLP/agent-reward-bench/blob/b6d17e646009d6cb63d5dd7be78807b680693f61/judgments/webarena/GenericAgent-meta-llama_Llama-3.3-70B-Instruct/gpt-4o-mini-noscreen/webarena.229.json) · [Qwen trace](https://huggingface.co/datasets/McGill-NLP/agent-reward-bench/blob/b6d17e646009d6cb63d5dd7be78807b680693f61/judgments/webarena/GenericAgent-Qwen_Qwen2.5-VL-72B-Instruct/gpt-4o-mini-noscreen/webarena.229.json)

## How often did we see this pattern?

We took all 62 automatic-grader disagreements across 48 distinct task IDs. Two model readers independently examined each trace for evidence that the agent answered or treated a narrower or different question as solved. They agreed on 54/62 labels, including 24 positive cases. In **14 runs on 13 distinct tasks**, both readers tagged a scope substitution, GPT-4o mini passed the run, and the published expert marked it unsuccessful. Those 14 came from 36 language-pass, functional-fail, expert-fail disagreements. All 14 are additional to the original Qwen example. Removing both agents’ runs on its task still leaves 13 runs on 12 other task IDs.

Scope is a broader category than inspecting one customer. It includes using the wrong page, population, time window or candidate set. The literal customer-view pattern also recurred on task 344: Llama answered for the shop from a customer-specific review grid. Here the expert accepted the answer too. A questionable method and an unsuccessful outcome are distinct observations. The review sampled disagreements by design. It cannot estimate the frequency of scope errors across all web-agent runs. [Rubric and method](AUDIT.md) · [All 62 paired ratings](audit.json)

## Did the grader change the winner?

Qwen finished ahead of Llama under both automatic graders on 96 matched WebArena tasks. The functional check put Qwen ahead by 9.4 percentage points. GPT-4o mini put it ahead by 15.6 points. The published expert labels put the gap at 10.4 points.

| Successful runs | Qwen2.5-VL-72B | Llama-3.3-70B |
| --- | ---: | ---: |
| WebArena functional check | 26 | 17 |
| GPT-4o mini, accessibility tree without screenshots | 53 | 38 |
| Expert judgment | 32 | 22 |

The automatic graders disagreed on 62 of 192 runs. On those 62, the experts sided with the functional check 38 times and the language grader 24 times. Over all runs, agreement with experts was 157/192 and 143/192 respectively. Paired task bootstrap 95% intervals for the Qwen lead were [1.0, 17.7], [3.1, 28.1], and [2.1, 19.8] percentage points, respectively. These exploratory intervals describe variation across sampled task IDs. Related task templates may make them optimistic.

## Inspect one decision

The first disagreement in numeric task order was Qwen on WebArena 15. The goal asked how many store reviews mentioned a particular word. The final grid showed one customer's reviews. The agent entered the word in the page banner and the grid's review filter remained empty. The run timed out before the agent sent a final count. GPT-4o mini still passed it. The functional check and expert marked it unsuccessful. A separate model reviewer given only goal and trajectory evidence, with agent identity and verdicts withheld, also judged it unsuccessful. In the full follow-up, one reader tagged the substitution in the agent’s reasoning. The second judged the agent was still trying to run the intended search. We excluded it from the consensus count. Blinding of the original expert annotators is unverified.

## Reproduce and explore

Run `python3 study.py` with Python 3.9+ and curl. The script downloads published annotations and archived judgments at a fixed dataset revision, caches them locally, and regenerates decisions.csv. No model API or keys are needed. To switch graders and inspect any trace, run `python3 -m http.server 8080 --bind 127.0.0.1` in this directory and open http://localhost:8080. Each evidence link contains the goal, agent actions and recorded grader response.

We included the two open-weight agent configurations available for WebArena. Of 98 jointly annotated task IDs, 96 had a definitive, internally consistent expert success label for both agents. Repeated agreeing annotations count once. Both automatic verdicts come from the same saved trajectory record. Each task contributes equal weight. The bootstrap resamples the paired outcomes 10,000 times at seed 42. The reference measures expert-rated completion and can itself be fallible. This reanalysis does not establish a universal grader ranking, a causal effect, or a new benchmark.

Source: [AgentRewardBench, Lu et al.](https://arxiv.org/abs/2504.08942) and its [versioned data and terms](https://huggingface.co/datasets/McGill-NLP/agent-reward-bench/tree/b6d17e646009d6cb63d5dd7be78807b680693f61). The researchers produced the underlying trajectories, judgments and annotations. This reanalysis adds the paired comparison, trace explorer and scope-error annotations. Run `python3 audit.py` for the audit counts.
