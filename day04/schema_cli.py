import sys
import json
from day04.ollama_client import OllamaClient
print("Python scripti çalışmaya başladı!", flush=True)
PROBLEM_ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "category": {"type": "string"},
        "risks": {
            "type": "array",
            "items": {"type": "string"}
        },
        "next_step": {"type": "string"}
    },
    "required": [
        "summary",
        "category",
        "risks",
        "next_step"
    ]
}

def validate_problem_analysis(data: dict) -> bool:
    """
    Gelen JSON sözlüğünün (data) gerçekten bizim istediğimiz yapıda olup olmadığını kontrol eder.
    Dökümandaki şu 3 soruyu cevaplar:
    1. Parse edilebilir mi? (Bunu main'de json.loads ile zaten yapacağız)
    2. Yapısal olarak geçerli mi? (Gerekli anahtarlar var mı?)
    3. Semantik olarak doğru mu? (Tipler doğru mu?)
    """

    required_keys = ["summary","category","risks","next_step"]

    for i in required_keys:
        if i  not in data :
            return False
        
    if not isinstance(data["summary"], str):
        return False
        
    if not isinstance(data["category"], str):
        return False
        
    if not isinstance(data["risks"], list):
        return False
        
    if not isinstance(data["next_step"], str):
        return False

    return True
        

def main():
    client = OllamaClient()
    
    problem_text = "Bir e-ticaret firması müşteri yorumlarını analiz ederek kritik şikayetleri insan operatörlere yönlendirmek istiyor."
    
    prompt = f"""
    Aşağıdaki problemi analiz et ve istenilen formatta bir yapı oluştur.
    Format içinde summary (kısa özet), category (kategori), risks (olası riskler listesi) ve next_step (atılacak ilk adım) olmalıdır.
    
    Problem: {problem_text}
    """
    
    print("Ollama'dan Schema formatında veri bekleniyor...\n")

    response = client.chat(prompt=prompt, response_format=PROBLEM_ANALYSIS_SCHEMA)
    
    metin_cevap = response.get("message", {}).get("content")
    
    try:
        dict_cevap = json.loads(metin_cevap)
    except json.JSONDecodeError:
        print("HATA: Modelden gelen cevap geçerli bir JSON değil!")
        sys.exit(1)
        
    print("--- Modelin Döndürdüğü JSON ---")
    print(json.dumps(dict_cevap, indent=4, ensure_ascii=False))
    
    print("\n--- Validasyon (Doğrulama) ---")
    is_valid = validate_problem_analysis(dict_cevap)
    
    if is_valid:
        print("[BAŞARILI] JSON verisi şablona (schema) tamamen uygun!")
    else:
        print("[HATA] JSON verisi şablona uymuyor!")

if __name__ == "__main__":
    main()