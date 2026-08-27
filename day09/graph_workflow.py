from langgraph.graph import StateGraph, START, END
from day09.state import WorkflowState
from day09.nodes import (
    classify_node, direct_generate_node, retrieve_node, 
    quality_node, rewrite_node, generate_node, 
    validate_node, tool_node, fallback_node
)

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

def route_after_classification(state: dict) -> str:
    route = state["route"]
    if route not in {"smalltalk", "knowledge", "tool"}:
        return "fallback"
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
        "fallback": "fallback",
    },
)

# Arama yaptıktan sonra zorunlu olarak kalite kontrolüne git
builder.add_edge("retrieve", "check_quality")

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

# haritayı çalıştırılabilir bir motora dönüştür
graph = builder.compile()