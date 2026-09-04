ACTION_POLICIES = {
    "search_notes": {
        "approval_required": False,
    },
    "calculate_shipping_cost": {
        "approval_required": False,
    },
    "publish_report": {
        "approval_required": True,
    },
}

def requires_approval(action_type: str) -> bool:
    if action_type not in ACTION_POLICIES:
        raise ValueError(f"Action type '{action_type}' is not allowed.")
    return ACTION_POLICIES[action_type]["approval_required"]
    

def validate_decision(decision: str) -> str:
    if decision not in ["approve", "reject"]:
        raise ValueError("Decision must be 'approve' or 'reject'")
    return decision

def validate_resume_payload(payload) -> str:
    if not isinstance(payload, dict):
        raise ValueError("Resume payload must be a dictionary")
    
    decision = payload.get("decision")
    if not isinstance(decision, str):
        raise ValueError("Decision value must be a string")
        
    return validate_decision(decision)