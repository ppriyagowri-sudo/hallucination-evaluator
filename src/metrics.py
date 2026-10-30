import pandas as pd
import matplotlib.pyplot as plt

d = pd.read_csv("results/results_reviewed.csv")
d["failure_type"] = d["failure_type"].fillna("")
order = ["supported", "missing", "incomplete", "contradictory"]

# Table 1: pass rate per category and prompt
by_cat = d.groupby(["category", "prompt_type"])["manual_pass"].mean().unstack().reindex(order)
by_cat.to_csv("results/pass_rate_by_category.csv")

# Table 2: failure counts by type
fails = (d[d.failure_type != ""]
         .groupby(["failure_type", "prompt_type"]).size().unstack(fill_value=0))
fails.to_csv("results/failure_counts.csv")

# Summary
summary = d.groupby("prompt_type").agg(
    accuracy=("manual_pass", "mean"),
    hallucinations=("failure_type", lambda s: (s == "hallucination").sum()),
    over_abstentions=("failure_type", lambda s: (s == "over_abstention").sum()),
    missed_conflicts=("failure_type", lambda s: (s == "missed_conflict").sum()),
)
summary.to_csv("results/summary.csv")
print(summary, "\n")
print(by_cat.round(2), "\n")
print(fails)

colors = {"naive": "#d9534f", "careful": "#4a90a4"}

# Chart 1: pass rate by category
ax = by_cat[["naive", "careful"]].plot(kind="bar", figsize=(8, 5),
                                       color=[colors["naive"], colors["careful"]])
ax.set_ylabel("Pass rate")
ax.set_xlabel("Evidence category")
ax.set_ylim(0, 1.1)
ax.set_title("Pass rate by evidence category and prompt type")
plt.xticks(rotation=0)
plt.legend(title="Prompt")
plt.tight_layout()
plt.savefig("results/chart_pass_rate_by_category.png", dpi=150)
plt.close()

# Chart 2: failure types by prompt
ax = fails[["naive", "careful"]].plot(kind="bar", figsize=(8, 5),
                                      color=[colors["naive"], colors["careful"]])
ax.set_ylabel("Number of cases (out of 20)")
ax.set_xlabel("Failure type")
ax.set_title("Failure types by prompt type")
plt.xticks(rotation=0)
plt.legend(title="Prompt")
plt.tight_layout()
plt.savefig("results/chart_failure_types.png", dpi=150)
plt.close()

print("\nSaved 3 tables and 2 charts in results/")
