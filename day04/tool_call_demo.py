import sys
import json
from day04.ollama_client import OllamaClient
from day04.tools import SHIPPING_TOOL
from day04.tool_dispatcher import execute_tool

def main():
    if len(sys.argv) < 2:
        print("HATA: Lütfen bir soru girin.")
        sys.exit(1)
        
    user_prompt = sys.argv[1]
    
    # 1. YENİ SÖZLEŞMEYE UYGUN MESAJ LİSTESİ
    messages = [{"role": "user", "content": user_prompt}]
    tools = [SHIPPING_TOOL] 
    
    client = OllamaClient()
    print("1. AŞAMA: Model Düşünüyor (Araç Seçimi)...\n")
    
    # 2. ESKİ 'prompt' YERİNE 'messages' KULLANILIYOR
    response = client.chat(
        messages=messages,
        tools=tools
    )
    response_message = response.get("message", {})
    
    if "tool_calls" in response_message:
        tool_call = response_message["tool_calls"][0] 
        
        print(f"Model Kararı: '{tool_call['function']['name']}' aracını kullanmak istiyorum.")
        print(f"Modelin Gönderdiği Veriler: {tool_call['function']['arguments']}\n")
        
        # 3. Modelin ilk cevabını geçmişe (messages) ekliyoruz
        messages.append(response_message)
        
        print("2. AŞAMA: Python Güvenlik Kontrolünü Yapıp Aracı Çalıştırıyor...\n")
        tool_result = execute_tool(
            tool_call["function"]["name"],
            tool_call["function"]["arguments"]
        )
        print(f"Araçtan Çıkan Sonuç: {tool_result}\n")
        
        # 4. Aracın sonucunu da geçmişe (messages) ekliyoruz
        messages.append({
            "role": "tool",
            "content": json.dumps(tool_result)
        })
        
        print("3. AŞAMA: Model, araçtan gelen sonuca göre final cevabını hazırlıyor...\n")
        
        # 5. FİNAL ÇAĞRISI: Yine 'messages' kullanıyoruz
        final_response = client.chat(messages=messages, tools=tools)
        
        print("--- FİNAL CEVAP ---")
        print(final_response.get("message", {}).get("content"))
        
    else:
        print("Model herhangi bir araç kullanmaya gerek duymadı. Normal cevap:")
        print(response_message.get("content"))

if __name__ == "__main__":
    main()