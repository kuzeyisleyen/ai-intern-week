from day04.tools import calculate_shipping_cost
from day02.text_utils_updated import analyze_text

AVAILABLE_TOOLS = {
    "calculate_shipping_cost": calculate_shipping_cost,
    "analyze_text": analyze_text
}

def execute_tool(tool_name: str, arguments: dict) -> dict:

    if tool_name not in AVAILABLE_TOOLS:
        return {"error": f"Tool '{tool_name}' bulunamadı veya izinsiz."}

    if tool_name == "calculate_shipping_cost":
        city = arguments.get("city")
        weight_kg = arguments.get("weight_kg")
  
        if city is None: 
            return {"error": "Şehir bilgisi eksik"}
        if weight_kg is None:
            return {"error": "Kilo bilgisi eksik"}
  
        if not isinstance(weight_kg, (int, float)):
            return {"error": "Kilo sayısal bir değer olmalıdır (int veya float)."}
     
        if weight_kg <= 0:
            return {"error": "Geçersiz kilo, sıfırdan büyük olmalı"}

        # TODO 2: Eğer tool_name "analyze_text" ise, 'text' parametresinin varlığını ve string olup olmadığını kontrol eden bir validation (if) bloğu ekle
        # İpucu: arguments.get("text") boş mu diye bakabilir ve isinstance(text, str) ile kontrol edebilirsin.

        if tool_name == "analyze_text":
            text = arguments.get("text")
            if text is None:
                return {"error": "Metin (text) bilgisi eksik."}
        
            if not isinstance(text, str):
                return {"error": "Analiz edilecek veri string (metin) formatında olmalıdır."}

    # 5. Güvenli Execution 
    fonksiyon = AVAILABLE_TOOLS[tool_name]
    try:
        sonuc = fonksiyon(**arguments)
        return sonuc
    except Exception as e:
        return {"error": f"Tool çalışırken hata oluştu: {str(e)}"}