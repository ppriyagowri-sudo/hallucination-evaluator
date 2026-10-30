# AI Hallucination and Reliability Evaluator

Tests whether a question-answering system makes unsupported claims when the evidence it is given is missing, incomplete or contradictory.

## Goal
Measure how often a small open-source language model hallucinates instead of saying "not enough information", and whether a grounding instruction in the prompt reduces it.

## Test dataset
`data/test_cases.csv` has 20 cases, 5 in each category:
- supported: the answer is in the evidence
- missing: the answer is not in the evidence
- incomplete: the evidence answers only part of the question
- contradictory: the evidence contains conflicting facts

## Method
1. Each case is sent to a local model (Llama 3.2 3B via Ollama) with two prompts: naive and careful.
2. An automatic grader gives a first pass, then every answer is reviewed by hand.
3. Metrics: accuracy, hallucinations, over-abstentions and missed conflicts, per prompt and per category.

## Results
Llama 3.2 3B, 20 test cases, 2 prompt types, graded by hand after an automatic first pass.

| Prompt | Accuracy | Hallucinations | Over-abstentions | Missed conflicts |
|---|---|---|---|---|
| Naive | 13/20 (65%) | 6 | 0 | 1 |
| Careful | 16/20 (80%) | 2 | 2 | 0 |

Key findings:
- A grounding instruction cut hallucinations from 6 to 2.
- The model often filled gaps from memory, even with correct facts that were not in the evidence.
- Incomplete evidence was the hardest category (20% naive, 40% careful).
- The grounding prompt caused 2 over-abstentions, so it trades one failure for another.

![Pass rate by category](results/chart_pass_rate_by_category.png)

Full write-up: [report/report.md](report/report.md)

## Project structure
- `data/` test dataset
- `src/qa_system.py` model calls and prompts
- `src/evaluate.py` runs all test cases and does the first-pass grading
- `src/review.py` applies the manual grade corrections
- `src/metrics.py` computes metrics and charts
- `results/` outputs and charts
- `report/` research report

## How to run
1. Install Ollama from ollama.com and run `ollama pull llama3.2:3b`
2. Set up Python:

        python -m venv venv
        venv\Scripts\activate
        pip install -r requirements.txt

3. Run the pipeline:

        python src/evaluate.py
        python src/review.py
        python src/metrics.py

## Tools
Python, pandas, matplotlib, Ollama
