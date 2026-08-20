import urllib.request
import json

class OllamaClient:
    # Kendi kullandığın model adını (örneğin "qwen2.5:3b" veya dökümandaki "qwen3:1.7b") buraya yazabilirsin.
    def __init__(self, base_url="http://ollama:11434", model="qwen3:1.7b"): 
        self.base_url = base_url
        self.model = model

    # Artık 'messages' ve 'tools' parametrelerini de kabul ediyor!
    def chat(self, prompt=None, response_format=None, messages=None, tools=None):
        url = f"{self.base_url}/api/chat"
        
        # Eğer dışarıdan hazır bir mesaj listesi verilmediyse, prompt'u mesaja çevir
        if messages is None:
            messages = [{"role": "user", "content": prompt}]
            
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        
        if response_format:
            payload["format"] = response_format
            
        # Eğer modelden araç kullanmasını istiyorsak bunu da pakete ekliyoruz!
        if tools:
            payload["tools"] = tools
            
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            print(f"Ollama API Hatası: {e}")
            return {}