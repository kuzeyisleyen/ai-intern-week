import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from day02.text_utils_updated import analyze_text

def test_hello_world():
    sonuc = analyze_text("Hello world")
    assert sonuc["word_count"] == 2


def test_empty_input():
    sonuc = analyze_text("")
    assert sonuc["word_count"] == 0

def test_whitespace_input():
    sonuc = analyze_text("   ")
    assert sonuc["word_count"] == 0


def test_repeated_words():
    sonuc = analyze_text("test test test")
    assert sonuc["word_count"] == 3
    assert sonuc["unique_word_count"] == 1

def test_punctuation_and_case():
    sonuc = analyze_text("Hello World!This is a test.")
    assert sonuc["word_count"] == 6
    assert sonuc["unique_word_count"] == 6

"""
normal metin
boş string
yalnızca whitespace
tekrar eden kelimeler
noktalama ve büyük/küçük harf
"""