from day05.agent_loop import run_agent

# "Sahte test" İstemcisi
class FakeClient:
    def chat(self, messages, tools):
        # Eğer ajan daha önce bir hata aldıysa ve bunu messages içine "tool" rolüyle eklediyse
        # döngünün sonsuza girmemesi için normal bir cevap verip bitiriyoruz.
        if any(m.get("role") == "tool" for m in messages):
            return {
                "message": {
                    "role": "assistant",
                    "content": "Hatayı gördüm, işlemi iptal ediyorum."
                }
            }
        
        # İlk iterasyonda bilerek OLMAYAN bir aracı çağırması için modeli taklit ediyoruz
        return {
            "message": {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "olmayan_arac",
                            "arguments": {}
                        }
                    }
                ]
            }
        }

def run_test():
    print("Test başlıyor: Bilinmeyen tool çağrısı senaryosu...\n")
    
    # Ajanı gerçek Ollama ile değil, bizim FakeClient ile başlatıyoruz
    fake_client = FakeClient()
    final_state = run_agent("Test prompt", client=fake_client)
    
    print("\n--- Test Sonuçları ---")
    
    # Kontrol 1: Hata listesi (errors) boş olmamalı
    if len(final_state["errors"]) > 0:
        print("BAŞARILI: Hata durumu 'state.errors' listesine eklendi.")
    else:
        print("HATA: 'state.errors' listesi boş!")
        
    # Kontrol 2: tool_history içindeki status 'error' olmalı
    last_tool = final_state["tool_history"][0]
    if last_tool["status"] == "error":
        print(f"BAŞARILI: tool_history status'u doğru şekilde 'error' olarak kaydedildi.")
    else:
        print(f"HATA: tool_history status'u yanlış! Şu anki değer: {last_tool['status']}")

if __name__ == "__main__":
    run_test()