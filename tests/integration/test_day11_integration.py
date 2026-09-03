from pydoc import doc

import pytest
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import SparseTextEmbedding
from day06.embedding_client import EmbeddingClient
from day11.sparse_retriever import retrieve_sparse
from day11.hybrid_retriever import retrieve_hybrid


@pytest.fixture(scope="module")
def test_env():
    client = QdrantClient(url="http://qdrant:6333")
    embed_client = EmbeddingClient()
    sparse_model = SparseTextEmbedding(model_name="Qdrant/bm25")
    col_name = "test_integration_collection"

    docs = [
        {"id": 1, "source": "doc-a.md", "text": "MAX_REWRITES limits query rewriting"},
        {"id": 2, "source": "doc-b.md", "text": "containers use volumes for persistence"},
        {"id": 3, "source": "doc-c.md", "text": "agent retries retrieval queries"}
    ]

    # Vektör boyutunu dinamik olarak modelden öğren
    sample_vector = embed_client.embed(docs[0]["text"])
    vector_size = len(sample_vector)

    if client.collection_exists(col_name):
        client.delete_collection(col_name)

    client.create_collection(
        collection_name=col_name,
        vectors_config={"dense": models.VectorParams(size=vector_size, distance=models.Distance.COSINE)},
        #Modifier.IDF eklendi
        sparse_vectors_config={"sparse": models.SparseVectorParams(modifier=models.Modifier.IDF)}
    )

    points = []
    for doc in docs:
        dense_vec = embed_client.embed(doc["text"])
        sparse_gen = list(sparse_model.embed(doc["text"]))[0]
        points.append( models.PointStruct(
                id=doc["id"],
                payload={"source": doc["source"], "chunk_id": f"chunk-{doc['id']}"},
                vector={
                    "dense": dense_vec,
                    "sparse": models.SparseVector(
                        indices=sparse_gen.indices.tolist(),
                        values=sparse_gen.values.tolist()
                    )
                }
            )
        )
    client.upsert(collection_name=col_name, points=points)
    
    yield client, embed_client, sparse_model, col_name
    client.delete_collection(col_name)

@pytest.mark.integration
def test_sparse_retrieval_contract(test_env):
    client, _, sparse_model, col_name = test_env
    
    results = retrieve_sparse("volumes", qdrant_client=client, sparse_model=sparse_model, top_k=2, collection_name=col_name)
    
    assert isinstance(results, list)
    assert len(results) > 0
    # Payload korunumunu ve kontrat yapısını doğrula
    assert "source" in results[0]
    assert "chunk_id" in results[0]
    assert "score" in results[0]
    assert "rank" in results[0]

@pytest.mark.integration
def test_hybrid_retrieval_ranking_and_contract(test_env):
    client, embed_client, sparse_model, col_name = test_env
    
    # Full Smoke Test: Gerçek modeller üzerinden Qdrant'a karmaşık arama
    results = retrieve_hybrid("MAX_REWRITES", qdrant_client=client, embedding_client=embed_client, sparse_model=sparse_model, top_k=3, collection_name=col_name)
    
    assert len(results) > 0
    # Sayısal skor (exact numeric) yerine sıralamaya ve ID'ye odaklan
    assert results[0]["source"] == "doc-a.md"
    assert results[0]["rank"] == 1