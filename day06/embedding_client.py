import os
import requests

class EmbeddingClient:
    def __init__(self, base_url=None, model=None, timeout=30):
        # TODO: os.getenv kullanarak "OLLAMA_BASE_URL" çevresel değişkenini oku. 
        # Eğer yoksa varsayılan olarak "http://localhost:11434" kullan.
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL","http://localhost:11434")
        
        # TODO: os.getenv kullanarak "OLLAMA_EMBED_MODEL" çevresel değişkenini oku.
        # Eğer yoksa varsayılan olarak "embeddinggemma" kullan.
        self.model = model or os.getenv("OLLAMA_EMBED_MODEL","embeddinggemma")
        
        self.timeout = timeout
        
        # Endpoint URL'ini oluşturuyoruz
        self.endpoint = f"{self.base_url.rstrip('/')}/api/embed"

    def embed(self, text: str) -> list[float]:
        """
        Verilen metni Ollama API'si üzerinden vektöre dönüştürür.
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text boş olmayan bir string olmalıdır")
    
        # TODO: İstek için gerekli JSON payload'unu oluştur (model ve input anahtarları)
        payload = {
            "model" : self.model,
            "input" : text
        }

        try:
            # TODO: requests.post ile self.endpoint adresine payload'u JSON olarak gönder.
            # timeout=self.timeout parametresini eklemeyi unutma.
            response = requests.post(self.endpoint,json=payload,timeout=self.timeout)
            
            # TODO: HTTP hatalarını yakalamak için raise_for_status() metodunu çağır.
            response.raise_for_status()
            # TODO: Gelen yanıtı JSON olarak ayrıştır.
            data = response.json()
            
            # TODO: Yanıtın içinde "embeddings" anahtarının olduğunu ve boş olmadığını kontrol et.
            # Yoksa ValueError fırlat.
            if "embeddings" not in data or not data["embeddings"]:
                raise ValueError("Ollama yanıtında 'embeddings' alanı bulunamadı veya boş.")
            
            # TODO: "embeddings" listesinin içindeki ilk vektörü (0. indeks) al ve döndür.
            return data["embeddings"][0]

        except requests.exceptions.RequestException as e:
            # TODO: Yakalanan hatayı RuntimeError olarak fırlat ve içine e'yi ekle.
            raise RuntimeError(f"Ollama apisine ulaşılamadı veya http hatası : {e}")
if __name__ == "__main__":
    client = EmbeddingClient()
    
    # 1. İlk Deney
    print("--- 1. İLK DENEY ---")
    ilk_metin = "Docker container içindeki veriyi kalıcı tutmak istiyorum."
    vector = client.embed(ilk_metin)
    dimension = len(vector)
    print(f"Dimension: {dimension}")
    print(f"İlk 5 Değer: {vector[:5]}\n")

    # 2. Üç Küçük Gözlem
    print("--- 2. ÜÇ KÜÇÜK GÖZLEM ---")
    texts = {
        "A": "Docker container verilerini kalıcı saklamak istiyorum.",
        "B": "Container silinse bile dosyalarım kaybolmasın.",
        "C": "Kedim bugün pencerenin önünde uyuyor."
    }

    for key, text in texts.items():
        vec = client.embed(text)
        print(f"Metin {key} - Dimension: {len(vec)} | İlk 3 değer: {vec[:3]}")

    # Aynı metin tekrar embed edildiğinde ne oluyor?
    vec_tekrar = client.embed(texts["A"])
    vec_ilk = client.embed(texts["A"])
    print(f"\nAynı metin (A) tekrar embed edildiğinde sonuç aynı mı?: {vec_ilk == vec_tekrar}")