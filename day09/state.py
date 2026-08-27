from typing import TypedDict


class WorkflowState(TypedDict):
    original_query: str
    query: str
    retrieval_query: str

    route: str

    retrieved_chunks: list[dict]
    retrieval_quality: str

    answer: str | None
    citations: list[str]

    tool_name: str | None
    tool_result: dict | None

    rewrite_count: int
    step_count: int
    status: str
    errors: list[str]
    node_trace: list[str]


def create_initial_state(query: str) -> WorkflowState:
    return {
        "query": query,
        "original_query": query,
        "retrieval_query": query,
        "route": "",
        "retrieved_chunks": [],
        "retrieval_quality": "",
        "answer": None,
        "citations": [],
        "tool_name": None,
        "tool_result": None,
        "rewrite_count": 0,
        "step_count": 0,
        "status": "started",
        "errors": [],
        "node_trace": [],
    }
