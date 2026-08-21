import pytest
from day05.agent_loop import run_agent

class FakeClient:
    def __init__(self, responses):
        self.responses = responses

    def chat(self, *args, **kwargs):
        # Listeden sıradaki cevabı çıkar ve ajana gönder
        return self.responses.pop(0)

def test_no_tool_final():
    """Ajanın hiç tool çağırmadan doğrudan cevap verdiği senaryo."""
    # Ajan ilk iterasyonda doğrudan text döner, tool istemez.
    fake_responses = [
        {"message": {"role": "assistant", "content": "Merhaba, kargo sistemi emrinizde.", "tool_calls": []}}
    ]
    client = FakeClient(fake_responses)
    state = run_agent("Selam", client=client)
    assert state["status"] == "completed"
    assert len(state["tool_history"]) == 0
    assert state["iteration"] == 1

def test_single_tool_final():
    """Ajanın 1 kez tool çağırıp, sonra cevabı verdiği senaryo."""
    fake_responses = [
        {
            "message": {
                "role": "assistant", "content": "", 
                "tool_calls": [{"function": {"name": "calculate_shipping_cost", "arguments": {"city": "İzmir", "weight_kg": 2}}}]
            }
        },
        {"message": {"role": "assistant", "content": "İzmir için 2kg kargo ücreti hesaplandı.", "tool_calls": []}}
    ]
    client = FakeClient(fake_responses)
    state = run_agent("İzmir 2kg kargo", client=client)
    assert state["status"] == "completed"
    assert len(state["tool_history"]) == 1
    assert state["iteration"] == 2

def test_unknown_tool():
    """Ajanın olmayan bir tool (örn: make_coffee) çağırmaya çalıştığı senaryo."""
    # TODO: Tool call listesinde adı "make_coffee" olan bir fake_response ver
    # TODO: assert ile error policy'nin bunu yakaladığını test et
    fake_responses = [
        {
            "message": {
                "role": "assistant", "content": "", 
                "tool_calls": [{"function": {"name": "make_coffee", "arguments": {"sugar": 2}}}]
            }
        },
        {"message": {"role": "assistant", "content": "Üzgünüm, kahve yapma yeteneğim yok.", "tool_calls": []}}
    ]
    client = FakeClient(fake_responses)
    state = run_agent("Bana şekerli kahve yap", client=client)
    assert state["status"] == "completed"
    assert "error" in state["tool_history"][0]["result"]

def test_invalid_argument():
    """Ajanın parametreleri yanlış veya eksik gönderdiği senaryo."""
    fake_responses = [
        {
            "message": {
                "role": "assistant", "content": "", 
                "tool_calls": [{"function": {"name": "calculate_shipping_cost", "arguments": {"city": "İzmir", "weight_kg": "iki kilo"}}}]
            }
        },
        {"message": {"role": "assistant", "content": "Kilo bilgisi hatalı olduğu için işlem yapılamadı.", "tool_calls": []}}
    ]
    client = FakeClient(fake_responses)
    state = run_agent("İzmir 2kg kargo", client=client)
    assert state["status"] == "completed"
    assert "error" in state["tool_history"][0]["result"]


def test_tool_exception():
    """Tool çalışırken beklenmedik bir hata fırlatırsa veya eksik veri gelirse."""
    fake_responses = [
        {
            "message": {
                "role": "assistant", "content": "", 
                "tool_calls": [{"function": {"name": "calculate_shipping_cost", "arguments": {"city": None, "weight_kg": -10}}}]
            }
        },
        {"message": {"role": "assistant", "content": "Tool hata fırlattığı için işlemi tamamlayamıyorum.", "tool_calls": []}}
    ]
    client = FakeClient(fake_responses)
    state = run_agent("Bozuk kargo hesabı yap", client=client)
    assert state["status"] == "completed"
    assert "error" in state["tool_history"][0]["result"]

def test_max_iteration():
    """Ajanın sürekli tool çağırarak sonsuz döngüye girmeye çalıştığı senaryo."""
    # TODO: Max iteration sınırını aşacak kadar uzun bir liste ver.
    fake_responses = [
        {"message": {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "analyze_text", "arguments": {"text": f"Deneme {i}"}}}]}}
        for i in range(1, 7) # 6 adet fake response üretir
    ]
    client = FakeClient(fake_responses)
    state = run_agent("Sürekli analiz yap", client=client)
    
    assert state["status"] == "stopped"
    assert state["iteration"] == 5

def test_repeated_tool_call():
    """Ajanın aynı tool'u aynı parametrelerle defalarca çağırdığı senaryo."""
    # TODO: Ajan tamamen aynı isteği, aynı parametrelerle 3 kez üst üste tekrarlasın
    fake_responses = [
        {"message": {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "calculate_shipping_cost", "arguments": {"city": "Ankara", "weight_kg": 5}}}]}},
        {"message": {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "calculate_shipping_cost", "arguments": {"city": "Ankara", "weight_kg": 5}}}]}},
        {"message": {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "calculate_shipping_cost", "arguments": {"city": "Ankara", "weight_kg": 5}}}]}}
    ]
    client = FakeClient(fake_responses)
    state = run_agent("Ankara'ya 5kg kargo gönder", client=client)
    
    assert state["status"] == "stuck"