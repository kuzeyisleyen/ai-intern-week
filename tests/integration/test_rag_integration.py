import pytest
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

from day08.rag_pipeline import RAGPipeline
from day08.retriever import create_default_retriever

from day08.rag_cli import OllamaClient
# 1. QDRANT ENTEGRASYON TESTİ
@pytest.mark.integration
def test_qdrant_retrieval_fake_vectors():
    """Gerçek Qdrant sunucusunda, sahte (fake) vektörlerle test"""
    client = QdrantClient(url="http://qdrant:6333")
    col_name = "test_integration_collection"
    
    # Varsa temizle
    if client.collection_exists(col_name):
        client.delete_collection(col_name)
        
    client.create_collection(
        collection_name=col_name,
        vectors_config=VectorParams(size=3, distance=Distance.COSINE)
    )
    
    # Fake data yükle
    client.upsert(
        collection_name=col_name,
        points=[
            PointStruct(id=str(uuid.uuid4()), vector=[1.0, 0.0, 0.0], payload={"source": "doc1", "text": "Test metni 1"}),
            PointStruct(id=str(uuid.uuid4()), vector=[0.0, 1.0, 0.0], payload={"source": "doc2", "text": "Test metni 2"})
        ]
    )
    
    # Arama yap
    res = client.query_points(collection_name=col_name, query=[1.0, 0.0, 0.0], limit=1).points    
    assert len(res) == 1
    assert res[0].payload["source"] == "doc1"
    
    # Test bitince temizle
    client.delete_collection(col_name)


#2. UÇTAN UCA (SMOKE) RAG TESTİ
@pytest.mark.integration
def test_full_rag_smoke():
    """Bütün RAG mimarisinin (Qdrant + Ollama) uçtan uca (Smoke) testi"""
    retriever = create_default_retriever()
    generation_client = OllamaClient(model_name="qwen3:1.7b", base_url="http://ollama:11434")
    
    pipeline = RAGPipeline(retriever=retriever, generation_client=generation_client)
    
    # Gerçek senaryo koştur (Pipeline çökmüyor mu ve dolu bir cevap dönüyor mu?)
    result = pipeline.answer("Named volume nedir?", top_k=1)
    
    assert result is not None
    assert isinstance(result.answer, str)
    assert len(result.answer) > 0
    # Context varsa veya yoksa duruma göre çökmeyi engelleriz
    # Ama pipeline bize her halükarda RAGResult dönmeli.