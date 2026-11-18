"""Write a verdict-free review packet per grader disagreement, in seeded order."""
import argparse
import csv
import json
import random
from pathlib import Path

from study import fetch


def main(destination):
    destination.mkdir(parents=True, exist_ok=False)
    with Path(__file__).with_name("decisions.csv").open() as source:
        rows = [r for r in csv.DictReader(source) if r["language"] != r["functional"]]
    random.Random(117).shuffle(rows)
    for number, row in enumerate(rows, 1):
        path = f"judgments/webarena/{row['agent']}/gpt-4o-mini-noscreen/{row['task']}.json"
        trace = json.loads(fetch(path))
        blocks = trace["chat_messages"][1]["content"]
        evidence = "\n".join(b["text"] for b in blocks if b["type"] == "text")
        (destination / f"C{number:02d}.txt").write_text(evidence, encoding="utf-8")
    print(f"Wrote {len(rows)} packets. Give readers only the packet folder and the rubric.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="A new directory for local review")
    main(parser.parse_args().destination)
