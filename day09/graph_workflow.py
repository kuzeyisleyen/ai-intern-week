from langgraph.graph import StateGraph, START, END
from day09.state import WorkflowState
from day09.state import create_initial_state
from day09.nodes import (
    classify_node, direct_generate_node, retrieve_node, 
    quality_node, rewrite_node, generate_node, 
    validate_node, tool_node, fallback_node,error_node
)
from day10.exceptions import (WorkflowError, 
DependencyUnavailableError, 
DependencyTimeOutError,
WorkflowLimitError,
ResponseContractError)
import time

# 1. Boş iskeleti başlatma
builder = StateGraph(WorkflowState)

# 2.(İsim, Fonksiyon)
builder.add_node("classify_query", classify_node)
builder.add_node("direct_generate", direct_generate_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("check_quality", quality_node)
builder.add_node("rewrite_query", rewrite_node)
builder.add_node("generate_with_context", generate_node)
builder.add_node("validate_citations", validate_node)
builder.add_node("execute_tool", tool_node)
builder.add_node("fallback", fallback_node)
builder.add_node("error_node", error_node)

def route_after_classification(state: dict) -> str:
    route = state["route"]
    if route not in {"smalltalk", "knowledge", "tool"}:
        return "error" # fallback yerine error oldu
    return route

def route_after_retrieval(state: dict) -> str:
    if state["retrieval_quality"] == "usable":
        return "generate"
    if state["rewrite_count"] < 1:
        return "rewrite"
    return "fallback"

# Başlangıç noktası
builder.add_edge(START, "classify_query")

# Sınıflandırma sonrası yol ayrımı
builder.add_conditional_edges(
    "classify_query",
    route_after_classification,
    {
        "smalltalk": "direct_generate",
        "knowledge": "retrieve",
        "tool": "execute_tool",
        "error": "error_node",   
          },
)

# Arama yaptıktan sonra zorunlu olarak kalite kontrolüne git
def route_after_retrieve(state: dict) -> str:
    # Eğer içeride bir hata yakalanmışsa doğrudan hata düğümüne git
    if state.get("status") == "error":
        return "error"
    return "check"

# Arama yaptıktan sonra duruma göre yol ayrımı
builder.add_conditional_edges(
    "retrieve",
    route_after_retrieve,
    {
        "check": "check_quality",
        "error": "error_node"
    }
)
# Kalite kontrolü sonrası yol ayrımı 
builder.add_conditional_edges(
    "check_quality",
    route_after_retrieval,
    {
        "generate": "generate_with_context",
        "rewrite": "rewrite_query",
        "fallback": "fallback",
    },
)

# Diğer düz bağlantılar ve Bitiş (END) noktaları
builder.add_edge("rewrite_query", "retrieve")
builder.add_edge("generate_with_context", "validate_citations")

builder.add_edge("validate_citations", END)
builder.add_edge("direct_generate", END)
builder.add_edge("execute_tool", END)
builder.add_edge("fallback", END)
builder.add_edge("error_node", END)

# haritayı çalıştırılabilir bir motora dönüştür
graph = builder.compile()

#Derlenmiş haritayı güvenle çağıran fonksiyon
def run_graph_workflow(query: str) -> dict:
    initial_state = create_initial_state(query)
    start_time = time.time() # Kronometreyi başlat
    
    try:
        final_state = graph.invoke(initial_state)
        # Başarılı senaryoda süreyi kaydet
        final_state["duration_ms"] = int((time.time() - start_time) * 1000)
        return final_state
        
    except WorkflowLimitError as e:
        initial_state.update({
            "status": "stopped",
            "error_type": "workflow_limit",
            "fallback_reason": "max_steps",
            "errors": initial_state.get("errors", []) + [str(e)],
            "duration_ms": int((time.time() - start_time) * 1000) # Durdurulma senaryosunda süreyi kaydet
        })
        return initial_state
        
    except WorkflowError as e:
        initial_state.update({
            "status": "error",
            "error_type": e.__class__.__name__,
            "errors": initial_state.get("errors", []) + [str(e)],
            "duration_ms": int((time.time() - start_time) * 1000) # Hata senaryosunda süreyi kaydet
        })
        return initial_state