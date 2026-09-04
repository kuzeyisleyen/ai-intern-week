import json
import time
from typing import Dict, Any

from day04.ollama_client import OllamaClient
from day14.keyword_router import run_keyword_router

ROUTE_SCHEMA = {
    "type": "object",
    "properties": {
        "route": {
            "type": "string",
            "enum": [
                "smalltalk",
                "knowledge",
                "tool",
            ],
        },
    },
    "required": ["route"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """Sen bir yapay zeka sisteminin akıllı yönlendiricisisin (Semantic Router).
Kullanıcının sorgusunu analiz et ve aşağıdaki üç rotadan birine yönlendir:

1. smalltalk:
Bilgi retrieval veya tool execution gerektirmeyen gündelik/selamlaşma konuşması.

2. knowledge:
Mevcut bilgi/RAG akışının cevaplamaya çalışacağı bilgilendirici soru.

3. tool:
Yalnız sistemde gerçekten mevcut ve allowlisted bir capability ile karşılanabilen istek.

Available tool capabilities (Mevcut yetenekler):
- calculate_shipping_cost: Şehir ve ağırlık verilmiş bir gönderinin ücretini hesaplar.
- search_notes: Kullanıcının proje notlarında arama yapar.

ÖNEMLİ KURAL: İş yapılabilir bir action içeren query'de selamlama ikincil ise 'tool' önceliklidir.
Yanıtını kesinlikle verilen JSON şemasına uygun olarak üret.
"""

def run_llm_router(query: str) -> Dict[str, Any]:
    """
    Sorguyu LLM kullanarak anlamsal olarak sınıflandırır.
    Hata durumunda keyword_router'a fallback yapar.
    """
    start_time = time.perf_counter()
    
    actual_route = None
    error_type = None
    fallback_used = False
    
    try:
        client = OllamaClient()
   
        response = client.chat(
            model="qwen3:1.7b",  
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            options={"temperature": 0},
            response_format=ROUTE_SCHEMA
        )
    
        raw_content = response.get("message", {}).get("content")
        
        # None veya boş string kontrolü
        if not raw_content:
            raise ValueError("LLM'den boş veya geçersiz yanıt geldi.")
            
        parsed_content = json.loads(raw_content)
        actual_route = parsed_content.get("route")
        
        if actual_route not in {"smalltalk", "knowledge", "tool"}:
            raise ValueError(f"Invalid route from LLM: {actual_route}")
        
    except Exception as e:
        error_type = type(e).__name__
        fallback_used = True
        
        fallback_result = run_keyword_router(query)
        actual_route = fallback_result.get("route")

    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000

    return {
        "route": actual_route,
        "router": "llm",
        "latency_ms": latency_ms,
        "fallback_used": fallback_used,
        "error_type": error_type,
    }