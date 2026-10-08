from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="qwen2.5-coder:7b"
)


def repository_agent(question: str, context: str):

    prompt = f"""
You are a Repository Analysis Agent.

Analyze the provided repository code and answer
the user's question.

Focus on:
- classes
- methods
- architecture
- dependencies
- how components work together

Repository code:

{context}

Question:

{question}

Give a clear technical answer.
Mention relevant files when possible.
"""

    return llm.invoke(prompt)