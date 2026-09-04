from uuid import uuid4
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt
from day13.state import DurableState
from day13.approval_policy import requires_approval, validate_resume_payload
from day13.actions import execute_once

def prepare_node(state: DurableState) -> dict:
    action_id = state.get("action_id")
    if not action_id:
        action_id = f"act-{uuid4()}"
        
    action_type = state.get("action_type", "publish_report")
        
    return {
        "status": "prepared",
        "action_type": action_type, 
        "action_id": action_id,
        "approval_required": requires_approval(action_type),
        "node_trace": [*state.get("node_trace", []), "prepare"]
    }

def approval_node(state: DurableState) -> dict:
    if state.get("approval_required"):
        # CLI'den Command(resume={"decision": ...}) ile dönen DICT değeri
        user_input = interrupt({
            "type": "approval_required",
            "action_id": state.get("action_id", ""),
            "action_type": state.get("action_type", ""),
            "summary": "Onay bekleniyor"
        })
        
        # Explicit validation helper
        validated_decision = validate_resume_payload(user_input)
        
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
        "status": "completed",
        "execution_status": result["status"],
        "node_trace": [*state.get("node_trace", []), "execute_action"]
    }

def rejected_node(state: DurableState) -> dict:
    return {
        "status": "rejected",
        "node_trace": [*state.get("node_trace", []), "rejected"]
    }

def route_after_approval(state: DurableState) -> str:
    if state.get("approval_status") == "approve" or state.get("approval_status") == "not_required":
        return "execute_action"
    return "rejected_node"

def get_durable_graph_builder():
    graph = StateGraph(DurableState)

    graph.add_node("prepare", prepare_node)
    graph.add_node("approval", approval_node) 
    graph.add_node("execute_action", execute_action_node)
    graph.add_node("rejected_node", rejected_node)
    
    graph.add_edge(START, "prepare")
    graph.add_edge("prepare", "approval")
    
    graph.add_conditional_edges("approval", route_after_approval)
    
    graph.add_edge("execute_action", END)
    graph.add_edge("rejected_node", END)
    
    return graph