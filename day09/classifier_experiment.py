import json
import requests
from day09.state import create_initial_state
from day09.nodes import classify_node

# structured output şeması
ROUTE_SCHEMA = {
    "type": "object",
    "properties": {
        "route": {
            "type": "string",
            "enum": ["smalltalk", "knowledge", "tool"]
        }
    },
    "required": ["route"]
}

#  test soruları
TEST_QUERIES = [
    "selam",
    "nasılsın?",
    "named volume ne işe yarar?",
    "container verisini kalıcı tutmak istiyorum",
    "Ankara'ya 3 kg kargo ne kadar?",
    "shipping fiyatı hesapla",
    "tool calling ne demek?"
]

def get_llm_route(query: str) -> str:
    prompt = f"""
    Görevin kullanıcı mesajı için workflow rotası seçmektir.

    Rotalar:

    - smalltalk:
        Selamlaşma, hal hatır sorma ve bilgi kaynağı veya araç
        gerektirmeyen gündelik konuşmalar.

    - knowledge:
        Docker, container, volume, tool calling, embeddings ve benzeri
        kavramlar hakkında bilgi isteyen mesajlar.
        Bu rota RAG/knowledge sistemini kullanır.

    - tool:
         Yalnız kargo fiyatı hesaplatmak gibi allowlisted shipping
        aracının gerçekten çalıştırılmasını gerektiren talepler.
        Bir araç veya tool kavramını sormak bu kategoriye girmez.

    Kurallar:

        - Soru işareti route belirlemez.
        - Mesajda "tool" kelimesinin geçmesi tek başına tool route anlamına gelmez.
        - Yalnız verilen mesajın niyetini sınıflandır.
        - Mutlaka smalltalk, knowledge veya tool değerlerinden birini seç.

    Örnekler:

        "Selam, nasılsın?" → smalltalk
        "Named volume nedir?" → knowledge
        "Tool calling ne demek?" → knowledge
        "Ankara'ya 3 kg kargo ne kadar?" → tool

    Kullanıcı mesajı:
        {query}
            """
    
    try:
        response = requests.post(
            "http://ollama:11434/api/generate",
            json={
                "model": "qwen3:1.7b",
                "prompt": prompt,
                "stream": False,
                "format": ROUTE_SCHEMA # format olarak şema
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json().get("response", "{}")
            return json.loads(data).get("route", "geçersiz_yanıt")
    except Exception as e:
        return f"hata: {str(e)}"
    
    return "geçersiz_yanıt"

def run_comparison():
    print(f"{'Sorgu':<45} | {'Kurallı Rota':<15} | {'LLM Rota':<15} | {'Aynı mı?'}")
    print("-" * 95)
    
    for query in TEST_QUERIES:
        # 1.deterministic rota
        state = create_initial_state(query)
        rule_result = classify_node(state)
        rule_route = rule_result["route"]
        
        # 2. LLMin verdiği rota
        llm_route = get_llm_route(query)
        
        # Karşılaştırma
        is_same = "Evet" if rule_route == llm_route else "Hayır"
        
        print(f"{query:<45} | {rule_route:<15} | {llm_route:<15} | {is_same}")

if __name__ == "__main__":
    run_comparison()