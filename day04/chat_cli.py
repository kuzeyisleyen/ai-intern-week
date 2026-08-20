import sys
import json
import os
from ollama_client import OllamaClient

def main():

    if len(sys.argv) < 2 :
        print("Kullanım: python chat_cli.py \"Sorunuzu buraya yazın\"")
        sys.exit(1)

    prompt = sys.argv[1]
  
    client = OllamaClient()
    try:
        response = client.chat(prompt)
    except Exception as e :
        print("Hata oluştu : {e}")
        sys.exit(1) 

    output_data ={ 
         "prompt" : prompt,
         "model" : response.get("model"),
         "content" : response.get("message", {}).get("content"),
         "metrics": {
            "total_duration": response.get("total_duration"),
            "load_duration": response.get("load_duration"),
            "prompt_eval_count": response.get("prompt_eval_count"),
            "eval_count": response.get("eval_count")
        }
    }

    print("Modelin cevabı : ")
    print(output_data["content"])

    output_path = "/app/output/day04-chat-response.json"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
        
    print(f"\n[Başarılı] Sonuç detayları '{output_path}' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()