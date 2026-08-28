import pytest
from unittest.mock import patch
from day04.tool_dispatcher import execute_tool
from day10.exceptions import ResponseContractError, ToolRuntimeError

def test_unknown_tool():
    with pytest.raises(ResponseContractError, match="Güvenlik ihlali"):
        execute_tool("make_coffee", {"seker_miktari": 2})

def test_missing_argument():
    with pytest.raises(ResponseContractError):
        execute_tool("calculate_shipping_cost", {"city": "İstanbul"})

def test_wrong_type():
     with pytest.raises(ResponseContractError):
         execute_tool("calculate_shipping_cost", {"city": "İstanbul", "weight_kg": "beş kilo"})

def test_negative_value():
    with pytest.raises(ResponseContractError):
        execute_tool("calculate_shipping_cost", {"city": "İstanbul", "weight_kg": -4})

def test_tool_exception():

    def patlayan_arac(**kwargs):
        raise RuntimeError("boom")
        
    import day04.tool_dispatcher
    orijinal_liste = day04.tool_dispatcher.AVAILABLE_TOOLS.copy()
    
    try:
        day04.tool_dispatcher.AVAILABLE_TOOLS["patlayan_arac"] = patlayan_arac
        
        # 3. Şimdi çalıştırıyoruz ve Runtime hatasının ToolRuntimeError'a dönüşerek fırlatılmasını bekliyoruz!
        with pytest.raises(ToolRuntimeError):
            execute_tool("patlayan_arac", {"test_verisi": 123})
            
    finally:
        day04.tool_dispatcher.AVAILABLE_TOOLS = orijinal_liste