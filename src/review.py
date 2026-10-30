import pandas as pd

d = pd.read_csv("results/results.csv")
d["manual_pass"] = d["auto_pass"]
d["failure_type"] = ""

# Auto grader was too strict: these are correct
for i in [7, 8, 10, 17]:
    d.loc[(d.id == i) & (d.prompt_type == "naive"), "manual_pass"] = True

# Auto grader was too lenient: careful prompt refused when it could answer part
for i in [12, 15]:
    m = (d.id == i) & (d.prompt_type == "careful")
    d.loc[m, "manual_pass"] = False
    d.loc[m, "failure_type"] = "over_abstention"

# Confirmed failures
fails = {
    "naive":   {6: "hallucination", 9: "hallucination", 11: "hallucination",
                12: "hallucination", 13: "hallucination", 14: "hallucination",
                19: "missed_conflict"},
    "careful": {6: "hallucination", 13: "hallucination"},
}
for ptype, cases in fails.items():
    for i, ftype in cases.items():
        d.loc[(d.id == i) & (d.prompt_type == ptype), "failure_type"] = ftype

cats = pd.read_csv("data/test_cases.csv")[["id", "category"]]
d = d.drop(columns=["category"]).merge(cats, on="id")
d.to_csv("results/results_reviewed.csv", index=False)

print(d.groupby("prompt_type")["manual_pass"].agg(["sum", "count"]))
print(d.groupby(["prompt_type", "category"])["manual_pass"].mean().unstack())
