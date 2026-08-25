import sqlite3
import json
import os
from pathlib import Path
from qdrant_client import QdrantClient
from day06.embedding_client import EmbeddingClient

DATA_PATH = Path(__file__).parent / "data" / "documents.json"
COLLECTION_NAME = "intern_documents"

def run_comparison():
    # 1. SQLITE KURULUMU VE VERİ EKLEME
    # ":memory:" kullanarak geçici bir veritabanı açıyoruz
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE documents (
            id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            source TEXT,
            text TEXT NOT NULL
        )
    """)
    
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)
        
    for doc in documents:
        cursor.execute(
            "INSERT INTO documents (id, category, source, text) VALUES (?, ?, ?, ?)",
            (doc["id"], doc["category"], doc["source"], doc["text"])
        )
    conn.commit()

    # 2. SQLITE SORGULARI (Kesin Eşleşme)

    print("SQLITE: EXACT MATCH (Kesin Eşleşme)")
    
    # Soru 1: doc-07 hangisi?
    print("\n[SQL] Sorgu: SELECT * FROM documents WHERE id = 'doc-07'")
    cursor.execute("SELECT id, category, text FROM documents WHERE id = ?", ("doc-07",))
    for row in cursor.fetchall():
        print(f" -> Bulundu: ID: {row[0]} | Kategori: {row[1]} | Metin: {row[2][:50]}...")

    # Soru 2: category=docker hangisi?
    print("\n[SQL] Sorgu: SELECT * FROM documents WHERE category = 'docker'")
    cursor.execute("SELECT id, text FROM documents WHERE category = ?", ("docker",))
    for row in cursor.fetchall():
        print(f" -> Bulundu: ID: {row[0]} | Metin: {row[1][:50]}...")

    # 3. QDRANT SORGUSU (Anlamsal Eşleşme)

    print("\nQDRANT: SEMANTIC SEARCH (Anlamsal Arama)")
    
    qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
    embedder = EmbeddingClient()
    
    query_text = "Container silinince verilerim kaybolmasın."
    print(f"\n[Qdrant] Sorgu: '{query_text}'")
    
    query_vector = embedder.embed(query_text)
    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=2,
        with_payload=True
    ).points
    
    for idx, result in enumerate(results, 1):
        print(f" -> {idx}. Skor: {result.score:.4f} | ID: {result.payload.get('document_id')} | Metin: {result.payload.get('text')}")

if __name__ == "__main__":
    run_comparison()