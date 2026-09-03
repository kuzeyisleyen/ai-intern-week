from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt
from day13.state import DurableState
from day13.approval_policy import requires_approval, validate_decision
from day13.actions import execute_once

def prepare_node(state: DurableState) -> dict:
    return {
        "status": "prepared",
        "action_type": state.get("action_type", "publish_report"), 
        "action_id": state.get("action_id", "act-123"),
        "node_trace": [*state.get("node_trace", []), "prepare"]
    }

def approval_node(state: DurableState) -> dict:
    if requires_approval(state.get("action_type", "")):
        # CLI'den Command(resume={"decision": ...}) ile dönen DICT değeri
        user_input = interrupt({
            "type": "approval_required",
            "action_id": state.get("action_id", ""),
            "action_type": state.get("action_type", ""),
            "summary": "Onay bekleniyor"
        })
        
        # dict içindeki stringi alıp kontrol
        decision_str = user_input.get("decision")
        validated_decision = validate_decision(decision_str)
        
        return {
            "approval_status": validated_decision,
            "node_trace": [*state.get("node_trace", []), "approval"]
        }
    
    # Onay gerekmeyen işlemler için 
    return {"approval_status": "not_required"}

def execute_action_node(state: DurableState) -> dict:

    state_action_id = state.get("action_id", "")
    state_action_type = state.get("action_type", "")
    result = execute_once(state_action_id, state_action_type)
    return {
        "status": result["status"],
        "node_trace": [*state.get("node_trace", []), "execute_action"]
    }

def route_after_approval(state: DurableState) -> str:
    if state.get("approval_status") == "approve":
        return "execute_action"
    return "mark_ready"

def mark_ready_node(state: DurableState) -> dict:
    return {
        "status": "ready",
        "node_trace": [*state.get("node_trace", []), "mark_ready"]
    }

def get_durable_graph_builder():
    graph = StateGraph(DurableState)

    graph.add_node("prepare", prepare_node)
    graph.add_node("approval", approval_node) 
    graph.add_node("execute_action", execute_action_node) 
    graph.add_node("mark_ready", mark_ready_node)
    
    graph.add_edge(START, "prepare")
    graph.add_edge("prepare", "approval")
    
    graph.add_conditional_edges("approval", route_after_approval)
    
    graph.add_edge("execute_action", "mark_ready")
    graph.add_edge("mark_ready", END)
    
    return graph