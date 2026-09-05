| Component | LLM-driven? | Deterministic? | External? | Persistent? | Security/control? | Eval evidence |
|---|---|---|---|---|---|---|
| **Semantic Router** | Evet | Evet (Doğrulama)| Evet (Ollama)| Hayır | Hayır | Routing golden dataset |
| **Tool Allowlist** | Hayır| Evet | Hayır | Hayır | Evet (Kontrol düzlemi) | Unit tests / Deterministic eval |
| **SQLite Checkpointer**| Hayır | Evet | Hayır | Evet (DB/Backup değil) | Hayır | Durable / HITL case set |
| **Hybrid Retrieval** | Hayır | Hayır | Evet (Qdrant) | Evet (Endeks) | Hayır | Retrieval evaluation |
| **LLM Generation** | Evet | Hayır | Evet (Ollama) | Hayır | Hayır | System evaluator |
| **Risk / Approval** | Hayır | Evet | Hayır | Hayır | Evet (Risk sınırı) | HITL approve/reject cases |


# Failure| Detect | Contain | Recover/Fallback| Observe
|---|---|---|---|---|
| **Router model unavailable**|OllamaClient| Router try-except| keyword_fallback devreye girdi|State'te error ve kaynak loglandı
| **MCP failure**| MCPToolAdapter | Adapter izole etti| Kontrollü ToolRuntimeError| Adaptör hatası diziye eklendi
| **Qdrant failure**| Retriever node | retrieve_node exception| rewrite denendi, sonra güvenli hata | Zincirleme hatalar loglandı

# Security Capstone Checklist

[x] arbitrary eval/exec yok
[x] arbitrary shell yok
[x] Docker socket yok
[x] unrestricted filesystem MCP resource yok
[x] tool allowlist var
[x] provider mapping deterministic
[x] LLM route authorization değil
[x] high-risk controlled action HITL istiyor
[x] raw prompts/tool args default loglanmıyor
[x] secrets trace/report'a yazılmıyor
[x] checkpoint backup diye anlatılmıyor
[x] JSONL idempotency concurrent exactly-once diye sunulmuyor
[x] Docker container perfect sandbox diye sunulmuyor

# Core Components
Semantic Router (llm_router.py)
Neden var?: Kullanıcı niyetini (intent) anlayarak soruyu en uygun araca veya veritabanına yönlendirmek için.

Failure mode?: Ollama çökerse try-except ile yakalanıp deterministik keyword_fallback moduna geçer.

Test/eval evidence?: day14-routing-comparison.json (A/B testleri) ve day15-capstone-summary.json (Tam başarı) ile kanıtlanmıştır.

# Hybrid Retriever (nodes.py & Qdrant)
Neden var?: Kullanıcı sorularına RRF (Reciprocal Rank Fusion) ile hem anlamsal hem de sözcüksel en alakalı bağlamı (context) getirmek için.

Failure mode?: Veritabanı bağlantısı koparsa veya veri kalitesi zayıfsa önce soruyu yeniden yazar (rewrite), ardından DependencyUnavailableError fırlatır.

Test/eval evidence?: day11/benchmark.py arama metrikleri ve day15/failure_drill.py (Tatbikat C) ile doğrulanmıştır.

# MCP Adapter (mcp_adapter.py)
Neden var?: Dış kaynakları ve sistemleri LangGraph akışına standart, izole bir protokolle (stdio) bağlamak için.

Failure mode?: MCP sunucusu veya protokol çökerse, ham hata sızdırılmaz; kontrollü bir ToolRuntimeError üretilir.

Test/eval evidence?: Hata enjeksiyonlu day15/failure_drill.py (Tatbikat B) çıktılarıyla izole edildiği kanıtlanmıştır.

# SQLite Checkpointer (durable_graph.py)
Neden var?: İş akışının durumunu kaydetmek, insan onayı (HITL) için duraklatmak ve kalınan yerden güvenle devam ettirmek için.

Failure mode?: Yanlış bir thread_id üzerinden işlem yapılmaya çalışılırsa reddedilir, sistemde yan etki (side effect) oluşmaz.

Test/eval evidence?: day13.hitl_cli testleri ve uçtan uca Capstone senaryo 6/7 (approval_required) başarılarıyla onaylanmıştır.

# Tool Allowlist (nodes.py)
Neden var?: Sistemin sadece önceden tanımlanmış, güvenli araçlara (tool) erişebilmesini garantilemek için.

Failure mode?: Model listede olmayan veya uydurma (hallucinated) bir aracı çağırırsa eylem bloke edilir ve hata durumuna geçilir.

Test/eval evidence?: CI entegrasyonlu birim testlerindeki test_invalid_route_returns_controlled_error metrikleriyle sınanmıştır.

# Data Flow
Sistemdeki veri akışı tamamen State nesnesi üzerinden ilerler. Kullanıcıdan gelen metin (User Query) grafiğin başlangıç noktasına girer. Yönlendirici (Router) bu girdiye bakarak route (örn: tool, knowledge) ve decision_source (örn: llm, deterministic_fastpath) anahtarlarını state'e yazar. Veri daha sonra ilgili rotadaki düğümlere (node) aktarılır; dış sistemlerden (Qdrant veya MCP) dönen cevaplar JSON/Metin formatında state nesnesindeki bellek alanlarına eklenerek nihai terminal_status üretilir.

# Control Flow
Orkestrasyon LangGraph tarafından yönetilmektedir. İşlem akışı düğümler (nodes) ve koşullu kenarlar (conditional edges) ile kontrol edilir. router_node, durum nesnesindeki route değişkenine göre akışı tool_node, knowledge_node veya smalltalk_node'a dallandırır (branching). Riskli işlemler tool_node içerisinde değerlendirilir; insan onayı gerekiyorsa kontrol akışı kesilir (interrupt) ve dış sistemden (kullanıcı) devam (resume) sinyali gelene kadar askıya alınır.

# Persistence Boundary
Sistemin durumunun (state) kalıcılaştığı tek sınır SQLite Checkpointer mimarisidir. Bu sınır bir veritabanı yedeği (backup) değil, yalnızca kesintiye uğrayan iş akışlarının bellek dökümünü tutan bir hafıza kartıdır. Bellekte geçici olarak tutulan grafik nesneleri ile diskte fiziksel olarak tutulan asenkron çalışma (thread) bilgileri bu sınırda birbirinden ayrılır.

# Trust Boundary
Güven sınırı (Trust Boundary), deterministik kod ile probabilistik model (LLM) arasına çizilmiştir.

Tool Execution: LLM'in araç çalıştırma yetkisi yoktur, sadece çalıştırılmasını tavsiye eder. Son kararı deterministik Tool Allowlist (Beyaz liste) verir.
Resource Access: İşletim sistemine doğrudan erişim yoktur; tüm dış kaynak (dosya, veri) okumaları MCP adaptörü sınırları içinde gerçekleşir.
Human Authorization: LLM kararı bir yetkilendirme (authorization) sayılmaz. Yüksek riskli (High-risk) işlemler mutlak suretle Trust Boundary dışındaki bir insan kullanıcının onayına (HITL) sunulur.

# Evaluation Path
Sistem, varsayımlara değil kanıtlara (evidence-driven) dayalı olarak değerlendirilir. Yerel (local) makinede 8 farklı uçtan uca senaryoyu kapsayan Golden Dataset çalıştırılır (day15/capstone.py). Değerlendirme mekanizması, sadece cevabın doğru olup olmadığına değil; doğru kararın doğru kaynaktan (decision_source), doğru araçla (tool_name) ve doğru sürede (duration_ms) alınıp alınmadığına bakar.

# Observability Path
Gözlemlenebilirlik (Observability), OpenTelemetry "Span" prensiplerine göre tasarlanmıştır. Her düğüm geçişinde veya dış sistem çağrısında (LLM, Qdrant), gecikme süreleri (latency_ms), hatalar (errors) ve kararın kök nedeni (decision_source) state üzerine işlenir. Sessiz hatalar (silent failures) engellenerek, sistemin log çıktılarında veya day15-capstone-summary.json raporunda her işlemin uçtan uca izlenebilirliği (traceability) sağlanır.

# Router Policy
Sistem, "Two-Stage" (İki Aşamalı) yönlendirme politikası kullanır.

Stage 1 (Deterministic Fastpath): Gelen sorgu önce basit kural tabanlı eşleşmelere ("Selam", "Merhaba") sokulur. Eşleşme sağlanırsa LLM'e gidilmeden sıfır gecikmeyle yanıt üretilir (decision_source: deterministic_fastpath).

Stage 2 (Semantic LLM Router): Hızlı yol eşleşmezse, sorgu qwen3:1.7b modeline gönderilir. Modelin JSON olarak döndüğü intent (niyet) LangGraph'a iletilir (decision_source: llm). LLM çökerse, sistem keyword_fallback ile kurtarılır.

# External Dependencies
Ollama (qwen3:1.7b, embeddinggemma): Metin üretimi, niyet sınıflandırması ve vektör dönüştürme (embedding) işlemleri için.
Qdrant: Dense ve Lexical vektörlerin tutulduğu, hibrit (RRF) indeksleme yapan vektör veritabanı.
MCP Server / Client (mcp): Dış not arama (search_notes) araçları ile ana sistemin stdio protokolü üzerinden haberleşmesini sağlayan standart.
LangGraph: Ajan düğümlerini ve kontrol akışını yöneten orkestrasyon çerçevesi.