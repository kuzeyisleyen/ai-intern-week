import pytest
from unittest.mock import patch, MagicMock
from day14.llm_router import run_llm_router

# Her testte gerçek Ollama'ya gitmemek için mock (sahte) objeler kullanıyoruz
@pytest.fixture
def mock_keyword():
    with patch("day14.llm_router.run_keyword_router") as mock:
        # Fallback devreye girerse varsayılan olarak "knowledge" dönsün
        mock.return_value = {"route": "knowledge"}
        yield mock

@pytest.fixture
def mock_ollama():
    with patch("day14.llm_router.OllamaClient") as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        yield mock_instance


def test_valid_json_output(mock_ollama, mock_keyword):
    """Geçerli bir JSON döndüğünde doğru rotayı yakalamalıdır."""
    mock_ollama.chat.return_value = {
        "message": {"content": '{"route": "tool"}'}
    }

    result = run_llm_router("Ankara'ya 2 kg kargo ne kadar?")
    
    assert result["route"] == "tool"
    assert result["router"] == "llm"
    assert result["fallback_used"] is False
    assert result["error_type"] is None
    mock_keyword.assert_not_called()


def test_invalid_enum_output(mock_ollama, mock_keyword):
    """Şemada olmayan bir rota (weather) döndüğünde fallback yapmalıdır."""
    mock_ollama.chat.return_value = {
        "message": {"content": '{"route": "weather"}'}
    }

    result = run_llm_router("Bugün hava nasıl?")
    
    assert result["fallback_used"] is True
    assert result["error_type"] == "ValueError"
    assert result["route"] == "knowledge" # Fallback'ten gelen yanıt
    mock_keyword.assert_called_once()


def test_malformed_json_output(mock_ollama, mock_keyword):
    """JSON formatı bozuk geldiğinde parser hatayı yakalayıp fallback yapmalıdır."""
    mock_ollama.chat.return_value = {
        "message": {"content": 'knowledge'} # JSON değil, düz metin
    }

    result = run_llm_router("RAG nedir?")
    
    assert result["fallback_used"] is True
    assert result["error_type"] == "JSONDecodeError"
    mock_keyword.assert_called_once()


def test_extra_prose_output(mock_ollama, mock_keyword):
    """Model şema dışına çıkıp fazladan metin üretirse fallback yapmalıdır."""
    mock_ollama.chat.return_value = {
        "message": {"content": 'Tabii, hemen yönlendiriyorum! {"route": "tool"}'}
    }

    result = run_llm_router("Kargo hesapla")
    
    assert result["fallback_used"] is True
    assert result["error_type"] == "JSONDecodeError"
    mock_keyword.assert_called_once()


def test_timeout_or_connection_error(mock_ollama, mock_keyword):
    """Ollama servisi yanıt vermezse/hata fırlatırsa fallback yapmalıdır."""
    # Chat metodunun bir Exception fırlatmasını sağlıyoruz
    mock_ollama.chat.side_effect = ConnectionError("Bağlantı koptu")

    result = run_llm_router("Merhaba")
    
    assert result["fallback_used"] is True
    assert result["error_type"] == "ConnectionError"
    mock_keyword.assert_called_once()


def test_empty_response(mock_ollama, mock_keyword):
    """Model boş yanıt dönerse kontrollü şekilde fallback yapmalıdır."""
    mock_ollama.chat.return_value = {
        "message": {"content": ""}
    }

    result = run_llm_router("Test")
    
    assert result["fallback_used"] is True
    assert result["error_type"] == "ValueError"
    mock_keyword.assert_called_once()