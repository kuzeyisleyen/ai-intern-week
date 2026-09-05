# AI Intern Week
---
## What This Repository Demonstrates
Bu proje, yapay zeka destekli bir sistemin temel mekanizmalarından üretim kalitesindeki (production-ready) mimarisine kadar uzanan üç haftalık inşa sürecini gösterir. Temel mühendislik prensibi olarak "native-first → framework later" (önce saf Python, sonra orkestrasyon) yaklaşımı benimsenmiştir.
---

## Architecture
Sistem, donanım tüketimini düşük tutmak ve yerel (local) cihazlarda çalışabilmek için tamamen açık kaynaklı modeller ve modüler konteynerler üzerine kurulmuştur.
* **Generation & Routing:** Yapılandırılmış çıktı (structured output), araç kullanımı (tool calling) ve iki aşamalı yönlendirme (two-stage routing) için Ollama altyapısında `qwen3:1.7b` modeli kullanılmıştır.
* **Embedding & Vector Space:** Metinleri 768 boyutlu uzayda vektörlere dönüştürmek için `embeddinggemma` modeli entegre edilmiştir.
* **Storage & Retrieval:** Vektör (Dense) ve sözcüksel (Lexical/BM25) arama sinyallerini RRF (Reciprocal Rank Fusion) ile birleştiren hibrit arama altyapısı Qdrant üzerinde çalıştırılmaktadır.

## Core Learning Progression

### Week 1 — Native Foundations
Python temelleri ve açık kaynaklı modellerin incelenmesiyle başlanmıştır. Çalışma ortamı Docker üzerine taşınmış ve modelin Python fonksiyonlarını tetiklediği (Tool Calling) mekanizmalar kurulmuştur. Haftanın sonunda, orkestrasyon araçları olmadan saf Python ile sonsuz döngü frenlerine ve kendini düzeltme (self-correction) yeteneğine sahip otonom bir ajan motoru inşa edilmiştir.

### Week 2 — Retrieval, RAG, Workflow, Reliability
Saf matematik ile kosinüs benzerliği algoritmaları yazılarak temeller atılmış, ardından sisteme Qdrant vektör veritabanı entegre edilmiştir. Uçtan uca native RAG mimarisi inşa edilerek arama kalitesi (Hit@k) ölçülmüştür. Hafta sonuna doğru LangGraph orkestrasyonuna geçilmiş, hata enjeksiyonu (failure injection) yöntemleriyle sistemin dayanıklılığı sınanmıştır.

### Week 3 — Evaluation, MCP, Durability, Observability
Qdrant üzerinde Dense, Lexical ve Hybrid (RRF) arama stratejilerinin kıyaslandığı kalite mühendisliği çalışmaları yapılmıştır. Model Context Protocol (MCP) `stdio` sunucu/istemci mimarisi kurularak bağımsız araç adaptörleri sisteme entegre edilmiştir. İş akışlarına kalıcılık (durability) sağlamak için LangGraph SQLite checkpointer eklenmiş, yüksek riskli işlemlere insan onayı (HITL) şartı getirilmiştir. Süreç, Semantic Router A/B testleri, OpenTelemetry standartlarında Observability ("Span") entegrasyonu ve uçtan uca Golden Dataset değerlendirmesiyle noktalanmıştır.

## Quick Start
Sistemi yerel ortamda başlatmak için Python 3.10.21, Git, Docker ve Docker Compose gereklidir.

```bash
# 1. Altyapı servislerini (Ollama ve Qdrant) başlatın
docker compose up -d ollama qdrant

# 2. Embedding modelini indirin
docker compose exec ollama ollama pull embeddinggemma

# 3. Ana uygulama imajını inşa edin
docker compose build app
```
## Main Demos
```bash
# Native Ajanı interaktif modda başlatmak (Week 1)
docker compose run --rm app python -m day05.agent_cli

# RAG sistemine soru sormak (Week 2)
docker compose run --rm app python -m day08.rag_cli "Named volume ne zaman kullanılır?"

# MCP entegrasyonuyla LangGraph çalıştırmak (Week 3)
docker compose run --rm app python -m day09.graph_cli "Notlarımda hybrid search hakkında ne yazıyor?"

# İnsan onaylı (HITL) bir iş akışını başlatmak (Week 3)
docker compose run --rm app python -m day13.hitl_cli start --thread-id demo-001 --action publish_report
```
## Testing
Testler, dış ağa/modele giden bileşenleri izole ederek (mocking) milisaniyeler içinde deterministik sonuçlar üretecek şekilde kurgulanmıştır.
```bash
# Hata yönetimini doğrulayan hızlı birim (Unit) testleri
docker compose run --rm app python -m pytest -q -m "not integration"

# Dış bağımlılıkları test eden entegrasyon (Integration) testleri
docker compose run --rm app python -m pytest -q -m integration

# Kontrollü kriz ve hata toleransı tatbikatı
docker compose run --rm app python -m day15.failure_experiements

```
## Evaluation
Projedeki semantic-router politikası, varsayımlar yerine evidence-driven (kanıt odaklı) bir tasarıma dayanır.
```bash
# Arama stratejileri (Hybrid/Lexical/Dense) benchmark analizi
docker compose run --rm app python -m day11.benchmark --all

# Uçtan uca sistem değerlendirmesi ve Rota/Ajan analizi
docker compose run --rm app python -m day14.evaluate --all

# Üretim Kalitesi (Production) Kanıt Raporu (JSON) oluşturma
docker compose run --rm app python -m day15.capstone --all
```
## CI
Sistem "Ayrıştırılmış CI" (Bifurcated CI) stratejisine sahiptir. Deterministik olan birim ve entegrasyon testleri uzak CI sunucularında (hard gate) çalıştırılırken; probabilistik yapıdaki LLM, RAG ve End-to-End değerlendirme testleri yerel ortamda (Local CI) çalıştırılarak sonuçlar statik bir kanıt dosyasına (output/day15-capstone-summary.json) mühürlenir.

## Safety Boundaries
Mimari kurgulanırken ve değerlendirilirken sistemin sınırları şu gerçeklikler üzerine oturtulmuştur:
*MCP ≠ sandbox (Sadece protokol izolasyonudur)
*LLM router ≠ authorization (Yapay zeka sadece niyet belirler, izni Tool Allowlist verir)
*citation validation ≠ semantic grounding
*SQLite checkpoint ≠ backup (Sadece durum hafızasıdır)
*Docker ≠ perfect sandbox
*semantic-router policy = evidence-driven (A/B testleriyle kanıtlanmıştır)

## Known Limitations
*Tüm mimari, scriptler ve veritabanı yerel cihazlarda CPU üzerinde çalışacak şekilde optimize edilmiştir.
*Hızlı iterasyon amacıyla seçilen küçük parametreli LLM (qwen3:1.7b), çok katmanlı yönlendirme senaryolarında niyet karmaşası (intent confusion) yaşayabilmekte ve araç sorgularını bilgi (knowledge) rotasına yönlendirebilmektedir. Bu durum, mimarideki fallback mekanizmalarını ve kontrollü hata (graceful degradation) yönetimini test etmek için kullanılmıştır.
```bash
ai-intern-week/
├── .github/workflows/      # CI/CD pipeline yapılandırması (ci.yml)
├── .pytest_cache/          # Pytest önbellek dosyaları (göz ardı edilir)
├── .venv/                  # Lokal Python sanal ortamı (göz ardı edilir)
├── .vscode/                # VS Code çalışma alanı ayarları
├── day01/                  # Metin analizi ve native veri tipleri
├── day02/                  # Tokenizer ve Embedding laboratuvarı
├── day03/                  # Docker CLI uyarlamaları
├── day04/                  # Yerel LLM, yapılandırılmış çıktı ve Tool Calling
├── day05/                  # Native ajan döngüsü ve self-correction mekanizmaları
├── day06/                  # Kosinüs benzerliği ve arama motoru temelleri
├── day07/                  # Qdrant vektör DB ve Ingestion
├── day08/                  # Native RAG, chunking ve evaluation
├── day09/                  # LangGraph orkestrasyonu (nodes/edges)
├── day10/                  # Exception yönetimi ve Failure Injection sınırları
├── day11/                  # Hybrid (RRF), Dense, Lexical strateji benchmarkları
├── day12/                  # MCP stdio client/server adaptör mekanizmaları
├── day13/                  # SQLite Checkpointer, HITL onayı ve Idempotency
├── day14/                  # System Evaluation, Semantic Router ve Observability
├── day15/                  # Production CI, Capstone ve Drill operasyonları
├── docs/                   # Mimari ve bileşen dokümantasyonları
├── experiments/            # Otomatik kaydedilen deney sonuçları (JSON)
├── literature/             # Makale okuma notları ve teorik incelemeler
├── notes/                  # Teorik kavram cevapları ve framework mimari eşleştirmeleri
├── output/                 # Kalıcı trace, değerlendirme (eval) ve log çıktıları
├── reports/                # Günlük gelişim raporları (Blocker'lar ve öğrenimler)
├── sandbox_demo/           # Restricted Sandbox (Docker Security) laboratuvar dosyaları
├── tests/                  # Pytest birim ve entegrasyon senaryoları
├── .dockerignore           # Docker build context'e girmeyecek dosyalar
├── .gitignore              # Git tarafından takip edilmeyen dosyalar
├── compose.yaml            # Servis, volume ve environment tanımları
├── Dockerfile              # Proje imajının kurulum adımları
├── pytest.ini              # Pytest yapılandırması
├── README.md               # Proje dokümantasyonu
├── requirements-lab.txt    # Lokal deney kodları için ağır bağımlılıklar
└── requirements.txt        # Temel paket bağımlılıkları
```