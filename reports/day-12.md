---
day: 12
date: 2026-09-02
status: completed 
mcp_spec: 2026-07-28
mcp_python_sdk: 2.1.1
transport: stdio
unit_tests_passed: 4
integration_tests_passed: 4
---

# Gün 12 — MCP

## 1. Day 11 Kapanışı

IDF modifier:
models.SparseVectorParams(modifier=models.Modifier.IDF) olarak ayarlandı.

Prefetch limit:
Dense ve sparse prefetch limitleri ile final top_k değeri birbirinden ayrıldı.

Unanswerable behavior:
Unanswerable query'ler de retriever'lardan geçirildi (kaynaklar ve skorlar kaydedildi), ancak sıralama (ranking) metrik aggregate hesabından hariç tutuldu.

Sparse validation:
Dense ve hybrid ile aynı minimum sözleşme (query boş olamaz, top_k 0'dan büyük olmalı) uygulandı.

Integration embed/query_embed:
Integration fixture, üretim yoluyla eşitlendi; kaydedilen dokümanlar için embed, sorgular için query_embed kullanıldı

Yeni dense metrics:
[DENSE] Hit@1: 0.8824 | Hit@3: 1.0 | MRR: 0.9314

Yeni sparse metrics:
[LEXICAL] Hit@1: 0.5882 | Hit@3: 0.7059 | MRR: 0.6471

Yeni hybrid metrics:
[HYBRID] Hit@1: 0.8824 | Hit@3: 1.0 | MRR: 0.9314

Day 11 report/README düzeltmeleri:
README deki yanlış CLI komutları ve rapordaki çıktı dosya yolları gerçek sistemle eşleşecek şekilde güncellendi.

## 2. Bugün Kullandığım MCP Sürümü

Spec:
2026-07-28

Python SDK:
mcp==2.1.1

Eski tutorial'lardan farklı gördüğüm şey:
Manuel initialize/initialized döngüsü yazmak yerine, protokol pazarlığı ve keşif (discovery) detaylarını yönetebilen stateless core yapıya sahip v2 High-level Client kullanılması.

## 3. MCP Architecture

Host:
MCP yeteneklerini kullanan ana uygulama (örn. LangGraph, ajan yapısı).

Client:
Host uygulamasının içinde çalışan ve belirli bir sunucu ile protokol üzerinden bağlantı kuran iletişim katmanı.

Server:
Araçları, verileri (resource) ve promptları barındırıp dışarıya açan izole süreç/uygulama.

Transport:
İstemci ile sunucu arasındaki mesajların hangi kanal üzerinden taşındığı (şu an için stdio kullanılıyor).

## 4. Server Capabilities

### Resources
Uygulamaya veri veya bağlam sunan, genelde sabit salt okunur yüzeyler (örn. week2://system-review).

### Tools
Hesaplama yapan, eylem gerçekleştiren veya parametre alan çalıştırılabilir fonksiyonlar (örn. search_notes(query, top_k)).

### Prompts
Bugün kullandım mı?
Hayır bugün kullanmadım yalnızca okuma sırasında öğrendim.

## 5. Resource Discovery / Read

List result:
week2://system-review: Sadece izin verilen sistem inceleme notunu okur ve string olarak döner.

Read example:
LLM-driven Kararlar

Answer generation
Query rewrite
Exploratory LLM classifier
Tool call proposal

Deterministic (Python) Kontroller

Route allowlist
Tool allowlist
Citation label validation

## 6. Tool Discovery / Schema

Tool:
search_notes

Arguments/schema:
Sorgu için boş olmayan string, sonuç sayısı (top_k) için 1 ile 5 arasında tamsayı

## 7. Tool Call

Input:
{"query": "Notlarımda hybrid search hakkında ne yazıyor?"}

Normalized result:
"Arama sonucu: {\n  \"source\": \"embeddings.md\",\n  \"chunk_id\": \"embeddings_chunk_2\",\n  \"score\": 1.0,\n  \"rank\": 1\n}"

## 8. Contract Error Deneyleri

Missing argument:
search_notes aracına zorunlu query parametresi verilmediğinde, SDK şema doğrulaması devreye girdi ve 1 validation error fırlatarak fonksiyonu hiç tetiklemeden istemciye kontrollü bir hata metni döndü.

Invalid top_k:
top_k değeri sınırın çok üstünde (100) girildiğinde, sistemdeki kural devreye girip "top_k 1 ile 5 arasında bir tam sayı olmalıdır" mesajıyla bir ValueError tetikledi. Bu çökme durumu MCP sunucusunu veya ajanı patlatmadı sorun araç düzeyinde izole edilip istemciye Error executing tool search_notes olarak yapılandırılmış bir şekilde aktarıldı.

Unknown tool/resource:
Sistemde tanımlı olmayan bir araç (olmayan_arac) çağrıldığında süreç hiçbir şekilde kesintiye uğramadı, doğrudan "Unknown tool: olmayan_arac" yanıtını dönerek hata sözleşmesinin (failure contract) başarıyla işlediğini gösterdi.

## 9. Workflow MCP Adapter

Native kalan tool:
calculate_shipping

MCP tool:
search_notes

Provider selection nasıl yapılıyor?
TOOL_PROVIDERS = {
    "calculate_shipping_cost": "native", 
    "search_notes": "mcp",          
}

## 10. Trace

{
  "capability_name": "search_notes",
  "status": "completed",
  "provider": "mcp",
  "server_name": "ai-intern-week",
  "capability_type": "tool",
  "transport": "stdio",
  "duration_ms": 9006,
  "error_type": null
}

## 11. Native vs MCP

Discovery:
Native yapıda araçlar uygulamanın kendi kodunda önceden bilinirken, MCPde istemci tarafından protokol üzerinden liste halinde çekilip keşfedilir.

Coupling:
MCP ajanın karar alma mekanizması ile araçların entegrasyonu arasındaki sıkı bağı (coupling) gevşeterek capability sınırını netleştirir.

Schema:
Native yapıda tamamen kendi özel sözleşmen geçerliyken, MCPde standartlaştırılmış SDK sözleşmesi kullanılır.

Transport:
Native yapıda iletişim bellekte gerçekleşirken, MCP mesajları stdio veya ağ üzerinden aktarır.

Failure surface:
MCP kullanımıyla beraber süreçler arası iletişimin kopması sunucu yanıtsızlığı veya stdout kirlenmesi gibi yeni hata noktaları eklenmiştir.

Overhead:
MCP kullanımıyla per-call stdio spawn + model initialization latency yaratıyor

Security responsibility:
Her ikisinde de güvenlik, onay listesi ve yetki yönetimi uygulamanın/çalışma zamanının kendi sorumluluğundadır

## 12. Security / Trust Boundary

MCP neden sandbox değil?
MCP yalnızca bir entegrasyon standardıdır aracın dosya silmesini veya veritabanını değiştirmesini kısıtlayan bir güvenlik yalıtımı sağlamaz.

Tool listelenmesi neden güvenli demek değil?
Sunucunun sahip olduğu araçları keşfedilebilir yapması (discovery), bu eylemlerin yan etkisiz veya doğrudan çalıştırılabilir olduğu anlamına gelmez.

Resource/tool result neden untrusted olabilir?
Döndürülen verilerin (örn. dosyadan okunan bir notun) içerebileceği zararlı komutlar, modelin çalışma talimatını bozmaması için "system instruction" olarak kabul edilmemelidir.

Allowlist nerede?
Güvenilen Uygulama (Trusted Application/Host) tarafında tutulur ve yalnızca izin verilen araçların çalıştırılmasını kontrol eder.

## 13. Testler

Unit:
Gerçek bir subprocess oluşturmadan, kaynak eşleştirmeleri ve adaptör hata dönüşümleri In-Memory istemci/sunucu altyapısıyla test edildi.

Protocol integration:
Gerçek stdio alt süreci başlatılarak yeteneklerin keşfedilmesi (discovery), kaynakların okunması ve geçersiz argümanlarla tetiklenen araçların kontrollü hata mekanizmaları test edildi.

Full retrieval integration:
MCP stdio iletişimi, Qdrant veritabanı ve Day 11 arama yeteneği bir araya getirilerek uçtan uca çalışabilirlik doğrulandı.

## 14. AI Araçlarını Nasıl Kullandım?

Capability modelini önce kendim tasarladım mı?
Evet. Hangi yeteneğin veri sağlayan bir "Resource"  hangisinin parametre alıp işlem yapan bir "Tool" olacağına koda dökmeden önce karar verdim.

AI'dan istediğim review:
Yazdığım MCP sunucu implementasyonunu sadece güncel v2 SDK API kullanımına uygunluk açısından incelemesini istedim. Mimariyi baştan tasarlamamasını ve güncel olmayan bir yapı görürse bunu özellikle işaretlemesini belirttim. Ayrıca MCP adapter içerisindeki hata eşleştirmelerimi incelemesini istedim.

AI'nın önerdiği ama değiştirdiğim/reddettiğim öneri:
AI, sistemdeki herhangi bir dosyayı okuyabilmesi için argüman olarak dosya yolu alan genel bir okuma aracı (arbitrary file reader) eklememi önerdi.

Neden?
Bu öneriyi reddettim. Bugünün öğrenimlerinde belirtildiği gibi, istemcinin sunucuya  rastgele bir dosya yolu gönderip okutabilmesi güvenlik sınırını (trust boundary) ihlal eder. Bunun yerine, yalnızca izin verilen (allowlisted) dosyaların okunabildiği güvenli ve statik "Resource" tanımlamaları kullandım.

## 15. Günün En Önemli 5 Öğrenimi

1.Benchmark sonuçları sadece metriklerden ibaret değildir; bu metriklerin üretildiği konfigürasyon, aday havuzu ve değerlendirme politikası da sonucun ve kanıtın ayrılmaz bir parçasıdır.
2.MCP, araçları (tool) daha akıllı yapan bir sistem değil; yetenek sahipliği, keşfi ve çağrılma sözleşmesini istemci/sunucu sınırına standart bir şekilde taşıyan bir protokoldür.
3.MCPde yetenek tipini (Resource veya Tool) seçerken sadece sözdizimine (syntax) değil, yeteneğin semantiğine, işlevine ve kime ait olduğuna bakılmalıdır.
4.MCP şeması yapısal bir sözleşme sunarak entegrasyonu güçlendirir, ancak iş kurallarını (business rules) ve anlamsal doğrulamaları (semantic validation) sizin yerinize otomatik olarak icat etmez.
5.MCP yalnızca bir entegrasyon standardıdır; yetkilendirme (authorization), en az ayrıcalık prensibi (least privilege), korumalı alan (sandboxing) ve yan etki (side-effect) politikalarının sorumluluğunu ortadan kaldırmaz.

## 16. Day 13 — Durable State / HITL Hakkında Merak Ettiklerim

1. Sistem tehlikeli bir eylemi gerçekleştirmeden önce nasıl durup benden onay isteyecek?
2. Ben ekranda onay verene kadar uygulama çökerse veya süreci yeniden başlatmam gerekirse, sistem nerede kaldığını (durable state) nasıl hatırlıyor?
3.Bekleyen bir işleme "reddet"  dediğimde süreç tamamen mi çöküyor, yoksa model hatayı anlayıp başka bir çözüm mü arıyor?
