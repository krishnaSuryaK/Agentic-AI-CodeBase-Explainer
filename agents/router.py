from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="qwen2.5-coder:7b"
)


def route_question(question: str):

    prompt = f"""
Classify the following user question into exactly
ONE category.

Categories:

repository
bug
documentation

Use:

repository = architecture, classes, methods,
             dependencies, how components work

bug = bugs, errors, exceptions, vulnerabilities,
      problems, incorrect behavior

documentation = explanation, documentation,
                how to use, summary

Question:

{question}

Return ONLY one word:

repository
bug
documentation
"""

    result = llm.invoke(prompt)

    category = result.strip().lower()

    if category not in {
        "repository",
        "bug",
        "documentation"
    }:
        category = "repository"

    return category