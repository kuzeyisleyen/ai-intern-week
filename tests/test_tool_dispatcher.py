import pytest
from day04.tool_dispatcher import execute_tool

def test_unknown_tool():
    sonuc = execute_tool("calculate_shipping_cost", {"city": "İstanbul", "weight_kg": -4})
    assert "error" in sonuc

def test_missing_argument():
    sonuc = execute_tool("calculate_shipping_cost", {"city": "İstanbul"})
    assert "error" in sonuc

def test_wrong_type():
     sonuc = execute_tool("calculate_shipping_cost", {"city": "İstanbul", "weight_kg": "beş kilo"})
     assert "error" in sonuc

def test_negative_value():
    sonuc = execute_tool("calculate_shipping_cost", {"city": "İstanbul", "weight_kg": -4})
    assert "error" in sonuc