import pytest
from day04.ollama_client import OllamaClient

@pytest.mark.integration
def test_local_ollama_is_reachable():
    """Ollama API'sinin ayakta ve cevap veriyor olması gerekir."""
   
    client = OllamaClient()
   
    health_data = client.health()
  
    assert "version" in health_data