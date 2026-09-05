import json
from unittest.mock import patch
from day14.evaluator import execute_case, normalize_workflow_result

def print_result(name: str, raw_state: dict, actual: dict):
    print(f"\n[{name}] Sonuçları:")
    print(f"  Rota (Route): {actual.get('route')}")
    print(f"  Karar Kaynağı (Decision Source): {raw_state.get('decision_source')}")
    print(f"  Terminal Durumu: {actual.get('terminal_status')}")
    print(f"  Hatalar (Errors): {raw_state.get('errors', [])}")
    print(f"  Sistem ayakta kaldı mı?: {'Evet' if actual.get('terminal_status') == 'error' or actual.get('terminal_status') == 'completed' else 'Hayır'}")

def run_drills():
    print("kontrollü hata denemeleri başlatılıyor...")

    # FAILURE A: Ollama / Semantic Router Çökmesi

    print("\n--- Failure A: Yönlendirici (Ollama) Çöktü")
    case_a = {"suite": "workflow", "query": "kargo hesapla", "id": "drill-a"}
    
    with patch("day14.llm_router.OllamaClient.chat") as mock_chat:
        mock_chat.return_value = {"error": "Connection refused (Simulated)"}
        
        try:
            raw_state = execute_case(case_a)
            actual = normalize_workflow_result(raw_state)
            actual["decision_source"] = raw_state.get("decision_source")
            print_result("Failure A", raw_state, actual)
        except Exception as e:
            print(f"Failure A BAŞARISIZ! Sistem exception fırlatıp çöktü: {e}")

    # FAILURE B: MCP Aracı Çökmesi
    print("\n--- Failure B: MCP Sunucusu (search_notes) Çöktü ---")
    case_b = {"suite": "workflow", "query": "notlarımda RRF ara", "id": "drill-b"}
    
    # MCPToolAdapter'ın invoke_sync metodunun hata fırlatmasını simüle ediyoruz
    with patch("day09.nodes.MCPToolAdapter.invoke_sync") as mock_mcp:
        mock_mcp.side_effect = Exception("MCP Protocol Pipe Broken (Simulated)")

        with patch("day14.llm_router.run_llm_router") as mock_router:
            mock_router.return_value = {"route": "tool", "decision_source": "llm", "latency_ms": 10}
            
            try:
                raw_state = execute_case(case_b)
                actual = normalize_workflow_result(raw_state)
                print_result("Failure B", raw_state, actual)
            except Exception as e:
                print(f"Failure B BAŞARISIZ! Sistem exception fırlatıp çöktü: {e}")

    # FAILURE C: Qdrant (Vektör DB) Çökmesi
    print("\n--- Failure C: Qdrant (Vektör Veritabanı) Çöktü ---")
    case_c = {"suite": "workflow", "query": "Docker nedir?", "id": "drill-c"}
    
    # Retriever'ın hata fırlatmasını simüle ediyoruz
    with patch("day09.nodes.create_default_retriever") as mock_retriever_factory:
        mock_retriever = mock_retriever_factory.return_value
        mock_retriever.retrieve.side_effect = Exception("Qdrant Connection Timeout (Simulated)")
        
        with patch("day14.llm_router.run_llm_router") as mock_router:
            mock_router.return_value = {"route": "knowledge", "decision_source": "llm", "latency_ms": 10}
            
            try:
                raw_state = execute_case(case_c)
                actual = normalize_workflow_result(raw_state)
                print_result("Failure C", raw_state, actual)
            except Exception as e:
                print(f"Failure C BAŞARISIZ! Sistem exception fırlatıp çöktü: {e}")

if __name__ == "__main__":
    run_drills()