import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from day12.mcp_adapter import MCPToolAdapter

@pytest.fixture
def adapter():
    return MCPToolAdapter()

def test_unauthorized_provider(adapter):
    """Allowlist (TOOL_PROVIDERS) dışında bir araç çağrıldığında failure contract döner."""
    result = adapter.invoke_sync("unknown_tool", {})
    
    assert result["status"] == "failed"
    assert result["trace"]["provider"] == "unknown"
    assert "Bilinmeyen araç sağlayıcısı" in result["trace"]["error_type"]

@patch("day12.mcp_adapter.execute_tool")
def test_native_routing_and_trace(mock_execute_tool, adapter):
    """Native dispatcher çağrısı ve trace metadatasının in-process olarak işaretlenmesi."""
    mock_execute_tool.return_value = {"city": "Ankara", "weight_kg": 2, "cost": 84.0, "currency": "TRY"}
    
    result = adapter.invoke_sync("calculate_shipping_cost", {"city": "Ankara", "weight_kg": 2})
    
    assert result["status"] == "completed"
    assert result["result"]["cost"] == 84.0
    
    trace = result["trace"]
    assert trace["provider"] == "native"
    assert trace["transport"] == "in-process"
    assert trace["server_name"] == "local"
    assert "duration_ms" in trace
    assert trace["error_type"] is None

@patch("day12.mcp_adapter.Client")
def test_mcp_normalization_mocked(mock_client_class, adapter):
    """Karmaşık MCP objesinin (meta ve content) standart sözlüğe dönüştürülmesi."""
    # MCP Client mock kurgusu
    mock_client_instance = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client_instance
    
    # Fake response hazırlığı
    mock_content = MagicMock()
    mock_content.text = '{"source": "test.md", "chunk_id": "1"}'
    mock_response = MagicMock()
    mock_response.content = [mock_content]
    mock_client_instance.call_tool.return_value = mock_response

    result = adapter.invoke_sync("search_notes", {"query": "test"})
    
    assert result["status"] == "completed"
    assert "test.md" in result["result"]
    
    trace = result["trace"]
    assert trace["provider"] == "mcp"
    assert trace["transport"] == "stdio"
    assert trace["server_name"] == "ai-intern-week"

def test_trace_observability_contract(adapter):
    """Zorunlu 8 observability alanının varlık kontrolü."""
    # Başarısız bir durum üzerinden trace iskeletini kontrol ediyorum
    result = adapter.invoke_sync("unregistered_tool", {})
    trace = result.get("trace", {})
    
    required_keys = {
        "provider", "server_name", "capability_type", 
        "transport", "duration_ms", "error_type"
    }
    # status ve tool_name dışarıda tutulduğu için ayrı kontrole ettim
    assert required_keys.issubset(trace.keys())
    assert "status" in result
    assert "tool_name" in result