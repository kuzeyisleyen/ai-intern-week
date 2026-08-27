import pytest
from day09.state import create_initial_state
from day09.graph_workflow import graph
from day08.retriever import RetrievedChunk

#servisler
class FakeOllamaClient:
    def __init__(self, response):
        self.response = response
        
    def chat(self, messages, tools=None):
        return self.response

class FakeRetriever:
    def __init__(self, responses_list):
        self.responses_list = responses_list
        self.call_count = 0
        
    def retrieve(self, query, top_k=None, filters=None):
        result = self.responses_list[self.call_count]
        self.call_count += 1
        return result

def sahte_chunk_olustur():
    return RetrievedChunk(
        chunk_id="chunk-1", source="test.md", document_id="doc1",
        chunk_index=0, topic="test", text="Test bilgisi [S1].", score=0.90
    )

"""'Merhaba' gibi sohbet sorularının veritabanına (Qdrant) hiç gitmeden doğrudan cevaplandığını test ediyorum."""
def test_smalltalk_route_avoids_retriever(monkeypatch):
    def exploding_retriever():
        raise AssertionError("Retriever should not be called")
    
    monkeypatch.setattr("day09.nodes.create_default_retriever", exploding_retriever)
    
    # Sahte model cevabı
    sahte_client = FakeOllamaClient({"message": {"content": "Merhaba!"}})
    monkeypatch.setattr("day09.nodes.OllamaClient", lambda: sahte_client)
    
    state = create_initial_state("Merhaba")
    result = graph.invoke(state)
    
    assert result["route"] == "smalltalk"
    assert "retrieve" not in result["node_trace"]
    assert result["node_trace"] == ["classify_query", "direct_generate"]

"""Bilgi gerektiren soruların doğruca 'knowledge' rotasına gidip veritabanında arama yaptığını test ediyorum."""
def test_knowledge_retriever_retriever(monkeypatch):
    sahte_retriever = FakeRetriever([[sahte_chunk_olustur()]])
    monkeypatch.setattr("day09.nodes.create_default_retriever", lambda: sahte_retriever)
    
    sahte_client = FakeOllamaClient({"message": {"content": "Bilgi burada [S1]."}})
    monkeypatch.setattr("day09.nodes.OllamaClient", lambda: sahte_client)
    
    state = create_initial_state("Docker volume nedir?")
    result = graph.invoke(state)
    
    assert result["route"] == "knowledge"
    assert "retrieve" in result["node_trace"]

"""Veritabanı üst üste hiçbir şey bulamazsa, sistemin soruyu sadece 1 kez yeniden yazıp kontrollü bir şekilde pes ettiğini (fallback) test ediyorum."""
def test_weak_retrieval_triggers_single_rewrite(monkeypatch):
    sahte_retriever = FakeRetriever([[], []])
    monkeypatch.setattr("day09.nodes.create_default_retriever", lambda: sahte_retriever)
    
    monkeypatch.setattr("day09.nodes.rewrite_query", lambda q: "yeni soru")
    
    state = create_initial_state("Bilinmeyen zor bir soru")
    result = graph.invoke(state)
    
    assert result["rewrite_count"] == 1
    assert result["node_trace"][-1] == "fallback"
    assert result["status"] == "completed"

"""Kullanıcı kargo fiyatı sorduğunda sadece izin verdiğim kargo aracının çalıştığını test ediyorum."""
def test_tool_route_uses_allowlisted_tool(monkeypatch):
    tool_cevabi = {
        "message": {
            "tool_calls": [
                {
                    "function": {
                        "name": "calculate_shipping_cost",
                        "arguments": {"city": "Ankara", "weight_kg": 2}
                    }
                }
            ]
        }
    }
    sahte_client = FakeOllamaClient(tool_cevabi)
    monkeypatch.setattr("day09.nodes.OllamaClient", lambda: sahte_client)
    
    state = create_initial_state("Ankara'ya 2 kg kargo ne kadar?")
    result = graph.invoke(state)
    
    assert result["route"] == "tool"
    assert result["tool_name"] == "calculate_shipping_cost"