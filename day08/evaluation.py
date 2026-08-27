import json
from pathlib import Path
from day08.retriever import create_default_retriever
from day08.chunker import ChunkConfig 

def hit_at_k(expected_source: str, retrieved_sources: list[str], k: int) -> bool:
    """Beklenen kaynağın, gelen ilk k kaynak içinde olup olmadığını kontrol eder."""
    top_k_sources = retrieved_sources[:k]
    return expected_source in top_k_sources

def evaluate_retrieval(
    chunk_size: int = 600,
    overlap: int = 100,
    top_k_value: int = 3,
    data_path: str = "day08/data/eval_questions.json"
):
    output_path = f"output/day08-eval-c{chunk_size}-k{top_k_value}.json"
    # 1. Dataset'i Yükle
    path = Path(data_path)
    if not path.exists():
        print(f"HATA: {data_path} bulunamadı!")
        return

    with open(path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # 2. Retriever'ı Başlat
    retriever = create_default_retriever()

    real_settings = ChunkConfig(chunk_size=chunk_size, overlap=overlap)    
    # Çıktı klasörünü oluştur (yoksa)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    hit_1_count = 0
    hit_3_count = 0
    answerable_count = 0
    unanswerable_count = 0 
    
    results_log = []
    top_k_value = 3

    print("RETRIEVAL EVALUATION (Hit@k Metrikleri)")
    
    for item in dataset:
        if not item.get("answerable"):
            unanswerable_count += 1
            continue
            
        answerable_count += 1
        question = item["question"]
        expected = item["expected_source"]
        
        # 3. Sorguyu Çalıştır
        chunks = retriever.retrieve(question, top_k=top_k_value)       
        retrieved_sources = [c.source for c in chunks]
        scores = [round(c.score, 4) for c in chunks]
        
        # 4. Hit@k Kontrolleri 
        hit_1 = hit_at_k(expected, retrieved_sources, 1)
        hit_3 = hit_at_k(expected, retrieved_sources, 3)
        
        if hit_1: hit_1_count += 1
        if hit_3: hit_3_count += 1
            
        print(f"Soru: {question} | Hit@1: {'True' if hit_1 else 'False'}")
        
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
            "chunk_size": real_settings.chunk_size, 
            "overlap": real_settings.overlap,
            "dataset_stats": {
                "total_questions": len(dataset),
                "answerable": answerable_count,
                "unanswerable": unanswerable_count
            },
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
    print("GENEL SONUÇLAR ")
    print(f"Toplam Soru: {len(dataset)} ({answerable_count} Cevaplanabilir, {unanswerable_count} Cevaplanamaz)")
    print(f"Hit@1 Oranı: % { (hit_1_count / answerable_count) * 100 :.2f}")
    print(f"Hit@3 Oranı: % { (hit_3_count / answerable_count) * 100 :.2f}")
    print("="*45)
    print(f" Rapor başarıyla '{output_path}' konumuna kaydedildi.")

if __name__ == "__main__":
    chunk_sizes = [300, 600, 1000]
    top_ks = [1, 3, 5]
    
    print("Toplu değerlendirme başlatılıyor...")
    
    for c in chunk_sizes:
        for k in top_ks:
            print(f"\n--- Deney: Chunk Size = {c} | Top K = {k} ---")
            
            overlap_val = 50 
            
            evaluate_retrieval(
                chunk_size=c, 
                overlap=overlap_val, 
                top_k_value=k
            )
            
    print("\nTüm deneyler tamamlandı")