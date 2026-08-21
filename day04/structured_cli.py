import sys
import json
from day04.ollama_client import OllamaClient

def main():
    client = OllamaClient()
    
    
    prompt = "Bana en popüler 3 programlama dilini sadece şu JSON formatında ver: {'diller': ['dil1', 'dil2', 'dil3']}"
    
    print("Ollama'dan JSON verisi bekleniyor...\n")

    response = client.chat(prompt=prompt,response_format="json")
    
    metin_cevap = response.get("message", {}).get("content")
    
    dict_cevap = json.loads(metin_cevap)
  
    print("--- Ayrıştırılmış Veri ---")
    print("Veri Tipi:", type(dict_cevap))
    print("Sözlük İçeriği:", dict_cevap)

    if isinstance(dict_cevap, dict) and "diller" in dict_cevap:
         print(f"\nModelin seçtiği ilk dil: {dict_cevap['diller'][0]}")

if __name__ == "__main__":
    main()