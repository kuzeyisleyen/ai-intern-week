import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from day02.text_utils_updated import analyze_text

# Pytest'in tanıyacağı 1. Test
def test_hello_world():
    sonuc = analyze_text("Hello world")
    # sonucun boş olmadığını iddia ediyoruz (assert)
    assert sonuc is not None

# Pytest'in tanıyacağı 2. Test
def test_empty_input():
    sonuc = analyze_text("")
    # İçi boş metin gönderdiğimizde hata vermeden çalışmalı
    assert sonuc is not None or sonuc == {}

# Pytest'in tanıyacağı 3. Test
def test_whitespace_input():
    sonuc = analyze_text("   ")
    assert sonuc is not None or sonuc == {}
