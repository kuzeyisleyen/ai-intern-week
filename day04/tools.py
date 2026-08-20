# day04/tools.py

def calculate_shipping_cost(city: str, weight_kg: float) -> dict:
    """
    Gönderilen şehre ve kiloya göre kargo maliyetini hesaplar.
    Kurallar: 
    - İstanbul için taban fiyat 50, 
    - Ankara için 60, 
    - Diğer şehirler için 75.
    - Kilo başına ekstra 12 TL eklenir.
    """
  
    if city == "İstanbul":
        taban_fiyat = 50
    if city == "Ankara" : 
        taban_fiyat = 60
    else:
        taban_fiyat= 75
        
    cost = taban_fiyat + (weight_kg*12)
    
    return {
        "city": city,
        "weight_kg": weight_kg,
        "cost": cost,
        "currency": "TRY"
    }

SHIPPING_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate_shipping_cost",
        "description": "Calculate a synthetic shipping cost for training purposes. Use this when user asks about shipping costs.",
        "parameters": {
            "type": "object",
            "required": ["city", "weight_kg"],
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Destination city (e.g., Ankara, Istanbul)"
                },
                "weight_kg": {
                    "type": "number",
                    "description": "Package weight in kilograms"
                }
            }
        }
    }
}