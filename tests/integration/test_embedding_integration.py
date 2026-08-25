import pytest
from day06.embedding_client import EmbeddingClient

@pytest.mark.integration
def test_embed_returns_valid_vector():
    """Client'ın geçerli bir float listesi (vektör) döndürdüğünü test eder."""
    client = EmbeddingClient()
    text = "Docker container içindeki veriyi kalıcı tutmak istiyorum."
    
    # TODO: client.embed() metodunu kullanarak text'i vektöre çevir
    vector = client.embed(text)
    
    # TODO: vector'ün bir liste (list) olduğunu assert ile doğrula
    # TODO: vector'ün boş olmadığını (uzunluğunun 0'dan büyük olduğunu) assert ile doğrula
    # TODO: Listenin tüm elemanlarının float (veya int) tipinde olduğunu assert ile doğrula
    assert isinstance(vector,list)
    assert len(vector) > 0
    assert all(isinstance(x,(int,float)) for x in vector)

@pytest.mark.integration
def test_embed_determinism():
    """Aynı metnin her zaman aynı vektörü ürettiğini (determinizm) test eder."""
    client = EmbeddingClient()
    text = "Kalıcılık önemlidir."
    
    # TODO: Aynı metni iki kere embed et (vector1 ve vector2 değişkenlerine ata)
    vector1 = client.embed(text)
    vector2 = client.embed(text)
    
    # TODO: vector1 ve vector2'nin birbirine eşit olduğunu assert ile doğrula

    assert len(vector1) == len(vector2)
    assert vector1 == vector2

@pytest.mark.integration
def test_embed_different_texts_same_dimension():
    """Farklı uzunluktaki metinlerin aynı boyutta (dimension) vektör ürettiğini test eder."""
    client = EmbeddingClient()
    
    text_short = "Kısa."
    text_long = "Bu çok daha uzun bir cümle, hatta içinde virgül bile var!"
    
    # TODO: İki metni de embed et
    vector_short = client.embed(vector_short)
    vector_long = client.embed(vector_long)
    
    # TODO: İki vektörün uzunluklarının (len) birbirine eşit olduğunu assert ile doğrula
    assert len(vector_short) ==len(vector_long)
    assert len(vector_short) >0