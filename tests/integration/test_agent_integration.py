import pytest
from day05.agent_loop import run_agent

@pytest.mark.integration
def test_run_agent_basic_completion():
    """Agent'ın tool gerektirmeyen basit bir diyalogda hata vermeden tamamlandığını doğrular."""
    state = run_agent(user_prompt="Merhaba, nasılsın? Sadece kısaca selam ver.")
    
    # State oluşuyor mu
    assert isinstance(state, dict), "State bir dictionary olmalı."
    
    # Status geçerli mi
    assert state["status"] == "completed", f"Status 'completed' olmalı, {state['status']} geldi."
    
    # Messages var mı
    assert len(state["messages"]) >= 2, "En az user ve assistant mesajları olmalı."
    
    # Final response okunabilir mi
    assert isinstance(state["final_response"], str), "Final response bir string olmalı."
    assert len(state["final_response"]) > 0, "Final response boş olmamalı."

@pytest.mark.integration
def test_run_agent_with_tool():
   # Modele aracı kullanması gerektiğini açıkça belirten bir system prompt
    sys_prompt = "You are a helpful assistant. You MUST use the provided tools to calculate shipping costs."
    
    # Aracın parametreleriyle birebir eşleşecek net bir soru
    # (weight: 2.5, method: express vb. beklediğini varsayarak)
    prompt = "What is the cost of shipping a 2.5 kg package to Ankara with express delivery?"
    
    state = run_agent(user_prompt=prompt, system_prompt=sys_prompt)
    
    # State oluşuyor mu?
    assert isinstance(state, dict)
    
    # Tool history oluşuyor mu?
    assert len(state["tool_history"]) > 0, "Ajanın kargo ücretini hesaplamak için aracı çağırması gerekiyordu."
    
    # Tool history içeriği yapısal olarak doğru mu
    last_tool_call = state["tool_history"][-1]
    assert "tool_name" in last_tool_call
    assert "arguments" in last_tool_call
    assert "result" in last_tool_call
    
    # Messages güncellenmiş mi? (user, tool call(s), tool result(s), final response)
    assert len(state["messages"]) >= 4, "Mesaj akışında en az 4 aşama olmalı."