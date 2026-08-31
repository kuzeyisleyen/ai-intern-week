from typing import TypedDict
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import SparseTextEmbedding

class RetrievalResult(TypedDict):
    source: str
    chunk_id: str
    score: float
    rank: int

def retrieve_sparse(
    query: str,
    *,
    qdrant_client: QdrantClient,
    sparse_model: SparseTextEmbedding,
    top_k: int = 5,
    collection_name: str = "rag_chunks_hybrid",
) -> list[RetrievalResult]:
    """
    Qdrant üzerinde kelime frekansına (BM25) dayalı Lexical arama yapar.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query boş olamaz.")

    # FastEmbed ile sparse vektörü oluştur
    sparse_generator = sparse_model.query_embed(query)
    sparse_vector_data = list(sparse_generator)[0]

    query_vector = models.SparseVector(
        indices=sparse_vector_data.indices.tolist(),
        values=sparse_vector_data.values.tolist(),
    )

    # Qdranta using=sparse parametresiyle sor
    response = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        using="sparse", 
        limit=top_k,
        with_payload=True,
    )

    normalized_results: list[RetrievalResult] = []

    for rank, hit in enumerate(response.points, start=1):
        payload = hit.payload or {}
        
        normalized_results.append(
            {
                "source": str(payload.get("source")),
                "chunk_id": str(payload.get("chunk_id")),
                "score": float(hit.score),
                "rank": rank,
            }
        )

    return normalized_results