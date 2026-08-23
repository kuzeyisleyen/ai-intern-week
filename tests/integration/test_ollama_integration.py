import pytest
from day04.ollama_client import OllamaClient
from day04.tools import SHIPPING_TOOL
from day04.tool_dispatcher import execute_tool

@pytest.mark.integration
def test_local_ollama_is_reachable():
    """Ollama API'sinin ayakta ve cevap veriyor olması gerekir. (Connectivity Test)"""
    client = OllamaClient()
    health_data = client.health()
    assert "version" in health_data

@pytest.mark.integration
def test_agent_smoke_flow():
    """Agent'ın aracı seçip, sonucunu alıp final cevabı ürettiğini (akışı tamamladığını) doğrular. (Smoke Test)"""
    client = OllamaClient()
    tools = [SHIPPING_TOOL]
    
    # 1. AŞAMA: Kullanıcı sorusu
    messages = [
        {"role": "user", "content": "Ankara'dan Antalya'ya 3 desi kargo ne kadar tutar?"}
    ]
    
    response_1 = client.chat(messages=messages, tools=tools)
    message_1 = response_1.get("message", {})
    
    # Doğrulama 1: Model sadece sohbet etmek yerine araç kullanmaya (tool_calls) karar verdi mi?
    assert "tool_calls" in message_1, "Model araç kullanmaya karar vermedi!"
    tool_calls = message_1["tool_calls"]
    assert len(tool_calls) > 0, "Tool calls listesi boş geldi!"
    
    tool_call = tool_calls[0]
    # Doğrulama 2: Doğru aracı (calculate_shipping_cost) seçti mi?
    assert tool_call["function"]["name"] == "calculate_shipping_cost"
    
    # 2. AŞAMA: Python'un aracı çalıştırması (Dispatcher)
    tool_result = execute_tool(
        tool_call["function"]["name"],
        tool_call["function"]["arguments"]
    )
    
    # Doğrulama 3: Araç patlamadan (Exception olmadan) çalışıp bir veri/hesap döndürdü mü?
    assert "error" not in tool_result, f"Araç çalışırken hata verdi: {tool_result}"
    
    # 3. AŞAMA: Modelin araç sonucunu okuyup final cevabı üretmesi
    messages.append(message_1)
    messages.append({
        "role": "tool",
        "content": str(tool_result),
        "name": tool_call["function"]["name"]
    })
    
    response_2 = client.chat(messages=messages, tools=tools)
    final_message = response_2.get("message", {})
    
    # Doğrulama 4: Model finalde boş dönmeyip okunaklı bir metin (content) üretti mi?
    assert "content" in final_message, "Model final cevabı üretmedi!"
    assert len(final_message["content"]) > 10, "Modelin cevabı çok kısa/anlamsız!"