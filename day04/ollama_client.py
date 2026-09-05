import os
import requests

class OllamaClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")    

    def health(self):
        """Ollama API'sinin ayakta olup olmadığını kontrol eder."""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5.0)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Health check başarısız: {e}")
            return {"status": "error", "details": str(e)}

    def chat(
        self,
        messages: list,
        tools: list = None,
        model: str = None,
        response_format=None,
        options: dict = None,
        think: bool = None,
        keep_alive: int | str = None,  # int (saniye) veya str ("5m") desteği
        timeout: float = 60.0,         # Deneyler için esnek timeout
    ) -> dict:
        """
        Model ile etkileşimi kuran asıl fonksiyon.
        """
        endpoint = f"{self.base_url}/api/chat"
    
        # 1. Dışarıdan model gelirse onu, gelmezse sınıfın varsayılan modelini kullan
        payload = {
            "model": model or getattr(self, "model", "qwen3:1.7b"),
            "messages": messages,
            "stream": False
        }
    
        if tools:
            payload["tools"] = tools
        
        # 2. JSON formatı payload'a ekleniyor
        if response_format is not None:
            payload["format"] = response_format

        # 3. Model ayarları (temperature vb.) payload'a ekleniyor
        if options is not None:
            payload["options"] = options

        # Kılavuz Ders 9: Deney parametreleri ekleniyor
        if think is not None:
            payload["think"] = think
            
        if keep_alive is not None:
            payload["keep_alive"] = keep_alive

        try:
            # Sabit 30.0 yerine metoda geçirilebilen timeout kullanıldı
            response = requests.post(endpoint, json=payload, timeout=timeout) 
            response.raise_for_status() 
            return response.json()
    
        except requests.exceptions.Timeout as e:
            # Ollama hatası fırlatıldığında yönlendirici gerçek root cause'u koruyacak
            return {"error": f"Timeout (Zaman Aşımı): {str(e)}"}
        
        except requests.exceptions.RequestException as e:
            return {"error": f"Bağlantı hatası: {str(e)}"}
        
        except ValueError as e:
            return {"error": f"Geçersiz JSON/yanıt formatı: {str(e)}"}