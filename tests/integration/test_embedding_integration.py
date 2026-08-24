import pytest
from day06.embedding_client import EmbeddingClient

@pytest.mark.integration
def test_embed_returns_valid_vector():
    """Client'ın geçerli bir float listesi (vektör) döndürdüğünü test eder."""
    client = EmbeddingClient()
    text = "Docker container içindeki veriyi kalıcı tutmak istiyorum."
    
    # TODO: client.embed() metodunu kullanarak text'i vektöre çevir
    vector = None
    
    # TODO: vector'ün bir liste (list) olduğunu assert ile doğrula
    # TODO: vector'ün boş olmadığını (uzunluğunun 0'dan büyük olduğunu) assert ile doğrula
    # TODO: Listenin ilk elemanının float (veya int) tipinde olduğunu assert ile doğrula


@pytest.mark.integration
def test_embed_determinism():
    """Aynı metnin her zaman aynı vektörü ürettiğini (determinizm) test eder."""
    client = EmbeddingClient()
    text = "Kalıcılık önemlidir."
    
    # TODO: Aynı metni iki kere embed et (vector1 ve vector2 değişkenlerine ata)
    vector1 = None
    vector2 = None
    
    # TODO: vector1 ve vector2'nin birbirine eşit olduğunu assert ile doğrula


@pytest.mark.integration
def test_embed_different_texts_same_dimension():
    """Farklı uzunluktaki metinlerin aynı boyutta (dimension) vektör ürettiğini test eder."""
    client = EmbeddingClient()
    
    text_short = "Kısa."
    text_long = "Bu çok daha uzun bir cümle, hatta içinde virgül bile var!"
    
    # TODO: İki metni de embed et
    vector_short = None
    vector_long = None
    
    # TODO: İki vektörün uzunluklarının (len) birbirine eşit olduğunu assert ile doğrula