import pytest
import asyncio
import json
from mcp.client.stdio import stdio_client
from mcp import Client, StdioServerParameters
from day12.mcp_adapter import MCPToolAdapter

pytestmark = pytest.mark.integration

@pytest.fixture
def server_params():
    return StdioServerParameters(command="python", args=["-m", "day12.mcp_server"])

def test_discovery_contract(server_params):
    """Tool ve Resource Discovery testleri."""
    async def run():
        async with Client(stdio_client(server_params)) as client:
            tools_response = await client.list_tools()
            tool_names = [t.name for t in tools_response.tools]
            assert "search_notes" in tool_names
            
            resources_response = await client.list_resources()
            resource_uris = [r.uri for r in resources_response.resources]
            assert "week2://system-review" in resource_uris
    
    asyncio.run(run())

def test_read_resource_content(server_params):
    """Resource read işleminin integration test üzerinden içeriğinin kontrolü."""
    async def run():
        async with Client(stdio_client(server_params)) as client:
            response = await client.read_resource("week2://system-review")
            content = response.contents[0].text
            
            assert content is not None
            assert len(content.strip()) > 0
            assert "#" in content 
            
    asyncio.run(run())

def test_invalid_args_controlled_failure(server_params):
    async def run():
        async with Client(stdio_client(server_params)) as client:
            response = await client.call_tool("search_notes", {"top_k": 3})
            assert response.is_error is True
            
    asyncio.run(run())

def test_unknown_tool_failure(server_params):
    async def run():
        async with Client(stdio_client(server_params)) as client:
            response = await client.call_tool("hayali_arac", {})
            assert response.is_error is True
                
    asyncio.run(run())

def test_full_retrieval_smoke():
    """Adapter -> Server -> Qdrant uçtan uca bütünlük testi."""
    adapter = MCPToolAdapter()
    
    result = adapter.invoke_sync("search_notes", {"query": "hybrid search", "top_k": 1})
    
    assert result["status"] == "completed"
    assert result["trace"]["provider"] == "mcp"
    assert result["trace"]["error_type"] is None
    
    result_data = json.loads(result["result"])
    
    if isinstance(result_data, list):
        assert len(result_data) > 0
        assert "source" in result_data[0]
        assert "chunk_id" in result_data[0]
    elif isinstance(result_data, dict):
        assert "source" in result_data
        assert "chunk_id" in result_data