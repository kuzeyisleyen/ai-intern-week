import os
import re
from dataclasses import asdict

import requests

from day04.ollama_client import OllamaClient
from day04.tool_dispatcher import execute_tool
from day04.tools import SHIPPING_TOOL
from day08.context_builder import build_context
from day08.rag_pipeline import SYSTEM_PROMPT, build_user_prompt, validate_citations
from day08.retriever import RetrievedChunk, create_default_retriever
from day10.exceptions import (WorkflowError, 
DependencyUnavailableError, 
DependencyTimeOutError,
WorkflowLimitError,
ResponseContractError)
from day12.mcp_adapter import MCPToolAdapter
from day12.trace import log_tool_trace

SEARCH_NOTES_TOOL = {
    "type": "function",
    "function": {
        "name": "search_notes",
        "description": "Kullanıcının notlarında ve veritabanında semantik arama yapar.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Aranacak kelime veya cümle (örneğin: 'hybrid search')"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Döndürülecek sonuç sayısı"
                }
            },
            "required": ["query"]
        }
    }
}

MAX_REWRITES = 1
MAX_STEPS = 12

ALLOWED_ROUTES = {"smalltalk", "knowledge", "tool"}
ALLOWED_TOOL_NAMES = {"calculate_shipping_cost", "search_notes"}

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
GEN_MODEL = os.getenv("GEN_MODEL", "qwen3:1.7b")

REWRITE_PROMPT = """
Kullanıcının niyetini değiştirmeden,
bu soruyu semantic retrieval için daha açık bir arama sorgusuna dönüştür.

Cevap verme.
Yeni bilgi ekleme.
Yalnız rewritten query döndür.

Orijinal Soru: {query}
""".strip()

def next_step(state: dict, node_name: str) -> dict:
    new_step = state.get("step_count", 0) + 1

    if new_step > MAX_STEPS:
        raise WorkflowLimitError("Akışın Limiti Aşıldı") #

    return {
        "step_count": new_step,
        "node_trace": state.get("node_trace", []) + [node_name],
    }


# Gelen soruyu basit kelime kurallarıyla 'smalltalk', 'tool' veya 'knowledge' rotalarına ayırıyorum.
def classify_keyword(query: str) -> str:
    lowered = query.lower()

    if any(
        greeting in lowered
        for greeting in ("merhaba", "selam", "hello")
    ):
        return "smalltalk"

    if "kargo" in lowered or "notlar" in lowered:
        return "tool"

    return "knowledge"


def classify_node(state: dict) -> dict:
    route = classify_keyword(state["original_query"])

    update = next_step(state, "classify_query")
    update["route"] = route
    return update


# RAG veya veritabanına hiç bulaşmadan, smalltalk sorularına doğrudan kısa bir cevap üretiyorum.
def direct_generate_node(state: dict) -> dict:
    client = OllamaClient()
    response = client.chat(
        messages=[
            {
                "role": "system",
                "content": "Kısa, doğal ve doğrudan bir smalltalk cevabı ver.",
            },
            {"role": "user", "content": state["original_query"]},
        ]
    )

    update = next_step(state, "direct_generate")
    
    if "error" in response:
        update["status"] = "error"
        update["error_type"] = "DependencyUnavailableError"
        update["failed_node"] = "direct_generate"
        update["errors"] = state.get("errors", []) + [response["error"]]
        return update

    update["answer"] = response.get("message", {}).get("content", "").strip()
    update["status"] = "completed"
    return update

# Sadece izin verdiğim kargo aracını kullanarak modelin hesaplama yapmasını sağlıyorum.
def tool_node(state: dict) -> dict:
    client = OllamaClient()
    
    response = client.chat(
        messages=[{"role": "user", "content": state["original_query"]}],
        tools=[SHIPPING_TOOL,SEARCH_NOTES_TOOL], 
    )

    update = next_step(state, "tool_node")

    if "error" in response:
        update["status"] = "error"
        update["error_type"] = "DependencyUnavailableError"
        update["failed_node"] = "tool"
        update["errors"] = state.get("errors", []) + [response["error"]]
        return update

    tool_calls = response.get("message", {}).get("tool_calls", [])
    
    if not tool_calls:
        update["status"] = "error"
        update["error_type"] = "ResponseContractError"
        update["failed_node"] = "tool"
        update["errors"] = state.get("errors", []) + ["Model geçerli bir tool çağrısı üretmedi."]
        return update

    function_call = tool_calls[0]["function"]
    tool_name = function_call["name"]
    arguments = function_call["arguments"]

    if tool_name not in ALLOWED_TOOL_NAMES:
        update["status"] = "error"
        update["error_type"] = "ResponseContractError"
        update["failed_node"] = "tool"
        update["errors"] = state.get("errors", []) + [f"İzinsiz tool: {tool_name}"]
        return update

    # Yeni yapı yönlendirme adaptöre devredildi.
    try:
        adapter = MCPToolAdapter()
        adapter_response = adapter.invoke_sync(tool_name, arguments)
            
        # İster başarısız olsun ister başarılı, sonucu ayrı bir json dosyasına logla
        log_tool_trace(adapter_response, tool_name)
            
        if adapter_response["status"] == "failed":
            update["status"] = "error"
            update["error_type"] = "ToolRuntimeError"  
            update["failed_node"] = "tool"
            update["errors"] = state.get("errors", []) + [adapter_response.get("trace", {}).get("error_type", "Bilinmeyen Adaptör Hatası")]
            return update
            
        tool_result = adapter_response["result"]
        trace_data = adapter_response.get("trace", {})
        
    except Exception as e:
        update["status"] = "error"
        update["error_type"] = "ToolRuntimeError"  
        update["failed_node"] = "tool"
        update["errors"] = state.get("errors", []) + [f"Adaptör veya çalışma zamanı hatası: {str(e)}"]
        return update

    update["tool_name"] = tool_name
    update["tool_result"] = tool_result
    
    if tool_name == "calculate_shipping_cost":
        update["answer"] = f"{tool_result['city']} için {tool_result['weight_kg']} kg kargo ücreti {tool_result['cost']} {tool_result['currency']}."
    else:
        update["answer"] = f"Arama sonucu: {tool_result}"
        
    update["status"] = "completed"
    update["trace"] = trace_data
    
    return update


# Qdrant'taki vektör veritabanımı tarayıp soruyla en alakalı 3 metin parçasını çekiyorum.
def retrieve_node(state: dict) -> dict:

    """Day 8 retriever'ını yeniden kullanarak retrieval yapar."""
    update = next_step(state, "retrieve")

    try:
        retriever = create_default_retriever()
        retrieved_chunks = retriever.retrieve(state["retrieval_query"], top_k=3)
        update["retrieved_chunks"] = [asdict(chunk) for chunk in retrieved_chunks]
    except Exception as e :
        update["error_type"] = "DependencyUnavailableError" #
        update["failed_node"] = "retrieve"
        update["errors"] = state.get("errors", []) + [f"Qdrant bağlantı hatası: {str(e)}"]
  
        update["status"] = "error"
        update["retrieved_chunks"] = []

    return update


# Veritabanından sonuç döndüyse kaliteye 'usable', liste boşsa 'weak' diyorum ki akış karar verebilsin.
def quality_node(state: dict) -> dict:
    """Kılavuzdaki güvenli başlangıç policy'si: sonuç varsa usable."""
    chunks = state.get("retrieved_chunks", [])
    retrieval_quality = "usable" if chunks else "weak"

    update = next_step(state, "retrieval_quality")
    update["retrieval_quality"] = retrieval_quality
    return update


# Bulduğum bağlamı modele gönderip cevap ürettiriyorum ve içinde geçen [Sx] kaynak etiketlerini topluyorum.
def generate_node(state: dict) -> dict:
    chunks = [RetrievedChunk(**chunk) for chunk in state.get("retrieved_chunks", [])]
    context = build_context(chunks)
    user_prompt = build_user_prompt(state["original_query"], context)

    response = OllamaClient().chat(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )

    update = next_step(state, "generate")

    if "error" in response:
        update["status"] = "error"
        update["error_type"] = "DependencyUnavailableError" #
        update["failed_node"] = "generate"
        update["errors"] = state.get("errors", []) + [response["error"]]
        return update

    answer = response.get("message", {}).get("content", "").strip()
    citations = sorted(set(re.findall(r"\[(S\d+)\]", answer)))

    update["answer"] = answer
    update["citations"] = citations
    return update


# Modelin verdiği [Sx] etiketlerinin gerçekten benim verdiğim metinlerde olup olmadığını kontrol ediyorum.
def validate_node(state: dict) -> dict:
    chunks = [RetrievedChunk(**chunk) for chunk in state.get("retrieved_chunks", [])]
    context = build_context(chunks)
    invalid_citations = validate_citations(state["answer"] or "", context.valid_labels)

    update = next_step(state, "validate_citations")

    if invalid_citations:
        update["status"] = "error"
        update["error_type"] = "ResponseContractError"  
        update["failed_node"] = "validate"
        update["errors"] = state.get("errors", []) + [f"Geçersiz citation: {citation}" for citation in invalid_citations]
        return update

    update["status"] = "completed"
    return update


# Arama sonuçları kötüyse, modeli kullanarak orijinal soruyu arama motorunun daha iyi anlayacağı şekilde baştan yazdırıyorum.
def rewrite_query(query: str) -> str:
    """Kılavuzdaki prompt ile yalnız retrieval sorgusunu yeniden yazar."""
    prompt = REWRITE_PROMPT.format(query=query)
    
    try:
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json={"model": GEN_MODEL, "prompt": prompt, "stream": False},
            timeout=30,
        )
        response.raise_for_status() 
        
        rewritten = response.json().get("response", "").strip()
        if rewritten:
            return rewritten
            
    except requests.RequestException as e:
        raise DependencyUnavailableError(f"Ollama rewrite servisi çöktü: {str(e)}") #
        
    return query


# Yeni baştan yazılan soruyu kaydedip sonsuz döngüye girmemek için rewrite sayacını bir artırıyorum.
def rewrite_node(state: dict) -> dict:
    update = next_step(state, "rewrite")
    
    try:
        rewritten_query = rewrite_query(state["retrieval_query"])
        update["retrieval_query"] = rewritten_query
        update["rewrite_count"] = state.get("rewrite_count", 0) + 1
        
    except DependencyUnavailableError as e: #
        update["status"] = "error"
        update["error_type"] = "DependencyUnavailableError"
        update["failed_node"] = "rewrite"
        update["errors"] = state.get("errors", []) + [str(e)]
        
    return update


# Hiçbir şey bulamazsam veya limitleri aşarsam, kontrollü bir şekilde 'bilmiyorum' deyip akışı güvenle bitiriyorum.
def fallback_node(state: dict) -> dict:
    update = next_step(state, "fallback")
    update["answer"] = "Üzgünüm, bu konuda yeterli bilgi bulamadım."
    update["status"] = "completed"
    return update

def error_node(state: dict) -> dict:
    update = next_step(state, "error_node")
    update["status"] = "error"
    
    if state.get("route") not in {"smalltalk", "knowledge", "tool"}:
        update["errors"] = state.get("errors", []) + [f"Bilinmeyen rota: {state.get('route')}"]
        
    return update