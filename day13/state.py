from typing import TypedDict

class DurableState(TypedDict, total=False):
    request : str
    action_id : str
    action_type : str
    approval_required : bool
    approval_status : str
    status : str
    execution_status : str
    node_trace : list[str]