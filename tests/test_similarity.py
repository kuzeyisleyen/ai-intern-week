import pytest
import math
from day06.similarity import cosine_similarity

def test_cosine_same_vector():
    """Aynı vektörlerin benzerliği 1.0 olmalıdır."""
    assert math.isclose(cosine_similarity([1.0, 0.0], [1.0, 0.0]), 1.0)

def test_cosine_orthogonal_vector():
    """Dik (alakasız) vektörlerin benzerliği 0.0 olmalıdır."""
    assert math.isclose(cosine_similarity([1.0, 0.0], [0.0, 1.0]), 0.0)

def test_cosine_dimension_mismatch():
    """Farklı boyuttaki vektörler karşılaştırıldığında program kontrollü hata vermelidir."""
    with pytest.raises(ValueError):
        cosine_similarity([1.0, 2.0], [1.0, 2.0, 3.0])

def test_cosine_empty_vector():
    """Boş vektör geldiğinde program kontrollü hata vermelidir."""
    with pytest.raises(ValueError):
        cosine_similarity([], [])