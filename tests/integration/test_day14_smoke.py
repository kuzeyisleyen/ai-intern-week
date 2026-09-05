from unittest import result

import pytest
from day14.llm_router import run_llm_router
from day09.native_workflow import run_native_workflow

ALLOWED_ROUTES = {"smalltalk", "knowledge", "tool"}

@pytest.mark.integration
def test_ollama_structured_router_smoke():
    """Gerçek Ollama servisine giderek LLM'in JSON çıktısı ürettiğini doğrular."""
    # Kılavuza göre 5-8 routing case
    cases = [
        "Selam", 
        "Ankara'ya 2 kg paket maliyeti ne?", 
        "RAG nedir?",
        "Bugün hava nasıl?", 
        "Notlarımda hybrid search'i bul",
        "Agentic workflow ne demek?"
    ]
    
    for query in cases:
        result = run_llm_router(query)
        assert result["route"] in ALLOWED_ROUTES
        assert "latency_ms" in result
        
        if not result["fallback_used"]:
            assert result["decision_source"] in ["llm", "deterministic_fastpath"]

@pytest.mark.integration
def test_workflow_eval_smoke():
    """Sistemin ana hatlarını temsil eden alt kümede LangGraph akışını test eder."""
    queries = {
        "smalltalk": "Merhaba nasılsın?",
        "knowledge": "Named volume nedir?",
        "native_tool": "Ankara'ya 2 kiloluk kargo paketinin ücretini hesaplar mısın?",
        "mcp_tool": "Notlarımda hybrid search hakkında ne yazıyor?",
        "hitl": "Q3 finansal raporunu yayınla"
    }
    
    for expected_intent, query in queries.items():
        state = run_native_workflow(query)
        assert state.get("status") != "error", f"'{query}' sorgusu hata verdi: {state.get('error_type')}"
        
        if expected_intent == "hitl":
            pass
        else:
            assert state.get("route") in ALLOWED_ROUTES