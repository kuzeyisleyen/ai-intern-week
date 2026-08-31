from typing import TypedDict

from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import SparseTextEmbedding

from day06.embedding_client import EmbeddingClient


class RetrievalResult(TypedDict):
    source: str
    chunk_id: str
    score: float
    rank: int


def retrieve_hybrid(
    query: str,
    *,
    qdrant_client: QdrantClient,
    embedding_client: EmbeddingClient,
    sparse_model: SparseTextEmbedding,
    top_k: int = 5,
    collection_name: str = "rag_chunks_hybrid",
) -> list[RetrievalResult]:
    """
    Qdrant'ın Prefetch ve Fusion özelliklerini kullanarak
    Hybrid (Dense + Sparse) arama yapar ve RRF ile harmanlar.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query boş olmayan bir string olmalıdır")

    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
        raise ValueError("top_k pozitif bir tam sayı olmalıdır")

    #Dense vektörü oluştur
    query_vector_dense = embedding_client.embed(query.strip())

    if not query_vector_dense:
        raise ValueError("EmbeddingClient boş query vector döndürdü")

    #Sparse vektörü oluştur
    sparse_generator = sparse_model.query_embed(query.strip())
    sparse_vector_data = list(sparse_generator)[0]

    query_vector_sparse = models.SparseVector(
        indices=sparse_vector_data.indices.tolist(),
        values=sparse_vector_data.values.tolist(),
    )

    # Qdrant üzerinde Hybrid arama
    response = qdrant_client.query_points(
        collection_name=collection_name,
        prefetch=[
            models.Prefetch(
                query=query_vector_dense,
                using="dense",
                limit=top_k,
            ),
            models.Prefetch(
                query=query_vector_sparse,
                using="sparse",
                limit=top_k,
            ),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=top_k,
        with_payload=True,
    )

    # Sonuçları benchmark uygun normalize etme
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