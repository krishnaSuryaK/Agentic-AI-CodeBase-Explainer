from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from vectorstore.chroma_store import get_vector_store

from .router import route_question
from .repository_agent import repository_agent
from .bug_agent import bug_agent
from .documentation_agent import documentation_agent


# -----------------------------------------
# State
# -----------------------------------------

class AgentState(TypedDict):

    question: str
    category: str
    context: str
    answer: str


# -----------------------------------------
# Retrieve repository code
# -----------------------------------------

def retrieve_code(state: AgentState):

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        state["question"],
        k=5
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

    return {
        "context": "\n".join(context_parts)
    }


# -----------------------------------------
# Router
# -----------------------------------------

def router_node(state: AgentState):

    category = route_question(
        state["question"]
    )

    print(
        f"\nSelected Agent: {category}"
    )

    return {
        "category": category
    }


# -----------------------------------------
# Agent nodes
# -----------------------------------------

def repository_node(state: AgentState):

    answer = repository_agent(
        state["question"],
        state["context"]
    )

    return {
        "answer": answer
    }


def bug_node(state: AgentState):

    answer = bug_agent(
        state["question"],
        state["context"]
    )

    return {
        "answer": answer
    }


def documentation_node(state: AgentState):

    answer = documentation_agent(
        state["question"],
        state["context"]
    )

    return {
        "answer": answer
    }


# -----------------------------------------
# Routing function
# -----------------------------------------

def choose_agent(state: AgentState):

    return state["category"]


# -----------------------------------------
# Build graph
# -----------------------------------------

graph = StateGraph(AgentState)


graph.add_node(
    "retrieve_code",
    retrieve_code
)

graph.add_node(
    "router",
    router_node
)

graph.add_node(
    "repository_agent",
    repository_node
)

graph.add_node(
    "bug_agent",
    bug_node
)

graph.add_node(
    "documentation_agent",
    documentation_node
)


graph.add_edge(
    START,
    "retrieve_code"
)

graph.add_edge(
    "retrieve_code",
    "router"
)


graph.add_conditional_edges(
    "router",
    choose_agent,
    {
        "repository": "repository_agent",
        "bug": "bug_agent",
        "documentation": "documentation_agent"
    }
)


graph.add_edge(
    "repository_agent",
    END
)

graph.add_edge(
    "bug_agent",
    END
)

graph.add_edge(
    "documentation_agent",
    END
)


app = graph.compile()