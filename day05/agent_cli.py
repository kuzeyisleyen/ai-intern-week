from day05.agent_loop import run_agent
from day05.trace_writer import write_trace

SYSTEM_INSTRUCTION = """You are a local tool-using assistant.
Use provided tools when required.
Do not invent tool results.
Use tool results in the final answer."""
    
def main():
    print("=== Otonom Kargo Ajanına Hoş Geldiniz ===")
    print("Çıkmak için 'q' veya 'quit' yazabilirsiniz.\n")

    while True:
        # TODO: Kullanıcıdan input al
        user_input = input("Sen : ") 
        # TODO: Kullanıcı 'q', 'quit' veya 'exit' yazarsa döngüyü kır (break)
        if user_input.lower() in ["q","quit","exit"]:
            print("görüşmek üzere")
            break

        # Boş girdileri atla
        if not user_input.strip():
            continue

        print("\n[Ajan Çalışıyor...]")
        
        # TODO: run_agent fonksiyonunu user_input ile çağır ve dönen sonucu final_state değişkenine ata
        final_state = run_agent(user_input, system_prompt=SYSTEM_INSTRUCTION)

        
        print("\n" + "="*30)
        print("=== AJAN ÇIKTISI ===")
        
        # TODO: final_state içinden "status" değerini ekrana yazdır
        print(f"Durum(states) : {final_state['status']}")

        # TODO: final_state içinden "iteration" (kaç adım sürdüğü) değerini ekrana yazdır
        print(f"iteration : {final_state['iteration']}")
        
        # TODO: Eğer final_state içinde "errors" listesi boş değilse hataları ekrana yazdır
        if final_state["errors"]:
            print(f"Hatalar : {final_state['errors']}")
            
        # TODO: final_state içinden "final_response" değerini ekrana yazdır
        print(f"Final response : {final_state['final_response']}")
        
        print("="*30 + "\n")

        # 1. Ajanı çalıştır (Burası while döngüsünün İÇİNDE olmalı)
        final_state = run_agent(user_input)
        
        # 2. Ekrana yazdırma işlemleri
        print("\n==============================")
        print("=== AJAN ÇIKTISI ===")
        print(f"Durum(states) : {final_state['status']}")
        print(f"iteration : {final_state['iteration']}")
        print(f"Final response : {final_state['final_response']}")
        print("==============================\n")
        
        # 3. YENİ EKLENEN: İşlem bitince trace'i kaydet (Burası da while'ın İÇİNDE)
        write_trace(final_state)

if __name__ == "__main__":
    main()
   