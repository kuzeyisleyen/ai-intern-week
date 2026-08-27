import json
from dataclasses import asdict
from pathlib import Path

from day08.retriever import create_default_retriever
from day09.nodes import rewrite_query


OUTPUT_PATH = Path("output/day09-rewrite-experiment.json")
VALID_ASSESSMENTS = {"iyileştirdi", "değiştirmedi", "kötüleştirdi"}


def summarize_chunks(chunks: list) -> list[dict]:
    return [asdict(chunk) for chunk in chunks]


def ask_assessment() -> str:
    while True:
        assessment = input(
            "Sonuç (iyileştirdi / değiştirmedi / kötüleştirdi): "
        ).strip().lower()
        if assessment in VALID_ASSESSMENTS:
            return assessment
        print("Lütfen üç geçerli değerlendirmeden birini yaz.")


def run_experiment(queries: list[str]) -> list[dict]:
    retriever = create_default_retriever()
    experiment_results = []

    for index, original_query in enumerate(queries, 1):
        print(f"\n{'=' * 50}\nDENEY {index}")
        print(f"Original query: {original_query}")

        original_top_3 = retriever.retrieve(original_query, top_k=3)
        for chunk in original_top_3:
            print(f"  {chunk.chunk_id}: {chunk.score:.4f} - {chunk.source}")

        rewritten_query = rewrite_query(original_query)
        print(f"Rewritten query: {rewritten_query}")

        rewritten_top_3 = retriever.retrieve(rewritten_query, top_k=3)
        for chunk in rewritten_top_3:
            print(f"  {chunk.chunk_id}: {chunk.score:.4f} - {chunk.source}")

        assessment = ask_assessment()
        experiment_results.append(
            {
                "original_query": original_query,
                "original_top_3": summarize_chunks(original_top_3),
                "rewritten_query": rewritten_query,
                "rewritten_top_3": summarize_chunks(rewritten_top_3),
                "assessment": assessment,
            }
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(experiment_results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nDeney kaydı: {OUTPUT_PATH}")
    return experiment_results


if __name__ == "__main__":
    run_experiment(
        [
            "Container silindiğinde dosyalarımın kaybolmasını nasıl engellerim?",
            "İki konteynerin birbiriyle iletişim kurmasını nasıl sağlarım?",
            "Docker imaj boyutunu küçültmek için ne yapmalıyım?",
        ]
    )
