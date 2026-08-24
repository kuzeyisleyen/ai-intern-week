import os
from day06.embedding_client import EmbeddingClient
from day06.semantic_search import load_and_embed_documents, semantic_search

def run_cli():
    print("Sistem başlatılıyor...")
    client = EmbeddingClient()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data", "documents.json")
    
    print("Dokümanlar okunuyor ve hafızaya (embedding) alınıyor. Lütfen bekleyin...")
    # TODO: load_and_embed_documents fonksiyonunu data_path ve client parametreleriyle çağır
    embedded_docs = load_and_embed_documents(data_path,client)
    
    
    print(f"{len(embedded_docs)} doküman başarıyla işlendi!\n")
    print("-" * 40)

    queries = [
        "Container silinse bile veriyi nasıl saklarım?",
        "Modelin bir Python fonksiyonunu seçmesi nasıl çalışıyor?",
        "Testlerimin gerçek LLM'e bağımlı olmasını istemiyorum."
    ]

    # TODO: queries listesi üzerinde for döngüsüyle dön:
    #   - Ekrana "SORGU: {q}" yazdır.
    #   - semantic_search() fonksiyonunu çağır (q, embedded_docs, client, top_k=3 parametreleriyle)
    #   - Dönen top_k listesi üzerinde tekrar bir for döngüsü dön ve ekrana skoru ve metni yazdır:
    #     print(f"  [{res['score']:.4f}] {res['text']}")
    #   - Her sorgudan sonra araya bir çizgi ("-" * 40) ekle.

    for q in queries:
        print(f"Sorgu : {q}")
        top_results = semantic_search(q,embedded_docs,client,top_k=3)
        for i in top_results:
            print(f" [{i['score']:.4f}] {i['text']}")
            print("-" * 40)

if __name__ == "__main__":
    run_cli()