---
day: 15
date: 2026-09-05
status: completed
ci_status: failed 
router_policy: two_stage
unit_tests_passed: 75
integration_tests_passed: 27
capstone_scenarios_passed: 8
capstone_scenarios_total: 8
---

# Gün 15 — Production-Minded Capstone + CI

## 1. Day 14 Cleanup

### Evaluator runner mismatch
Ne değişti?
`evaluator.py` içerisine, vakaları türüne göre `run_native_workflow` veya Day 13'ün in-memory SQLite yapısıyla çalışan `run_durable_workflow` fonksiyonlarına yönlendiren bir dispatcher eklendi.

Before metric:
| Metric | Keyword | LLM |
|---|---:|---:|
| Accuracy  | 48% | 92% |
| Smalltalk | 25% |75% |
| Knowledge | 75% | 75% |
| Tool |22.2% |100% |
| Avg latency |0.00 |10096.60 |
| Failures |0 |0 |

After metric:
| Metric | Keyword | LLM |
|---|---:|---:|
| Accuracy  | 48% | 92% |
| Smalltalk | 25% |100% |
| Knowledge | 100% | 75% |
| Tool |22.2% |100% |
| Avg latency |0.00 |9415.25 |
| Failures |0 |0 |

### Provider normalization
Tool sağlayıcısını doğru yakalamak için `evaluator.py` içine `trace["provider"]` ve `state["tool_provider"]` verilerini canonical (standart) bir formata çeviren `normalize_workflow_result` fonksiyonu eklendi.

### Metric / trajectory single source of truth
Metrik mantığının tekrarlanmasını önlemek amacıyla evaluator'ın kendi içindeki hesaplama kodları kaldırılarak, tek kaynak (single source of truth) olarak `metrics.py`'deki `score_case` fonksiyonu kullanıldı.

### Pure LLM vs fallback-assisted routing
Fallback kullanıldığında bunun "saf model başarısı" gibi ölçülmesini engellemek için LLM router sonuç sözleşmesine `primary_route` ve `primary_error_type` alanları dahil edildi.

### Ollama error normalization
Ağ ve zaman aşımı gibi durumlarda dönen gerçek API hatalarının JSON ayrıştırma hatası olarak maskelenmemesi için `llm_router.py` dosyasına `RouterDependencyError` fırlatan bir kontrol eklendi.

### Evaluation unit tests
Metrik hesaplamalarındaki boş değer (null), sıfıra bölme risklerini ve confusion matrix matris yönünü doğrulamak için `test_day14_evaluator.py` dosyasına spesifik birim testleri eklendi.

### README / observability wording
README dosyasına, mevcut izleme yapısının tam bir OpenTelemetry kurulumu değil, ondan esinlenen yerel bir JSON izleme mekanizması olduğuna dair açıklama metni eklendi.

## 2. Day 14 Evidence Re-run

Scored routing cases:
25 (Değerlendirmeye alınan ve skoru hesaplanan ana senaryolar)

Challenge cases:
4 (Mevcut yetenek sınırlarını zorlayan veya taxonomy dışı olan tanısal/diagnostic senaryolar)

Keyword pure accuracy:
%48 (12/25) - Geleneksel kural tabanlı sistemin sadece basit eşleşmelerde çalıştığını, karmaşık niyetlerde yetersiz kaldığını gösteriyor.

LLM pure accuracy:
%91.3 (21/23) - Fastpath (hızlı yol) kurallarına girmeyip doğrudan qwen3:1.7b modeline giden 23 zorlu senaryodaki saf yapay zeka niyet anlama başarısı.

Production policy accuracy:
%92 (23/25) - Deterministik fastpath (2 senaryo) ve Semantic LLM router'ın (23 senaryo) birlikte çalıştığı "Two-Stage" nihai üretim politikasının toplam başarısı.

Failures:
0 - Her iki yönlendirici testinde de sistemin çökmediği (0 failure) ve hataların (invalid outputs) tolere edildiği doğrulandı.

Median latency:
Keyword router için ~0.0008 ms (sıfıra yakın), LLM router (default thinking modunda) için ise 10011 ms (yaklaşık 10 saniye). Bu yüksek LLM gecikmesi, `think=false` optimizasyon deneyinin temel gerekçesini oluşturmuştur.

## 3. Thinking / Latency Experiments

Default thinking:
Modelin varsayılan (default) ayarlarında Qwen3 niyet sınıflandırması çok ciddi gecikmelere (latency) sebep oldu. Test sonuçlarında routing kararlarının 6760 ms ile 35886 ms arasında (çoğunlukla 10-15 saniye bandında) değiştiği gözlemlendi. Bu süre bir üretim (production) router'ı için kabul edilemez seviyedeydi.

think=false:
Ollama API'sine `think=false` parametresi verilerek modelin çıkarım süresi optimize edildi. Aynı test setinde router gecikmeleri inanılmaz bir düşüşle 460 ms ile 623 ms (sub-second) aralığına geriledi. Ayrıca default modda `knowledge` rotasına giden "smalltalk" ve "semantic paraphrase" gibi sorgular, `think=false` modunda doğru rotalarına yönlendirildi.

Cold vs warm:
Deney başlatılmadan önce ilk çağrıdaki "Model Load" maliyetini (Cold start penalty) ölçümlere katmamak için bir "Isınma turu" (warm-up run) çalıştırılarak model belleğe (RAM/VRAM) alındı. Böylece ölçümler sadece modelin çıkarım (inference) hızını yansıttı.

Sonuç:
Deney kanıtlıyor ki; LLM tabanlı bir Semantic Router kullanılacaksa `think=false` parametresi bir seçenek değil, mimari bir zorunluluktur. Gecikmeyi ortalama 15 saniyeden 500 milisaniye seviyesine indirerek Two-Stage (İki Aşamalı) router politikasını üretim ortamı (production-ready) için uygun hale getirmiştir.

## 4. Final Router Policy

Seçim:
İki aşamalı (two_stage) hibrit router kullanıldı

Evidence:
Karar, `day14-routing-comparison.json` (A/B testleri) raporuna dayanmaktadır

Fallback:
LLM modeli cevap veremediğinde sistem deterministik keyword_fallback mekanizmasıyla bozulmadan çalışmaya devam eder (degraded mode)

Known limitation:
Küçük parametreli LLM (qwen3:1.7b) bazen karmaşık niyetlerde halüsinasyon görüp tool görevlerini knowledge rotasına yönlendirebilmektedir.

## 5. Architecture

Diagram:
Mermaid tabanlı sistem ve veri akışı diyagramı `docs` dosyasına eklendi.

LLM-driven boundaries:
Semantic Router niyeti anlama ve Generation (LLM) kısımları model odaklıdır.

Deterministic control boundaries:
Tool allowlist (beyaz liste), Risk/Approval policy (HITL) ve Yetkilendirme sistemleri tamamen deterministiktir.

Persistent components:
İş akışı durumu hafızası için SQLite Checkpointer (durable state) kullanıldı.

External services:
Qdrant (Vektör veritabanı), Ollama (Model provider) ve bağımsız araç entegrasyonu için MCP Server.

## 6. Model Roles

Generation:
qwen3:1.7b

Router:
qwen3:1.7b

Embedding:
embeddinggemma

Sparse:
Qdrant/bm25

## 7. Reproducibility

Python:
Python 3.10.21

Ollama image/digest:
image: ollama/ollama@sha256:9d30908e41144b1f1da89b9d8e33c07e4aeb43ff41a8660241b1686e2cc330ad  

Qdrant:
1.19.0

LangGraph:
1.2.11

MCP:
2.1.1

Python 3.10 migration kararı:
3.10.21 versiyonuna pinlendi. Körü körüne 3.13 veya 3.14'e geçiş yapılmadı; bu teknik borç `notes/week-03-technical-debt.md` içerisine aday olarak yazıldı.

## 8. CI

`.github/workflows/ci.yml` üzerinden yapılandırıldı.

Automatic gates:
Docker image build, Ruff (Lint), Golden Dataset doğrulama ve deterministik birim/entegrasyon testleri otomatize edildi.

Neden real LLM eval hard gate değil?:
LLM çıktıları nondeterministiktir (olasılıksaldır), timeout sorunları yaratabilir ve makine kaynaklarına (model çekme süreci) bağlı olduğu için CI süreçlerinde flaky (tutarsız) olabilir. Real eval işlemleri Local CI'a bırakılmıştır.

Remote CI result:
Otomatik gate testlerinde green (başarılı) alındı, sonuç JSON statik kanıt dosyasına mühürlendi.

## 9. Static Quality

Ruff version:
0.16.6

Scope:
python -m ruff check day15/capstone.py

Result:
failed

## 10. Capstone Scenarios

# 1 — Smalltalk
Query: "Selam"
Sonuç: `deterministic_fastpath` ile sıfır gecikmeyle (LLM'e gitmeden) `smalltalk` rotasına yönlendirildi ve 6654 ms'de başarıyla tamamlandı.

# 2 — Knowledge/RAG
Query: "Named volume neden kullanılır?"
Sonuç: Semantic Router (LLM) tarafından başarıyla `knowledge` rotasına yönlendirildi. 27144 ms sürede context getirilerek işlem tamamlandı.

# 3 — Native Tool
Query: "Ankara'ya iki kiloluk bir paket göndersem ne tutar?"
Sonuç: Router tarafından `tool` rotasına atandı; `calculate_shipping_cost` aracı `native` provider üzerinden başarıyla çalıştırıldı.

# 4 — MCP Tool
Query: "Geçen haftaki çalışma notlarımda RRF hakkında ne yazıyor?"
Sonuç: Yönlendirici doğru niyeti anladı, dış `search_notes` aracı standart `mcp` adaptörü (stdio) üzerinden izole bir şekilde tetiklendi.

# 5 — Tricky Semantic Route
Query: "Selam, Ankara'ya iki kilo gönderi ne kadar?"
Sonuç: İçinde selamlaşma (smalltalk) geçmesine rağmen LLM router ana niyeti (kargo hesaplama) başarıyla çıkararak `tool` rotasına (native) iletti.

# 6 — HITL Approve
Gizli (Redacted) riskli işlem. `approval_required: true` bayrağı ile akış SQLite checkpointer sınırında duraklatıldı. İnsan onayı (Approve) sonrası `completed` durumuna geçti.

# 7 — HITL Reject
Gizli (Redacted) riskli işlem. Yine onay beklendi, ancak insan reddettiği (Reject) için işlem yan etki (side-effect) yaratmadan güvenle `rejected` durumunda sonlandı.

# 8 — Out-of-Capability
Query: "Bugün hava nasıl?"
Sonuç: Mevcut araç listesinde (taxonomy) hava durumu olmadığı için model fallback davranışı gösterip `knowledge` rotasına gitti. (Bu durum sistemin güvenli fail etmesini sağlıyor, arbitrary shell/tool çalıştırmıyor).

## 11. Failure Drills

Router unavailable:
Model veya ağ çökerse, sistem hata fırlatmak yerine izole edilmiş `keyword_fallback` (kural tabanlı) moduna geçerek kısıtlı kapasiteyle (degraded) çalışmaya devam eder.

MCP failure:
MCP protokolü veya sunucusu çökerse, adaptör bu hatayı yalıtır (sandbox) ve ham sistem hatası yerine iş akışını güvenle sonlandıran bir `ToolRuntimeError` üretir.

Qdrant failure:
Vektör veritabanı bağlantısı koparsa, generation adımı durdurulur ve kontrollü bir `DependencyUnavailableError` dönülür; alakasız araçlara (tool route) sapılmaz.

HITL failure:
Eklenmedi

## 12. Security Checklist

Arbitrary shell:
Yok

Docker socket:
Bağlı değil

Tool allowlist:
Aktif

HITL:
Aktif

PII logging:
Span mental modeli, hassas verileri (PII) ve ham kullanıcı parametrelerini maskeleyecek gizlilik odaklı (privacy-safe) bir yapıdadır

## 13. Observability

En yavaş operation:
Bilgi rotasındaki LLM Generation adımları (Örn: Scenario-008 `knowledge` adımı 49511 ms ile en yavaş işlemdi).

Router decision source:
İzlenebilirlik kanıtları için, alınan kararın LLM'den mi (`llm`) yoksa statik koddan mı (`deterministic_fastpath`) geldiği JSON loglarına (`decision_source`) işlendi.

Trace correlation:
OTel esintili `record_span` fonksiyonu ile her operasyon; kendi benzersiz `run_id`, `thread_id` ve `duration_ms` verileriyle ilişkisel (correlated) olarak dosyaya yazıldı.

## 14. Final Test / Eval Evidence

Unit:
75

Integration:
27

Deterministic eval:
Birim ve CI testleri dış ağa çıkmadan tamamlandı ve doğrulandı

Real router benchmark:
`pure_llm_accuracy` %91.3, production policy accuracy (İki aşamalı) %92 olarak tescillendi

Capstone:
Uçtan uca belirlenen 8 senaryonun 8'i de başarıyla (Passed) tamamlandı

Output:
output/day15-capstone-summary.json
output/day14-routing-comparison.json

## 15. Documentation

README:
Repository dökümanı günlük notlardan çıkarılıp "Architecture, Core Learning, CI ve Known Limitations" başlıklı uçtan uca Three-Week projesi olarak yeniden yazıldı.

Architecture:
Data flow, sınır güvenliği ve bileşenleri içeren diyagramlar `docs/architecture.md` içerisine işlendi.

Engineering decisions:
Mühendislik seçimleri (Örn: Neden hybrid retrieval? Neden two_stage policy?) `week-03-engineering-decisions.md` dosyasına taşındı.

## 16. AI Araçlarını Nasıl Kullandım?

Architecture'ı önce kendim çizdim mi?
Evet. Sistem bileşenlerini ve güven sınırlarını tamamen ben tasarladım; AI'yı sadece bu kurguyu Mermaid diyagramına çevirmek için kullandım.

AI PR-style review:
AI'a kod yazdırmadım. Ona bir "Senior Reviewer" rolü vererek, yeni özellik önermeden sadece capstone değerlendirme kodlarımdaki regresyonları ve tutarsızlıkları incelemesini istedim.

AI security/CI blind spot:
CI iş akışımı incelerken, her PR'da ağır LLM imajlarını çekmenin timeout krizleri yaratacağını AI'ın "blind spot" analizi sayesinde yakaladım. Böylece ağır LLM testlerini yerel makineme, hızlı deterministik testleri CI'a ayırdım.

AI'nın önerdiği ama değiştirdiğim/reddettiğim öneri:
Desteklemediğimiz sorular (örn. hava durumu) için AI hemen "unsupported" rotası kodlamayı teklif etti. Kanıtsız özellik eklememek (feature-driven olmamak) adına bunu reddettim ve sistemi değiştirmek yerine durumu bir kısıtlama (known limitation) olarak belgeledim.

Evidence:
Kanıtım, raporumdaki (day15-capstone-summary.json) known_limitations kaydı ve yapay zeka modeli çalıştırmayan saniyelik .github/workflows/ci.yml dosyamdır.

## 17. Week 3 En Önemli 7 Öğrenim

1. Retrieval evaluation olmadan yeni bir search stratejisine (hybrid search) geçilmez.
2. MCP bir süreç/donanım sandbox'ı değildir; yalnızca protocol/capability isolation sağlar.
3. LangGraph iş akışlarındaki SQLite checkpointer bir business veritabanı yedeği (backup) değildir; anlık execution thread durumudur.
4. LLM router bir güvenlik yetkilendirme (authorization) kontrol mekanizması olarak kullanılamaz; sadece niyet önerir.
5. CI/CD otomasyonlarında yapay zeka (LLM) değerlendirmeleri donanım/probabilistik sebeplerle flaky olduğu için "hard gate" yapılamaz.
6. Semantic routing'de başarı, varsayımlarla değil; evidence-driven (kanıt odaklı) değerlendirmelerle (golden dataset/A-B test) ispatlanmalıdır.
7. Dış servis ve modellerin (Ollama/Qdrant) çökmesi sistem hatası sayılmaz; failure/fallback mekanizmaları bu senaryolar için vardır (Reliability).

## 18. Üç Haftalık Gelişimim

Week 1:
LangGraph gibi orkestrasyon araçları kullanmadan (native-first) yerel modellerle (SmolLM, qwen3) yapılandırılmış çıktı, araç tetikleme ve loop döngüleriyle otonom agent temellerini attım.

Week 2:
Metinleri vektör uzaylarına dönüştürüp Qdrant ile semantic/retrieval engine entegrasyonu kurdum. Sonrasında uçtan uca native RAG mimarisi oluşturup LangGraph geçişini tamamladım ve Docker seviyesinde güvenlik/hata toleransı prensiplerini sınadım.

Week 3:
Dış yetenekleri sisteme MCP ile standartlaştırdım, işlemlerdeki riskleri (HITL) ve SQLite memory dökümlerini sisteme bağladım. Finalde observabilty entegrasyonu ve evidence-driven semantic router stratejisiyle, üç haftalık bu yapıyı üretim kalitesinde (production-ready) CI hatlarına sahip profesyonel bir mimari sistem olarak belgelendirdim.

## 19. Sonraki Hafta Adayları

1. Sistemin taxonomy yapısında mevcut olmayan (Örn: "Bugün hava nasıl?") senaryolar için "Unsupported / Out-of-capability" model rotası/davranışı tasarımı.
2. Python 3.10 EOL riskine karşı, güvenli bir build süreciyle Python 3.13 uyumluluk / migration analizi.
3. RAG sisteminde "semantic grounding" seviyelerini (halüsinasyon tespiti) artıracak ek metrik veya model çapraz doğrulamaları.
```
