# AI Intern Week

# Amaç

Bu depo (repository), Python programlama disiplinini geliştirmek, temiz kod ve otomatik test alışkanlığı kazanmak, aynı zamanda açık kaynaklı yapay zeka modellerinin (LLM) temel çalışma prensiplerini (Token, Embedding, Base vs. Instruct, Generation Parametreleri, Tool Calling ve Otonom Ajanlar) kontrollü deneylerle uygulamalı olarak öğrenmek amacıyla hazırlanmıştır.

# Gereksinimler

Python 3.10 veya üzeri

Git

Docker ve Docker Compose

Aktif bir internet bağlantısı

# Kullanılan Modeller

Proje boyunca yerel (local) çıkarım (inference), hızlı iterasyon ve düşük donanım tüketimi amacıyla aşağıdaki açık kaynaklı küçük/orta ölçekli modeller tercih edilmiştir:

SmolLM2-360M: Hugging Face ekosisteminde (Day 2); Tokenizer yapısını anlama, Embedding vektörlerini inceleme ve metin üretim parametreleri (temperature, top_p) deneylerinde kullanılmıştır.

qwen3:1.7b: Ollama altyapısında (Day 4 ve Day 5); JSON formatında yapılandırılmış çıktı (Structured Output) üretme, dış Python fonksiyonlarını tetikleme (Tool Calling) ve çoklu adım gerektiren Otonom Ajan (Agent) senaryolarında orkestrasyon motoru olarak kullanılmıştır.

embeddinggemma: Ollama altyapısında (Day 6 ve Day 7); metinleri 768 boyutlu uzayda koordinatlara (vektörlere) dönüştürmek ve "Kosinüs Benzerliği" (Cosine Similarity) aracılığıyla Anlamsal Arama (Semantic Search) motoru mantığını kurmak için temsil modeli olarak kullanılmıştır.

# Kurulum (Lokal Python Ortamı)

Projeyi lokalinizde çalıştırmak isterseniz aşağıdaki adımları izleyebilirsiniz. Ancak 3. Gün itibarıyla projenin ana çalıştırma ortamı Docker Compose olarak belirlenmiştir.

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

Day 5 (Otonom Ajan Mimarisi ve Orkestrasyon)

Beşinci gün, LangChain gibi dış framework'lere bağımlı kalmadan sıfırdan (native) otonom bir ajan motorunun yazıldığı modüldür. Sisteme; sonsuz döngüleri engelleyen fren mekanizmaları (Termination Guards), hata durumlarında modelin kendini düzeltmesini sağlayan geri besleme döngüsü (Self-Correction) ve ajanın kararlarını şeffaflaştıran, şifre maskelemeli benzersiz ID'lere sahip bir gözlemlenebilirlik (Trace/Observability) altyapısı kazandırılmıştır.

Ana Scriptler: day05/agent_loop.py, day05/agent_cli.py, day05/trace_writer.py

Day 6 (Embedding ve Anlamsal Arama - Semantic Search)

Altıncı gün, framework kullanmadan saf matematik (Kosinüs Benzerliği) ile sıfırdan bir Anlamsal Arama (Semantic Search) motorunun inşa edildiği modüldür. Metinlerin uzaydaki yönlerini ölçerek çalışan sistem; Top-K sıralaması, Keyword (Kelime) araması ile Semantic (Anlamsal) aramanın kıyaslanması ve Retrieval Observability (Görünürlük) kavramlarının uygulamalı olarak deneyimlenmesini sağlamıştır.

Ana Scriptler: day06/similarity.py, day06/semantic_search.py, day06/semantic_search_cli.py, day06/final_experiment.py

Day 7 (Vektör Veritabanı ve Kalıcılık - Vector DB & Persistence)

Yedinci gün, Qdrant kullanılarak yerel bir vektör veritabanının ayağa kaldırıldığı, anlamsal arama (semantic search) ve meta veri filtreleme (metadata filtering) yeteneklerinin entegre edildiği modüldür. Veri kalıcılığı (persistence), bellek içi (in-memory) arama ile Qdrant'ın performans/mimari farkları ve geleneksel ilişkisel veritabanları (SQLite) ile vektör veritabanlarının (Exact vs. Semantic) farkları deneysel olarak incelenmiştir.

Ana Scriptler: day07/ingest.py, day07/search.py, day07/compare.py, day07/sqlite_vs_qdrant.py

Çalıştırma (Docker Compose ile)

Projenin bağımlılıkları ve çalışma ortamı Docker imajı içerisine paketlenmiştir. Projeyi ayağa kaldırmak ve çalıştırmak için:

# 1. Ollama (AI motoru) ve Qdrant (Vektör DB) servislerini arka planda başlatın (Day 4 ve sonrası için)
docker compose up -d ollama qdrant

# 2. App imajını inşa edin
docker compose build app

# 3. Uygulamayı çalıştırın (Örnek: Day 4 Tool Calling)
docker compose run --rm app python -m day04.tool_call_demo "Ankara'ya 3 desi kargo göndereceğim. Maliyeti hesapla."

# 4. Ajanı interaktif modda çalıştırın (Örnek: Day 5 Otonom Ajan CLI)
docker compose run --rm app python -m day05.agent_cli

# 5. Day 6 Semantic Search için 'embeddinggemma' modelini Ollama içerisine indirin
docker compose exec ollama ollama pull embeddinggemma

# 6. Day 6 Anlamsal Arama test uygulamasını çalıştırın
docker compose run --rm app python -m day06.semantic_search_cli

# 7. Day 7 Qdrant veritabanına dokümanları vektörleştirip yükleyin (Ingestion)
docker compose run --rm app python -m day07.ingest

# 8. Day 7 Qdrant üzerinde anlamsal arama (Semantic Search) yapın
docker compose run --rm app python -m day07.search "Container silinince verilerim kaybolmasın."

Test

Testler, uygulamanın çalıştığı environment ile aynı koşulları sağlaması amacıyla yalnızca Docker Compose üzerinden çalıştırılmalıdır.

# Sadece birim (Unit) testlerini çalıştırmak için:
docker compose run --rm app python -m pytest -v -m "not integration"

# Dış servislere (Ollama, Qdrant) bağlanan entegrasyon (Integration) testlerini çalıştırmak için:
docker compose run --rm app python -m pytest -v -m integration

Proje Yapısı

ai-intern-week/
├── day01/              # 1. Gün metin analizi kodları
├── day02/              # 2. Gün LLM ve tokenizer laboratuvar kodları
├── day03/              # 3. Gün Docker CLI ve Python uyarlamaları
├── day04/              # 4. Gün yerel LLM, yapılandırılmış çıktı ve Tool Calling kodları
├── day05/              # 5. Gün native ajan döngüsü, state yönetimi ve CLI kodları
├── day06/              # 6. Gün Embedding vektörleri, kosinüs benzerliği ve arama motoru kodları
├── day07/              # 7. Gün Qdrant vektör veritabanı, Ingestion, Search, SQL vs Vector DB deney kodları
├── output/             # Docker üzerinden host'a yazılan kalıcı trace, arama ve log çıktıları
├── experiments/        # Otomatik kaydedilen deney sonuçları (JSON)
├── literature/         # Makale (Toolformer, MRKL vb.) okuma notları ve teorik incelemeler
├── notes/              # Teorik kavram cevapları, araştırmalar ve framework mimari eşleştirmeleri
├── reports/            # Günlük gelişim raporları (Blocker'lar ve öğrenimler)
├── tests/              # Pytest ile yazılmış otomatik test senaryoları (Unit & Integration klasörleriyle)
├── .gitignore          # Git tarafından takip edilmeyen geçici/sistem dosyaları
├── .dockerignore       # Docker build context'e girmeyecek dosyalar
├── pytest.ini          # Pytest konfigürasyonu (Test discovery ve marker ayarları)
├── Dockerfile          # Proje imajının kurulum adımları
├── compose.yaml        # Servis, volume (ollama_data, qdrant_data) ve environment tanımları
├── requirements-lab.txt # Lokal laboratuvar/deney kodları için ağır bağımlılıklar (torch, transformers)
├── requirements.txt    # Docker ve lokal için temel bağımlılıklar (pytest, requests, qdrant-client vb.)
└── README.md           # Proje dokümantasyonu

Bilinen Limitasyonlar

Donanım: Scriptler lokal cihazda CPU üzerinde çalışacak şekilde kurgulanmıştır.

Model Ölçeği: Kullanılan modeller hızlı test için küçük boyutludur. Karmaşık mantık yürütme sorularında halüsinasyon riskleri yüksektir veya bazı durumlarda tool seçmekte/parametreyi doğru okumakta zorlanabilirler. Bu limitasyon, ajan motorunun kendi kendini düzelten (self-correction) yapısını test etmek için bir avantaja dönüştürülmüştür.