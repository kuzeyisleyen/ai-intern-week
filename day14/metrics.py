from __future__ import annotations

from day14 import trajectory

ROUTES = (
    "smalltalk",
    "knowledge",
    "tool",
)
BOOLEAN_SCORE_KEYS = (
    "route_correct",
    "tool_correct",
    "provider_correct",
    "approval_correct",
    "terminal_correct",
    "trajectory_correct",
)

def score_expected_field(
    case: dict,
    actual: dict,
    *,
    expected_key: str,
    actual_key: str,
) -> bool | None:
    """Tek bir expected/actual alanını karşılaştırır.

    Beklenti JSON kaydında yoksa veya değeri ``null`` ise bu metric ilgili
    vakaya uygulanmaz ve ``None`` döner.
    """
    if expected_key not in case:
        return None
    if case[expected_key] is None:
        return None
    if actual.get(actual_key) == case[expected_key]:
        return True
    return False

def score_route(case: dict, actual: dict) -> bool | None:
    """Route seçiminin doğruluğunu skorlar."""
    return score_expected_field(case, actual, expected_key="expected_route", actual_key="route")

def score_tool(case: dict, actual: dict) -> bool | None:
    """Tool seçiminin doğruluğunu skorlar."""
    return score_expected_field(case, actual, expected_key="expected_tool", actual_key="tool")

def score_provider(case: dict, actual: dict) -> bool | None:
    """Native/MCP provider eşleşmesini skorlar."""
    return score_expected_field(case, actual, expected_key="expected_tool_provider", actual_key="provider")

def score_approval(case: dict, actual: dict) -> bool | None:
    return score_expected_field(
        case,
        actual,
        expected_key="approval_required",
        actual_key="approval_required",
    )

def score_terminal(case: dict, actual: dict) -> bool | None:
    """Business terminal state sonucunu skorlar."""
    return score_expected_field(case, actual, expected_key="expected_terminal_status", actual_key="terminal_status")

def score_case(case: dict, actual: dict) -> dict[str, bool | None]:
    """Bir vaka için metrics.py tarafından sahiplenilen skorları üretir."""
    return {
         "route_correct": score_route(case, actual),
         "tool_correct": score_tool(case, actual),
         "provider_correct": score_provider(case, actual),
         "approval_correct": score_approval(case, actual),
         "terminal_correct": score_terminal(case, actual),
         "trajectory_correct": trajectory.score_trajectory(case, actual),
     }

def aggregate_boolean_scores(values: list[bool | None]) -> dict:
    """Boolean/None skor listesini correct, denominator ve accuracy'ye çevirir."""
    scored_values = []
    
    # None değerlerini yoksay ve sadece bool olanları listeye ekle
    for value in values:
        if value is not None:
            scored_values.append(value)
            
    denominator = len(scored_values)
    
    # Doğru (True) olanların sayısını bul
    correct = 0
    for value in scored_values:
        if value is True:
            correct += 1
            
    # Sıfıra bölme hatasını engelle
    if denominator == 0:
        accuracy = None
    else:
        accuracy = correct / denominator
        
    return {
        "correct": correct,
        "denominator": denominator,
        "accuracy": accuracy,
    }
    
def aggregate_score(
    case_results: list[dict],
    score_key: str,
) -> dict:
    """Per-case result listesinden tek bir metric'i aggregate eder."""
    values = []
    
    for result in case_results:
        # Sonuç içerisindeki scores sözlüğünü al, yoksa boş sözlük dön
        scores = result.get("scores", {})
        
        # İstenilen score_key değerini al
        score_value = scores.get(score_key)
        
        # Gelen değerin geçerli bir tipte (True, False, None) olduğunu kontrol et
        if score_value not in (True, False, None):
            raise ValueError(f"Geçersiz skor değeri bulundu: {score_value}")
            
        values.append(score_value)
        
    return aggregate_boolean_scores(values)

def _index_results_by_id(case_results: list[dict]) -> dict[str, dict]:
    """Per-case sonuçlarını benzersiz vaka ID'sine göre indeksler."""
    indexed_results = {}
    
    for result in case_results:
        result_id = result.get("id")
        
        # ID'nin boş olmayan bir string olduğunu doğrula
        if not isinstance(result_id, str) or not result_id.strip():
            raise ValueError(f"Geçersiz veya boş result id bulundu: {result_id}")
            
        # Aynı ID'den birden fazla varsa hata fırlat
        if result_id in indexed_results:
            raise ValueError(f"Tekrar eden result id bulundu: {result_id}")
            
        indexed_results[result_id] = result
        
    return indexed_results

def calculate_route_accuracy(case_results: list[dict]) -> dict:
    """Global route accuracy sonucunu hesaplar."""
    return aggregate_score(case_results, "route_correct")

def calculate_per_class_route_accuracy(
    cases: list[dict],
    case_results: list[dict],
) -> dict[str, dict]:
    """Smalltalk, knowledge ve tool için ayrı route accuracy hesaplar."""
    indexed_results = _index_results_by_id(case_results)
    
    # Sınıf bazlı skorları tutmak için boş sözlük oluştur
    class_scores = {route: [] for route in ROUTES}
    
    for case in cases:
        expected_route = case.get("expected_route")
        
        # Challenge vakalarını (None olanları) atla
        if expected_route is None:
            continue
            
        # Beklenen route geçerli bir route değilse atla veya hata fırlat
        if expected_route in class_scores:
            case_id = case["id"]
            result = indexed_results.get(case_id)
            
            if result is not None:
                route_score = result.get("scores", {}).get("route_correct")
                class_scores[expected_route].append(route_score)
                
    # Her sınıf için toplu (aggregate) hesaplama yap
    per_class_accuracy = {}
    for route, scores in class_scores.items():
        per_class_accuracy[route] = aggregate_boolean_scores(scores)
        
    return per_class_accuracy

def build_confusion_matrix(
    cases: list[dict],
    case_results: list[dict],
) -> dict[str, dict[str, int]]:
    """Expected route satırları ve predicted route sütunlarıyla matrix üretir."""
    indexed_results = _index_results_by_id(case_results)
    
    # Tüm hücreleri sıfır olan 3x3 matrisi oluştur
    matrix = {
        row_route: {col_route: 0 for col_route in ROUTES}
        for row_route in ROUTES
    }
    
    for case in cases:
        expected_route = case.get("expected_route")
        
        # Challenge vakalarını atla
        if expected_route is None:
            continue
            
        case_id = case["id"]
        result = indexed_results.get(case_id)
        
        if result is None:
            continue
            
        predicted_route = result.get("actual", {}).get("route")
        
        # Beklenen veya tahmin edilen rotalar tanımsızsa kontrollü hata fırlat
        if expected_route not in ROUTES:
            raise ValueError(f"Bilinmeyen expected_route: {expected_route}")
            
        if predicted_route not in ROUTES:
            raise ValueError(f"Bilinmeyen predicted_route: {predicted_route}")
            
        # Matristeki ilgili hücreyi 1 artır
        matrix[expected_route][predicted_route] += 1
        
    return matrix

def calculate_retrieval_metrics(
    cases: list[dict],
    case_results: list[dict],
) -> dict:
    """Expected source bulunan vakalar için Day 11 retrieval metric'lerini çalıştırır."""
    
    # metrics_2.py dosyasındaki fonksiyonları import ediyoruz
    from day11.metrics import hit_at_k, reciprocal_rank, mean_reciprocal_rank

    indexed_results = _index_results_by_id(case_results)
    
    hit_1_scores = []
    hit_3_scores = []
    mrr_scores = []
    
    for case in cases:
        expected_source = case.get("expected_source")
        
        # Yalnızca expected_source olanları işleme al
        if expected_source is None:
            continue
            
        case_id = case["id"]
        result = indexed_results.get(case_id)
        if result is None:
            continue
            
        # Actual retrieved source listesini al
        retrieved_sources = result.get("actual", {}).get("retrieved_sources", [])

        hit_1 = hit_at_k(retrieved_sources, expected_source, 1)
        hit_3 = hit_at_k(retrieved_sources, expected_source, 3)
        mrr = reciprocal_rank(retrieved_sources, expected_source)
        
        hit_1_scores.append(hit_1)
        hit_3_scores.append(hit_3)
        mrr_scores.append(mrr)
        
    denominator = len(hit_1_scores)
    
    if denominator == 0:
        return {
            "denominator": 0,
            "hit_at_1": None,
            "hit_at_3": None,
            "mrr": None,
        }
        
    return {
        "denominator": denominator,
        "hit_at_1": sum(hit_1_scores) / denominator,
        "hit_at_3": sum(hit_3_scores) / denominator,
        "mrr": mean_reciprocal_rank(mrr_scores),
    }

def aggregate_metrics(
    cases: list[dict],
    case_results: list[dict],
) -> dict:
    """Kılavuzdaki system-level metric özetini oluşturur."""
    
    # Tüm metric türleri için toplu sonuçları oluştur
    return {
        "case_count": len(cases),
        "route_accuracy": calculate_route_accuracy(case_results),
        "per_class_route_accuracy": calculate_per_class_route_accuracy(cases, case_results),
        "confusion_matrix": build_confusion_matrix(cases, case_results),
        "tool_accuracy": aggregate_score(case_results, "tool_correct"),
        "provider_accuracy": aggregate_score(case_results, "provider_correct"),
        "approval_accuracy": aggregate_score(case_results, "approval_correct"),
        "terminal_accuracy": aggregate_score(case_results, "terminal_correct"),
        "trajectory_accuracy": aggregate_score(case_results, "trajectory_correct"),
        "retrieval": calculate_retrieval_metrics(cases, case_results),
    }

__all__ = [
    "BOOLEAN_SCORE_KEYS",
    "ROUTES",
    "aggregate_boolean_scores",
    "aggregate_metrics",
    "aggregate_score",
    "build_confusion_matrix",
    "calculate_per_class_route_accuracy",
    "calculate_retrieval_metrics",
    "calculate_route_accuracy",
    "score_approval",
    "score_case",
    "score_expected_field",
    "score_provider",
    "score_route",
    "score_terminal",
    "score_tool",
]