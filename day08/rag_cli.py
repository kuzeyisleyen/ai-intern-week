import sys
import requests
from day08.rag_pipeline import RAGPipeline
from day08.retriever import create_default_retriever 

class OllamaClient:
    """Ollama /api/chat uç noktası ile konuşan basit istemci."""
    def __init__(self, model_name: str = "qwen3:1.7b", base_url: str = "http://ollama:11434"):
        self.model_name = model_name
        self.base_url = base_url

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]


def main():
    retriever = create_default_retriever()
    
    generation_client = OllamaClient(model_name="qwen3:1.7b")
    pipeline = RAGPipeline(
        retriever=retriever, 
        generation_client=generation_client
    )

    if len(sys.argv) > 1:
        questions = [" ".join(sys.argv[1:])]
    else:
        questions = [
            "Named volume ile bind mount arasındaki temel fark nedir?",
            "Agent loop'ta max_iterations neden var?",
            "Vector database relational database'in tamamen yerine geçer mi?"
        ]

    print("NATIVE RAG PIPELINE TESTİ")

    for q in questions:
        print(f"\n--- SORU ---\n{q}")
        try:
            result = pipeline.answer(q, top_k=3)
            
            print("\n--- RETRIEVED CHUNKS ---")
            if not result.retrieved_chunks:
                print("Hiçbir chunk bulunamadı!")
            else:
                for chunk in result.retrieved_chunks:
                    print(f"- [Score: {chunk.score:.4f}] Kaynak: {chunk.source} | Metin: {chunk.text[:60]}...")
            print("\n--- GENERATED ANSWER ---")
            print(result.answer)
            
            if result.invalid_citations:
                print(f"\nDİKKAT: Model uydurma kaynak üretti! Geçersiz etiketler: {result.invalid_citations}")
            else:
                print("\nTüm kaynak etiketleri (citations) geçerli.")
            if result.is_missing_citations:
                print("\nDİKKAT: Model kurala uymadı ve HİÇ kaynak etiketi (citation) kullanmadı!")
            elif result.invalid_citations:
                print(f"\nDİKKAT: Model uydurma kaynak üretti! Geçersiz etiketler: {result.invalid_citations}")
            else:
                print("\nTüm kaynak etiketleri (citations) geçerli ve kullanılmış.")
                
        except Exception as e:
            print(f"\nÇALIŞMA HATASI: {e}")

if __name__ == "__main__":
    main()