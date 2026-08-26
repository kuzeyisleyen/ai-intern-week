import pytest
from day08.rag_pipeline import RAGResult, validate_question
from day08.retriever import RetrievedChunk
from day08.context_builder import build_context

# 1. CHUNK_TEXT() & EDGE CASES
def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Test için basitleştirilmiş chunker simülasyonu"""
    if not text or chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        return []
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += (chunk_size - overlap)
        if start + chunk_size >= len(text) and start < len(text):
            chunks.append(text[start:])
            break
    return chunks

def test_chunking_edge_cases():
    assert chunk_text("", 100, 10) == []
    assert chunk_text("Merhaba", 0, 0) == []
    assert chunk_text("Merhaba", -5, 0) == []
    assert chunk_text("Merhaba", 10, -2) == []
    assert chunk_text("Merhaba", 10, 10) == []
    assert chunk_text("Kısa", 100, 10) == ["Kısa"]

# 2. CONTEXT BUILDER & SOURCE-LABEL MAPPING 
def test_context_builder_and_mapping():
    chunks = tuple([
        RetrievedChunk(text="Metin 1", source="docker.md", score=0.9, topic="docker", chunk_id="1", document_id="d1", chunk_index=0),
        RetrievedChunk(text="Metin 2", source="compose.md", score=0.8, topic="compose", chunk_id="2", document_id="d2", chunk_index=1)
    ])
    
    context = build_context(chunks)

    # BuiltContextin texti içinde kaynak etiketlerinin oluştuğundan emin ol
    assert "[S1]" in context.text
    assert "docker.md" in context.text
    assert "Metin 1" in context.text
    assert "[S2]" in context.text

#3. CITATION VALIDATOR
def test_citation_validator():
    chunks = tuple([
        RetrievedChunk(text="A", source="doc1.md", score=0.9, topic="test", chunk_id="3", document_id="d3", chunk_index=0),
        RetrievedChunk(text="B", source="doc2.md", score=0.8, topic="test", chunk_id="4", document_id="d4", chunk_index=1)
    ]) 
    
    # Gerçek contexti asıl kodumuzdan üretiyoruz
    real_context = build_context(chunks)
    
    # Geçerli Senaryo
    valid_result = RAGResult(
        question="test sorusu", 
        context=real_context,  # Senin orijinal BuiltContext nesnen gidiyor
        retrieved_chunks=chunks, 
        answer="Cevap [S1] ve [S2]"
    )
    assert not valid_result.invalid_citations
    
    # Geçersiz Senaryo
    invalid_result = RAGResult(
        question="test sorusu", 
        context=real_context, 
        retrieved_chunks=chunks, 
        answer="Cevap [S9]"
    )
    assert "S9" in invalid_result.invalid_citations

# 4. HIT@K METRİĞİ MANTIĞI
def test_hit_at_k():
    expected_source = "agent-loop.md"
    retrieved_sources = ["docker.md", "agent-loop.md", "compose.md"]
    
    hit_1 = len(retrieved_sources) > 0 and retrieved_sources[0] == expected_source
    hit_3 = expected_source in retrieved_sources[:3]
    
    assert hit_1 is False
    assert hit_3 is True

# 5. INPUT VALIDATION
def test_input_validation():
    with pytest.raises(ValueError, match="Question boş olamaz"):
        validate_question("")
    
    with pytest.raises(ValueError, match="Question boş olamaz"):
        validate_question("   ")
        
    assert validate_question("Geçerli bir soru") == "Geçerli bir soru"