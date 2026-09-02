import asyncio
from importlib import resources
from xmlrpc import client
from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_client():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "day12.mcp_server"],
    )

    async with Client(stdio_client(server_params)) as client:
        #discovery
        print("\nSunucu Yetenekleri")

        tools_response = await client.list_tools()
        resources_response = await client.list_resources()
        print("Sunucuda bulunan araçlar (tools):")
        for tool in tools_response.tools:
            print(f"- {tool.name}: {tool.description}")
            
        print("\nSunucuda bulunan kaynaklar (resources):")
        for resource in resources_response.resources:
            print(f"- {resource.name}: {resource.description}")

        #resource
        print("\nResource Okunuyor")

        resource_response = await client.read_resource("week2://system-review")
        review_text = resource_response.contents[0].text
        print(f"\nOkunan Kaynak (İlk 200 Karakter): {review_text[:200]}")

        #tool çağırma
        print("\nTool Çağrılıyor")

        tool_result = await client.call_tool("search_notes", {"query": "hybrid search neden var?", "top_k": 3})
        print(f"\nTool Sonucu (İlk 200 Karakter): {str(tool_result)[:200]}")

if __name__ == "__main__":
    asyncio.run(run_client())