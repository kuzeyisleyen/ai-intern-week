from mcp.server import MCPServer
from pathlib import Path
import logging
from day11.hybrid_retriever import retrieve_hybrid
from fastembed import SparseTextEmbedding
from qdrant_client import QdrantClient
from day06.embedding_client import EmbeddingClient

qdrant_client = QdrantClient(url="http://qdrant:6333")
embedding_client = EmbeddingClient()
sparse_model = SparseTextEmbedding(model_name="Qdrant/bm25")

logger = logging.getLogger(__name__)

mcp = MCPServer("ai-intern-week")

RESOURCE_MAP = {
    "week2://system-review": Path("notes/week-02-system-review.md"),
    "week3://day11-report": Path("reports/day-11.md"),
}

@mcp.resource("week2://system-review")
def week2_system_review() -> str:
    """
    Sadece izin verilen sistem inceleme notunu okur ve string olarak döner.
    """
    file_path = RESOURCE_MAP.get("week2://system-review")
    if not file_path or not file_path.exists():
        raise FileNotFoundError("İzin verilen dosya bulunamadı veya mevcut değil.")
    return file_path.read_text(encoding="utf-8")

@mcp.tool()
def search_notes(query: str, top_k: int = 3) -> list[dict]:
    """
    Day 11 arama altyapısını kullanarak notlar içinde retrieval yapar.
    """
    if not query or not isinstance(query, str) or not query.strip():
        raise ValueError("query boş olmayan bir string olmalıdır")
    if  isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 5:
        raise ValueError("top_k 1 ile 5 arasında bir tam sayı olmalıdır")

    logger.info(f"Arama tool'u tetiklendi. Query: {query}, top_k: {top_k}")

    hybrid_model = retrieve_hybrid(query = query,
                                   qdrant_client=qdrant_client,
                                   embedding_client=embedding_client,
                                   sparse_model=sparse_model,
                                   top_k=top_k)
    
    return hybrid_model

if __name__ == "__main__":
    mcp.run()