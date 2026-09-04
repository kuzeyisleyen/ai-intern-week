def check_trajectory_strict(expected: list[str], actual: list[str]) -> bool:
    """
    Trajectory adımlarının birebir (uzunluğuyla ve sırasıyla) aynı olduğunu kontrol eder.
    """
    if len(expected) != len(actual):
        return False

    for i in range(len(expected)):
        if expected[i] != actual[i]:
            return False

    return True

def check_trajectory_ordered(expected_core: list[str], actual: list[str]) -> bool:
    """
    Beklenen adımların, actual içinde verilen sırayla (araya başka adımlar girse de)
    bulunup bulunmadığını kontrol eder.
    """
    expected_idx = 0
    for node in actual:
        if expected_idx < len(expected_core) and node == expected_core[expected_idx]:
            expected_idx += 1
            if expected_idx == len(expected_core):
                return True
    return False


def score_trajectory(case: dict, actual: dict) -> bool | None:
    """
    Vakadaki expectation ayarlarına göre doğru trajectory kontrolünü çalıştırır.
    metrics.py formatına uyumludur.
    """
    actual_trajectory = actual.get("trajectory", [])

    if "strict_trajectory" in case:
        expected_strict = case["strict_trajectory"]
        return check_trajectory_strict(expected_strict, actual_trajectory)

    if "allowed_trajectory" in case:
        expected_allowed = case["allowed_trajectory"]
        return check_trajectory_ordered(expected_allowed, actual_trajectory)
  
    return None