from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="qwen2.5-coder:7b"
)


def documentation_agent(question: str, context: str):

    prompt = f"""
You are a Documentation Agent.

Explain the provided repository code in a way
that a developer can easily understand.

Focus on:

- what the code does
- important classes
- important methods
- configuration
- dependencies
- usage

Repository code:

{context}

Question:

{question}

Give a clear and structured explanation.
"""

    return llm.invoke(prompt)