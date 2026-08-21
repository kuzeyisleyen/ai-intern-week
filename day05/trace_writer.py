import json
import os
from datetime import datetime

def write_trace(state: dict, filename_prefix: str = "trace"):
    """
    Ajanın o anki durumunu (state) timestamp ile birlikte bir JSON dosyasına kaydeder.
    """
    # Dosya adını tarih-saat ile oluştur 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/{filename_prefix}_{timestamp}.json" 
    
    # State içindeki verileri dosyaya yaz
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)
        print(f"\n[TRACE] Ajanın işlem özeti kaydedildi: {filename}")
    except Exception as e:
        print(f"\n[TRACE ERROR] Trace yazılamadı: {e}")