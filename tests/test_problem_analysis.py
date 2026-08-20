from day04.schema_cli import validate_problem_analysis

def test_validate_problem_analysis_success():
    """Doğru veri geldiğinde True dönmeli."""
    
   
    gecerli_veri = {
        "summary": "Müşteriler kargodan şikayetçi.",       
        "category": "Lojistik",                           
        "risks": ["Müşteri kaybı", "Marka zedelenmesi"],  
        "next_step": "Kargo firmasıyla görüşülecek."      
    }
    

    sonuc = validate_problem_analysis(gecerli_veri)
    assert sonuc == True

def test_validate_problem_analysis_missing_key():
    """Eksik anahtar geldiğinde False dönmeli."""

    hatali_veri = {
                   "summary": "Müşteriler kargodan şikayetçi.",       
                   "category": "Lojistik",                           
                   "next_step": "Kargo firmasıyla görüşülecek."  
    }
    
    sonuc = validate_problem_analysis(hatali_veri)
    assert sonuc == False

def test_validate_problem_analysis_wrong_type():
    """Yanlış tip (örneğin risks liste değil de string ise) False dönmeli."""
    
    tipi_hatali_veri = {
            "summary": "Müşteriler kargodan şikayetçi.",       
             "category": "Lojistik",                           
             "risks": "Müşteri Kaybı",  
             "next_step": "Kargo firmasıyla görüşülecek."  
    }
    

    sonuc = validate_problem_analysis(tipi_hatali_veri)
    assert sonuc == False