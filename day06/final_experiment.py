import os
import json
from day06.embedding_client import EmbeddingClient
from day06.semantic_search import load_and_embed_documents, semantic_search

def keyword_score(query: str, text: str) -> int:
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    return len(query_words & text_words)

def run_experiment():
    print("Sistem başlatılıyor...")
    client = EmbeddingClient()
    
    # 1. Dokümanları Yükle
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data", "documents.json")
    embedded_docs = load_and_embed_documents(data_path, client)

    # KEYWORD VS SEMANTIC BÖLÜMÜ
    print("\n--- KEYWORD SEARCH DENEYİ ---")
    query_exact = "pytest komutu nedir?"
    print(f"Sorgu: {query_exact}")
    
    # TODO: embedded_docs içinde for döngüsü ile dön.
    # Her bir doc için keyword_score'u hesapla.
    # Eğer skor 0'dan büyükse ekrana skoru ve metni yazdır.
    
    for doc in embedded_docs:
        skore = keyword_score(query_exact,doc["text"])
        if skore > 0 :
            print(f"[Score: {skore}] {doc['text']}")
    

    # TOP-K DENEYİ VE JSON ÇIKTISI BÖLÜMÜ 
    print("\n--- TOP-K DENEYİ ---")
    
    # Rapor şablonu
    report = {
        "embedding_model": client.model,
        "embedding_dimension": len(embedded_docs[0]["embedding"]),
        "experiments": []
    }

    test_query = "Container silinince verim kaybolmasın."
    k_values = [1, 3, 5]
    
    for k in k_values:
        # TODO: semantic_search fonksiyonunu kullanarak 'test_query'yi arat.
        results = semantic_search(test_query, embedded_docs, client, top_k=k)
        
        # Sonucu rapora ekliyoruz
        experiment_data = {
            "query": test_query,
            "top_k": k,
            "results": results
        }
        report["experiments"].append(experiment_data)
        print(f"Top-K = {k} testi tamamlandı.")

    # 2. JSON Çıktısını Kaydetme
    # Projenin ana dizinindeki (day06'nın bir üstü) output klasörü
    output_dir = os.path.join(os.path.dirname(current_dir), "output")
    os.makedirs(output_dir, exist_ok=True) # Klasör yoksa oluştur
    
    output_file = os.path.join(output_dir, "day06-semantic-search.json")
    
    # TODO: 'report' değişkenini JSON formatında output_file yoluna kaydet.
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    

    print(f"\nDeney tamamlandı! Çıktı şuraya kaydedildi: {output_file}")

if __name__ == "__main__":
    run_experiment()