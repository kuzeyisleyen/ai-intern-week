import argparse
import json
import datetime
from pathlib import Path

from qdrant_client import QdrantClient
from fastembed import SparseTextEmbedding
from day06.embedding_client import EmbeddingClient

from day11.dense_retriever import retrieve_dense
from day11.sparse_retriever import retrieve_sparse
from day11.hybrid_retriever import retrieve_hybrid

from day11.metrics import hit_at_k, reciprocal_rank, mean_reciprocal_rank


def run_benchmark():
    parser = argparse.ArgumentParser(description="Retrieval Benchmark Runner")
    parser.add_argument("--strategy", type=str, choices=["dense", "lexical", "hybrid", "all"], required=True)
    args = parser.parse_args()

    print("İstemciler başlatılıyor...")
    qdrant_client = QdrantClient(url="http://qdrant:6333")
    embedding_client = EmbeddingClient()
    
    print("Sparse model (BM25) yükleniyor...")
    sparse_model = SparseTextEmbedding(model_name="Qdrant/bm25")

    dataset_path = Path("data/retrieval_eval.json") 
    if not dataset_path.exists():
        dataset_path = Path("day11/data/retrieval_eval.json")
        
    with open(dataset_path, "r", encoding="utf-8") as f:
        eval_dataset = json.load(f)

    print(f"\nToplam {len(eval_dataset)} sorgu yüklendi.")

    # Çalıştırılacak stratejiler
    strategies_to_run = ["dense", "lexical", "hybrid"] if args.strategy == "all" else [args.strategy]
    
    output_queries = []
    report_strategies = {}
    report_query_types = {}

    def calculate_aggregates(scores_dict):
        if not scores_dict["mrr"]:
            return {"hit_at_1": 0.0, "hit_at_3": 0.0, "mrr": 0.0}
        return {
            "hit_at_1": round(sum(scores_dict["hit_1"]) / len(scores_dict["hit_1"]), 4),
            "hit_at_3": round(sum(scores_dict["hit_3"]) / len(scores_dict["hit_3"]), 4),
            "mrr": round(mean_reciprocal_rank(scores_dict["mrr"]), 4)
        }

    # Değerlendirme
    for current_strategy in strategies_to_run:
        print(f"--- {current_strategy.upper()} Stratejisi Test Ediliyor ---")
        overall_scores = {"hit_1": [], "hit_3": [], "mrr": []}
        type_scores = {}

        for item in eval_dataset:
            q_id = item["id"]
            q_text = item["question"]
            q_type = item.get("query_type", "unknown")
            expected_source = item.get("expected_source")
            is_answerable = item.get("answerable", True)           

            # Arama
            if current_strategy == "dense":
                results = retrieve_dense(query=q_text, qdrant_client=qdrant_client, embedding_client=embedding_client, top_k=5, collection_name="rag_chunks_hybrid")
            elif current_strategy == "lexical":
                results = retrieve_sparse(query=q_text, qdrant_client=qdrant_client, sparse_model=sparse_model, top_k=5, collection_name="rag_chunks_hybrid")
            elif current_strategy == "hybrid":
                results = retrieve_hybrid(query=q_text, qdrant_client=qdrant_client, embedding_client=embedding_client, sparse_model=sparse_model, top_k=5, collection_name="rag_chunks_hybrid")
            
            # Metrik Hesaplamaları
            retrieved_sources = [r["source"] for r in results]
            
            if is_answerable and expected_source:
                rr = reciprocal_rank(retrieved_sources, expected_source)
                h1 = hit_at_k(retrieved_sources, expected_source, k=1)
                h3 = hit_at_k(retrieved_sources, expected_source, k=3)
                
                expected_rank = None
                unique_sources = list(dict.fromkeys(retrieved_sources))
                if expected_source in unique_sources:
                    expected_rank = unique_sources.index(expected_source) + 1
            else:
                # Unanswerable sorular için metrikleri boş geçiyoruz
                rr, h1, h3, expected_rank = None, None, None, None

            if is_answerable:
                if q_type not in type_scores:
                    type_scores[q_type] = {"hit_1": [], "hit_3": [], "mrr": []}

                # Havuzları Doldur
                overall_scores["mrr"].append(rr)
                overall_scores["hit_1"].append(h1)
                overall_scores["hit_3"].append(h3)

                type_scores[q_type]["mrr"].append(rr)
                type_scores[q_type]["hit_1"].append(h1)
                type_scores[q_type]["hit_3"].append(h3)

            # Çıktı listesine ekle
            output_queries.append({
                "query_id": q_id,
                "query_type": q_type,
                "question": q_text,
                "expected_source": expected_source,
                "strategy": current_strategy,
                "retrieved_sources": retrieved_sources,
                "scores": [r["score"] for r in results],
                "expected_rank": expected_rank,
                "hit_at_1": h1,
                "hit_at_3": h3,
                "reciprocal_rank": round(rr, 4) if rr is not None else None,
                "note": "Unanswerable query; excluded from ranking metrics" if not is_answerable else None
            })

        # Strateji bazlı kümeleri kaydet
        report_strategies[current_strategy] = calculate_aggregates(overall_scores)
        report_query_types[current_strategy] = {q_type: calculate_aggregates(scores) for q_type, scores in type_scores.items()}

    # JSON Raporunu Oluştur
    report = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "dataset_size": len(eval_dataset),
        "dense_model": "embeddinggemma",
        "sparse_model": "Qdrant/bm25",
        "chunk_config": {
            "chunk_size": 600,
            "overlap": 100
        },
        "strategies": report_strategies,
        "query_type_metrics": report_query_types if args.strategy == "all" else report_query_types[args.strategy],
        "queries": output_queries
    }

    # Dosyaya Yazma
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    filename = "day11-retrieval-benchmark-all.json" if args.strategy == "all" else f"day11-retrieval-benchmark_{args.strategy}.json"
    output_file = output_dir / filename

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Konsol Çıktısı
    print(f"\nBenchmark tamamlandı! Sonuçlar {output_file} dosyasına kaydedildi.")
    if args.strategy != "all":
        print(f"[{args.strategy.upper()}] Hit@1: {report_strategies[args.strategy]['hit_at_1']} | "
              f"Hit@3: {report_strategies[args.strategy]['hit_at_3']} | "
              f"MRR: {report_strategies[args.strategy]['mrr']}")
    else:
        for strat, metrics in report_strategies.items():
            print(f"[{strat.upper()}] Hit@1: {metrics['hit_at_1']} | Hit@3: {metrics['hit_at_3']} | MRR: {metrics['mrr']}")

if __name__ == "__main__":
    run_benchmark()