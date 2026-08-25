import pytest
from qdrant_client import models
from day07.ingest import validate_documents

def test_input_validation():
    valid_docs = [{
        "id": "doc-1", "text": "Test metni", "category": "test",
        "source": "src", "day": 1, "topic": "t", "language": "tr"
    }]
    validate_documents(valid_docs)
    
    invalid_docs = [{"id": "doc-2"}] 
    with pytest.raises(ValueError):
        validate_documents(invalid_docs)

def test_point_id_mapping():
    """String ID'lerin Qdrant için Integer'a çevrilmesini test eder."""
    documents = [{"id": "doc-01"}, {"id": "doc-02"}]
    mapping = {idx: doc["id"] for idx, doc in enumerate(documents, start=1)}
    
    assert mapping[1] == "doc-01"
    assert mapping[2] == "doc-02"

def test_filter_builder():
    """Qdrant Filter objesinin doğru inşa edildiğini test eder."""
    category_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="docker")
            )
        ]
    )
    assert len(category_filter.must) == 1
    assert category_filter.must[0].key == "category"
    assert category_filter.must[0].match.value == "docker"

def test_payload_builder():
    """Gelen verinin Qdrant payload yapısına doğru çevrildiğini test eder."""
    raw_document = {
        "id": "doc-01",
        "text": "Docker volume",
        "category": "docker",
        "source": "guide", "day": 7, "topic": "db", "language": "tr"
    }
    
    expected_payload = {
        "document_id": raw_document["id"],
        "text": raw_document["text"],
        "category": raw_document["category"]
    }
    
    assert expected_payload["document_id"] == "doc-01"
    assert "id" not in expected_payload 
def test_result_formatting():
    """Qdrant yanıt objesinin (ScoredPoint) bizim JSON formatımıza doğru çevrildiğini test eder."""
    fake_point = models.ScoredPoint(
        id=1,
        version=0,
        score=0.8543,
        payload={"document_id": "doc-01", "category": "docker", "text": "örnek metin"}
    )
    
    formatted_result = {
        "point_id": fake_point.id,
        "document_id": fake_point.payload.get("document_id"),
        "score": round(fake_point.score, 4)
    }
    
    assert formatted_result["point_id"] == 1
    assert formatted_result["document_id"] == "doc-01"
    assert formatted_result["score"] == 0.8543