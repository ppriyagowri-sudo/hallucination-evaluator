import ollama

MODEL = "llama3.2:3b"   # change this to test another model later

PROMPTS = {
    # Baseline: no guidance, so we can see natural hallucination
    "naive": (
        "Context: {context}\n\n"
        "Question: {question}\n\n"
        "Answer the question."
    ),
    # Careful: tells the model to stay grounded in the context
    "careful": (
        "Use ONLY the context below to answer. Rules:\n"
        "- If the context does not contain the answer, reply exactly: NOT ENOUGH INFORMATION.\n"
        "- If the context answers only part of the question, answer that part and say what is missing.\n"
        "- If the context contains conflicting information, say CONFLICT and describe both versions.\n\n"
        "Context: {context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    ),
}


def ask(context, question, prompt_type="naive", model=MODEL):
    prompt = PROMPTS[prompt_type].format(context=context, question=question)
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0},   # same input gives same output
    )
    return response["message"]["content"].strip()


if __name__ == "__main__":
    ctx = "The Eiffel Tower was completed in 1889."
    q = "How tall is the Eiffel Tower?"
    print("NAIVE  :", ask(ctx, q, "naive"))
    print("CAREFUL:", ask(ctx, q, "careful"))
    