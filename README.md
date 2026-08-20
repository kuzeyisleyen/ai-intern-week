Markdown
# AI Intern Week

## Amaç
Bu depo (repository), Python programlama disiplinini geliştirmek, temiz kod ve otomatik test alışkanlığı kazanmak, aynı zamanda açık kaynaklı yapay zeka modellerinin (LLM) temel çalışma prensiplerini (Token, Embedding, Base vs. Instruct, Generation Parametreleri) kontrollü deneylerle uygulamalı olarak öğrenmek amacıyla hazırlanmıştır. 

## Gereksinimler
* Python 3.9 veya üzeri
* Git
* Docker ve Docker Compose 
* Aktif bir internet bağlantısı

## Kurulum (Lokal Python Ortamı)
Projeyi lokalinizde çalıştırmak isterseniz aşağıdaki adımları izleyebilirsiniz. Ancak 3. Gün itibarıyla projenin ana çalıştırma ortamı **Docker Compose** olarak belirlenmiştir.

```bash
# 1. Sanal ortam (virtual environment) oluşturun
python -m venv .venv

# 2. Sanal ortamı aktif edin (Windows)
.venv\Scripts\activate.bat
# (macOS/Linux)
source .venv/bin/activate

# 3. Temel bağımlılıkları yükleyin
python -m pip install -r requirements.txt

# Opsiyonel: 2. Gün gibi LLM/Tokenizer laboratuvar çalışmalarını lokalde çalıştırmak isterseniz ağır kütüphaneleri de kurun:
python -m pip install -r requirements-lab.txt
Modüller
Day 1
İlk gün, Python temellerinin atıldığı ve metin analizi araçlarının geliştirildiği modüldür. Koda; hata yönetimi, veri tipleri, döngüler ve uç durum (edge-case) güvenlik kontrolleri eklenmiştir.
Ana Script: day01/text_utils.py

Day 2
İkinci gün, Hugging Face ekosistemine giriş yapılan ve açık kaynaklı modellerin (SmolLM2-360M) incelendiği laboratuvar günüdür. Token/Embedding kavramları ve metin üretim parametreleri üzerine tekrarlanabilir deneyler yapılmıştır.
Ana Scriptler: day02/token_embedding_lab.py, day02/generation_experiment.py

Day 3 (Docker & Compose Entegrasyonu)
Üçüncü gün, projenin ve testlerin lokal Python ortamından bağımsızlaştırılarak Docker Compose üzerinden yönetildiği mimariye geçiş günüdür. Uygulama çıktıları (JSON, log vb.) bind mount yöntemiyle host makinedeki output/ klasöründe kalıcı hale getirilmiştir.
Ana Script: day03/text_cli.py

Day 4 (Yerel LLM ve Tool Calling)
Dördüncü gün, Ollama konteyneri kullanılarak yerel yapay zeka çıkarımının (local inference) sağlandığı, modelden yapılandırılmış veri (Structured Output) elde edildiği ve modelin Python fonksiyonlarını (Tool Calling) güvenli bir dispatcher üzerinden kullanmayı öğrendiği modüldür.
Ana Scriptler: day04/tool_call_demo.py, day04/problem_analyzer.py, day04/ollama_client.py

Çalıştırma (Docker Compose ile)
Projenin bağımlılıkları ve çalışma ortamı Docker imajı içerisine paketlenmiştir. Projeyi ayağa kaldırmak ve çalıştırmak için:

Bash
# 1. Ollama servisini (AI motorunu) arka planda başlatın (Day 4 ve sonrası için)
docker compose up -d ollama

# 2. App imajını inşa edin
docker compose build app

# 3. Uygulamayı çalıştırın (Örnek: Day 4 Tool Calling)
docker compose run --rm app python day04/tool_call_demo.py "Ankara'ya 3 kg paket göndereceğim. Maliyeti hesapla."
Test
Testler, uygulamanın çalıştığı environment ile aynı koşulları sağlaması amacıyla yalnızca Docker Compose üzerinden çalıştırılmalıdır.

Bash
# Sadece birim (Unit) testlerini çalıştırmak için:
docker compose run --rm app python -m pytest -v -m "not integration"

# Ollama servisine bağlanan entegrasyon (Integration) testlerini çalıştırmak için:
docker compose run --rm app python -m pytest -v -m integration
Proje Yapısı
Plaintext
ai-intern-week/
├── day01/                  # 1. Gün metin analizi kodları
├── day02/                  # 2. Gün LLM ve tokenizer laboratuvar kodları
├── day03/                  # 3. Gün Docker CLI ve Python uyarlamaları
├── day04/                  # 4. Gün yerel LLM, yapılandırılmış çıktı ve Tool Calling kodları
├── output/                 # Docker üzerinden host'a yazılan kalıcı çıktılar
├── experiments/            # Otomatik kaydedilen deney sonuçları (JSON)
├── literature/             # Makale (Toolformer vb.) okuma notları ve teorik incelemeler
├── notes/                  # Teorik kavram cevapları ve araştırmalar
├── reports/                # Günlük gelişim raporları (Blocker'lar ve öğrenimler)
├── tests/                  # Pytest ile yazılmış otomatik test senaryoları (Unit & Integration)
├── .gitignore              # Git tarafından takip edilmeyen geçici/sistem dosyaları
├── .dockerignore           # Docker build context'e girmeyecek dosyalar
├── pytest.ini              # Pytest konfigürasyonu (Test discovery ve marker ayarları)
├── Dockerfile              # Proje imajının kurulum adımları
├── compose.yaml            # Servis, volume (ollama_data) ve environment tanımları
├── requirements-lab.txt    # Lokal laboratuvar/deney kodları için ağır bağımlılıklar (torch, transformers)
├── requirements.txt        # Docker ve lokal için temel bağımlılıklar (pytest, requests vb.)
└── README.md               # Proje dokümantasyonu
Bilinen Limitasyonlar
Donanım: Scriptler lokal cihazda CPU üzerinde çalışacak şekilde kurgulanmıştır.

Model Ölçeği: Kullanılan modeller hızlı test için küçük boyutludur (SmolLM2-360M, qwen3:1.7b). Karmaşık mantık yürütme sorularında halüsinasyon riskleri yüksektir veya bazı durumlarda tool seçmekte zorlanabilirler.