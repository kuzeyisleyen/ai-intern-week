from day04.tools import calculate_shipping_cost
from day02.text_utils_updated import analyze_text
from day10.exceptions import ResponseContractError, ToolRuntimeError

AVAILABLE_TOOLS = {
    "calculate_shipping_cost": calculate_shipping_cost,
    "analyze_text": analyze_text
}

def execute_tool(tool_name: str, arguments: dict) -> dict:

    if tool_name not in AVAILABLE_TOOLS:
        raise ResponseContractError(f"Güvenlik ihlali:Tool {tool_name} bulunamadı.")

    if tool_name == "calculate_shipping_cost":
        # 1. Fazla argüman reddi (Strict Boundary)
        allowed_keys = {"city", "weight_kg"}
        actual_keys = set(arguments.keys())
        if not actual_keys.issubset(allowed_keys):
            raise ResponseContractError(f"Beklenmeyen parametreler reddedildi: {actual_keys - allowed_keys}")

        city = arguments.get("city")
        weight_kg = arguments.get("weight_kg")
  
        if not city:
            raise ResponseContractError("Şehir bilgisi eksik") 
        if weight_kg is None:
            raise ResponseContractError("Kilo bilgisi eksik")
  
        try:
            weight_kg = float(weight_kg)
        except ValueError:
            raise ResponseContractError("Kilo sayısal bir değere dönüştürülemedi.")
            
        if weight_kg <= 0:
            raise ResponseContractError("Geçersiz kilo, sıfırdan büyük olmalı.")
            
        # Doğrulanmış veriyi sözlüğe geri yaz
        arguments["weight_kg"] = weight_kg

    elif tool_name == "analyze_text":
        allowed_keys = {"text"}
        actual_keys = set(arguments.keys())
        
        if not actual_keys.issubset(allowed_keys):
            raise ResponseContractError(f"Beklenmeyen parametreler reddedildi: {actual_keys - allowed_keys}")
        text = arguments.get("text")
        if not text:
            raise ResponseContractError("Metin bilgisi eksik veya boş")
        if not isinstance(text, str):
            raise ResponseContractError("Analiz edilicek veri string formatında olmalıdır.")

    # Güvenli Execution 
    fonksiyon = AVAILABLE_TOOLS[tool_name]
    try:
        sonuc = fonksiyon(**arguments)
        return sonuc
    except Exception as e:
        raise ToolRuntimeError(f"Tool çalışma zamanı hatası: {str(e)}")