from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, ScoredPoint

from day06.embedding_client import EmbeddingClient


SUPPORTED_FILTER_FIELDS = {"topic", "source"}


class RetrievalError(RuntimeError):
    """Retrieval hattı çalıştırılamadığında kullanılır."""

@dataclass(frozen=True)
class RetrieverConfig:
    """Retriever'ın ingestion ayarlarıyla uyumlu olması gereken değerleri."""

    collection_name: str = "rag_chunks"
    embedding_model: str = "embeddinggemma"
    qdrant_url: str = "http://qdrant:6333"
    default_top_k: int = 3


@dataclass(frozen=True)
class RetrievedChunk:

    chunk_id: str
    source: str
    document_id: str
    chunk_index: int
    topic: str
    text: str
    score: float


def validate_retrieval_request(query: str, top_k: int) -> str:

    if not isinstance(query,str):
        raise TypeError("query değeri string olmalıdır.")

    cleaned_query = query.strip()

    if not cleaned_query:
        raise ValueError("query boş veya boşluklu olamaz")
    if isinstance(top_k,bool) or not isinstance(top_k,int):
        raise TypeError("Top_k bool olmayan bir tam sayı olmalıdır.")
    if top_k <= 0 :
        raise ValueError("top_k 0 dan küçük olamaz.")
    
    return cleaned_query
    

def build_qdrant_filter(
    filters: Mapping[str, str] | None,
) -> Filter | None:

    if filters is None : 
        return None
    
    if not isinstance(filters,Mapping):
        raise TypeError("filters parametresi dict/Mapping olmalıdır ")
    conditions = []
    for key,value in filters.items():
        if key not in SUPPORTED_FILTER_FIELDS:
            raise ValueError(f"Desteklenmeyen filtre alanı: '{key}'. "
                f"Sadece şu alanlar desteklenir: {SUPPORTED_FILTER_FIELDS}")
        
        if not isinstance(value,str) or not value.strip():
            raise ValueError(f"'{key}' filtresinin değeri boş olmayan bir string olmalıdır; alınan: '{value}'")

        condition = FieldCondition(
            key = key,
            match=MatchValue(value=value.strip())
        )    
        conditions.append(condition)

    if not conditions:
        return None
    return Filter(must = conditions)
        

def normalize_scored_point(point: ScoredPoint) -> RetrievedChunk:

    payload = point.payload
    
    if not isinstance(payload, Mapping):
        raise TypeError(
            f"Point ID {point.id} geçersiz. Payload bir sözlük (Mapping) olmalıdır."
        )

    text_fields = ["chunk_id", "source", "document_id", "topic", "text"]
    
    for field in text_fields:
        if field not in payload:
            raise ValueError(
                f"Point ID {point.id} eksik veri içeriyor: '{field}' alanı bulunamadı."
            )
            
        value = payload[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Point ID {point.id} hatalı veri içeriyor: '{field}' boş olmayan bir string (str) olmalıdır."
            )
            
    if "chunk_index" not in payload:
        raise ValueError(
            f"Point ID {point.id} eksik veri içeriyor: 'chunk_index' alanı bulunamadı."
        )
        
    chunk_index_val = payload["chunk_index"]
    if isinstance(chunk_index_val, bool) or not isinstance(chunk_index_val, int):
        raise TypeError(
            f"Point ID {point.id} hatalı veri içeriyor: 'chunk_index' tam sayı (int) olmalıdır."
        )

    try:
        score = float(point.score)
    except (TypeError, ValueError):
        raise ValueError(
            f"Point ID {point.id} hatalı veri içeriyo. "
        )

    return RetrievedChunk(
        chunk_id=payload["chunk_id"],
        source=payload["source"],
        document_id=payload["document_id"],
        chunk_index=payload["chunk_index"],
        topic=payload["topic"],
        text=payload["text"],
        score=score
    )

class Retriever:

    def __init__(
        self,
        config: RetrieverConfig,
        embedding_client: EmbeddingClient,
        qdrant_client: QdrantClient,
    ) -> None:
        self.config = config
        self.embedding_client = embedding_client
        self.qdrant_client = qdrant_client

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        filters: Mapping[str, str] | None = None,
    ) -> list[RetrievedChunk]:

        effective_top_k = self.config.default_top_k if top_k is None else top_k

        clean_query = validate_retrieval_request(query, effective_top_k)

        try:
            query_vector = self.embedding_client.embed(clean_query)
        except Exception as e:
            raise RetrievalError(f"Sorgu vektöre dönüştürülemedi: {e}") from e

        if not query_vector or len(query_vector) == 0:
            raise ValueError("Üretilen query vektörü boş olamaz.")

        qdrant_filter = build_qdrant_filter(filters)

        try:
            if not self.qdrant_client.collection_exists(self.config.collection_name):
                raise RetrievalError(
                    f"'{self.config.collection_name}' collection bulunamadı. "
                    "Önce day08 ingestion komutunu çalıştırın."
                )

            response = self.qdrant_client.query_points(
                collection_name=self.config.collection_name,
                query=query_vector,
                query_filter=qdrant_filter,
                limit=effective_top_k,
                with_payload=True,
                with_vectors=False,
            )
        except RetrievalError:
            raise
        except Exception as e:
            raise RetrievalError(
                f"Qdrant sorgulama hatası (Collection: '{self.config.collection_name}'): {e}"
            ) from e

        points = getattr(response, "points", [])

        normalized_chunks = []
        for point in points:
            chunk = normalize_scored_point(point)
            normalized_chunks.append(chunk)

        return normalized_chunks

def create_default_retriever(
    config: RetrieverConfig | None = None,
) -> Retriever: 
    if config is None:
        config = RetrieverConfig()

    embedding_client = EmbeddingClient()
    qdrant_client = QdrantClient(url=config.qdrant_url,timeout=10.0)

    return Retriever(
        config=config,
        embedding_client=embedding_client,
        qdrant_client=qdrant_client
    )
