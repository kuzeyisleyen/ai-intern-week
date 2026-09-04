import os
from qdrant_client.http import model
import requests

class OllamaClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL","http://ollama:11434")
        
        self.model = os.getenv("OLLAMA_MODEL" , "qwen3:1.7b")    

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
        
    # 2. JSON formatı (eski string formatı veya yeni JSON Schema sözlüğü) payload'a ekleniyor
        if response_format is not None:
            payload["format"] = response_format

    # 3. Temperature gibi model ayarları için options alanı payload'a ekleniyor
        if options is not None:
            payload["options"] = options

        try:
            response = requests.post(endpoint, json=payload, timeout=30.0) 
            response.raise_for_status() 
            return response.json()
    
        except requests.exceptions.Timeout as e:
            return {"error": f"Zaman Aşımı: {str(e)}"}
        
        except requests.exceptions.RequestException as e:
            return {"error": f"Bağlantı hatası: {str(e)}"}
        
        except ValueError as e:
            return {"error": f"Geçersiz yanıt formatı: {str(e)}"}