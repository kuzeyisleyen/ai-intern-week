"""
İlk Qdrant collection'ını oluşturur,
örnek bir point ekler ve kaydı doğrular.
"""

import os
from typing import Any
from day06.embedding_client import EmbeddingClient
from qdrant_client import QdrantClient, models

COLLECTION_NAME = "intern_documents"
SAMPLE_TEXT = "Docker named volume kalıcı veri saklar."


def create_qdrant_client() -> QdrantClient:
    """
    QDRANT_URL environment değişkenini okuyarak
    Qdrant client oluşturur.
    """

    qdrant_url = os.getenv("QDRANT_URL","http://qdrant:6333")
    return QdrantClient(url=qdrant_url)

def create_embedding_client() -> Any:
    """
    Projede daha önce yazılan embedding client'ını oluşturur.
    """
    return EmbeddingClient()

def create_sample_vector(
    embedding_client: Any,
    text: str,
) -> list[float]:
    """
    Örnek metinden gerçek embedding üretir.
    """
    vector = embedding_client.embed(text)
    return vector

def validate_vector(vector: list[float]) -> int:
    """
    Vector'ün temel contract'ını kontrol eder
    ve dimension değerini döndürür.
    """
    if not isinstance(vector,list):
        raise TypeError("Vector liste olmalı")
    if len(vector) == 0:
        raise ValueError("vector boş olamaz")
    if not all(isinstance(x,(int,float))for x in vector):
        raise TypeError("vector sadece int/float değer içermeli")

    return len(vector)
    
def ensure_collection(
    client: QdrantClient,
    collection_name: str,
    dimension: int,
) -> None:
    """
    Collection yoksa COSINE metriğiyle oluşturur.
    Varsa mevcut yapılandırmayı kontrol eder.
    """

    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config = models.VectorParams(
                size = dimension,
                distance = models.Distance.COSINE,
            ),
        )
        print(f"Collection {collection_name} oluşturuldu.Boyut : {dimension}")

    else:
        collection_info = client.get_collection(collection_name)
        existing_dimension = collection_info.config.params.vectors.size 

        if existing_dimension != dimension:
            raise ValueError(f"colleciton boyutu uyuşmuyor|Beklenen:{dimension},MEvcut:{existing_dimension}")
        print(f"Collection {collection_name} zaten mevcut ve yapılandırması doğru.")

def build_first_point(
    vector: list[float],
    text: str,
) -> models.PointStruct:
    """
    İlk PointStruct nesnesini hazırlar.
    """

    return models.PointStruct(
        id=1,
        vector=vector,
        payload={
            "document_id": "doc-01",
            "text": text,
            "category": "docker",
            "language": "tr",
        },
    )
        

def upsert_point(
    client: QdrantClient,
    collection_name: str,
    point: models.PointStruct,
) -> None:
    """
    Point'i Qdrant'a ekler veya günceller.
    """

    client.upsert(
        collection_name = collection_name,
        points = [point]
    )
    print("Point başarıyla eklendi.")

def retrieve_point(
    client: QdrantClient,
    collection_name: str,
    point_id: int,
) -> Any:
    """
    Point'i ID üzerinden Qdrant'tan geri okur.
    """

    retrieved =client.retrieve(
        collection_name = collection_name,
        ids = [point_id],
        with_payload = True,
        with_vectors = False
    )
    if not retrieved:
        raise ValueError(f"ID : {point_id} ile point bulunmadı")
    return retrieved[0]

def print_summary(
    dimension: int,
    stored_point: Any,
) -> None:
    """
    Deney sonucunu okunabilir biçimde gösterir.
    """

    payload = stored_point.payload
    print("\n--- İŞLEM ÖZETİ ---")
    print(f"Collection Name : {COLLECTION_NAME}")
    print(f"Vector Dimension: {dimension}")
    print(f"Internal ID : {stored_point.id}")
    print(f"Document ID : {payload.get('document_id')}")
    print(f"Category : {payload.get('category')}")
    print(f"Language : {payload.get('language')}")
    print(f"Text: {payload.get('text')}")
    print("-------------------\n")


def main() -> None:
    """
    Bütün adımları doğru sırada çalıştırır.
    """

    qdrant = create_qdrant_client()
    embedder = create_embedding_client()

    vector = create_sample_vector(embedder,SAMPLE_TEXT)
    dimension = validate_vector(vector)

    ensure_collection(qdrant,COLLECTION_NAME,dimension)

    point = build_first_point(vector,SAMPLE_TEXT)
    upsert_point(qdrant,COLLECTION_NAME,point)

    stored = retrieve_point(qdrant,COLLECTION_NAME,point.id)
    print_summary(dimension,stored)


if __name__ == "__main__":
    main()