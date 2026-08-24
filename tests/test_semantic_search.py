from day06.semantic_search import semantic_search

# Ollama'ya bağlanmamak için sahte bir client oluşturuyoruz
class MockClient:
    def embed(self, text):
        return [1.0, 0.0]  # Ne gelirse gelsin sabit bir vektör dön

def test_semantic_search_top_k_exceeds_docs():
    """top_k değeri, doküman sayısından büyükse program çökmek yerine eldekileri dönmelidir."""
    client = MockClient()
    docs = [
        {"id": "1", "text": "A", "embedding": [1.0, 0.0]},
        {"id": "2", "text": "B", "embedding": [0.8, 0.6]}
    ]
    
    # 2 doküman var ama top_k=50 istiyoruz
    results = semantic_search("test", docs, client, top_k=50)
    
    assert len(results) == 2 

def test_semantic_search_empty_docs():
    """Doküman listesi boş ise program boş liste dönmelidir."""
    client = MockClient()
    results = semantic_search("test", [], client)
    
    assert results == []