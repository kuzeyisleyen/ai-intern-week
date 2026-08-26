#  AI Intern Week

> **Python, Temiz Kod, Otomatik Testler ve Açık Kaynaklı Yapay Zeka Modelleri (LLM)**
> Bu proje, yazılım mühendisliği disiplinlerini uygulayarak LLM'lerin çalışma prensiplerini (Token, Embedding, Tool Calling, Otonom Ajanlar ve RAG) sıfırdan ve framework kullanmadan inşa etmeyi amaçlayan bir staj simülasyonudur.

---

##  Gereksinimler

Projeyi sorunsuz çalıştırmak için bilgisayarınızda aşağıdakilerin kurulu olduğundan emin olun:

*   **Python** 3.10 veya üzeri
*   **Git** versiyon kontrol sistemi
*   **Docker** ve **Docker Compose**
*   Aktif bir internet bağlantısı

---

##  Kullanılan Modeller

Proje boyunca yerel (local) çıkarım (inference), hızlı iterasyon ve düşük donanım tüketimi amacıyla aşağıdaki açık kaynaklı modeller tercih edilmiştir:

*   **SmolLM2-360M:** Hugging Face ekosisteminde (Day 2); Tokenizer yapısını anlama, Embedding vektörlerini inceleme ve metin üretim parametreleri (temperature, top_p) deneylerinde kullanılmıştır.
*   **qwen3:1.7b:** Ollama altyapısında (Day 4, 5 ve 8); JSON formatında yapılandırılmış çıktı (Structured Output) üretme, dış Python fonksiyonlarını tetikleme (Tool Calling), Otonom Ajan (Agent) senaryolarında ve RAG sisteminde "Grounded" (bağlama sadık) metin üretim motoru olarak kullanılmıştır.
*   **embeddinggemma:** Ollama altyapısında (Day 6, 7 ve 8); metinleri 768 boyutlu uzayda vektörlere dönüştürmek, Qdrant üzerinde "Kosinüs Benzerliği" (Cosine Similarity) aracılığıyla Anlamsal Arama (Semantic Search) motoru kurmak için kullanılmıştır.

---

##  Kurulum (Lokal Python Ortamı)

Projeyi lokalinizde çalıştırmak isterseniz aşağıdaki adımları izleyebilirsiniz. *(Not: 3. Gün itibarıyla projenin ana çalıştırma ortamı Docker Compose olarak belirlenmiştir.)*

```bash
# 1. Sanal ortam (virtual environment) oluşturun
python -m venv .venv

# 2. Sanal ortamı aktif edin (Windows)
.venv\Scripts\activate.bat

# (macOS/Linux)
source .venv/bin/activate

# 3. Temel bağımlılıkları yükleyin
python -m pip install -r requirements.txt

# Opsiyonel: 2. Gün laboratuvar çalışmalarını lokalde çalıştırmak için ağır kütüphaneleri de kurun
python -m pip install -r requirements-lab.txt

```

#  Modüller
# Day 1 (Temeller):
 Python temellerinin atıldığı modüldür. Koda; hata yönetimi, veri tipleri, döngüler ve uç durum (edge-case) güvenlik kontrolleri eklenmiştir. (Ana Script: day01/text_utils.py)

# Day 2 (Hugging Face Laboratuvarı):
 Açık kaynaklı modellerin incelendiği laboratuvar günüdür. Token/Embedding kavramları ve metin üretim parametreleri üzerine deneyler yapılmıştır. (Ana Scriptler: day02/token_embedding_lab.py, day02/generation_experiment.py)

# Day 3 (Docker Entegrasyonu):
 Projenin ve testlerin Docker Compose üzerine taşındığı, çıktıların output/ klasöründe kalıcı hale getirildiği geçiş günüdür. (Ana Script: day03/text_cli.py)

# Day 4 (Yerel LLM ve Tool Calling):
 Ollama kullanılarak modelden yapılandırılmış veri (Structured Output) elde edildiği ve modelin Python fonksiyonlarını (Tool Calling) tetiklediği modüldür. (Ana Scriptler: day04/tool_call_demo.py, day04/ollama_client.py)

# Day 5 (Otonom Ajan Mimarisi):
 LangChain olmadan sıfırdan otonom bir ajan motorunun yazıldığı modüldür. Sisteme; sonsuz döngü frenleri, kendini düzelten (Self-Correction) yapı ve gözlemlenebilirlik (Trace) altyapısı eklenmiştir. (Ana Scriptler: day05/agent_loop.py, day05/agent_cli.py)

# Day 6 (Anlamsal Arama):
 Framework kullanmadan saf matematik ile Anlamsal Arama (Semantic Search) motorunun inşa edildiği modüldür. Kelime bazlı arama ile anlamsal arama kıyaslanmıştır. (Ana Scriptler: day06/similarity.py, day06/semantic_search_cli.py)

# Day 7 (Vektör Veritabanı):
 Qdrant kullanılarak yerel bir vektör veritabanının ayağa kaldırıldığı, anlamsal arama ve meta veri filtreleme (metadata filtering) yeteneklerinin entegre edildiği modüldür. (Ana Scriptler: day07/ingest.py, day07/search.py)

# Day 8 (Native RAG ve Evaluation):
 Dış bir framework kullanmadan sıfırdan "Retrieval-Augmented Generation" (RAG) mimarisinin kurulduğu modüldür. Dökümanları parçalama, Qdrant'ta arama, bağlam oluşturma (citation) ve Hit@k metrikleriyle arama motoru kalitesi ölçülmüştür. (Ana Scriptler: day08/rag_pipeline.py, day08/rag_cli.py, day08/evaluation.py)

#  Çalıştırma (Docker Compose ile)
Projenin tüm bağımlılıkları Docker imajı içerisine paketlenmiştir. Projeyi ayağa kaldırmak için:


```bash
# 1. Ollama (AI motoru) ve Qdrant (Vektör DB) servislerini arka planda başlatın
docker compose up -d ollama qdrant

# 2. App imajını inşa edin
docker compose build app

# 3. Uygulamayı çalıştırın (Örnek: Day 4 Tool Calling)
docker compose run --rm app python -m day04.tool_call_demo "Ankara'ya 3 desi kargo göndereceğim. Maliyeti hesapla."

# 4. Ajanı interaktif modda çalıştırın (Örnek: Day 5)
docker compose run --rm app python -m day05.agent_cli

# 5. Day 6 Semantic Search için 'embeddinggemma' modelini indirin
docker compose exec ollama ollama pull embeddinggemma

# 6. Day 6 Anlamsal Arama uygulamasını çalıştırın
docker compose run --rm app python -m day06.semantic_search_cli

# 7. Day 7 Qdrant Ingestion (Veri yükleme)
docker compose run --rm app python -m day07.ingest

# 8. Day 7 Qdrant Arama (Semantic Search)
docker compose run --rm app python -m day07.search "Container silinince verilerim kaybolmasın."

# 9. Day 8 RAG sistemi için dökümanları Qdrant'a kaydedin (Ingestion)
docker compose run --rm app python -m day08.ingest

# 10. Day 8 Uçtan uca RAG sistemine soru sorun
docker compose run --rm app python -m day08.rag_cli "Named volume ne zaman kullanılır?"

# 11. Day 8 RAG sisteminin arama motoru kalitesini (Hit@k) ölçün
docker compose run --rm app python -m day08.evaluation

```
# Test
Testler, ortam tutarsızlıklarını önlemek için yalnızca Docker Compose üzerinden çalıştırılmalıdır.

```bash
# Sadece birim (Unit) testlerini çalıştırmak için:
docker compose run --rm app python -m pytest -v -m "not integration"

# Dış servislere (Ollama, Qdrant) bağlanan entegrasyon testlerini çalıştırmak için:
docker compose run --rm app python -m pytest -v -m integration

```
# Proje Yapısı
```
ai-intern-week/
├── day01/                  # 1. Gün metin analizi kodları
├── day02/                  # 2. Gün LLM ve tokenizer laboratuvar kodları
├── day03/                  # 3. Gün Docker CLI ve Python uyarlamaları
├── day04/                  # 4. Gün yerel LLM, yapılandırılmış çıktı ve Tool Calling kodları
├── day05/                  # 5. Gün native ajan döngüsü, state yönetimi ve CLI kodları
├── day06/                  # 6. Gün Embedding vektörleri, kosinüs benzerliği ve arama motoru kodları
├── day07/                  # 7. Gün Qdrant vektör DB, Ingestion ve Vector DB deney kodları
├── day08/                  # 8. Gün Native RAG, chunking, context builder ve evaluation kodları
├── output/                 # Docker'dan host'a yazılan kalıcı trace, arama ve log çıktıları
├── experiments/            # Otomatik kaydedilen deney sonuçları (JSON)
├── literature/             # Makale okuma notları ve teorik incelemeler
├── notes/                  # Teorik kavram cevapları ve framework mimari eşleştirmeleri
├── reports/                # Günlük gelişim raporları (Blocker'lar ve öğrenimler)
├── tests/                  # Pytest ile yazılmış otomatik test senaryoları
├── .gitignore              # Git tarafından takip edilmeyen dosyalar
├── .dockerignore           # Docker build context'e girmeyecek dosyalar
├── pytest.ini              # Pytest konfigürasyonu
├── Dockerfile              # Proje imajının kurulum adımları
├── compose.yaml            # Servis, volume ve environment tanımları
├── requirements-lab.txt    # Lokal deney kodları için ağır bağımlılıklar (torch, transformers)
├── requirements.txt        # Temel bağımlılıklar (pytest, requests, qdrant-client vb.)
└── README.md               # Proje dokümantasyonu
```

# Bilinen Limitasyonlar
Donanım: Scriptler lokal cihazda CPU üzerinde çalışacak şekilde kurgulanmıştır.

Model Ölçeği: Kullanılan modeller hızlı test için küçük boyutludur. Karmaşık mantık yürütme sorularında halüsinasyon riskleri yüksektir veya tool seçmekte zorlanabilirler. Bu limitasyon, ajan motorunun kendi kendini düzelten (self-correction) yapısını ve RAG sistemindeki kaynak zorunluluğunu (citation policy) test etmek için bir avantaja dönüştürülmüştür.