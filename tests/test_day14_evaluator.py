from day14.evaluator import evaluate_trajectory

def test_ordered_subsequence_match():
    """ 'ordered/allowed trajectory' mantığını test eder."""
    expected = ["classify_query", "retrieve", "generate"]
    
    # 1. Birebir aynı (Strict match)
    assert evaluate_trajectory(expected, ["classify_query", "retrieve", "generate"]) is True
    
    # 2. Araya opsiyonel kalite kontrol düğümü girmiş (Ordered subsequence)
    assert evaluate_trajectory(expected, ["classify_query", "retrieve", "quality_check", "generate"]) is True
    
    # 3. Beklenen bir düğüm eksik
    assert evaluate_trajectory(expected, ["classify_query", "generate"]) is False
    
    # 4. Sıralama yanlış
    assert evaluate_trajectory(expected, ["classify_query", "generate", "retrieve"]) is False