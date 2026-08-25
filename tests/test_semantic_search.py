from day06.semantic_search import semantic_search
from day06.similarity import cosine_similarity
import pytest

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

def test_semantic_search_ranking():
    """Arama sonuçlarının cosine similarity skoruna göre azalan (descending) sırada döndüğünü test eder."""
    client = MockClient()
    docs = [
        {"id": "A", "text": "A", "embedding": [1.0, 0.0]},
        {"id": "B", "text": "B", "embedding": [0.0, 1.0]},
        {"id": "C", "text": "C", "embedding": [0.8, 0.2]}
    ]
    results = semantic_search("test",docs,client,top_k=3)
    assert len(results) == 3
    assert results[0]["id"]=="A"
    assert results[1]["id"]=="C"
    assert results[2]["id"]=="B"

def semantic_search_invalid_top_k() :
    """top_k değerinin 0 veya negatif olması durumunda sistemin bunu açıkça reddettiğini doğrular."""
    client = MockClient()
    docs = [{"id":"A","text":"A","embedding":[1.0,0.0]}]

    with pytest.raises(ValueError):
        semantic_search("test",docs,client,top_k=0)
    with pytest.raises(ValueError):
        semantic_search("test",docs,client,top_k=1)

def test_cosine_zero_vector():
    """Sıfır vektörü ile cosine hesabı yapılmaya çalışıldığında ValueError fırlatıldığını doğrular."""
    with pytest.raises(ValueError):
        cosine_similarity([0.0, 0.0], [1.0, 0.0])
