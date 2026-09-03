import pytest
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command
from day13.durable_graph import get_durable_graph_builder

pytestmark = pytest.mark.integration

pytestmark = pytest.mark.integration

def test_1_approve_flow_with_restart(tmp_path):
    """Test 1: invoke -> interrupt -> close -> reopen -> resume -> completed"""
    db_path = str(tmp_path / "test.sqlite")
    builder = get_durable_graph_builder()
    config = {"configurable": {"thread_id": "test-1"}}
    
    with SqliteSaver.from_conn_string(db_path) as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)
        graph.invoke({"request": "start", "action_type": "publish_report"}, config)
    
    with SqliteSaver.from_conn_string(db_path) as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)
        graph.invoke(Command(resume={"decision": "approve"}), config)
        
        state = graph.get_state(config)

        assert state.values["approval_status"] == "approve"
        assert "execute_action" in state.values["node_trace"]
    

def test_2_reject_no_side_effect(tmp_path):
    """Test 2: interrupt -> resume reject -> execute action yok"""
    db_path = str(tmp_path / "test.sqlite")
    builder = get_durable_graph_builder()
    config = {"configurable": {"thread_id": "test-2"}}
    
    with SqliteSaver.from_conn_string(db_path) as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)
        graph.invoke({"request": "start", "action_type": "publish_report"}, config)
        graph.invoke(Command(resume={"decision": "reject"}), config)
        
        state = graph.get_state(config)

        assert state.values["approval_status"] == "reject"
        assert "execute_action" not in state.values["node_trace"]

def test_3_state_isolation(tmp_path):
    """Test 3: thread-A ve thread-B state isolation"""
    db_path = str(tmp_path / "test.sqlite")
    builder = get_durable_graph_builder()
    
    config_a = {"configurable": {"thread_id": "thread-A"}}
    config_b = {"configurable": {"thread_id": "thread-B"}}
    
    with SqliteSaver.from_conn_string(db_path) as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)
        
        graph.invoke({"request": "start", "action_type": "publish_report"}, config_a)
        graph.invoke({"request": "start", "action_type": "publish_report"}, config_b)
        
        graph.invoke(Command(resume={"decision": "approve"}), config_a)
        
        state_a = graph.get_state(config_a)
        assert state_a.next == ()
        
        state_b = graph.get_state(config_b)
        assert state_b.next == ("approval",)

def test_4_duplicate_action_graph_level(tmp_path, monkeypatch):
    """Test 4: duplicate action ID -> business effect yalnız bir kez"""
    test_log_file = tmp_path / "test-actions.jsonl"
    monkeypatch.setattr("day13.actions.LOG_FILE", str(test_log_file))
    
    db_path = str(tmp_path / "test.sqlite")
    builder = get_durable_graph_builder()
    config_4 = {"configurable": {"thread_id": "test-4"}}
    config_5 = {"configurable": {"thread_id": "test-5"}}
    
    with SqliteSaver.from_conn_string(db_path) as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)
        
        graph.invoke({"request": "start", "action_type": "publish_report", "action_id": "act-dup-1"}, config_4)
        graph.invoke(Command(resume={"decision": "approve"}), config_4)
        
        with open(test_log_file, "r") as f:
            assert len(f.readlines()) == 1
        
        graph.invoke({"request": "start", "action_type": "publish_report", "action_id": "act-dup-1"}, config_5)
        graph.invoke(Command(resume={"decision": "approve"}), config_5)
        
        with open(test_log_file, "r") as f:
            assert len(f.readlines()) == 1