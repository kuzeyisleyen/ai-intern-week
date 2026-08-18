# AI Intern Week

## Amaç
Bu depo (repository), Python programlama disiplinini geliştirmek, temiz kod ve otomatik test alışkanlığı kazanmak, aynı zamanda açık kaynaklı yapay zeka modellerinin (LLM) temel çalışma prensiplerini (Token, Embedding, Base vs. Instruct, Generation Parametreleri) kontrollü deneylerle uygulamalı olarak öğrenmek amacıyla hazırlanmıştır.

## Gereksinimler
* Python 3.9 veya üzeri
* Git
* Aktif bir internet bağlantısı (Modellerin ilk kurulumda Hugging Face üzerinden indirilmesi için gereklidir)

## Kurulum
Projeyi bilgisayarınıza klonladıktan sonra, kütüphane çakışmalarını önlemek için bağımlılıkları izole bir sanal ortamda (virtual environment) kurmanız önerilir. Aşağıdaki adımları sırasıyla terminalinizde çalıştırın:


# 1. Sanal ortam (virtual environment) oluşturun
python -m venv .venv

# 2. Sanal ortamı aktif edin
# Windows (Command Prompt) için:
.venv\Scripts\activate.bat

# Windows (PowerShell) için:
.venv\Scripts\Activate.ps1

# macOS ve Linux için:
source .venv/bin/activate

# 3. Gerekli kütüphaneleri (PyTorch, Transformers, Pytest vb.) yükleyin
python -m pip install -r requirements.txt


Day 1
İlk gün, Python temellerinin atıldığı ve metin analizi araçlarının geliştirildiği modüldür. Koda; hata yönetimi (try/except), veri tipleri, döngüler (while) ve beklenmeyen girdiler (boş string, whitespace vb.) için uç durum (edge-case) güvenlik kontrolleri eklenmiştir.

Ana Script: day01/text_utils.py

Day 2
İkinci gün, Hugging Face ekosistemine giriş yapılan ve açık kaynaklı modellerin incelendiği laboratuvar günüdür. SmolLM2-360M (Base) ve SmolLM2-360M-Instruct modelleri kullanılarak model kartı okuma, Token/Token ID/Embedding kavramları arasındaki yapısal farklar ve metin üretim parametreleri (Greedy, Sampling, Temperature) üzerine tekrarlanabilir deneyler yapılmıştır.

Ana Scriptler:

day02/token_embedding_lab.py

day02/open_model_compare.py

day02/generation_experiment.py

Çalıştırma
Sanal ortamınız aktif durumdayken, incelemek istediğiniz günün scriptini terminal üzerinden çalıştırabilirsiniz. Deney sonuçları JSON formatında ilgili klasöre kaydedilecektir.

Örnek bir metin üretim (generation) deneyini başlatmak için:

python day02/generation_experiment.py

Test
Proje içerisindeki temel fonksiyonların ve edge-case'lerin (uç durumların) doğruluk kontrolleri pytest kütüphanesi kullanılarak otomatikleştirilmiştir. Tüm test senaryolarını çalıştırmak için proje ana dizininde şu komutu kullanın:

python -m pytest -v

Proje Yapısı

ai-intern-week/
├── day01/                  # 1. Gün metin analizi kodları
├── day02/                  # 2. Gün LLM ve tokenizer laboratuvar kodları
├── experiments/            # Otomatik kaydedilen deney sonuçları (JSON)
├── notes/                  # Teorik kavram cevapları ve model karşılaştırma tabloları
├── reports/                # Günlük gelişim raporları (Blocker'lar ve öğrenimler)
├── tests/                  # Pytest ile yazılmış otomatik test senaryoları
├── .gitignore              # Git tarafından takip edilmeyen geçici/sistem dosyaları
├── requirements.txt        # Projenin çalışması için gereken paketlerin listesi
└── README.md               # Proje kurulum ve kullanım dokümantasyonu

Bilinen Limitasyonlar

Donanım: Scriptler lokal cihazda CPU üzerinde çalışacak şekilde kurgulanmıştır. GPU bulunmayan cihazlarda metin üretimi (generation) birkaç saniye sürebilir.

Model Ölçeği: Deneylerde kullanılan modeller hızlı test edilebilmesi için küçük boyutludur (360 Milyon parametre). Bu sebeple karmaşık mantık yürütme sorularında veya varsayımsal senaryolarda halüsinasyon (yanlış bilgi uydurma) riskleri yüksektir.