"""Compare two frozen graders on paired public WebArena trajectories."""
import csv
import io
import json
import random
import re
import subprocess
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from statistics import mean

REV = "b6d17e646009d6cb63d5dd7be78807b680693f61"
BASE = f"https://huggingface.co/datasets/McGill-NLP/agent-reward-bench/resolve/{REV}/"
AGENTS = ["GenericAgent-Qwen_Qwen2.5-VL-72B-Instruct",
          "GenericAgent-meta-llama_Llama-3.3-70B-Instruct"]
CACHE = Path(__file__).resolve().parent / ".cache" / REV
GRADERS = ["functional", "language", "expert"]


def fetch(path):
    target = CACHE / path
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        data = subprocess.check_output(["curl", "-fsSL", "--retry", "3", BASE + path])
        target.write_bytes(data)
    return target.read_bytes()


def score(item):
    task, agent, expert = item
    path = f"judgments/webarena/{agent}/gpt-4o-mini-noscreen/{task}.json"
    data = json.loads(fetch(path))
    assert data["agent"] == agent and data["trajectory_info"]["valid"]
    reward = data["trajectory_info"]["summary_info"]["cum_reward"]
    assert reward in (0, 1)
    verdict = re.findall(r"<success>\s*(.*?)\s*</success>", data["response"]["choices"][0]["message"]["content"], re.I)
    if len(verdict) != 1 or verdict[0].lower() not in ("successful", "unsuccessful"):
        raise ValueError(f"Unsupported verdict for {path}: {verdict}")
    return task, agent, dict(functional=int(reward), language=int(verdict[0].lower()=="successful"), expert=expert)


def main():
    labels = defaultdict(set)
    for row in csv.DictReader(io.StringIO(fetch("data/annotations.csv").decode())):
        if row["benchmark"] == "webarena" and row["model_name"] in AGENTS:
            labels[row["task_id"], row["model_name"]].add(row["trajectory_success"])
    shared = sorted({t for t, a in labels if all((t, model) in labels for model in AGENTS)},
                    key=lambda t: int(t.split(".")[-1]))
    tasks = [t for t in shared if all(labels[t, a] in ({"Successful"}, {"Unsuccessful"}) for a in AGENTS)]
    items = [(t, a, int(labels[t, a] == {"Successful"})) for t in tasks for a in AGENTS]
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = {(t,a):scores for t,a,scores in pool.map(score, items)}
    print(f"{len(shared)} shared tasks; {len(tasks)} with unambiguous expert labels for both agents.")
    for judge in GRADERS:
        totals = [sum(rows[t,a][judge] for t in tasks) for a in AGENTS]
        deltas = [rows[t,AGENTS[0]][judge]-rows[t,AGENTS[1]][judge] for t in tasks]
        rng = random.Random(42)
        boot = sorted(sum(rng.choices(deltas,k=len(tasks)))/len(tasks) for _ in range(10000))
        print(judge, totals, "Qwen minus Llama, pp %.1f [%.1f, %.1f]" %
              (100*mean(deltas),100*boot[249],100*boot[9749]))
    for judge in GRADERS[:2]:
        print(judge, "agrees with expert", sum(r[judge]==r["expert"] for r in rows.values()), "/", len(rows))
    disagreements = [(t,a) for t,a in rows if rows[t,a]["language"] != rows[t,a]["functional"]]
    print("Grader disagreements:", len(disagreements))
    if disagreements:
        t,a = disagreements[0]
        print("First disagreement:", t,a,rows[t,a])
    with open(Path(__file__).with_name("decisions.csv"),"w",newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["task","agent"]+GRADERS)
        for (t,a),r in rows.items():
            writer.writerow([t,a]+[r[j] for j in GRADERS])


if __name__ == "__main__":
    main()
