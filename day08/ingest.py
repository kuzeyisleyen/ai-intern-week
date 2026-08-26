import logging
from pathlib import Path
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance,PointStruct,PayloadSchemaType

from day08.chunker import ChunkConfig,chunk_documents,Chunk
from day08.loader import load_documents
from day06.embedding_client import EmbeddingClient

LOGGER = logging.getLogger(__name__)

class IngestionConfig:
    COLLECTION_NAME = "rag_chunks"
    CORPUS_DIR = Path("day08/corpus")
    CHUNK_SIZE = 600
    CHUNK_OVERLAP = 100
    EMBEDDING_MODEL = "embeddinggemma" 
    DISTANCE_METRIC = Distance.COSINE
    QDRANT_URL = "http://qdrant:6333" 

def create_points(chunks: List[Chunk], embeddings: List[List[float]]) -> List[PointStruct]:
    """10. Point Oluşturma Sorumluluğu: Chunk ve Vektörleri birleştirir."""
    
    # uzunluklar eşit olmalı
    if len(chunks) != len(embeddings):
        raise ValueError(f"Chunk sayısı ({len(chunks)}) ile vektör sayısı ({len(embeddings)}) eşleşmiyor!")

    # vektörler boş olmamalı ve hepsi aynı boyutta olmalı
    dimension = len(embeddings[0])
    if dimension == 0:
        raise ValueError("Vektör boyutu 0 olamaz")

    points = []
    for index, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        if len(vector) != dimension:
            raise ValueError(f"Vektör boyutu uyuşmazlığı beklenen: {dimension}, bulunan: {len(vector)}")
            
        payload = {
            "source": chunk.source,
            "document_id": chunk.document_id,
            "chunk_id": chunk.chunk_id,
            "chunk_index": chunk.chunk_index,
            "topic": chunk.topic,
            "text": chunk.text
        }
        
        point = PointStruct(
            id=index + 1, # qdrant integer ID (1'den başlar)
            vector=vector,
            payload=payload
        )
        points.append(point)
        
    return points

def run_ingestion():
    """Tüm Ingestion Hattını Orkestre Eder."""
    
    # yanlış collection silinmesini engelle
    assert IngestionConfig.COLLECTION_NAME == "rag_chunks", "Kritik Hata: Sadece 'rag_chunks' kullanılmalıdır!"

    print("1. Dosyalar yükleniyor...")
    docs = load_documents(IngestionConfig.CORPUS_DIR)
    if not docs:
        raise ValueError("Corpusta doküman bulunamadı!")

    print("2. Metinler chunklanıyor...")
    chunk_config = ChunkConfig(chunk_size=IngestionConfig.CHUNK_SIZE, overlap=IngestionConfig.CHUNK_OVERLAP)
    chunks = chunk_documents(docs, chunk_config)
    if not chunks:
        raise ValueError("Hiç chunk üretilemedi")

    print(f"3. Embeddingler üretiliyor (Model: {IngestionConfig.EMBEDDING_MODEL})...")
    embed_client = EmbeddingClient()    
    # ilk chunkı embed et
    first_vector = embed_client.embed(chunks[0].text)
    dimension = len(first_vector)
    print(f"-> Vektör boyutu (dimension) {dimension} olarak tespit edildi.")
    
    # ilk vektörü tekrar üretmemek için listeye baştan ekle
    all_embeddings = [first_vector]
    
    # Kalan chunk'ları embed et
    for chunk in chunks[1:]:
        vector = embed_client.embed(chunk.text)
        all_embeddings.append(vector)

    print("4. Qdrant Pointleri hazırlanıyor...")
    points = create_points(chunks, all_embeddings)

    print("5. Qdrant Collection ve Index yönetimi yapılıyor...")
    qdrant = QdrantClient(url=IngestionConfig.QDRANT_URL)
    
    # Lifecycle: Varsa sil
    if qdrant.collection_exists(IngestionConfig.COLLECTION_NAME):
        qdrant.delete_collection(collection_name=IngestionConfig.COLLECTION_NAME)
        
    # dimension ile collection oluştur
    qdrant.create_collection(
        collection_name=IngestionConfig.COLLECTION_NAME,
        vectors_config=VectorParams(size=dimension, distance=IngestionConfig.DISTANCE_METRIC)
    )

    # payload indexleri oluştur
    qdrant.create_payload_index(
        collection_name=IngestionConfig.COLLECTION_NAME,
        field_name="topic",
        field_schema=PayloadSchemaType.KEYWORD
    )
    qdrant.create_payload_index(
        collection_name=IngestionConfig.COLLECTION_NAME,
        field_name="source",
        field_schema=PayloadSchemaType.KEYWORD
    )

    print("6. Point'ler Qdrant'a yazılıyor (Upsert)...")
    qdrant.upsert(
        collection_name=IngestionConfig.COLLECTION_NAME,
        points=points
    )

    # ingestion Çıktısı 
    print("\n" + "="*40)
    print("INGESTION RAPORU")
    print("="*40)
    print(f"Collection: {IngestionConfig.COLLECTION_NAME}")
    print(f"Embedding model: {IngestionConfig.EMBEDDING_MODEL}")
    print(f"Chunk size: {IngestionConfig.CHUNK_SIZE}")
    print(f"Overlap: {IngestionConfig.CHUNK_OVERLAP}")
    print(f"Document count: {len(docs)}")
    print(f"Chunk count: {len(chunks)}")
    print(f"Vector dimension: {dimension}")
    print(f"Payload indexes: source, topic")
    print(f"Upserted points: {len(points)}")
    print("Status: completed")
    print("="*40 + "\n")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        run_ingestion()
    except Exception as e:
        LOGGER.error(f"Ingestion başarısız oldu: {e}")
        raise