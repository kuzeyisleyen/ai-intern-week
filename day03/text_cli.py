import sys 
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from day02.text_utils_updated import analyze_text

def main():
#Çıktı klasörünü belirle ve yoksa oluştur
    OUTPUT_DIR = Path("/app/output")
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
#Terminalden gelen girdiyi kontrol et
    if len(sys.argv) < 2:
        print("Hata.Analiz edilicek bir emtin girin.")
        sys.exit(1)
# sys.argv listesindeki 1. indeks, komut satırından gönderilen metindir
    input_text = sys.argv[1]
#Metni analiz et
    analyze_result = analyze_text(input_text)
#JSON formatında yazdır
    print("Analiz Sonucu : ")
    print(json.dumps(analyze_result,indent=4,ensure_ascii=False))

#Sonucu /app/output/ klasörü altına JSON dosyası olarak kaydet
    output_file_path =OUTPUT_DIR / "text-analysis.json"

    with open(output_file_path,"w",encoding="utf-8") as json_file:
        json.dump(analyze_result,json_file,indent=4,ensure_ascii=False)

    print(f"Başarılı.Dosya şuraya kaydedildi : {output_file_path}")

if __name__ == "__main__":
    main()