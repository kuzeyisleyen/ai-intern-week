from typing import TypedDict

from day06.embedding_client import EmbeddingClient
from qdrant_client import QdrantClient


class RetrievalResult(TypedDict):
    source: str
    chunk_id: str
    score: float
    rank: int


def retrieve_dense(
    query: str,
    top_k: int = 5,
    *,
    qdrant_client: QdrantClient,
    embedding_client: EmbeddingClient,
    collection_name: str = "rag_chunks",
) -> list[RetrievalResult]:
    """
    Dense search yapar ve sonuçları ortak benchmark
    kontratına göre normalize eder.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query boş olmayan bir string olmalıdır")

    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
        raise ValueError("top_k pozitif bir tam sayı olmalıdır")

    query_vector = embedding_client.embed(query.strip())

    if not query_vector:
        raise ValueError("EmbeddingClient boş query vector döndürdü")

    response = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        using="dense",
        limit=top_k,
        with_payload=True,
    )

    normalized_results: list[RetrievalResult] = []

    for rank, hit in enumerate(response.points, start=1):
        payload = hit.payload or {}
        source = payload.get("source")
        chunk_id = payload.get("chunk_id")

        if not isinstance(source, str) or not source:
            raise ValueError(
                f"Qdrant sonucu geçerli source içermiyor: point_id={hit.id}"
            )

        if not isinstance(chunk_id, str) or not chunk_id:
            raise ValueError(
                f"Qdrant sonucu geçerli chunk_id içermiyor: point_id={hit.id}"
            )

        normalized_results.append(
            {
                "source": source,
                "chunk_id": chunk_id,
                "score": float(hit.score),
                "rank": rank,
            }
        )

    return normalized_results