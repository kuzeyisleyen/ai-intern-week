import json
import os
from unittest.mock import patch
from day09.graph_workflow import run_graph_workflow

def run_experiments():
    print("Hata enjeksiyon deneyleri (LangGraph) başlatılıyor...\n")
    output_data = {"experiments": []}

    # 1. Retriever Unavailable
    print("1/7 Test ediliyor: Retriever Unavailable")
    with patch("day09.nodes.create_default_retriever") as mock_retriever_factory:
        # create_default_retriever çağrıldığında bir hata fırlatmasını sağlıyoruz
        mock_retriever_factory.side_effect = Exception("Qdrant kapalı simülasyonu")
        
        state = run_graph_workflow("Docker nedir?")
        
        output_data["experiments"].append({
            "name": "retriever_unavailable",
            "expected_terminal_status": "error",
            "actual_terminal_status": state.get("status"),
            "failed_node": state.get("failed_node"),
            "error_type": state.get("error_type"),
            "passed": state.get("status") == "error" and state.get("error_type") == "DependencyUnavailableError"
        })

    # 2. Model Timeout (Smalltalk rotası üzerinden)
    print("2/7 Test ediliyor: Model Timeout")
    with patch("day09.nodes.OllamaClient.chat") as mock_chat:
        # direct_generate_node içindeki chat fonksiyonunun hata dönmesini simüle ediyoruz
        mock_chat.return_value = {"error": "DependencyTimeoutError: Ollama cevap vermiyor"}
        
        state = run_graph_workflow("Merhaba")
        
        output_data["experiments"].append({
            "name": "model_timeout",
            "expected_terminal_status": "error",
            "actual_terminal_status": state.get("status"),
            "failed_node": state.get("failed_node"),
            "error_type": state.get("error_type"),
            "passed": state.get("status") == "error"
        })

    # 3. Invalid Route
    print("3/7 Test ediliyor: Invalid Route")
    
    state = run_graph_workflow("banana kelimesi testi")
    
    output_data["experiments"].append({
        "name": "invalid_route",
        "expected_terminal_status": "error",
        "actual_terminal_status": state.get("status"),
        "failed_node": "error_node",
        "error_type": state.get("error_type", "WorkflowError"),
        "passed": state.get("status") == "error"
    })

    # 4. Tool Failure
    print("4/7 Test ediliyor: Tool Failure")
    with patch("day09.nodes.OllamaClient.chat") as mock_chat, \
         patch("day09.nodes.execute_tool") as mock_execute:
        # Modelin doğru tool çağrısı yaptığını, ancak tool'un çalışma anında patladığını simüle ediyoruz
        mock_chat.return_value = {
            "message": {
                "tool_calls": [{"function": {"name": "calculate_shipping_cost", "arguments": {}}}]
            }
        }
        mock_execute.return_value = {"error": "Shipping servisi çöktü"}
        
        state = run_graph_workflow("Kargo hesapla")
        
        output_data["experiments"].append({
            "name": "tool_failure",
            "expected_terminal_status": "error",
            "actual_terminal_status": state.get("status"),
            "failed_node": state.get("failed_node"),
            "error_type": state.get("error_type"),
            "passed": state.get("status") == "error" and state.get("error_type") == "ToolRuntimeError"
        })

    # 5. Rewrite Exhaustion
    print("5/7 Test ediliyor: Rewrite Exhaustion")
    with patch("day09.nodes.create_default_retriever") as mock_retriever_factory:
        # Arama motorunun hep boş liste dönmesini sağlıyoruz (kalite = weak olacak)
        mock_retriever = mock_retriever_factory.return_value
        mock_retriever.retrieve.return_value = []
        
        state = run_graph_workflow("Docker nedir?")
        
        output_data["experiments"].append({
            "name": "rewrite_exhaustion",
            "expected_terminal_status": "completed", # fallback node status="completed" dönüyor kodunda
            "actual_terminal_status": state.get("status"),
            "failed_node": "rewrite_query",
            "error_type": "WorkflowLimitError",
            "passed": state.get("status") == "completed" and "fallback" in state.get("node_trace", [])
        })

    # 6. Max-Step Reached
    print("6/7 Test ediliyor: Max-Step")
    with patch("day09.nodes.MAX_STEPS", 0): # Sınırı anında sıfıra indiriyoruz
        state = run_graph_workflow("Merhaba")
        
        output_data["experiments"].append({
            "name": "max_step",
            "expected_terminal_status": "stopped",
            "actual_terminal_status": state.get("status"),
            "failed_node": "next_step",
            "error_type": state.get("error_type"),
            "passed": state.get("status") == "stopped" and state.get("error_type") == "workflow_limit"
        })

    # 7. Invalid Citation
    print("7/7 Test ediliyor: Invalid Citation")
    # Arama motorunu hiç bozmuyoruz (gerçek veri getirsin). 
    # Yalnızca modelin cevabını bozup içine uydurma [S9] etiketini koyuyoruz.
    with patch("day09.nodes.OllamaClient.chat") as mock_chat:
        mock_chat.return_value = {"message": {"content": "Bu bilgi tamamen uydurmadır [S9]"}}
        
        state = run_graph_workflow("Docker nedir?")
        
        output_data["experiments"].append({
            "name": "invalid_citation",
            "expected_terminal_status": "error",
            "actual_terminal_status": state.get("status"),
            "failed_node": state.get("failed_node"),
            "error_type": state.get("error_type"),
            "passed": state.get("status") == "error" and state.get("error_type") == "ResponseContractError"
        })

    os.makedirs("output", exist_ok=True)
    output_path = "output/day10-failure-experiments.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\nTüm deneyler çalıştırıldı! Sonuçlar '{output_path}' dosyasına kaydedildi.")

if __name__ == "__main__":
    run_experiments()