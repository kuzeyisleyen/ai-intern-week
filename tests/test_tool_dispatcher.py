import pytest
from unittest.mock import patch
from day04.tool_dispatcher import execute_tool

def test_unknown_tool():
    sonuc = execute_tool("make_coffee", {"seker_miktari": 2})
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

def test_tool_exception():
    # KANIT: Parametreler doğru olsa bile, içeride çalışan kod beklenmedik bir sistem hatası 
    # (Runtime Exception) fırlatırsa, sistemin bunu güvenle yakaladığını kanıtlar.
    
    # 1. Kasıtlı olarak patlayan sahte bir araç yazıyoruz
    def patlayan_arac(**kwargs):
        raise RuntimeError("boom")
        
    # 2. Bunu dispatcher'ın okuduğu kayıt defterine çaktırmadan ekliyoruz (gerçek 'tools' içindeki import'lara dokunmadan)
    import day04.tool_dispatcher
    orijinal_liste = day04.tool_dispatcher.AVAILABLE_TOOLS.copy()
    
    try:
        # Sahte aracı sisteme kaydediyoruz
        day04.tool_dispatcher.AVAILABLE_TOOLS["patlayan_arac"] = patlayan_arac
        
        # 3. Şimdi çalıştırıyoruz!
        sonuc = execute_tool("patlayan_arac", {"test_verisi": 123})
        
        # Sonuçta 'error' anahtarı olmalı (yani try-except ile yakalanmış olmalı)
        assert "error" in sonuc
        
    finally:
        # Test bitince ortalığı temizleyip orijinal listeyi geri koyuyoruz ki diğer testler bozulmasın
        day04.tool_dispatcher.AVAILABLE_TOOLS = orijinal_liste