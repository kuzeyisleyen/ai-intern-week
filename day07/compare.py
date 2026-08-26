import json
import os
from pathlib import Path
from qdrant_client import QdrantClient

# 1. Kendi client ve fonksiyonlarını import et
from day06.embedding_client import EmbeddingClient
from day06.similarity import cosine_similarity

COLLECTION_NAME = "intern_documents"
DATA_PATH = Path(__file__).parent / "data" / "documents.json"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "day07-vector-db-experiments.json"

def run_comparison():
    print("Karşılaştırma testi başlıyor...")
    embedder = EmbeddingClient()
    qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
    
    query_text = "Container silindiğinde dosyalarımın kaybolmasını nasıl engellerim?"
    top_k = 3
    query_vector = embedder.embed(query_text)

    experiments = []

    # DAY 6: IN-MEMORY SEARCH (Python List)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)
    
    memory_results = []
    
    # TODO 1: documents listesi içinde dönerek her bir doc["text"] için embedder.embed() ile vektör üret.
    # TODO 2: Ürettiğin vektör ile query_vector arasındaki benzerliği kendi cosine_similarity() fonksiyonunla hesapla.
    # TODO 3: Elde ettiğin skoru ve dokümanı memory_results listesine sözlük (dict) olarak ekle. 
    #         Örn: memory_results.append({"doc": doc, "score": score})
    
    # TODO 4: memory_results listesini skora göre büyükten küçüğe sırala ve sadece ilk 'top_k' (3) tanesini al.
    for doc in documents:
        doc_vector = embedder.embed(doc["text"])
        score = cosine_similarity(query_vector, doc_vector)
        memory_results.append({
            "doc": doc,
            "score": score
        })

    memory_results.sort(key=lambda x: x["score"], reverse=True)
    top_memory_results = memory_results[:top_k]

    memory_experiment_results = []
    for item in top_memory_results:
        memory_experiment_results.append({
            "document_id": item["doc"]["id"],
            "score": round(item["score"], 4),
            "payload": {
                "category": item["doc"]["category"],
                "text": item["doc"]["text"]
            }
        })

    memory_experiment = {
        "backend": "day6_memory",
        "query": query_text,
        "top_k": top_k,
        "filter": None,
        # TODO 5: Sıralanmış listedeki sonuçları formatlayıp 'results' listesine ekle.
        "results": memory_experiment_results 
    }
    experiments.append(memory_experiment)

    # DAY 7: QDRANT SEARCH
    # TODO 6: qdrant.query_points(...) metodunu kullanarak query_vector ile arama yap. limit=top_k olsun.
    
    qdrant_response = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )
    
    qdrant_experiment_results = []
    for point in qdrant_response.points:
        qdrant_experiment_results.append({
            "point_id": point.id, 
            "document_id": point.payload.get("document_id"),
            "score": round(point.score, 4),
            "payload": {
                "category": point.payload.get("category"),
                "text": point.payload.get("text")
            }
        })
 # TODO 7: Qdrant'tan dönen response.points üzerinde dönerek sonuçları 'results' listesine ekle.
    qdrant_experiment = {
        "backend": "day7_qdrant",
        "query": query_text,
        "top_k": top_k,
        "filter": None,
        "results": qdrant_experiment_results
    }
    experiments.append(qdrant_experiment)

    # SONUÇLARI JSON OLARAK KAYDET 
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(experiments, f, ensure_ascii=False, indent=2)
        
    print(f"Deney sonuçları başarıyla kaydedildi: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_comparison()