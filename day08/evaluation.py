import json
from pathlib import Path
from day08.retriever import create_default_retriever

def evaluate_retrieval(
    data_path: str = "day08/data/eval_questions.json", 
    output_path: str = "output/day08-rag-retrieval-eval.json"
):
    # 1. Dataset'i Yükle
    path = Path(data_path)
    if not path.exists():
        print(f"HATA: {data_path} bulunamadı!")
        return

    with open(path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # 2. Retriever'ı Başlat
    retriever = create_default_retriever()
    
    # Çıktı klasörünü oluştur (yoksa)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    hit_1_count = 0
    hit_3_count = 0
    answerable_count = 0
    
    # JSON için toplayacağımız sonuç listesi
    results_log = []

    print("=== RETRIEVAL EVALUATION (Hit@k Metrikleri) ===")
    
    top_k_value = 3

    for item in dataset:
        if not item["answerable"]:
            continue
            
        answerable_count += 1
        question = item["question"]
        expected = item["expected_source"]
        
        # 3. Sorguyu Çalıştır
        chunks = retriever.retrieve(question, top_k=top_k_value)
        retrieved_sources = [c.source for c in chunks]
        scores = [round(c.score, 4) for c in chunks]
        
        # 4. Hit@k Kontrolleri
        hit_1 = len(retrieved_sources) > 0 and retrieved_sources[0] == expected
        hit_3 = expected in retrieved_sources
        
        if hit_1: hit_1_count += 1
        if hit_3: hit_3_count += 1
            
        print(f"Soru: {question} | Hit@1: {'True' if hit_1 else 'False'}")
        
        # log kaydı
        results_log.append({
            "question": question,
            "expected_source": expected,
            "retrieved_sources": retrieved_sources,
            "scores": scores,
            "hit_at_1": hit_1,
            "hit_at_3": hit_3
        })

    # 5. JSON Yapısı
    final_output = {
        "metadata": {
            "embedding_model": retriever.config.embedding_model,
            "generation_model": "qwen3:1.7b",
            "chunk_size": 50, 
            "overlap": 10,
            "top_k": top_k_value,
            "overall_hit_at_1": round(hit_1_count / answerable_count, 2) if answerable_count else 0,
            "overall_hit_at_3": round(hit_3_count / answerable_count, 2) if answerable_count else 0
        },
        "results": results_log
    }

    # 6. JSON Dosyasına Yaz
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)

    print("\n" + "="*45)
    print("=== GENEL SONUÇLAR ===")
    print(f"Toplam Soru: {answerable_count}")
    print(f"Hit@1 Oranı: % { (hit_1_count / answerable_count) * 100 :.2f}")
    print(f"Hit@3 Oranı: % { (hit_3_count / answerable_count) * 100 :.2f}")
    print("="*45)
    print(f" Rapor başarıyla '{output_path}' konumuna kaydedildi.")

if __name__ == "__main__":
    evaluate_retrieval()