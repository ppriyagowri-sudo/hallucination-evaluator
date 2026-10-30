import re
import pandas as pd
from qa_system import ask

ABSTAIN = ["not enough information", "does not contain", "doesn't contain", "not mentioned",
           "not provided", "no information", "cannot be determined", "can't be determined",
           "not specified", "does not specify", "not stated", "i don't know", "unable to",
           "does not say", "doesn't say", "no mention"]
GAP = ABSTAIN + ["missing", "not given", "not available", "does not state"]
CONFLICT = ["conflict", "contradict", "discrepan", "inconsistent", "disagree", "differ"]


def numbers(text):
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def has_any(text, words):
    t = text.lower()
    return any(w in t for w in words)


def grade(row, answer):
    new_nums = numbers(answer) - numbers(row["context"]) - numbers(row["question"])
    cat = row["category"]
    if cat == "supported":
        ok = str(row["gold_answer"]).lower() in answer.lower() and not new_nums
    elif cat == "missing":
        ok = has_any(answer, ABSTAIN) and not new_nums
    elif cat == "incomplete":
        ok = has_any(answer, GAP) and not new_nums
    else:  # contradictory
        ok = has_any(answer, CONFLICT)
    return ok, ", ".join(sorted(new_nums))


df = pd.read_csv("data/test_cases.csv")
rows = []
for _, row in df.iterrows():
    for ptype in ["naive", "careful"]:
        answer = ask(row["context"], row["question"], ptype)
        ok, new_nums = grade(row, answer)
        rows.append({
            "id": row["id"], "category": row["category"], "prompt_type": ptype,
            "answer": answer, "new_numbers": new_nums, "auto_pass": ok,
        })
        print(f"case {row['id']:>2} {ptype:<8} pass={ok}")

pd.DataFrame(rows).to_csv("results/results.csv", index=False)
print("Saved results/results.csv")
