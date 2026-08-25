import json
from day06.embedding_client import EmbeddingClient
from day06.similarity import cosine_similarity

def load_and_embed_documents(filepath: str, client: EmbeddingClient) -> list[dict]:
    """
    JSON dosyasını okur, her bir dokümanın metnini embed eder ve hafızada (memory) tutar.
    """
    # TODO: Python 'open' fonksiyonu ile filepath'i aç ve json.load ile oku.
    with open(filepath,'r',encoding='utf-8') as f:
        documents = json.load(f)

    # TODO: Okuduğun JSON listesi üzerinde (for doc in documents) dön:
    #   1. client.embed() metodunu kullanarak doc["text"] verisini vektöre çevir.
    #   2. doc sözlüğünün içine "embedding" adında yeni bir anahtar ekle ve bu vektörü ata.
    # (Bu işlem bittiğinde return documents diyerek güncellenmiş listeyi geri dön),
    for doc in documents : 
        vec = client.embed(doc["text"])
        doc["embedding"] = vec
    return documents

def semantic_search(query: str, embedded_documents: list[dict], client: EmbeddingClient, top_k: int = 3) -> list[dict]:
    """
    Sorguyu alır, vektöre çevirir, tüm dokümanlarla karşılaştırır ve en yüksek skorlu top_k sonucu döner.
    """
    if top_k <= 0:
        raise ValueError("top_k değeri 0'dan büyük olmalıdır.")
    # TODO: 1. Kullanıcının aradığı metni (query) client.embed() ile vektöre çevir (query_vector)
    query_vector = client.embed(query)

    # Tüm dokümanlar için skor hesaplayıp saklayacağımız liste
    results = []

    # TODO: 2. embedded_documents listesi içinde for döngüsü ile dön:
    #   - cosine_similarity() fonksiyonuna query_vector ile döngüdeki doc["embedding"] verisini ver.
    #   - Çıkan sonucu 'score' değişkenine ata.
    #   - results listesine şu sözlüğü ekle (append): {"id": doc["id"], "text": doc["text"], "score": score}
    for doc in embedded_documents:
        score = cosine_similarity(query_vector,doc["embedding"])
        results.append({"id": doc["id"], "text": doc["text"], "score": score})

    # TODO: 3. results listesini skora göre büyükten küçüğe sırala. 
    # İpucu: results.sort(key=lambda x: x["score"], reverse=True)
    results.sort(key = lambda x:x["score"],reverse=True)
    
    # TODO: 4. Sıralanmış listenin sadece ilk 'top_k' kadarını geri dön.
    return results[:top_k]