import sys
import json
import os
from day04.ollama_client import OllamaClient
from schema_cli import PROBLEM_ANALYSIS_SCHEMA, validate_problem_analysis

def main():
    if len(sys.argv) < 2:
        print("HATA: Lütfen analiz edilecek bir problem metni girin.")
        print("Örnek: python day04/problem_analyzer.py \"Müşteriler kargodan şikayetçi.\"")
        sys.exit(1)
        
    problem_text = sys.argv[1]
  
    client = OllamaClient()
    prompt = f"""
    Aşağıdaki problemi analiz et ve istenilen formatta bir yapı oluştur.
    Format içinde summary (kısa özet), category (kategori), risks (olası riskler listesi) ve next_step (atılacak ilk adım) olmalıdır.
    
    Problem: {problem_text}
    """
    
    print("Ollama'dan analiz bekleniyor, lütfen bekleyin...\n")
    
    response = client.chat(prompt=prompt, response_format=PROBLEM_ANALYSIS_SCHEMA)
    metin_cevap = response.get("message", {}).get("content")
     
    try:
        dict_cevap = json.loads(metin_cevap)
    except json.JSONDecodeError:
        print("HATA: Model geçerli bir JSON döndürmedi!")
        sys.exit(1)
    
    sonuc = validate_problem_analysis(dict_cevap)
    if not sonuc:
        print("HATA: JSON yapısı şablona uymuyor!")
        sys.exit(1)


    os.makedirs("output", exist_ok=True)
    
    dosya_yolu = "output/day04-problem-analysis.json"

    with open(dosya_yolu, "w", encoding="utf-8") as dosya:
        json.dump(dict_cevap, dosya, ensure_ascii=False, indent=4)

    print(f"[BAŞARILI] Analiz sonucu kaydedildi: {dosya_yolu}")

if __name__ == "__main__":
    main()