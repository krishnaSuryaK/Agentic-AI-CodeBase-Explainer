from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="qwen2.5-coder:7b"
)


def bug_agent(question: str, context: str):

    prompt = f"""
You are a Bug Analysis Agent.

Analyze the provided repository code for potential:

- bugs
- exceptions
- incorrect logic
- null/None problems
- security issues
- bad error handling

Repository code:

{context}

User question:

{question}

If you find a problem:
1. Explain the problem.
2. Explain why it can happen.
3. Suggest a fix.
4. Mention the file if possible.

Do not invent problems that are not supported
by the provided code.
"""

    return llm.invoke(prompt)