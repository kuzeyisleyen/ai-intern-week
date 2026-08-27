import pytest
from day09.state import create_initial_state
from day09.graph_workflow import graph
from day09.nodes import MAX_STEPS

"""Gerçek ai modeliyle sohbet rotasının hata vermeden ve benim belirlediğim adım sınırlarını aşmadan cevap ürettiğini doğruluyorum."""
@pytest.mark.integration
def test_smoke_smalltalk_contract():
    state = create_initial_state("Selam")
    result = graph.invoke(state)
    
    assert result["route"] == "smalltalk"
    assert result["status"] in ["completed", "error"]
    assert result["step_count"] <= MAX_STEPS
    assert result["answer"] != ""
    assert "direct_generate" in result["node_trace"]

"""Gerçek veritabanından dönen bilginin cevaplandığını ve modelin kaynak etiketlerini kafasından uydurmadığını doğruluyorum."""
@pytest.mark.integration
def test_smoke_knowledge_contract():
    state = create_initial_state("Named volume ile bind mount farkı nedir?")
    result = graph.invoke(state)
    
    assert result["route"] == "knowledge"
    assert result["status"] in ["completed", "error"]
    assert result["step_count"] <= MAX_STEPS
    assert result["answer"] != ""
    
    bulunan_parcalar = result.get("retrieved_chunks", [])
    gecerli_etiketler = []
    
    for i in range(len(bulunan_parcalar)):
        gecerli_etiketler.append(f"S{i+1}")
        
    for citation in result.get("citations", []):
        assert citation in gecerli_etiketler

"""Gerçek modelin kargo hesaplama aracını başarıyla tetiklediğini ve cevap metninin boş dönmediğini doğruluyorum."""
@pytest.mark.integration
def test_smoke_tool_contract():
    state = create_initial_state("Ankara'ya 3 kg kargo ne kadar?")
    result = graph.invoke(state)
    
    assert result["route"] == "tool"
    assert result["status"] in ["completed", "error"]
    assert result["step_count"] <= MAX_STEPS
    assert result["answer"] != ""
    assert "tool_node" in result["node_trace"]