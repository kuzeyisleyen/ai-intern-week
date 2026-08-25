import os
from qdrant_client import QdrantClient, models
from day06.embedding_client import EmbeddingClient

COLLECTION_NAME = "intern_documents"

def test_search():
    # 1. İstemcileri Başlat
    # TODO: QdrantClient'ı başlat 
    # TODO: EmbeddingClient'ı başlat
    qdrant = QdrantClient(url = os.getenv("QDRANT_URL", "http://localhost:6333"))
    embedder = EmbeddingClient()

    query_text = "Container silindiğinde dosyalarımın kaybolmasını nasıl engellerim?"
    print(f"\nSorgu: '{query_text}'\n")
    
    # 2. Vektör Üretimi
    # TODO: query_text metnini embedding modeline göndererek vektöre (query_vector) dönüştür.
    query_vector = embedder.embed(query_text)

    # --- TEST 1: FİLTRESİZ ARAMA ---
    print("FİLTRESİZ ARAMA")
   
    response_1 = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3,
        with_payload=True
    )
    # TODO: Dönen sonuçları döngüyle yazdır. 
    for idx, result in enumerate(response_1.points, 1):
        print(f"{idx}. Skor: {result.score:.4f} | Point ID: {result.id} | Doc ID: {result.payload.get('document_id')} | Kategori: {result.payload.get('category')}")
        print(f"   Metin: {result.payload.get('text')}\n")

    # --- TEST 2: FİLTRELİ ARAMA (Metadata Filtering) ---
    print("\nTEST 2: FİLTRELİ ARAMA")
    
    # TODO: qdrant.query_points metodunu tekrar çağır. Test 1'deki parametrelere EK OLARAK:
    # - query_filter=models.Filter(must=[...]) ekle.
    response_2 = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3,
        with_payload=True,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="category",
                    match=models.MatchValue(value="docker"),
                )
            ]
        )
    )
    # TODO: Dönen filtrelenmiş sonuçları döngüyle yazdır.
    if not response_2.points:
        print("Uygun sonuç bulunamadı.\n")
    else:
        for idx, result in enumerate(response_2.points, 1):
            print(f"{idx}. Skor: {result.score:.4f} | Point ID: {result.id} | Doc ID: {result.payload.get('document_id')} | Kategori: {result.payload.get('category')}")
            print(f"   Metin: {result.payload.get('text')}\n")

if __name__ == "__main__":
    test_search()