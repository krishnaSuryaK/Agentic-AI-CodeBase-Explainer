from langchain_ollama import OllamaLLM

from vectorstore.chroma_store import get_vector_store


def ask_repository(question: str):

    # -----------------------------------------
    # 1. Get Chroma vector store
    # -----------------------------------------

    vector_store = get_vector_store()

    # -----------------------------------------
    # 2. Search for relevant code
    # -----------------------------------------

    results = vector_store.similarity_search(
        question,
        k=3
    )

    # -----------------------------------------
    # 3. Build context from retrieved code
    # -----------------------------------------

    context_parts = []

    for result in results:

        file_path = result.metadata["file_path"]

        start_line = result.metadata["start_line"]

        end_line = result.metadata["end_line"]

        code = result.page_content

        context_parts.append(
            f"""
File: {file_path}
Lines: {start_line}-{end_line}

{code}
"""
        )

    context = "\n".join(context_parts)

    # -----------------------------------------
    # 4. Create prompt
    # -----------------------------------------

    prompt = f"""
You are a code analysis assistant.

Answer the user's question using ONLY the
repository code provided below.

If the answer cannot be found in the provided
code, say that you could not find enough
information in the repository.

Repository code:

{context}

User question:

{question}

Give a clear and concise explanation.
"""

    # -----------------------------------------
    # 5. Call local LLM
    # -----------------------------------------

    llm = OllamaLLM(
        model="qwen2.5-coder:7b"
    )

    answer = llm.invoke(prompt)

    return answer