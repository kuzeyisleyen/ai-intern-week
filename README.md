# AI Intern Week

**Proje Durumu:** Day 13 Tamamlandı (Week 3 devam ediyor)

> **Python, Temiz Kod, Otomatik Testler ve Açık Kaynaklı Yapay Zeka Modelleri (LLM)**
> Proje, temel mekanizmaları önce native Python ile görünür biçimde kurup, ihtiyaç ortaya çıktıktan sonra LangGraph gibi orchestration abstraction'larıyla eşlemeyi amaçlar.
---

## Gereksinimler

Projeyi sorunsuz çalıştırmak için bilgisayarınızda aşağıdakilerin kurulu olduğundan emin olun:

*   **Python** 3.10 veya üzeri
*   **Git** versiyon kontrol sistemi
*   **Docker** ve **Docker Compose**
*   Aktif bir internet bağlantısı

---

## Kullanılan Modeller

Proje boyunca yerel (local) çıkarım (inference), hızlı iterasyon ve düşük donanım tüketimi amacıyla aşağıdaki açık kaynaklı modeller tercih edilmiştir:

*   **SmolLM2-360M:** Hugging Face ekosisteminde (Day 2); Tokenizer yapısını anlama, Embedding vektörlerini inceleme ve metin üretim parametreleri (temperature, top_p) deneylerinde kullanılmıştır.
*   **qwen3:1.7b:** Ollama altyapısında (Day 4, 5 ve 8); JSON formatında yapılandırılmış çıktı (Structured Output) üretme, dış Python fonksiyonlarını tetikleme (Tool Calling), Otonom Ajan (Agent) senaryolarında ve RAG sisteminde "Grounded" (bağlama sadık) metin üretim motoru olarak kullanılmıştır.
*   **embeddinggemma:** Ollama altyapısında (Day 6, 7 ve 8); metinleri 768 boyutlu uzayda vektörlere dönüştürmek, Qdrant üzerinde "Kosinüs Benzerliği" (Cosine Similarity) aracılığıyla Anlamsal Arama (Semantic Search) motoru kurmak için kullanılmıştır.
*   **Qdrant/bm25 (FastEmbed):** Qdrant üzerinde yerel (local-first) işlem gücüyle sözcüksel (lexical/sparse) arama sinyallerini oluşturmak için Day 11 kapsamında eklenmiştir.

---

## Kurulum (Lokal Python Ortamı)

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
# Modüller
Day 1 (Temeller): Python temellerinin atıldığı modüldür. Koda; hata yönetimi, veri tipleri, döngüler ve uç durum (edge-case) güvenlik kontrolleri eklenmiştir. (Ana Script: day01/text_utils.py)

Day 2 (Hugging Face Laboratuvarı): Açık kaynaklı modellerin incelendiği laboratuvar günüdür. Token/Embedding kavramları ve metin üretim parametreleri üzerine deneyler yapılmıştır. (Ana Scriptler: day02/token_embedding_lab.py, day02/generation_experiment.py)

Day 3 (Docker Entegrasyonu): Projenin ve testlerin Docker Compose üzerine taşındığı, çıktıların output/ klasöründe kalıcı hale getirildiği geçiş günüdür. (Ana Script: day03/text_cli.py)

Day 4 (Yerel LLM ve Tool Calling): Ollama kullanılarak modelden yapılandırılmış veri (Structured Output) elde edildiği ve modelin Python fonksiyonlarını (Tool Calling) tetiklediği modüldür. (Ana Scriptler: day04/tool_call_demo.py, day04/ollama_client.py)

Day 5 (Otonom Ajan Mimarisi): LangChain olmadan sıfırdan otonom bir ajan motorunun yazıldığı modüldür. Sisteme; sonsuz döngü frenleri, kendini düzelten (Self-Correction) yapı ve gözlemlenebilirlik (Trace) altyapısı eklenmiştir. (Ana Scriptler: day05/agent_loop.py, day05/agent_cli.py)

Day 6 (Anlamsal Arama): Framework kullanmadan saf matematik ile Anlamsal Arama (Semantic Search) motorunun inşa edildiği modüldür. Kelime bazlı arama ile anlamsal arama kıyaslanmıştır. (Ana Scriptler: day06/similarity.py, day06/semantic_search_cli.py)

Day 7 (Vektör Veritabanı): Qdrant kullanılarak yerel bir vektör veritabanının ayağa kaldırıldığı, anlamsal arama ve meta veri filtreleme (metadata filtering) yeteneklerinin entegre edildiği modüldür. (Ana Scriptler: day07/ingest.py, day07/search.py)

Day 8 (Native RAG ve Evaluation): Dış bir framework kullanmadan sıfırdan "Retrieval-Augmented Generation" (RAG) mimarisinin kurulduğu modüldür. Dökümanları parçalama, Qdrant'ta arama, bağlam oluşturma (citation) ve Hit@k metrikleriyle arama motoru kalitesi ölçülmüştür. (Ana Scriptler: day08/rag_pipeline.py, day08/rag_cli.py, day08/evaluation.py)

Day 9 (LangGraph Orchestration): Native workflow ile LangGraph framework'ünün karşılaştırıldığı modüldür. Düğümler (nodes), kenarlar (edges) ve framework mimarisinin entegrasyonu tamamlanmıştır. (Ana Scriptler: day09/nodes.py, day09/graph_workflow.py, day09/graph_cli.py)

Day 10 (Reliability & Security Boundaries): Sistemin hata yönetiminin (Failure Injection, özel Exception sınıfları) güçlendirildiği ve modelin ürettiği kodu çalıştırmak için Docker düzeyinde (network none, read-only, tmpfs, non-root) güvenlik yalıtım sınırlarının (Sandbox) test edildiği 2. hafta kapanış modüldür. (Ana Script: day10_failure_experiments.py)

Day 11 (Retrieval Quality Engineering): Sisteme yeni bir arama yöntemi eklemeden önce Hit@k ve MRR (Mean Reciprocal Rank) metrikleriyle kalitenin ölçüldüğü modüldür. Dense (anlamsal), Lexical (sözcüksel) ve RRF (Reciprocal Rank Fusion) kullanan Hybrid arama stratejileri değerlendirme veri setleri üzerinden karşılaştırılmıştır. (Ana Scriptler: day11/ingest.py, day11/benchmark.py)

Day 12 (Model Context Protocol): Araç ve veri kaynağı keşfinin, tip doğrulamasının ve tetikleme sözleşmesinin standardize edildiği, statik bağımlılıkları ortadan kaldıran MCP entegrasyonu yapılmıştır. stdio transfer protokolüyle araç çağrıları ayrı bir istemci-sunucu katmanına ayrılmış, sözleşme hataları (contract errors) test edilerek LangGraph akışına bağımsız adaptörlerle bağlanmıştır. (Ana Scriptler: day12/mcp_server.py, day12/mcp_client.py, day12/mcp_adapter.py)

Day 13 (Durable Workflow & HITL): İş akışının kritik noktalarda duraklatılabilmesi (interrupt) ve kalıcı durum (persistent state) yönetimi için SQLite checkpointer entegre edilmiştir. Yüksek riskli işlemlerde insan onayı (Human-in-the-Loop) beklenmesi ve işlemlerin güvenle yeniden başlatılabilmesi için (idempotency) önlemler alınmıştır. (Ana Scriptler: day13/durable_graph.py, day13/hitl_cli.py, day13/trace.py)

# Çalıştırma (Docker Compose ile)
Aşağıdaki komutların tamamı terminale doğrudan yapıştırılıp test edilebilir şekilde ayarlanmıştır.
```bash
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

# 12. Day 9 LangGraph Orkestrasyonunu çalıştırın
docker compose run --rm app python -m day09.graph_cli "Ankara'ya 2 kg kargo ne kadar?"

# 13. Day 10 Hata Enjeksiyonu (Failure Injection) deneylerini çalıştırın
docker compose run --rm app python day10.failure_experiments

# 14. Day 10 Hata yönetimini (Exceptions) doğrulayan tüm birim testlerini (Unit Tests) çalıştırın
docker compose run --rm app python -m pytest -v -m "not integration"

# 15. Day 10 Kısıtlı Sandbox imajını derleyin (Build)
docker build -t sandbox-demo sandbox_demo

# 16. Day 10 Öğrenilen tüm güvenlik katmanlarını (Isolation Layers) içeren Canonical Sandbox Testini çalıştırın
docker run --rm --network none --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m --memory=128m --cpus=0.5 --pids-limit=64 --cap-drop=ALL --security-opt no-new-privileges=true sandbox-demo

# 17. Day 11 Hybrid collection ingestion (Veri yükleme)
docker compose run --rm app python -m day11.ingest

# 18. Day 11 Sadece Dense (Anlamsal) Benchmark testini çalıştırın
docker compose run --rm app python -m day11.benchmark --strategy dense

# 19. Day 11 Sadece Lexical/Sparse (Sözcüksel) Benchmark testini çalıştırın
docker compose run --rm app python -m day11.benchmark --strategy lexical

# 20. Day 11 Hybrid (Dense + Lexical) Benchmark testini çalıştırın
docker compose run --rm app python -m day11.benchmark --strategy hybrid

# 21. Day 11 Tüm arama stratejilerini yan yana test edip analiz edin
docker compose run --rm app python -m day11.benchmark --all

# 22. Day 12 MCP Stdio sunucusunu çalıştırın (Sunucu arka planda bekleyecektir, başka bir sekme gerekir)
docker compose run --rm app python -m day12.mcp_server

# 23. Day 12 İstemci (Client) keşif ve araç/veri kaynağı çekim yeteneklerini test edin
docker compose run --rm app python -m day12.mcp_client

# 24. Day 12 LangGraph orkestrasyonunu ve MCP entegrasyonunu (Not aracı testi) çalıştırın
docker compose run --rm app python -m day09.graph_cli "Notlarımda hybrid search hakkında ne yazıyor?"

# 25. Day 13 İlk durable run (İş akışı onaya kadar ilerleyip duraklatılır)
docker compose run --rm app python -m day13.hitl_cli start --thread-id demo-001 --action publish_report 

# 26. Day 13 Aynı thread'i approve (onay) kararı ile devam ettir (resume)
docker compose run --rm app python -m day13.hitl_cli resume --thread-id demo-001 --decision approve 

# 27. Day 13 Mevcut thread'in durumunu ve sıradaki düğümü kontrol et (inspect)
docker compose run --rm app python -m day13.hitl_cli inspect --thread-id demo-001 

```
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
├── day09/                  # 9. Gün LangGraph entegrasyonu, graph objesi ve node/edge yönetim kodları
├── day10/                  # 10. Gün Hata yönetimi (Exception), Failure Injection ve Security Sandbox incelemeleri
├── day11/                  # 11. Gün Dense, Lexical, Hybrid arama stratejileri, RRF füzyonu ve MRR/Hit@k kodları
├── day12/                  # 12. Gün Model Context Protocol sunucu, istemci, adaptör mekanizmaları ve observability trace'leri
├── day13/                  # 13. Gün Durable Workflow, SQLite checkpointer, HITL onayı ve Idempotency mekanizmaları
├── experiments/            # Otomatik kaydedilen deney sonuçları (JSON)
├── literature/             # Makale okuma notları ve teorik incelemeler
├── notes/                  # Teorik kavram cevapları ve framework mimari eşleştirmeleri
├── output/                 # Docker'dan host'a yazılan kalıcı trace, arama ve log çıktıları
├── reports/                # Günlük gelişim raporları (Blocker'lar ve öğrenimler)
├── sandbox_demo/           # 10. Gün Restricted Sandbox (Docker Security) laboratuvar dosyaları
├── tests/                  # Pytest ile yazılmış otomatik test senaryoları
├── .dockerignore           # Docker build context'e girmeyecek dosyalar
├── .gitignore              # Git tarafından takip edilmeyen dosyalar
├── compose.yaml            # Servis, volume ve environment tanımları
├── Dockerfile              # Proje imajının kurulum adımları
├── pytest.ini              # Pytest konfigürasyonu
├── README.md               # Proje dokümantasyonu
├── requirements-lab.txt    # Lokal deney kodları için ağır bağımlılıklar (torch, transformers)
└── requirements.txt        # Temel bağımlılıklar (pytest, requests, qdrant-client vb.)
```

# Bilinen Limitasyonlar
Donanım: Scriptler lokal cihazda CPU üzerinde çalışacak şekilde kurgulanmıştır.

# Model Ölçeği:
 Kullanılan modeller hızlı test için küçük boyutludur. Karmaşık mantık yürütme sorularında halüsinasyon riskleri yüksektir veya tool seçmekte zorlanabilirler. Bu limitasyon, ajan motorunun kendi kendini düzelten (self-correction) yapısını ve RAG sistemindeki kaynak zorunluluğunu (citation policy) test etmek için bir avantaja dönüştürülmüştür.