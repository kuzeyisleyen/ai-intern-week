from day04.tools import calculate_shipping_cost

def test_istanbul_cost():
    sonuc = calculate_shipping_cost("İstanbul",2)
    assert sonuc["cost"] == 74