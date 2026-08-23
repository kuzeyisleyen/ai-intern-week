import json
import os
import time
import uuid

# Sansürlenecek tehlikeli anahtar kelimeler listesi
SECRET_KEYS = ["api_key", "token", "password", "secret"]

def mask_secrets(data):
    """
    Sözlük (dictionary) veya liste (list) içindeki gizli bilgileri bulup sansürler.
    """
    if isinstance(data, dict):
        masked_data = {}
        for key, value in data.items():
            # Eğer anahtar kelimenin içinde (küçük harflerle) tehlikeli bir kelime varsa:
            if any(secret in key.lower() for secret in SECRET_KEYS):
                masked_data[key] = "********[MASKED]********"
            else:
                # İç içe sözlükler (nested dict) için fonksiyonu kendi içinde tekrar çağırıyoruz (Recursive)
                masked_data[key] = mask_secrets(value)
        return masked_data
    
    elif isinstance(data, list):
        # Eğer veri bir listeyse, listenin içindeki her elemanı kontrolden geçir
        return [mask_secrets(item) for item in data]
    
    else:
        # Veri düz bir metin veya sayıysa dokunma
        return data


def write_trace(state, output_dir="output"):
    """
    Agent'ın o anki durumunu (state) güvenli ve benzersiz bir şekilde dosyaya yazar.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. ÇÖZÜM: Aynı saniyede çakışmayı önlemek için UUID (Benzersiz Kimlik) ekliyoruz
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6] # 6 haneli rastgele bir harf/sayı kombosu üretir
    filename = f"trace_{timestamp}_{unique_id}.json"
    
    filepath = os.path.join(output_dir, filename)
    
    # 2. ÇÖZÜM: Dosyaya yazmadan önce içindeki şifreleri maskeliyoruz
    safe_state = mask_secrets(state)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(safe_state, f, ensure_ascii=False, indent=2)
        
    return filepath