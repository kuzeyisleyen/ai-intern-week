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
        user_input = input("Sen : ")

        if user_input.lower() in ["q","quit","exit"]:
            print("sistem kapatılıyor...")
            break

        if not user_input.strip():
            continue
        print("ajan çalıştırılıyor...")

        final_state = run_agent(user_input,system_prompt=SYSTEM_INSTRUCTION)

        print("Ajan Çıktısı")
        print(f"Durum : {final_state['status']}")
        print(f"iteration : {final_state['iteration']}")

        if final_state["errors"]: 
            print(f"Hatalar : {final_state['errors']}")
            print(f"Final response : {final_state['final_response']}")

            write_trace(final_state)


if __name__ == "__main__":
    main()
   