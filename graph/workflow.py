from langgraph.graph import StateGraph, START, END
from langchain_ollama import OllamaLLM

from vectorstore.chroma_store import get_vector_store

from .state import AgentState


# -----------------------------------------
# Retrieve relevant repository code
# -----------------------------------------

def retrieve_code(state: AgentState):

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        state["question"],
        k=4
    )

    context_parts = []

    for result in results:

        metadata = result.metadata

        context_parts.append(
            f"""
File: {metadata["file_path"]}
Lines: {metadata["start_line"]}-{metadata["end_line"]}

{result.page_content}
"""
        )

    context = "\n".join(context_parts)

    return {
        "context": context
    }


# -----------------------------------------
# Generate answer using Qwen
# -----------------------------------------

def generate_answer(state: AgentState):

    llm = OllamaLLM(
        model="qwen2.5-coder:7b"
    )

    prompt = f"""
You are an AI software repository assistant.

Answer the question using the repository
code provided below.

Do not invent code or functionality.

If the repository code does not contain enough
information, clearly say so.

Repository code:

{state["context"]}

Question:

{state["question"]}

Give a clear answer and mention the relevant
file when possible.
"""

    answer = llm.invoke(prompt)

    return {
        "answer": answer
    }


# -----------------------------------------
# Build LangGraph
# -----------------------------------------

graph = StateGraph(AgentState)


graph.add_node(
    "retrieve_code",
    retrieve_code
)

graph.add_node(
    "generate_answer",
    generate_answer
)


graph.add_edge(
    START,
    "retrieve_code"
)

graph.add_edge(
    "retrieve_code",
    "generate_answer"
)

graph.add_edge(
    "generate_answer",
    END
)


app = graph.compile()