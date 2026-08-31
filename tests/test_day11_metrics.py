import pytest
from day11.metrics import hit_at_k, reciprocal_rank, mean_reciprocal_rank

def test_reciprocal_rank_expected_rank_1():
    retrieved = ["doc-A", "doc-B", "doc-C"]
    assert reciprocal_rank(retrieved, "doc-A") == 1.0

def test_reciprocal_rank_expected_rank_2():
    retrieved = ["doc-A", "doc-B", "doc-C"]
    assert reciprocal_rank(retrieved, "doc-B") == 0.5

def test_reciprocal_rank_not_found():
    retrieved = ["doc-A", "doc-B", "doc-C"]
    assert reciprocal_rank(retrieved, "doc-D") == 0.0

def test_hit_at_k_logic():
    retrieved = ["doc-A", "doc-B", "doc-C"]
    assert hit_at_k(retrieved, "doc-B", k=1) is False
    assert hit_at_k(retrieved, "doc-B", k=3) is True

def test_hit_at_k_invalid_k():
    with pytest.raises(ValueError):
        hit_at_k(["doc-A"], "doc-A", k=0)
    with pytest.raises(ValueError):
        hit_at_k(["doc-A"], "doc-A", k=-1)

def test_mean_reciprocal_rank():
    scores = [1.0, 0.5, 0.0]
    assert mean_reciprocal_rank(scores) == 0.5