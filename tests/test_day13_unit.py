import pytest
import os
import json
from day13.approval_policy import requires_approval, validate_decision
from day13.actions import execute_once


def test_approval_policy():
    assert requires_approval("search_notes") is False
    assert requires_approval("publish_report") is True
    with pytest.raises(Exception):
        requires_approval("unknown_action")


def test_validate_decision():
    assert validate_decision("approve") == "approve"
    assert validate_decision("reject") == "reject"

    with pytest.raises(ValueError):
        validate_decision("maybe")

    with pytest.raises(ValueError):
        validate_decision(True)  

def test_execute_once_idempotency(tmp_path, monkeypatch):
    test_log_file = tmp_path / "test-actions.jsonl"
    monkeypatch.setattr("day13.actions.LOG_FILE", str(test_log_file))

    result1 = execute_once("act-unit-1", "test_action")
    assert result1["status"] == "executed"

    result2 = execute_once("act-unit-1", "test_action")
    assert result2["status"] == "already_executed"

    with open(test_log_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
    