import pytest
from day14.trajectory import check_trajectory_strict, check_trajectory_ordered
from day14.metrics import aggregate_boolean_scores, build_confusion_matrix, score_expected_field

def test_ordered_subsequence_match():
    """ 'ordered/allowed trajectory' mantığını test eder."""
    expected = ["classify_query", "retrieve", "generate"]
    
    assert check_trajectory_ordered(expected, ["classify_query", "retrieve", "generate"]) is True
    assert check_trajectory_ordered(expected, ["classify_query", "retrieve", "quality_check", "generate"]) is True
    assert check_trajectory_ordered(expected, ["classify_query", "generate"]) is False
    assert check_trajectory_ordered(expected, ["classify_query", "generate", "retrieve"]) is False

def test_strict_trajectory():
    """ 'strict trajectory' mantığını test eder."""
    expected = ["classify_query", "retrieve", "generate"]
    
    assert check_trajectory_strict(expected, ["classify_query", "retrieve", "generate"]) is True
    assert check_trajectory_strict(expected, ["classify_query", "retrieve"]) is False

def test_route_accuracy_denominator():
    """ Null (None) değerlerin hesaplamaya dahil edilmediğini test eder (Denominator logic)."""
    scores = [True, False, None, True]
    result = aggregate_boolean_scores(scores)
    
    assert result["denominator"] == 3
    assert result["correct"] == 2
    assert result["accuracy"] == (2 / 3)

def test_empty_denominator():
    """ Sıfıra bölme hatası engelleyici mantığı test eder."""
    result = aggregate_boolean_scores([None, None])
    
    assert result["denominator"] == 0
    assert result["accuracy"] is None

def test_tool_provider_not_applicable():
    """ Expected değeri olmayan case'lerde skorlamanın None dönmesini test eder."""
    case = {"id": "c1"}
    actual = {"tool": "search_notes"}
    
    assert score_expected_field(case, actual, expected_key="expected_tool", actual_key="tool") is None