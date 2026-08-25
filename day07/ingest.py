"""
Day 6 dokümanlarını Qdrant'a yükler.

Programın yaptığı işlemler:

1. JSON dosyasını okur.
2. Dokümanları kontrol eder.
3. Her doküman için embedding üretir.
4. Qdrant point'leri oluşturur.
5. Point'leri Qdrant'a yükler.
6. İlk point'i geri okuyarak işlemi doğrular.
"""

import json
from pathlib import Path

from qdrant_client import QdrantClient, models

from day07.first_collection import (
    COLLECTION_NAME,
    create_embedding_client,
    create_qdrant_client,
    ensure_collection,
    validate_vector,
)
#TODO 1 (Veriyi Yükle): Dosya yolunu kontrol et ve JSON'u listeye çevir.
#TODO 2 (Güvenlik Duvarı): Listedeki her belgede id, text, category var mı, tipleri doğru mu ve çift kopya ID var mı kontrol et.
#TODO 3 (Boyut Kilidi): Binlerce belgeyi işlemeden önce sadece ilk belgeyi vektöre çevir ve boyutunu (dimension) öğren.
#TODO 4 (Koleksiyon Kurulumu): Qdrant'a git, öğrendiğin bu tam boyutla ve COSINE metriğiyle tabloyu (collection) kur.
#TODO 5 (Dönüşüm): Tüm dokümanları dönüştür; metinleri vektör yap, ID'leri 1, 2, 3 diye sıraya diz, asıl metin ID'sini payload (meta veri) içine göm.
#TODO 6 (Yükleme ve İndeksleme): Verileri tek seferde (upsert) kaydet ve "category" alanı üzerinde hızlı arama için indeks (KEYWORD) oluştur.
#TODO 7 (Sağlamasını Yap): Veritabanından 1 numaralı kaydı geri çağır ve yüklediğinle aynı mı diye kontrol et.

DATA_PATH = Path(__file__).parent / "data" / "documents.json"

def load_documents(path: Path) -> list[dict]:
    """
    JSON dosyasını okur ve doküman listesini döndürür.
    """
    if not path.exists():
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise TypeError("JSON kökü bir liste (list) olmalıdır.")
    if not data:
        raise ValueError("JSON listesi boş olamaz.")

    return data

def validate_documents(documents: list[dict]) -> None:
    """
    Dataset içindeki dokümanların temel alanlarını kontrol eder.
    """
    required_fields = {
        "id",
        "text",
        "category",
        "source",
        "day",
        "topic",
        "language",
    }

    document_ids = set()

    for position, document in enumerate(documents):
        if not isinstance(document, dict):
            raise TypeError(f"Doküman {position} bir dictionary olmalıdır.")

        missing_fields = required_fields - document.keys()
        if missing_fields:
            raise ValueError(f"Doküman {position} içinde eksik alanlar var: {missing_fields}")

        if not isinstance(document["id"], str) or not document["id"].strip():
            raise ValueError(f"Doküman {position} için 'id' boş olmayan bir string olmalıdır.")

        if not isinstance(document["text"], str) or not document["text"].strip():
            raise ValueError(f"Doküman {position} için 'text' boş olmayan bir string olmalıdır.")

        if not isinstance(document["category"], str) or not document["category"].strip():
            raise ValueError(f"Doküman {position} için 'category' boş olmayan bir string olmalıdır.")

        if document["id"] in document_ids:
            raise ValueError(f"Duplicate (çift) document ID bulundu: {document['id']} (Pozisyon: {position})")
        
        document_ids.add(document["id"])


def build_points(
    embedding_client,
    documents: list[dict],
    expected_dimension: int,
) -> list[models.PointStruct]:
    """
    Doküman listesini Qdrant PointStruct listesine dönüştürür.
    """

    points = []

    for index, document in enumerate(documents, start=1):
        vector = embedding_client.embed(document["text"])
        
        dimension = validate_vector(vector)
        
        if dimension != expected_dimension:
            raise ValueError(
                f"Dimension uyuşmazlığı! Beklenen: {expected_dimension}, "
                f"Gelen: {dimension} (Doküman ID: {document['id']})"
            )

        payload = {
            "document_id": document["id"],
            "text": document["text"],
            "category": document["category"],
            "source": document["source"],
            "day": document["day"],
            "topic": document["topic"],
            "language": document["language"],
        }

        point = models.PointStruct(
            id=index,
            vector=vector,
            payload=payload
        )
        
        points.append(point)

    return points

def upload_points(
    client: QdrantClient,
    points: list[models.PointStruct],
) -> None:
    """
    Point listesini Qdrant'a yükler.
    """

    if not points:
        raise ValueError("Yüklenecek point bulunamadı (Points listesi boş).")

    operation_info = client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True
    )
    
    print(f"Upsert işlemi tamamlandı. Durum: {operation_info.status}")

def create_category_index(
    client: QdrantClient,
) -> None:
    """
    Category payload alanı için keyword index oluşturur.
    """

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="category",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )
    print("Payload index (category -> KEYWORD) hazırlandı.")

def verify_upload(
    client: QdrantClient,
    documents: list[dict],
    points: list[models.PointStruct],
) -> None:
    """
    İlk point'i Qdrant'tan geri okuyarak yüklemeyi doğrular.
    """

    if not points:
        raise ValueError("Doğrulanacak point listesi boş.")

    first_id = points[0].id

    retrieved = client.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[first_id],
        with_payload=True,
        with_vectors=False
    )

    if not retrieved:
        raise ValueError(f"ID {first_id} ile point Qdrant'tan geri çağrılamadı.")

    first_point = retrieved[0]

    if not first_point.payload:
        raise ValueError("Geri çağrılan point'in payload'ı boş.")

    retrieved_doc_id = first_point.payload.get("document_id")
    expected_doc_id = documents[0]["id"]
    
    if retrieved_doc_id != expected_doc_id:
        raise ValueError(
            f"Payload uyuşmazlığı! Beklenen document_id: {expected_doc_id}, "
            f"Gelen: {retrieved_doc_id}"
        )

    print("\n--- İLK POINT DOĞRULAMASI ---")
    print(f"Point ID   : {first_point.id}")
    print(f"Document ID: {retrieved_doc_id}")
    print(f"Category   : {first_point.payload.get('category')}")
    print(f"Text       : {first_point.payload.get('text')}")
    print("-----------------------------\n")

def main() -> None:
    """
    Ingestion işleminin ana akışı.
    """
# 1. Client'ları oluştur.
    qdrant_client = create_qdrant_client()
    embedding_client = create_embedding_client()

    print("Veriler okunuyor ve doğrulanıyor...")
    # 2. Dataset'i yükle.
    documents = load_documents(DATA_PATH)

    # 3. Dataset'i doğrula.
    validate_documents(documents)

    print("Örnek embedding üretiliyor ve boyut belirleniyor...")
    # 4. İlk dokümandan örnek embedding üret.
    sample_vector = embedding_client.embed(documents[0]["text"])

    # 5. Vector dimension'ı belirle.
    dimension = validate_vector(sample_vector)

    # 6. Collection'ı oluştur veya doğrula.
    ensure_collection(qdrant_client, COLLECTION_NAME, dimension)

    print(f"{len(documents)} doküman vektörlere çevriliyor...")
    # 7. Point listesini oluştur.
    points = build_points(embedding_client, documents, dimension)

    print("Qdrant'a yükleme işlemi başlıyor...")
    # 8. Point'leri Qdrant'a yükle.
    upload_points(qdrant_client, points)

    # 9. Category payload index oluştur.
    create_category_index(qdrant_client)

    # 10. Yüklemeyi doğrula.
    verify_upload(qdrant_client, documents, points)
    
    print("Bütün ingestion (içeri aktarma) süreci başarıyla tamamlandı.")
if __name__ == "__main__":
    main()