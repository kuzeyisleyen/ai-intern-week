import time
import asyncio
from urllib import response
from mcp.client.stdio import stdio_client
from mcp import Client, StdioServerParameters

from day04.tool_dispatcher import execute_tool

# Yönlendirme 
TOOL_PROVIDERS = {
    "calculate_shipping_cost": "native", 
    "search_notes": "mcp",          
}

class MCPToolAdapter:
    def __init__(self):
        # MCP Sunucu yapılandırması
        self.server_params = StdioServerParameters(
            command="python",
            args=["-m", "day12.mcp_server"],
        )

    async def call_async(self, tool_name: str, arguments: dict) -> dict:
        """
        Aracın sağlayıcısını kontrol eder ve ilgili rotaya (Native veya MCP) yönlendirir.
        """
        provider = TOOL_PROVIDERS.get(tool_name)
        
        if provider == "native":
            return await self._call_native(tool_name, arguments)
        elif provider == "mcp":
            return await self._call_mcp(tool_name, arguments)
        else:
            return self._build_error_response(tool_name, "unknown", f"Bilinmeyen araç sağlayıcısı: {tool_name}")

    async def _call_native(self, tool_name: str, arguments: dict) -> dict:
        """Eski usul (Native) Python fonksiyonlarını çalıştırır."""
        start_time = time.time()
        try:
            # Eski execute_tool fonksiyonunu çağır
            result = execute_tool(tool_name, arguments)
            
            if "error" in result:
                raise RuntimeError(result["error"])
                
            duration_ms = int((time.time() - start_time) * 1000)
            return self._build_success_response(tool_name, result, "native", duration_ms)
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return self._build_error_response(tool_name, "native", type(e).__name__, duration_ms)

    async def _call_mcp(self, tool_name: str, arguments: dict) -> dict:
        """Yeni usul (MCP) araçlarını standart protokol üzerinden çalıştırır."""
        start_time = time.time()
        try:
            # MCP istemcisi ile araç çağırma
            async with Client(stdio_client(self.server_params)) as client:
                response = await client.call_tool(tool_name, arguments)
                # MCP'den dönen cevap
                result_text = response.content[0].text if response.content else ""
                duration_ms = int((time.time() - start_time) * 1000)
                return self._build_success_response(tool_name, result_text, "mcp", duration_ms)
                    
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return self._build_error_response(tool_name, "mcp", type(e).__name__, duration_ms)

    def invoke_sync(self, tool_name: str, arguments: dict) -> dict:
        """
        Senkron LangGraph düğümlerinden (`nodes.py`) asenkron akışı çağırmak için köprü.
        """
        return asyncio.run(self.call_async(tool_name, arguments))

    # formatlama
    
    def _build_success_response(self, tool_name: str, result: any, provider: str, duration_ms: int) -> dict:
        return {
            "tool_name": tool_name,
            "result": result,
            "status": "completed",
            "trace": {
                "provider": provider,
                "server_name": "ai-intern-week" if provider == "mcp" else "local",
                "capability_type": "tool",
                "transport": "stdio" if provider == "mcp" else "in-process",
                "duration_ms": duration_ms,
                "error_type": None
            }
        }

    def _build_error_response(self, tool_name: str, provider: str, error_type: str, duration_ms: int = 0) -> dict:
        return {
            "tool_name": tool_name,
            "result": None,
            "status": "failed",
            "trace": {
                "provider": provider,
                "server_name": "ai-intern-week" if provider == "mcp" else "local",
                "capability_type": "tool",
                "transport": "stdio" if provider == "mcp" else "in-process",
                "duration_ms": duration_ms,
                "error_type": error_type
            }
        }
    
#workflowa bağlanmadan test etmek için
if __name__ == "__main__":
    print("--- Adaptör Testi Başlıyor ---")
    adapter = MCPToolAdapter()
    
    #Native Tool Testi
    print("\n1. Native Tool Çağrılıyor (calculate_shipping_cost)...")
    native_result = adapter.invoke_sync(
        "calculate_shipping_cost", 
        {"city": "Ankara", "weight_kg": 2}
    )
    import json
    print(json.dumps(native_result, indent=2, ensure_ascii=False))
    
    #MCP Tool Testi
    print("\n2. MCP Tool Çağrılıyor (search_notes)...")
    mcp_result = adapter.invoke_sync(
        "search_notes", 
        {"query": "hybrid search", "top_k": 1}
    )
    print(json.dumps(mcp_result, indent=2, ensure_ascii=False))