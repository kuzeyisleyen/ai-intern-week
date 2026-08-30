from day09.graph_workflow import run_graph_workflow
from day09.graph_cli import print_workflow_trace
from day10.exceptions import DependencyUnavailableError
import day09.nodes as nodes

# Fake dependency:
# Gerçek Qdrant'a gitmeden beklenen runtime failure'ı üretir.
class FailingRetriever:
    def retrieve(self, query: str, top_k: int = 3):
        print("\n[FAKE] Qdrant unavailable failure simüle ediliyor...")
        raise DependencyUnavailableError(
            "Qdrant sunucusuna şu anda ulaşılamıyor. "
            "(Simüle edilmiş hata)"
        )

# Fabrikayı (create_default_retriever) taklit eden sahte fonksiyon
def mock_create_default_retriever():
    return FailingRetriever()

def test_retriever_unavailable_failure():
    print("=" * 50)
    print("TEST: QDRANT UNAVAILABLE FAILURE INJECTION")
    print("=" * 50)

    # Attribute yoksa sessizce yeni bir attribute oluşturmak yerine
    # burada açıkça hata almayı tercih ediyoruz (fabrika fonksiyonu için).
    orijinal_create = nodes.create_default_retriever

    # Production kodunu değiştirmeden fake dependency enjekte edilir.
    nodes.create_default_retriever = mock_create_default_retriever

    try:
        final_state = run_graph_workflow("Named volume nedir?")

        print_workflow_trace(final_state)

        # Test gerçekten knowledge/retrieval yoluna girdi mi?
        assert "retrieve" in final_state["node_trace"], (
            "Test retrieval node'una ulaşmadı. "
            "Router farklı bir route seçmiş olabilir."
        )

        # RECOVER:
        # Workflow exception ile kapanmak yerine kontrollü sonuç üretmeli.
        assert final_state["status"] == "error", (
            f"Beklenen status='error', "
            f"gerçek status={final_state.get('status')!r}"
        )

        # OBSERVE:
        # Failure'ın türü ve konumu state içinde görünür olmalı.
        assert final_state["failed_node"] == "retrieve", (
            f"Beklenen failed_node='retrieve', "
            f"gerçek değer={final_state.get('failed_node')!r}"
        )

        assert final_state["error_type"] == "DependencyUnavailableError", (
            "Beklenen error_type='DependencyUnavailableError', "
            f"gerçek değer={final_state.get('error_type')!r}"
        )

        # CONTAIN:
        # Retrieval başarısız olduktan sonra generation çalışmamalı.
        assert "generate" not in final_state["node_trace"], (
            "Retrieval başarısız olmasına rağmen generate çalıştı."
        )

        print("\n[PASS] Retriever failure kontrollü yönetildi.")

        return final_state

    finally:
        # Test başarılı olsa da assertion/exception nedeniyle yarıda
        # kesilse de gerçek dependency mutlaka geri yüklenir.
        nodes.create_default_retriever = orijinal_create

if __name__ == "__main__":
    test_retriever_unavailable_failure()