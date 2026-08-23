import os
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
        

    def chat(self, messages: list, tools: list = None, response_format: str = None) -> dict:
        """
        Model ile etkileşimi kuran asıl fonksiyon.
        """
        endpoint = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        
        if tools:
            payload["tools"] = tools
            
        # 2. Eğer JSON formatı isteniyorsa, payload'a ekliyoruz (Ollama'nın resmi format desteği)
        if response_format == "json":
            payload["format"] = "json"

        try:
            response = requests.post(endpoint, json=payload,timeout=30.0) 
    
            response.raise_for_status() 
            
            return response.json()
        
        except requests.exceptions.Timeout as e:
            return {"error": f"Zaman Aşımı: {str(e)}"}
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Bağlantı hatası: {str(e)}"}
            
        except ValueError as e:
            return {"error": f"Geçersiz yanıt formatı: {str(e)}"}