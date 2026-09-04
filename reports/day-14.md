---
day: 14
date: 2026-09-04
status: completed
golden_cases: 32
routing_cases: 25
challenge_cases: 4
unit_tests_passed: 7
integration_tests_passed: 2
---

# Gün 14 — Agent Evaluation, Observability ve Semantic Router

## 1. Day 13 Kapanışı

Terminal semantics:
Sahte "ready" durumu kaldırılarak düğümler doğrudan END statüsüne bağlandı; böylece iş akışının güncel durumu ile nihai çalışma sonucu net bir şekilde birbirinden ayrıldı.

action_id strategy:
Sabit ID kullanımı bırakılarak, çakışmaları önlemek için uuid4() ile dinamik ID üretimine geçildi ve testler için CLI'a özel --action-id parametresi eklendi.

Test output isolation:
monkeypatch ve isolated_action_log fixture'ı kullanılarak test logları geçici dizine yönlendirildi, böylece gerçek üretim loglarının kirlenmesi engellendi.

Approve/reject assertions:
Testler log kontrolünün ötesine geçirilerek; approve senaryolarında tam tamamlanma (execution_status), reject senaryolarında ise işlemin gerçekten reddedildiği ve yan etki (side-effect) oluşturmadığı kesin olarak doğrulanabilir hale getirildi.

Resume payload validation:
Sisteme gönderilen resume komutlarının programatik olarak da güvenli olması için, geçerli bir sözlük (dict) yapısında ve doğru decision (approve/reject) değeri barındırdığını denetleyen validate_resume_payload doğrulaması eklendi.

Trace fields:
İzleme loglarındaki eksiklikler giderilerek; run_id, hesaplanan terminal_status ve approval_required gibi temel metriklerin gerçek değerleriyle kaydedilmesi sağlandı.

Day 12 wording:
Düzenlendi.

README:
Düzenlendi.

Current unit test baseline:
Yeni payload ve politika (policy) doğrulamaları eklenerek temel iş mantığını koruyan unit testler tamamen izole edildi ve hazır hale getirildi.

Current integration baseline:
Uygulanan dosya izolasyonu ve iş etkisi (side-effect) kontrolleri sayesinde integration testleri normal akışı bozmadan çok daha tutarlı ve güvenilir bir yapıya kavuştu.

## 2. Test vs Evaluation vs Observability

Test kodun beklenen sözleşmeye uyup uymadığını kontrol eder. Evaluation sistemin kalitesini ölçerken, observability bu işlemler sırasında sistemin canlı olarak nasıl davrandığını (süre, hata vb.) gösterir.

## 3. Golden Dataset

Toplam:
32

Routing:
25

Workflow:
5

Challenge:
4

Gold label policy:
Sistemin mevcut yeteneklerini ve kısıtlarını bilerek belirledim.

## 4. Deterministic System Metrics

Route accuracy: %80
Tool accuracy: %50
Provider accuracy: %0
Approval correctness: %25
Terminal correctness: %66.6
Trajectory correctness: %40
Retrieval metric reuse: Day 11 metrikleri kullanıldı.

## 5. Keyword Router Baseline

Accuracy: %48 (12/25)
Per-class: Smalltalk %25, Knowledge %100, Tool %22.2
Confusion matrix: Tool (araç) beklentili sorguların çoğu smalltalk ve knowledge olarak yanlış etiketlendi.
Average latency: 0.0016 ms
Median latency: 0.0013 ms
Failure analysis: "Kargo" veya "notlar" kelimesi geçmeyen tüm niyetler kaçırıldı.

## 6. LLM Semantic Router

Model: qwen3:1.7b
Structured schema: JSON formatı kullanıldı.
Temperature: 0
Available capability list: calculate_shipping_cost, search_notes
Fallback policy: Model hata verirse veya zaman aşımına uğrarsa keyword router'a dönülür.

## 7. LLM Router Metrics

Accuracy: %92
Per-class: Smalltalk %100, Knowledge %75, Tool %100
Confusion matrix: İki adet knowledge (bilgi) sorgusu yanlışlıkla tool (araç) olarak algılandı.
Invalid output count: 0
Timeout/failure count: 1 (Out-of-capability sorgusunda ValueError)
Average latency: 11845 ms
Median latency: 9579 ms

## 8. Keyword vs LLM

| Metric | Keyword | LLM |
|---|---:|---:|
| Accuracy  | 48% | 92% |
| Smalltalk | 25% |75% |
| Knowledge | 75% | 75% |
| Tool |22.2% |100% |
| Avg latency |0.00 |10096.60 |
| Failures |0 |0 |

## 9. Routing Failure Analysis

### Case 1 — Keyword yanlış / LLM doğru
İçinde kargo kelimesi olmayan "Ankara'ya 2 kilo paket göndereceğim, maliyeti ne?" sorgusunu LLM anlamsal olarak başarıyla yakaladı.

### Case 2 — Keyword doğru / LLM yanlış
"Qdrant'ta collection oluştururken..." sorgusunu LLM yanlışlıkla bir araç işlemi (tool) sandı.

### Case 3 — İkisi de yanlış
yok.

### Case 4 — Out-of-capability
"Bugün hava nasıl?" sorusunda LLM 30 saniye boyunca bocalyıp `ValueError` vererek fallback devresini tetikledi.

## 10. Final Router Kararım

Seçim: two-stage (Hybrid Router)

Neden?
LLM, 'tool' ve 'smalltalk' sınıflarında anlamsal eşleştirmeyi kusursuz (%100) yapsa da, 10 saniyelik gecikme süresi (latency) üretim (production) ortamında standart bir yönlendirme için çok yüksek bir maliyettir. Ayrıca 'knowledge' sınıfında %25'lik bir regresyon yaşanmıştır. Hem LLM'in anlamsal kavrama gücünden faydalanmak hem de Keyword'ün hızını korumak için iki aşamalı sistem en ideal mühendislik çözümüdür.

Hangi evidence?
- LLM Global Accuracy: %92.0 (Tool: %100.0)
- Keyword Global Accuracy: %48.0 (Tool: %22.2)
- LLM Avg Latency: 10096.60 ms
- Keyword Avg Latency: 0.00 ms
- LLM Knowledge Regression: %100 -> %75

Hangi limitation?
Bugünkü sistemde Hybrid Router henüz implemente edilmemiştir. Bu mimari Karar C olarak Cumartesi (capstone) projesinde teknik borç (technical debt) olarak ele alınacak ve geliştirilecektir. LLM-as-judge metriklerinin deterministik süreçler (tool name, provider vb.) için kullanılmaması gerektiği anlaşılmıştır.

## 11. Security

LLM route=tool dediğinde hangi deterministic kontroller devam ediyor?
Teoride LLM sadece niyet belirler, aracın çalıştırılması kod üzerindeki politikalara bağlıdır. Ancak testler gösterdi ki, yönlendirici tehlikeli bir komutu ("rapor yayınla") bilgi sorgusu (knowledge) sanarak asıl güvenlik aşamalarını tamamen atlayabiliyor.

Tool allowlist:
Kod seviyesinde tanımlı ancak yönlendirme hataları yüzünden pratikte tam güvenli değil.

Provider mapping:
Kodda tanımlı ancak bugünkü metriklerimize göre doğruluk oranımız şu an %0.

HITL:
Tasarımda var ancak bugünkü testlerde yönlendirici eylemi tanımadığı için onay mekanizması hiç tetiklenemedi. (Bu durum Cumartesi projesine devreden büyük bir güvenlik açığı ve teknik borçtur.)

## 12. Trajectory Evaluation

Strict examples:
Yörüngenin eksiksiz ve araya hiçbir ekstra düğüm girmeden tamamlanması beklenen senaryolar.

Allowed/ordered examples:
Ana düğümlerin (classify, retrieve, generate vb.) sırasını koruması şartıyla, araya opsiyonel düğümlerin girmesine izin veren esnek yapı.

En faydalı regression:
Knowledge (bilgi) akışlarında beklenen kalite kontrol veya arama düğümlerinin planlandığı gibi çalışmaması, yörünge başarı oranımızın (trajectory accuracy) %40'ta kalmasını sağlayarak bize çok değerli bir arıza kaydı verdi.

## 13. Observability

LLM Classifier (ortalama 10 saniye) ve uçtan uca knowledge aramaları (30 saniyeye kadar sonra hata).

Raw prompt/query logluyor muyum?
Hayır, kullanıcı gizliliğini ihlal etmemek için loglanmamaktadır.

## 14. OpenTelemetry Experiment

Yaptım mı?
Hayır, gerçek OpenTelemetry kütüphanelerini kurarak bir deneme yapmadım.

Yaptıysam ne öğrendim?
-

Yapmadıysam neden?
Zaman kısıtlaması nedeniyle kılavuzdaki opsiyonel hakkımı kullandım; asıl kütüphaneler yerine kendi yazdığım "minimal custom trace" altyapısıyla span mantığını kavramayı tercih ettim.

## 15. Output

Evaluation:
`day14-evaluation-report.json`

Router comparison:
`day14-routing-comparison.json`

## 16. Testler

Unit:
Trajectory subsequence ve LLM JSON çıktı format testleri.

Integration:
Workflow uçtan uca ve Ollama LLM smoke testleri.

Eval case count:
32

## 17. AI Araçlarını Nasıl Kullandım?

## 17. AI Araçlarını Nasıl Kullandım?

Golden label'ları önce kendim doğruladım mı?
Evet, her kategori (smalltalk, knowledge, tool, challenge) için temel referans örneklerini ve sistemin sınırlarını önce bizzat kendim oluşturup etiketledim. 

AI'dan dataset blind-spot review:
Oluşturduğum bu çekirdek veri setini AI'ya vererek, gözden kaçırdığım "kör noktaları" ve kullanıcıların sorabileceği uç (edge) durumları bulmasını istedim.

AI'dan prompt/schema review:
Semantik yönlendirici (LLM Router) için hazırladığım sistem promptunu AI'ya inceleterek, araç ve bilgi rotaları arasındaki anlamsal farkların yeterince net olup olmadığını teyit ettirdim.

AI'nın önerdiği ama kabul ettiğim/değiştirdiğim öneri:
AI ın "Veri setini belirlediğin formatta senin için çoğaltabilirim" teklifini kabul ettim. Temel şablonları (prototipleri) ve sınırları ben verdikten sonra, kalan case leri üretmesi için AI ı kullandım. Ancak AI'nın ürettiği verileri körü körüne almadım; her bir etiketi (label) ve yörüngeyi (trajectory) tek tek kontrol edip onaylayarak veri setine dahil ettim.

Neden?
Sıfırdan tüm veri setini AI a yazdırmak, sistemin kendi kendini ezberlemesine yol açardı ve değerlendirmenin mantığını bozardı. Ancak önce kendi kurallarımı koyup AI ı sadece "zaman kazandıran bir çoğaltıcı (generator)" olarak kullanmak, hem mühendislik prensiplerini korumamı sağladı hem de bana ciddi bir vakit kazandırdı.

## 18. Bugünün En Önemli 5 Öğrenimi

1. Sistem çalışıyor demekle, sistemin doğru yolu (trajectory) izleyerek sonuca ulaştığı aynı şey değildir.
2. Yönlendirmeyi yapay zekaya (semantic) bırakmak isabeti %92'lere çıkarıyor fakat saniyeler süren gecikme (latency) maliyeti getiriyor.
3. Sistemi devasa tek bir işlem (log) yerine, operasyon bazlı küçük parçalara (span) bölmek gözlemlenebilirliği (observability) mükemmelleştirir.
4. Gizlilik (privacy) gereği hiçbir log kaydına kullanıcı promptları veya hassas veriler maskelenmeden yazılmamalıdır.
5. Doğrudan kodla (deterministik) ölçülebilen olaylar için büyük dil modellerini hakem (judge) atamak gereksiz ve pahalıdır.

## 19. Cumartesi Capstone İçin Kalan Teknik Borç

1. Hız ve doğruluk dengesini kurmak için Two-Stage (Hybrid) router'ın kodlanıp ana akışa bağlanması.
2. Knowledge akışlarında %40'ta kalan yörünge başarı oranının (trajectory accuracy) düzeltilmesi için LangGraph rotalarının onarılması.
3. İnsan onayı (Approval) mekanizmasında yaşanan %25'lik başarısızlığın giderilerek HITL (Human-in-the-loop) akışının kusursuzlaştırılması.
```
