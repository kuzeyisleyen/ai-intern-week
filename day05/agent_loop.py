import json
from day04.ollama_client import OllamaClient
from day04.tool_dispatcher import execute_tool
from day04.tools import SHIPPING_TOOL, ANALYZE_TOOL

MAX_ITERATIONS = 5

def run_agent(user_prompt: str, client=None, system_prompt: str = None) -> dict:
    
    initial_messages = []
    if system_prompt:
        initial_messages.append({"role": "system", "content": system_prompt})
    
    initial_messages.append({"role": "user", "content": user_prompt})

    # 1. STATE (Ajanın Hafızası)
    state = {
        "messages": initial_messages, 
        "iteration": 0,
        "status": "running", 
        "errors": [],
        "tool_history": [],
        "final_response": None,
    }

    # TODO: OllamaClient'ı başlat ve araç şemalarını (schemas) getir
    if client is None:
        client = OllamaClient()
    tool_schema = [SHIPPING_TOOL, ANALYZE_TOOL]

    seen_signatures = set()

    # 2. MOTOR (While Döngüsü)
    while state["status"] == "running":
        # TODO: Fren 1 - iteration sayısı MAX_ITERATIONS'a ulaştıysa:
        # status'u 'stopped' yap, errors'a hata mesajı ekle ve döngüyü kır (break).
        if state["iteration"] >= MAX_ITERATIONS:
            state["status"] = "stopped"
            state["errors"].append("Max iterations")
            break

        state["iteration"] += 1
        print(f"\n--- İterasyon {state['iteration']} ---")

        # TODO: Modeli çağır (client.chat) ve cevabı state["messages"] içine ekle
        response = client.chat(messages=state["messages"], tools=tool_schema)

        # ollama_client.py hata durumunda {"error": "..."} döndürüyor — bunu ayır
        if "error" in response:
            state["status"] = "stopped"
            state["errors"].append(response["error"])
            break

        response_message = response["message"]
        state["messages"].append(response_message)
        # 3. TERMINATION (Bitiş ve Karar Kontrolleri)
        
        # TODO: Fren 2 - Gelen cevapta 'tool_calls' yoksa veya boşsa:
        # status'u 'completed' yap, final_response'u doldur ve döngüyü kır.
        if "tool_calls" not in response_message or not response_message["tool_calls"]:
            state["status"] = "completed"
            state["final_response"] = response_message.get("content","")
            break

        # Eğer tool call varsa, her bir tool için döngüye gir:
        # (Burada gelen tool_calls listesi üzerinde for döngüsü kurman gerekecek)
        # TODO: tool_name ve arguments bilgilerini değişkene al
        for tool_call in response_message["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            # TODO: Fren 3 - Takılma (Stuck) Kontrolü
            # tool_signature = (tool_name, arguments_json) şeklinde bir imza oluştur.
            # Eğer bu imza state["tool_history"] içindeyse:
            # status'u 'stuck' yap, errors'a bilgi ekle ve döngüyü kır.
            arguments_json = json.dumps(arguments, sort_keys=True)
            tool_signature = (tool_name, arguments_json)
            
            if tool_signature in seen_signatures:
                state["status"] = "stuck"
                state["errors"].append(f"Agent got stuck repeating: {tool_name}")
                break
                
            seen_signatures.add(tool_signature)

            # TODO: execute_tool çağrısını bir try-except bloğu içine al
            try:
                tool_result = execute_tool(tool_name, arguments)
                state["messages"].append({
                                "role":"tool",
                                "content" :json.dumps(tool_result)
                            })
            # TODO: Başarılı işlem detayını state["tool_history"] listesine dictionary olarak ekle
            # Format: {"iteration": state["iteration"], "tool_name": tool_name, "arguments": arguments, "result": tool_result, "status": "success"}
                state["tool_history"].append({
                    "iteration": state["iteration"],
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "result": tool_result,
                    "status": "success"
                })    

            except Exception as e:
                # TODO: Hatayı bir string olarak değişkene al (Örn: error_msg = f"Tool Error: {str(e)}")
                error_msg = f"Tool Error: {str(e)}"
                
                # TODO: Bu hatayı state["errors"] listesine append ile ekle (Loglamak için)
                state["errors"].append(error_msg)
                
                # TODO: MODELİN HATAYI GÖRMESİ İÇİN: Hata mesajını "tool" rolüyle state["messages"] listesine ekle. 
                # (Böylece model "Ha, bu tool'da hata yaptım" diyip diğer iterasyonda düzeltebilecek)
                state["messages"].append({
                    "role": "tool",
                    "content": error_msg,
                })

                # TODO: Hatalı işlem detayını state["tool_history"] listesine dictionary olarak ekle
                # Format: {"iteration": state["iteration"], "tool_name": tool_name, "arguments": arguments, "result": error_msg, "status": "error"}
                state["tool_history"].append({
                    "iteration" : state["iteration"],
                    "tool_name" : tool_name,
                    "arguments" : arguments,
                    "result" : error_msg,
                    "status" : "error"
                })

        # TODO: Eğer içerdeki tool döngüsünde status 'stuck' olduysa, ana while döngüsünü de kır
        if state["status"] == "stuck":
            break

    return state
