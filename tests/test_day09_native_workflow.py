from day08.retriever import RetrievedChunk
from day09.native_workflow import run_native_workflow


class FakeOllamaClient:
    def __init__(self, response: dict):
        self.response = response

    def chat(self, messages, tools=None):
        return self.response


class FakeRetriever:
    def __init__(self, results_per_call: list[list[RetrievedChunk]]):
        self.results_per_call = results_per_call
        self.call_count = 0

    def retrieve(self, query, top_k=None, filters=None):
        result = self.results_per_call[self.call_count]
        self.call_count += 1
        return result


def make_chunk() -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id="docker-volumes:0",
        source="docker-volumes.md",
        document_id="docker-volumes",
        chunk_index=0,
        topic="docker-volumes",
        text="Named volume veriyi container yaşam döngüsünden bağımsız tutar.",
        score=0.90,
    )


def test_smalltalk_does_not_call_retriever(monkeypatch):
    def exploding_retriever_factory():
        raise AssertionError("Smalltalk sorgusu retriever'a gitmemeli.")

    monkeypatch.setattr(
        "day09.nodes.create_default_retriever",
        exploding_retriever_factory,
    )
    monkeypatch.setattr(
        "day09.nodes.OllamaClient",
        lambda: FakeOllamaClient(
            {"message": {"content": "Merhaba! Sana nasıl yardımcı olabilirim?"}}
        ),
    )

    state = run_native_workflow("Merhaba")

    assert state["route"] == "smalltalk"
    assert state["status"] == "completed"
    assert state["node_trace"] == ["classify_query", "direct_generate"]
    assert "retrieve" not in state["node_trace"]


def test_knowledge_calls_retriever(monkeypatch):
    fake_retriever = FakeRetriever([[make_chunk()]])

    monkeypatch.setattr(
        "day09.nodes.create_default_retriever",
        lambda: fake_retriever,
    )
    monkeypatch.setattr(
        "day09.nodes.OllamaClient",
        lambda: FakeOllamaClient(
            {"message": {"content": "Named volume kalıcı veri sağlar [S1]."}}
        ),
    )

    state = run_native_workflow("Named volume nedir?")

    assert state["route"] == "knowledge"
    assert fake_retriever.call_count == 1
    assert state["retrieval_quality"] == "usable"
    assert state["rewrite_count"] == 0
    assert state["status"] == "completed"
    assert state["node_trace"] == [
        "classify_query",
        "retrieve",
        "retrieval_quality",
        "generate",
        "validate_citations",
    ]


def test_tool_route_calls_allowlisted_shipping_tool(monkeypatch):
    tool_response = {
        "message": {
            "tool_calls": [
                {
                    "function": {
                        "name": "calculate_shipping_cost",
                        "arguments": {"city": "Ankara", "weight_kg": 2},
                    }
                }
            ]
        }
    }
    monkeypatch.setattr(
        "day09.nodes.OllamaClient",
        lambda: FakeOllamaClient(tool_response),
    )

    state = run_native_workflow("Ankara'ya 2 kg kargo ne kadar?")

    assert state["route"] == "tool"
    assert state["tool_name"] == "calculate_shipping_cost"
    assert state["tool_result"] == {
        "city": "Ankara",
        "weight_kg": 2,
        "cost": 84,
        "currency": "TRY",
    }
    assert state["status"] == "completed"
    assert state["node_trace"] == ["classify_query", "tool_node"]
    assert "retrieve" not in state["node_trace"]


def test_weak_retrieval_rewrites_once_then_falls_back(monkeypatch):
    fake_retriever = FakeRetriever([[], []])
    original_query = "Corpus dışında kalan bir bilgi sorusu"
    rewritten_query = "semantic retrieval için yeniden yazılmış sorgu"

    monkeypatch.setattr(
        "day09.nodes.create_default_retriever",
        lambda: fake_retriever,
    )
    monkeypatch.setattr(
        "day09.nodes.rewrite_query",
        lambda query: rewritten_query,
    )

    state = run_native_workflow(original_query)

    assert state["route"] == "knowledge"
    assert fake_retriever.call_count == 2
    assert state["original_query"] == original_query
    assert state["retrieval_query"] == rewritten_query
    assert state["rewrite_count"] == 1
    assert state["status"] == "completed"
    assert state["node_trace"] == [
        "classify_query",
        "retrieve",
        "retrieval_quality",
        "rewrite",
        "retrieve",
        "retrieval_quality",
        "fallback",
    ]


from unittest.mock import patch

@patch("day14.llm_router.run_llm_router")
def test_invalid_route_returns_controlled_error(mock_router):
    mock_router.return_value = {"route": "banana_route", "decision_source": "llm", "latency_ms": 10}
    
    state = run_native_workflow("dummy query")
    
    assert state["route"] == "banana_route"