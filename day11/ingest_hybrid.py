import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import SparseTextEmbedding

from day06.embedding_client import EmbeddingClient
from day08.chunker import chunk_text, ChunkConfig

def main():
    print("İstemciler başlatılıyor...")
    qdrant_client = QdrantClient(url="http://qdrant:6333")
    
    # Dense Model
    dense_client = EmbeddingClient()
    dense_embed = getattr(dense_client, "embed", None) or getattr(dense_client, "get_embedding", None)
    if not dense_embed:
        raise AttributeError("EmbeddingClient içinde uygun metod bulunamadı.")
    
    # Sparse Model
    print("Sparse model (BM25) yükleniyor...")
    sparse_model = SparseTextEmbedding(model_name="Qdrant/bm25")

    # Dense vektör boyutunu dinamik bulma
    sample_dense = dense_embed("test")
    dense_vector_size = len(sample_dense)
    print(f"Dense vektör boyutu tespit edildi: {dense_vector_size}")

    collection_name = "rag_chunks_hybrid"
    
    #Hibrit Koleksiyonu Oluştur
    print(f"'{collection_name}' koleksiyonu oluşturuluyor...")
    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config={
            "dense": models.VectorParams(
                size=dense_vector_size, 
                distance=models.Distance.COSINE
            )
        },
        sparse_vectors_config={
            "sparse": models.SparseVectorParams()
        }
    )

    #Corpus Dosyalarını Oku ve Yükle
    corpus_dir = Path("day08/corpus") 
    if not corpus_dir.exists():
        print(f"Hata: {corpus_dir} dizini bulunamadı! Lütfen yolu kontrol edin.")
        return

    points = []
    config = ChunkConfig(chunk_size=600, overlap=100)
    
    for file_path in corpus_dir.glob("*.md"):
        print(f"İşleniyor: {file_path.name}")
        content = file_path.read_text(encoding="utf-8")
        
        chunks = chunk_text(content, config)
        
        for i, chunk_text_data in enumerate(chunks):
            # Dense Vektör
            d_vector = dense_embed(chunk_text_data)
            
            # Sparse Vektör
            s_vector_data = list(sparse_model.embed([chunk_text_data]))[0]
            s_vector = models.SparseVector(
                indices=s_vector_data.indices.tolist(),
                values=s_vector_data.values.tolist()
            )
            
            point_id = str(uuid.uuid4())
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector={
                        "dense": d_vector,
                        "sparse": s_vector
                    },
                    payload={
                        "source": file_path.name,
                        "chunk_id": f"{file_path.stem}_chunk_{i}",
                        "text": chunk_text_data
                    }
                )
            )

    #Qdrant'a Gönder
    if points:
        print(f"Toplam {len(points)} chunk Qdrant'a yükleniyor...")
        qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )
        print("Yükleme başarıyla tamamlandı!")

if __name__ == "__main__":
    main()