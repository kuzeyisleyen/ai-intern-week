from tools import calculate_shipping_cost

AVAILABLE_TOOLS = {
    "calculate_shipping_cost": calculate_shipping_cost
}

def execute_tool(tool_call: dict) -> dict:
    tool_name = tool_call.get("name")
    arguments = tool_call.get("arguments", {})
    
    # Tool bizde var mı?
    if tool_name not in AVAILABLE_TOOLS:
        return {"error": f"Tool '{tool_name}' bulunamadı veya izinsiz."}
        
    # Kargo fonksiyonu için özel güvenlik kontrolleri
    if tool_name == "calculate_shipping_cost":
        city = arguments.get("city")
        weight_kg = arguments.get("weight_kg")
        
    if not city : 
        return {"error":"şehir bilgisi eksik"}
    if weight_kg <= 0 :
        return {"error": "Geçersiz kilo sıfırdan büyük olmalı"}
       

    
    fonksiyon = AVAILABLE_TOOLS[tool_name]
    try:
        sonuc = fonksiyon(**arguments)
        return sonuc
    except Exception as e:
        return {"error": f"Tool çalışırken hata oluştu: {str(e)}"}