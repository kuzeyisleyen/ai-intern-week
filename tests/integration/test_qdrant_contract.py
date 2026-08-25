import os
import pytest
from uuid import uuid4
import urllib.request
from qdrant_client import QdrantClient, models

@pytest.fixture
def qdrant_test_setup():
    """Testler başlamadan önce koleksiyonu kurar, bitince siler."""
    client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
    test_collection = f"test_day07_{uuid4().hex}"
    
    client.create_collection(
        collection_name=test_collection,
        vectors_config=models.VectorParams(size=3, distance=models.Distance.COSINE),
    )
    
    points = [
        models.PointStruct(id=1, vector=[1.0, 0.0, 0.0], payload={"category": "A"}),
        models.PointStruct(id=2, vector=[0.0, 1.0, 0.0], payload={"category": "B"}),
        models.PointStruct(id=3, vector=[0.9, 0.1, 0.0], payload={"category": "C"}),
    ]
    client.upsert(collection_name=test_collection, points=points)
    
    yield client, test_collection
    
    client.delete_collection(test_collection)

# TEST 1: Sadece Anlamsal Yakınlık
@pytest.mark.integration
def test_nearest_match_logic(qdrant_test_setup):
    """Vektör matematiğinin (kosinüs benzerliği) doğru çalıştığını test eder."""
    client, collection_name = qdrant_test_setup
    
    response = client.query_points(
        collection_name=collection_name, query=[1.0, 0.0, 0.0], limit=2
    ).points
    
    assert response[0].id == 1  
    assert response[1].id == 3 


# TEST 2: Sadece Meta Veri Filtreleme
@pytest.mark.integration
def test_metadata_filter_logic(qdrant_test_setup):
    """Qdrant'ın Payload filtreleme özelliğini test eder."""
    client, collection_name = qdrant_test_setup
    
    filter_response = client.query_points(
        collection_name=collection_name, 
        query=[1.0, 0.0, 0.0], 
        limit=1,
        query_filter=models.Filter(
            must=[models.FieldCondition(key="category", match=models.MatchValue(value="B"))]
        )
    ).points
    
    assert len(filter_response) == 1
    assert filter_response[0].id == 2  

# Test 3 : Sistem Sağlığı
@pytest.mark.integration
def test_app_side_health_smoke():
    """App-side health smoke: Qdrant'ın HTTP API üzerinden sağlıklı yanıt verip vermediğini test eder."""
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    
    health_endpoint = f"{qdrant_url}/readyz"

    try:
        response = urllib.request.urlopen(health_endpoint)
        assert response.getcode() == 200 #dönerse sağlıklıdır
        
        body = response.read().decode("utf-8")
        assert "all shards are ready" in body.lower()
        
    except Exception as e:
        pytest.fail(f"Smoke test başarısız oldu. Qdrant'a ulaşılamıyor: {e}")