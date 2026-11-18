"""Verify the audit covers every grader disagreement and reproduce its counts."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def summarize():
    scores = {(r["task"], r["agent"]): r for r in
              csv.DictReader((ROOT / "decisions.csv").read_text().splitlines())}
    expected = {key for key, row in scores.items() if row["functional"] != row["language"]}
    audit = json.loads((ROOT / "audit.json").read_text())
    assert len(audit) == len(expected)
    assert {(r["task"], r["agent"]) for r in audit} == expected
    labels = Counter()
    accepted = []
    for row in audit:
        ratings = row["primary"], row["reviewer"]
        assert set(ratings) <= {"yes", "no", "unclear"}
        assert row["primary_evidence"].strip() and row["reviewer_evidence"].strip()
        labels[ratings] += 1
        score = scores[row["task"], row["agent"]]
        if ratings == ("yes", "yes") and score["language"] == "1" and score["expert"] == "0":
            accepted.append(row)
    print("Review matrix (primary, second reader):", sorted(labels.items()))
    print("Same rating:", sum(n for (a,b),n in labels.items() if a == b), "/", len(audit))
    print("Both readers found scope substitution:", labels["yes", "yes"])
    print("Both found substitution, language passed, expert failed:", len(accepted))
    print("Distinct task IDs in that subset:", len({r["task"] for r in accepted}))
    print("Task IDs:", sorted({int(r["task"].split(".")[-1]) for r in accepted}))
    return accepted


if __name__ == "__main__":
    summarize()
