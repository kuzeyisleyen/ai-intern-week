---
day: 9
date: 2026-08-27
status: completed
langgraph_version: 1.2.11
total_unit_tests_passed: 50
total_integration_tests_passed: 15
specific_unit_tests_passed: 9
specific_integration_tests_passed: 3
blocker_count: 0
---

# Gün 9 — Agentic Workflow ve LangGraph

## 1. Day 8 Kapanışı

Integration marker:
intagration testlere `@pytest.mark.integration` eklemesini yaptım.

Evaluation runner:
8 soruluk veri setini analiz eden ve metrik hesaplamalarını otomatize eden bir değerlendirme kodu yazdım.

Gerçek Hit@1:
Değerlendirme sonucunda, sistemin cevaplayabildiği 6 soruda %100 ilk sıra eşleşme başarısına ulaştığını doğruladım.

Gerçek Hit@3:
Sistem ilk aramada zaten %100 başarı sağladığı için Hit@3 metriğinde de doğal olarak eksiksiz eşleşme elde ettim.

Day 8 raporunda düzelttiğim aşırı güçlü iddialar:
Sistemin her şeyi bileceği yönündeki varsayımları kaldırıp, yalnızca verilen metin bağlamı (context) kadar yanıt verebileceğini netleştirdim.

README:
Testleri çalıştırma komutlarını (`docker compose run...`) içerecek şekilde güncelledim.

Full tests:
Tüm RAG (Retrieval-Augmented Generation) testlerimi başarıyla çalıştırıp hatasız sonuca ulaştım.

## 2. Native Workflow Diagram

[START]
   │
   ▼
[classify_node] ──(smalltalk)──► [direct_generate_node] ──────┐
   │                                                          │
   ├──(tool)────────► [tool_node] ────────────────────────────┤
   │                                                          │
   └──(knowledge)───► [retrieve_node]                         │
                           │                                  │
                     [quality_node]                           │
                           │                                  │
                        (usable)                              │
                           │                                  │
                           ▼                                  ▼
                   [generate_node] ──► [validate_node] ──► [END]

## 3. State Schema

Alanlar:
query, route, original_query, retrieval_query, rewrite_count, node_trace, retrieved_chunks, tool_name, status, answer, step_count, errors

State'in orchestration açısından görevi:
Tüm düğümler (nodes) arasında veri taşıyan ve sistemin o anki durumunu merkezi olarak kaydeden bellektir.

## 4. Route'lar

### Smalltalk
Örnek:
"Merhaba"
Neden Qdrant'a gitmedi?:
Veritabanında sohbet verisi olmadığı için gereksiz arama maliyetini ve zaman kaybını önlemek istedim.

### Knowledge
Örnek:
"Named volume nedir?"
Route:
Kural listesindeki "merhaba" veya "kargo" kelimelerine takılmadığı için doğrudan Qdrant'a giden knowledge rotasına yönlendirildi.

### Tool
Örnek:
"Ankara'ya 2 kg kargo ne kadar?"
Allowlisted tool:
Sistemin rastgele araçlar seçmesini engellemek için yalnızca açıkça izin verdiğim calculate_shipping_cost aracını çağırdım.
Allowlisted tool:
calculate_shipping_cost

## 5. Deterministic Classifier

Kurallar:
Soru metnindeki basit kelime eşleşmelerine ("merhaba", "kargo") dayalı basit if/elif kontrolleri yazdım.

İyi tarafı:
Hızlı çalışır, maliyeti yoktur ve sonucun ne olacağı her zaman %100 kesindir.

Zayıf tarafı:
Trace kayıtlarında da gördüğümüz "selam, bana shipping fiyatı hesapla" sorusundaki gibi kelime yanılgısına düşüp aracı atlayabiliyor.

## 6. LLM Classifier Experiment

Query sayısı:
Trace dosyamıza kaydettiğimiz üzere 5 farklı test sorusu kullandım.

Rule/LLM aynı route:
"Merhaba" veya "Named volume nedir" gibi düz sorularda kural tabanlı sistem ve LLM aynı sonucu buldu.

Farklı route:
"Selam, kargo hesapla" gibi karmaşık sorularda kurallar yanılırken, LLM niyeti daha iyi anlardı.

Main workflow'da hangisini seçtim?:
Geliştirme sürecinde kontrolü elimde tutmak için deterministik (kural tabanlı) yönlendiriciyi seçtim.

Neden?:
Testleri daha tutarlı bir şekilde izole edebilmek ve başlangıçta karmaşıklıktan uzak durmak için.

Invalid route'u nasıl engelledim?:
İzin verilen rotaları ALLOWED_ROUTES kümesinde tanımlayarak, bu listede olmayan tüm sonuçları bir hata koduna düşürdüm.

## 7. Retrieval Quality Policy

Bugün kullandığım policy:
Eğer Qdrant'tan dönen liste tamamen boş değilse (içinde eleman varsa) sonuçları "usable" olarak işaretledim.

Universal threshold kullanmadıysam neden?:
Qdrant ne kadar alakasız olursa olsun her zaman en yakın 3 sonucu döndürdüğü için sabit bir skor sınırı koymak esnekliği bozuyordu.

Kendi Day 8 score dağılımımdan ne gözlemledim?
...

## 8. Query Rewrite Experiment

Original query:
Birim testimizde kullandığımız "Bilinmeyen zor bir soru" (Mocklanmış değer).

Original retrieval:
Sorgu çok belirsiz olduğu için sahte veritabanımız boş küme [] döndürdü.

Rewritten query:
Sistem soruyu, sahte modelimiz üzerinden "yeni soru" olarak yeniden yazdı.

Rewritten retrieval:
Yeniden yazılan soruyla yapılan ikinci arama da boş dönünce sistem planlandığı gibi fallback (pes etme) düğümüne düştü.

İyileştirdi mi?:
Test ettiğim bu zayıf arama senaryosunda iyileştirmedi ve döngüyü kırıp akışı sonlandırdı.

Başka bir query'de kötüleştirdi mi?:
Elimdeki test senaryolarında başka bir sorgu için kötüleştirme verisi bulunmuyor.

## 9. Termination

MAX_REWRITES:
Sistemin aynı soruyu sürekli yeniden yazıp sonsuz döngüye girmesini engellemek için yeniden yazma limitini 1 olarak belirledim.

MAX_STEPS:
Tüm akışın kontrolden çıkma ihtimaline karşı maksimum 12 adım (step) sınırı koydum.

Cycle nasıl duruyor?:
Her fonksiyon çalıştığında state içindeki step_count değeri 1 artırılır; limit aşılırsa sistem hata fırlatıp acil duruş yapar.

## 10. LangGraph Mapping

Native state:
→ LangGraph: Düğümler arasında taşınan StateGraph paylaşımlı veri yapısına dönüştü.

if/elif:
→ LangGraph: add_conditional_edges metoduna verilen şartlı yönlendirme fonksiyonlarına dönüştü.

retry:
→ LangGraph: Düğümlerin birbirine geri dönmesini sağlayan döngüsel oklarla (edges) modellendi.

termination:
→ LangGraph: Akışın END adlı özel bitiş düğümüne bağlanmasıyla sağlandı.

## 11. Node ve Conditional Edges

Node'lar:
Mevcut durumu (state) alıp kendi görevini yaptıktan sonra durumu güncelleyerek geri döndüren bağımsız Python fonksiyonlarıdır.

Conditional routes:
Akışın sabit bir yoldan değil, state içindeki bir değere (örneğin seçilen rotaya) bakarak dinamik yön değiştirmesini sağlayan ayrımlardır.

START:
İş akışının başladığı ve ilk karar mekanizmasının tetiklendiği başlangıç noktasıdır.

END:
Ajanın işini başarıyla tamamladığı veya planlı bir şekilde pes ettiği bitiş noktasıdır.

## 12. Native vs LangGraph

State görünürlüğü:
Saf Python'da elden ele taşıdığım state, LangGraph'ta çerçevenin (framework) kendi arka planında gizlendi.

Routing:
Saf Python'da standart if/else bloklarındayken, LangGraph'ta okların bağlandığı harici şart fonksiyonlarına çekildi.

Retry/cycle:
Saf Python'da bir while döngüsü içindeyken, LangGraph'ta düğümler arası geri bağlanan oklarla kuruldu.

Testability:
LangGraph objesini izole etmek ve yazdığım sahte (fake) sınıflarla test etmek daha yapısal ve kolay oldu.

Boilerplate:
LangGraph başlangıçta düğümleri isimlendirmek gibi ekstra iş yükü getirse de, büyüyen kodda karmaşayı (spagetti) önledi.

Framework maliyeti:
Dışarıdan bir kütüphane bağımlılığı ve yeni bir kodlama standardı (syntax) öğrenme zorunluluğu getirdi.

LangGraph sistemi daha akıllı yaptı mı?:
Hayır, modele veya cevaplara ekstra bir zeka katmadı; yalnızca benim kurduğum mantığı soyutlayarak (abstraction) düğüm/kenar mimarisine geçirdi.

## 13. Workflow Traces

Dosya:
output/day09-workflow-traces.jsonl

Üç örnek route:
Kayıt dosyamızda smalltalk (Merhaba), knowledge (Named volume) ve tool (Kargo ücreti) rotalarının tüm düğüm izlerini (node_trace) net bir şekilde kaydettim.

## 14. Testler

Unit Passed: 9
Unit Failed: 0

Integration Passed: 3
Integration Failed: 0

Full workflow smoke:
Gerçek API ve Qdrant bağlantıları kullanılarak oluşturulan testler, sistemin belirlenen adım ve citation kurallarını başarıyla karşıladığını kanıtladı.

## 15. AI Araçlarını Nasıl Kullandım

Graph'ı çizmeden önce AI kullandım mı?:
Evet, kodlamaya geçmeden önce akışın mantığını doğrulamak için yapay zeka ile fikir alışverişi yaptım.

Kendi tasarımım:
nodes.py içindeki mantığı, karmaşıklıktan uzak durmak ve kontrolü elimde tutmak adına olabildiğince düz, if/else yapılarıyla yazdım.

AI'dan istediğim review:
Yazdığım native kodun LangGraph iskeletine doğru oturup oturmadığını ve mimari hatalarım olup olmadığını denetlemesini istedim.

AI'nın önerdiği ama değiştirdiğim/reddettiğim bir öneri:
Testleri yazarken önerilen karmaşık mock factory desenlerini ve iç içe lambda mimarilerini reddettim.

Neden?:
Bir öğrenci projesinde kodun rahat okunabilir kalmasını sağlamak için kendi yazdığım sade sınıfları kullandım.

## 16. Karşılaştığım Bir Hata

Problem:
Birim testlerini terminalde çalıştırmak isterken ModuleNotFoundError: No module named 'day09' hatası aldım.

Hangi state/node/edge'de?:
Bu hata bir düğümde (node) değil, testlerin toplanması (collection) aşamasında doğrudan terminalde yaşandı.

Trace nasıl yardımcı oldu?:
Pytest'in verdiği terminal traceback çıktısı, Python'un çalıştığım ana dizini doğru algılamadığını gösterdi.

Kaynak:
Doğrudan pytest komutu çalıştırıldığı için sistemin kök klasör yolunu (root path) bulamaması.

Çözüm:
Test komutunu python -m pytest şeklinde çalıştırarak, modüllerin ana dizin baz alınarak tanınmasını sağladım.

## 17. Bugünün En Önemli 5 Öğrenimi

1. LangGraph gibi framework'lerin sisteme ekstra bir zeka katmadığını, yalnızca benim yazdığım durum (state) yönetimini ve yönlendirmeleri düğüm-kenar (node-edge) mimarisiyle soyutladığını anladım.
2. Merkezi bir döngünün olmadığı graph mimarilerinde modelin sonsuz döngülere girmesini engellemek için, her bir düğüme adım sayacı (MAX_STEPS) gibi kesin fren mekanizmaları eklemem gerektiğini öğrendim.
3. Rota (route) kararlarımın doğruluğunu kanıtlamak için gerçek veritabanı veya model yerine sahte (fake) sınıflar ve hata fırlatan sahte servisler (ExplodingRetriever) kullanarak kodumu izole etmeyi kavradım.
4. Sistemin adımlarını izlemek için oluşturduğum JSONL trace (iz) dosyalarına, güvenlik standardı gereği ortam değişkenlerini veya gizli verileri asla ham haliyle yazmamam gerektiğini uygulayarak öğrendim.
5. Kelime eşleşmesine dayalı deterministik yönlendiricilerin çok hızlı ve kesin çalıştığını, ancak bağlamı kaçırıp yanlış rotaya gitme zaaflarının olduğunu test ederek gördüm.

## 18. Cuma Reliability / Sandbox Hakkında Merak Ettiklerim

1. Şu anki çalışan yapıma dinamik bir dış kaynak aracı eklediğimde sistemin dayanıklılığı nasıl etkilenecek?
