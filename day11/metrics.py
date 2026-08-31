import math


def _validate_expected_source(expected_source: str) -> None:
    if not isinstance(expected_source, str) or not expected_source.strip():
        raise ValueError(
            "expected_source boş olmayan bir string olmalıdır"
        )


def _unique_sources(retrieved_sources: list[str]) -> list[str]:
    if any(
        not isinstance(source, str) or not source.strip()
        for source in retrieved_sources
    ):
        raise ValueError(
            "retrieved_sources yalnızca boş olmayan string değerler içermelidir"
        )

    return list(dict.fromkeys(retrieved_sources))


def hit_at_k(
    retrieved_sources: list[str],
    expected_source: str,
    k: int,
) -> bool:
    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k pozitif bir tam sayı olmalıdır")

    _validate_expected_source(expected_source)
    unique_sources = _unique_sources(retrieved_sources)

    return expected_source in unique_sources[:k]


def reciprocal_rank(
    retrieved_sources: list[str],
    expected_source: str,
) -> float:
    _validate_expected_source(expected_source)
    unique_sources = _unique_sources(retrieved_sources)

    try:
        rank = unique_sources.index(expected_source) + 1
    except ValueError:
        return 0.0

    return 1.0 / rank


def mean_reciprocal_rank(values: list[float]) -> float:
    if not values:
        raise ValueError(
            "MRR hesaplamak için en az bir reciprocal rank gereklidir"
        )

    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or not 0.0 <= value <= 1.0
        for value in values
    ):
        raise ValueError(
            "Reciprocal rank değerleri 0.0 ile 1.0 arasında olmalıdır"
        )

    return sum(values) / len(values)