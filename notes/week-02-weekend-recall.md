1. Source Document
Neden var? Sistemin beslendiği ham bilgi tabanı (ground truth).
Tip: D (Deterministic)
Failure: Desteklenmeyen format, bozuk karakter kodlaması (encoding), eksik veri.

2. Chunking
Neden var? Uzun metinleri LLM'in bağlam penceresine (context window) sığdırmak ve anlamsal aramayı spesifik paragraflara odaklamak.
Tip: D (Deterministic)
Failure: Anlam bütünlüğünü bölen yanlış kesimler, optimum olmayan chunk_size ve overlap değerleri.

3. Embedding (Ollama)
Neden var? Metinleri matematiksel vektör uzayına taşıyarak "kosinüs benzerliği" (cosine similarity) hesaplamasına olanak tanımak.
Tip: L (LLM-driven / Neural Model)
Failure: Dildeki ince nüansları (örn. ironi) vektöre yansıtamama, model API zaman aşımı (timeout).

4. Qdrant
Neden var? Vektör depolama, hızlı benzerlik araması ve meta veri filtreleme (metadata filtering) işlemleri için kalıcı (persistent) hafıza.
Tip: D (Deterministic)
Failure: Servis çökmesi, yanlış koleksiyon adı, bağlantı kopukluğu.

5. Workflow Routing
Neden var? Kullanıcı sorgusunun niyetini belirleyip (sohbet, arama, dış işlem) akışı doğru düğüme yönlendirmek.
Tip: D (Kural tabanlı classifier)
Failure: Eş anlamlı kelimelerde şaşırma, geçersiz rota (invalid route) dönmesi ve akışın kilitlenmesi.

6. Tool / Knowledge / Smalltalk
Neden var? Farklı yeteneklerin birbirinden izole edilmiş, güvenli ve bağımsız iş mantığı alanlarında çalışması.
Tip: D (Tool mantığı) / L (Knowledge/Generation)
Failure: Tool içinde çalışma zamanı hatası, güvenlik sınırlarının dışına çıkılması.

7. Retrieval
Neden var? Vektör tabanlı sorgu çalıştırıp en alakalı K adet (top-k) belgeyi getirmek.
Tip: D (Deterministic)
Failure: Hiçbir sonuç bulunamaması, bağlamla alakasız (low relevance) belgelerin dönmesi.

8. Context Builder
Neden var? Gelen ham chunk'ları, LLM'in anlayabileceği etiketli ([S1], vb.) bir formatta string'e dönüştürüp prompt'a enjekte etmek.
Tip: D (Deterministic)
Failure: Boş liste gelmesi durumunda patlaması, etiket formatının yanlış inşa edilmesi.

9. LLM Generation
Neden var? Verilen bağlamı okuyarak kullanıcının niyetine uygun, doğal ve açıklayıcı nihai cevabı üretmek.
Tip: L (LLM-driven)
Failure: API zaman aşımı, bağlam dışına çıkma (halüsinasyon), talimata/formata uymama.

10. Citation Validation
Neden var? Modelin bağlamda olmayan uydurma kaynak etiketleri üretmesini engellemek.
Tip: D (Deterministic)
Failure: Modelin geçerli bir etiket (örn. [S1]) kullanıp tamamen alakasız bir iddiada bulunması (semantik doğrulaması eksik).

11. Trace / Terminal State
Neden var? İş akışının nerelerden geçtiğini kaydetmek, hata ayıklamak (observability) ve döngü sınırlarını (MAX_STEPS) kontrol etmek.
Tip: D (Deterministic)
Failure: Döngünün kırılamaması, kayıp veya eksik state güncellemeleri, diske yazılamayan loglar.


# Week 2 — Weekend Recall

## Week 1'den unutmamam gereken 5 şey

1.AI bana kod yazabilir ancak öğrenme sorumluluğunu devralamaz; yazdığı kodu okumak, sorgulamak, test etmek ve mantığını anlamak tamamen benim görevimdir.
2.Büyük dil modelleri (LLM) sihirli cevap motorları değil; mevcut bağlama (context) göre bir sonraki token'ın olasılık dağılımını üreten (next-token prediction) istatistiksel mekanizmalardır.
3.Kodu her zaman uç durumları (edge-case) düşünerek ve boş girdi gibi risklere karşı güvenli (try/except, kontrollü döngüler) hale getirerek yazmalıyım.
4.Yazılım projeleri bilgisayarımdan bağımsız ve taşınabilir olmalıdır; bunun için Docker, Docker Compose, .gitignore ve requirements.txt gibi hijyen standartlarını kullanmalıyım.
5.Modellerden yalnızca metin değil, yapılandırılmış çıktı (Structured Output) ve araç çağırma (Tool Calling) talepleri alabilirim, ancak o araçları (Python kodunu) gerçekten çalıştırma yetkisi ve güvenliği her zaman benim uygulamamdadır.

## Week 2 sistem diyagramım
[Kullanıcı Sorusu]
       │
       ▼
 [Classify Node] ────────(smalltalk)────────► [Direct Generate] ────┐
       │                                                            │
       ├──(tool)────────► [Tool Node] ──────────────────────────────┤
       │                    (Shipping/Analyze)                      │
       │                                                            │
       └──(knowledge)───► [Retrieve Node]                           │
                               │                                    │
                               ▼                                    │
                        [Quality Check]                             │
                               │                                    │
                         (weak)│(good)                              │
                               │  └──────────────┐                  │
                               ▼                 │                  │
                       [Rewrite Node]            │                  │
                               │                 │                  │
                               ▼                 │                  │
                        [Retrieve Node]          │                  │
                               │                 │                  │
                               ▼                 ▼                  │
                        [Generate Node] ◄── [Qdrant DB]             │
                         (RAG Context)           ▲                  │
                               │                 │                  │
                               ▼            [Ingestion]             │
                      [Validate Node]            ▲                  │
                               │             [Chunking]             │
                               ▼                 ▲                  │
                             [END] ◄──────── [Documents]            │
                               ▲                                    │
                               └────────────────────────────────────┘
## Artık kendi cümlemle açıklayabildiğim 5 kavram

1. Token/Tokenizer
2. Embedding
3. Semantic Retrieval
4. Chunking/Overlap
5. Conditional Edge

## Hâlâ birbirine karıştırdığım 3 konu

1. Citation Validity ile Grounding : Modelin cevabının sonuna veritabanından gelen [S1] etiketini doğru formatta ve uydurmadan eklemesi (citation validity), yazdığı cümlenin gerçekten o kaynak tarafından anlamsal olarak desteklendiğini (grounding/entailment) kanıtlamıyor; bu iki kavramın doğrulama sınırlarını bazen birbirine karıştırıyorum.
2. Agentic Loop (ReAct) ile Stateful Workflow (LangGraph Orkestrasyonu): Modelin reasoning (düşünme) ve acting (eylem) adımlarını serbest bir döngüde kendi kendine yönetmesi (ReAct) ile, benim durumu (state) merkeze alıp deterministik yönlendirmelerle (conditional edges) ona kontrollü bir iş akışı çizmem (Workflow) arasındaki mimari ayrımı ve sınırları tam oturtamıyorum.
3.Expected Runtime Failure (Beklenen Çalışma Zamanı Hatası) ile Programmer Bug (Programcı Hatası): Sistemde Qdrant'ın anlık cevap vermemesi gibi beklenen altyapı hatalarını (timeout vb.) yönetirken, yazdığım geniş bir try/except bloğunun kendi kodumdaki mantık hatalarını (örneğin KeyError) da yutarak "fallback" (pes etme) senaryosu gibi göstermesi riskini pratikte ayırt etmekte zorlanıyorum.

## Production sistemde henüz yapamayacağım / iddia etmeyeceğim şeyler

-Sistemim halüsinasyon görmeyi %100 oranında çözdü veya engelledi diyemem; çünkü retrieval (getirme) ne kadar iyi olursa olsun modelin bağlam dışına çıkma riski her zaman vardır.
-Kusursuz ve her ölçeğe uygun (scalable) bir vektör arama sistemi kurdum diyemem; çünkü HNSW optimizasyonları, cluster yönetimi veya devasa doküman setleri için performansı test etmedim.
-Tam korumalı (production-grade) kod yürütme sandbox'ı inşa ettim diyemem; çünkü kullandığım Docker izolasyonu (network none, cap-drop vb.) güçlü bir savunma sağlasa da, gVisor veya Firecracker gibi sanal makine tabanlı (microVM) bir yalıtım sağlamıyor.

## Week 2'den kalan technical debt

- Retrieval Quality (Arama Kalitesi) düğümüm şu an sadece "sonuç boş mu, değil mi?" diye bakıyor; bunu ileride model bazlı, corpus'a özgü ve ölçülebilir bir skor eşiğine (threshold) göre kalibre etmem gerekiyor.
- Etiket geçerliliği (Citation Validity) ile anlamsal doğruluk (Semantic Entailment) ayrımı: Şu an modelin ürettiği kaynak etiketlerinin (örn. [S1]) sadece format olarak geçerli olup olmadığına bakıyorum; ancak modelin o kaynağı çarpıtmadan, anlamsal olarak gerçekten doğru (grounded) kullanıp kullanmadığını ölçecek bir doğrulama/değerlendirme mekanizması eklemeliyim.
- Kural tabanlı yönlendiricinin (Deterministic Classifier) dil çeşitliliğine karşı kırılganlığı: Sorguları yönlendirirken kullandığım kelime eşleşmesine dayalı if/else yapısı, farklı doğal dil ifadelerinde kolayca kırılabiliyor; bu yapıyı, izin verilen rotalarla sınırlandırılmış güvenli bir LLM sınıflandırıcısıyla güncelleyerek esnekliği artırmam gerek.

## 3. haftaya taşımak istediğim 3 soru

1. İnsan onayına ihtiyaç duyan kritik yüksek riskli görevlerde (Human-in-the-loop), LangGraph üzerinde süreci duraklatıp dışarıdan onay bekleme (interrupt) mantığını nasıl entegre edebiliriz?
2. Hibrit Arama (Hybrid Search) ve Reranking yöntemlerini kullanarak Qdrant'tan dönen belgelerin isabet oranını (Hit@1) ve RAG kalitesini pratik olarak nasıl daha yukarı taşıyabiliriz?
3. ...
