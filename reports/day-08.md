---
day: 8
date: 2026-08-26
status: completed 
embedding_model: embeddinggemma
generation_model: qwen3:1.7b
vector_db: qdrant
rag_collection: rag_chunks
unit_tests_passed: 5
integration_tests_passed: 2
blocker_count: 0
---

# Gün 8 — Native RAG ve Retrieval Evaluation

## 1. Day 7 Kapanışı
Broken embedding integration:
Değişkenler düzeltildi.
Invalid top-k regression:
Fonksiyon ismi güncellendi.
Production build_points testi:
Kendi kendini test eden sahte objeler yerine gerçek build_points() fonksiyonu FakeEmbeddingClient ile çalıştırıldı.
Rapor düzeltmeleri:
Point ID ve SQL ifadeleri değiştirildi.
Full test sonucu:
Tüm Unit ve Integration testleri yeşil (Passed) durumda
## 2. Bugünkü RAG Mimarisi
Ingestion Katmanı: Dökümanlar okunur, chunk_text() ile bölünür embeddinggemma ile vektörleştirilip Qdranta kaydedilir.
Retrieval Katmanı: Gelen soru embeddinggemma ile gömülür, Qdrantta Cosine Similarity ile aranıp en iyi sonuçlar getirilir.
Context Katmanı: Gelen chunklar [S1], [S2] etiketleriyle birleştirilir.
Generation Katmanı: Ollama (`qwen3:1.7b`) sadece bağlama sadık kalarak etiketleri kullanarak cevap üretir.

## 3. Literatür
Lewis et al. 2020:
Bir dil modelinin içine gömülü statik bilgisi (parametric memory) ile dışarıdan aratılıp getirilen dinamik bilgiyi (non-parametric memory) birleştirerek RAG konseptini literatüre kazandıran makale.
Parametric memory:
Dil modelinin (örneğin Qwen) eğitildiği ağırlıkların (weights) tamamıdır
Non-parametric/retrieved memory:
Dışarıdan getirilen, güncellenebilir vektör indeksindeki (örneğin Qdrant'taki belgelerimiz) harici bilgidir
Bizim sistemimiz paper'dan hangi açıdan farklı?
Orijinal makale bilgi kaynağı olarak devasa bir Wikipedia indeksini ve geleneksel bir seq2seq modelini temel alırken bizim yerel sistemimiz kendi özel Markdown belgelerimizi Qdrant üzerinde indeksleyerek qwen3 ve embeddinggemma modelleriyle çalışan modern, kişiselleştirilmiş bir mimaridir.

Modern RAG survey:
RAG sistemlerinin basit vektör aramasından başlayıp sorgu optimizasyonu, yeniden sıralama ve ajan tabanlı modüler mimarilere doğru nasıl evrildiğinin kapsamlı ve güncel bir haritasını çizer
Naive / Advanced / Modular hakkında kısa not:
Naive (basit indeksleme ve arama), Advanced (sorgu iyileştirme ve hibrit arama) ve Modular (farklı stratejilerin ihtiyaca göre yönlendirilmesi) olmak üzere RAG evrimini üçe ayırır. Biz Naive seviyeyi kurduk, yavaş yavaş gelişmiş aşamalara geçeceğiz.

## 4. Görsel Kaynak
IBM videosundan 3 çıkarım:
1. RAG kullanmak, modelin ağırlıklarını kalıcı olarak değiştiren ve yeniden eğiten "fine-tuning" işlemiyle aynı şey değildir; modele o anki soru için sadece geçici bir bağlam vermektir.
2. Eğer arama katmanı (retriever) modele yanlış veya alakasız bir metin (chunk) getirirse, modeli ne kadar güçlü olursa olsun hatalı bir bağlama dayanacağı için mecburen yanlış bir cevap üretir
3. Yapay zeka modeli genel dil yeteneğini kendi içinde barındırırken, özel ve güncel bilgiler modele çalışma zamanında (runtime) dışarıdan aratılarak sağlanır.

## 5. Corpus
Document sayısı:
7
Dosyalar:
agent-loop.md
compose.md
docker.md
embeddings.md
function-calling.md
llm-basic.md
vector-database.md
Neden bu corpus?
Bu haftaki AI Intern Week staj programı boyunca uğraştığım araçların ve sistemlerin kendisini RAG sistemine eklemek istedim.

## 6. Chunking
Config:
chunk_size=600, overlap=100
Toplam chunk:
36
Payload metadata:
    source: str
    document_id: str
    chunk_id: str
    chunk_index: int
    topic: str
    text: str
Overlap gözlemim:
100 karakterlik örtüşme, paragraf sonlarında bölünen kelimelerin ve teknik komutların parçalanmasını gayet başarılı şekilde önledi.

## 7. Ingestion Pipeline
Collection:
`rag_chunks`
Payload indexes:
`source` alanına göre Keyword Index atandı
İşlem sırası:
Dosyaları Oku -> Chunkla -> Batch halinde Embedding al -> Qdranta `PointStruct` olarak Upsert et.

## 8. İlk Retrieval
Question:
"Named volume ile bind mount arasındaki temel fark nedir?",
Top-k:
3
Retrieved chunks:
docker.md ve compose.md

## 9. Context Construction
Context formatı:
`[S1] Kaynak: docker.md \n <metin>`
Source labels:
`S1`, `S2`, `S3` şeklinde dinamik olarak indekslenerek LLM'in kullanabileceği referans noktalarına dönüştürüldü.

## 10. İlk Grounded Answer
Question:
"Named volume nedir?"
Answer:
Named volume, Docker tarafından yönetilen kalıcı bir veri alanıdır.
Citations:
[S1]
Citation validation sonucu:
Geçerli.

## 11. Retrieval Evaluation Dataset
Question count:
8
Answerable:
6
Unanswerable:
2

## 12. Hit@k
Hit@1:
Gözle görülür şekilde iyi ama her zaman %100 değil, bazen benzer ama genel metinler 1. sıraya çıkabiliyor.
Hit@3:
Çok daha başarılı, istenen cevap genelde ilk 3 sonuç içinde mutlaka yer alıyor.
Yorumum:
Vektör uzayı kelime eşleşmesi aramadığı için, Hit@3 RAG sistemleri için çok daha güvenli bir bağlam oluşturuyor.

## 13. Chunk-size Experiment
300/50:
Çok spesifik komutlar için iyi ama kavramsal açıklamalarda bağlam kopukluğu yaratır.
600/100:
Benim corpusum için en idealiydi
1000/150:
Alakasız kelimeler embedding vektörünü sulandırabilir.
Bu corpus'ta gözlemim:
Sizelar ile ne kadar çok oynasam da veri setinin küçüklüğü ve net cevapların metin içiünde bulunmasından dolayı sonucum değişmedi.
Neden evrensel sonuç değil?
Çünkü çok uzun metinler çok daha uzun bağlamlara ihtiyaç duyar. Veriye göre değişir.

## 14. Top-k Experiment
top_k=1:
Bazen cevabın yarısını veren chunk'ı yakalıyor, cevaplar yetersiz kalıyor.
top_k=3:
Çoğu soruda ideal.
top_k=5:
Anlamlı sonuçlar gelşede 2 veya 3 sonuç biraz konunun  dışında kalmıştı
Context pollution gözlemim:
Gereksiz bağlam, modelin dikkatini dağıtarak cevabın kalitesini düşürüyor.

## 15. Metadata Filter Experiment
Filtresiz:
Tüm corpusta arama.
Doğru filter:
`{"source": "docker.md"}` uygulandığında hız ve precision %100'e çıkıyor.
Yanlış filter:
Soruda "Ollama" geçerken `{"source": "compose.md"}` filtresi atıldığında sistem boş dönüyor veya alakasız yerleri zorluyor.
Recall açısından ders:
Kullanıcı ne istediğini tam biliyorsa Metadata filtrelemesi, saf vektör aramasından çok daha etkilidir.

## 16. Unanswerable Case
Question:
Türkiye'nin başkenti neresidir?
Retrieved:
En yüksek Cosine değerine sahip ama alakası olmayan teknik chunklar.
Model answer:
"Context bu soruyu cevaplamak için yeterli değil."
Fallback yaptı mı?
Evet.
Unsupported claim var mı?
Hayır. System Promptu mükemmel çalıştı.

## 17. Manual Generation Review
5 soru için grounding / relevance / citation / unsupported claim özeti:
Modellerin kendi kendine halüsinasyon görme hevesini sıkı bir system prompt zorunlu kaynak politikası ve Regex validasyonu ile kilit altına almayı başardım. Çıktılar %100 oranında Grounded fakat bunu verilerimdeki keskinlik ve sorularımdaki netliğe bağlıyorum.

## 18. Output
output/day08-rag-retrieval-eval.json


## 19. Testler
Unit Passed:5
Unit Failed:0
Integration Passed:2
Integration Failed:0
Full RAG smoke:Passed


## 20. AI Araçlarını Nasıl Kullandım?
Önce kendim tasarladığım:Uygulamalı kod yazımında mantığını tam kuramadığım algoritmalarda kodu yazdırmak yerine AIdan bana bir To-Do listesi ve kod iskeleti hazırlamasını istedim. İskeleti ve adımları aldıktan sonra içini tamamen kendim kodladım. Ayrıca yoğun RAG literatürünü ve makaleleri okurken kavramları daha hızlı sindirebilmek için AIı bir okuma asistanı olarak kullandım.
AI review: Kendi doldurduğum kod iskeletlerinde gözden kaçırdığım mantık hataları olup olmadığını veya mimaride bir açık bırakıp bırakmadığımı doğrulamak için kod review istedim.
AI'nın önerdiği ama değiştirdiğim/reddettiğim öneri: AI Unit testler sırasında dış bağımlılıkları taklit etmek için bana sahte bir DummyContext sınıfı kullanmamı önerdi.
Neden?: Yazdığım asıl BuiltContext mimarisi halihazırda yeterince izole ve test edilebilirdi. Sistemi sahte sınıflarla test etmek yerine, doğrudan kendi üretim kodumu kullanarak test etmenin çok daha güvenli ve gerçekçi olacağına karar verip bu mock önerisini reddettim.

## 21. Karşılaştığım Bir Hata
Problem: Farklı bir dosyadan (modülden) içe aktardığım bir fonksiyonu pipeline içinde çağırırken parametrelerini eksik ve yanlış sırada girdiğim için sistem çalışma zamanında çöktü ve TypeError hatası aldım.
İlk hipotezim: Hatayı ilk gördüğümde sorunun veritabanı bağlantısında veya fonksiyonun kendi içindeki algoritmada patladığını düşündüm.
Hangi layerda olduğunu nasıl buldum?: Terminaldeki hata loglarını adım adım geriye doğru okuduğumda hatanın fonksiyonun iç işleyişinde değil, benim o fonksiyonu pipeline içinden çağırdığım tam o bağlantı noktasında meydana geldiğini fark ettim.
Kaynak: Başka bir modüldeki fonksiyonun sözleşmesini tam incelemeden ve IDEnin yönlendirmesine dikkat etmeden parametreleri ezbere vermem.
Çözüm: İlgili dosyadaki fonksiyonun tanımına gidip benden tam olarak hangi argümanları, hangi sırayla beklediğini kontrol ettim ve çağrımı eksiksiz olacak şekilde düzelttim. Bu tecrübe, kodlara tip belirteçleri eklemenin ve input validation yapmanın bu tür hataları kod çalışmadan önce yakalamak için ne kadar önemli olduğunu bana gösterdi.

## 22. Bugünün En Önemli 5 Öğrenimi
1. Chunking İşlemi Sadece Metni Bölmek Değilmiş: Chunking işleminin metinleri öylesine parçalamak olmadığını, aslında sistemimin "retrieval granularity'sini" (geri getirme hassasiyetini) belirleyen çok kritik bir tasarım kararı olduğunu yaşayarak gördüm.
2.Ingestion ve Query Aşamalarının Kesin Ayrımı: Sistemi tasarlarken veri yükleme (ingestion time) ve soru sorma (query time) aşamalarını birbirinden tamamen ayırmam gerektiğini fark ettim.
3. Önce Retriever'ı (Arama Motorunu) Ölçme Zorunluluğu: Ürettiğim cevap gözüme güzel göründüğünde "sistem harika çalışıyor" demek yerine, önce arama (retrieval) kalitesine Hit@k gibi metriklerle bakmam gerektiğini öğrendim.
4. aha Büyük Bağlam Her Zaman Daha İyi Olmuyor: Sisteme vereceğim "Top-k" değerini sürekli artırmanın kaliteyi artırmadığını, tam aksine "context pollution" (bağlam kirliliği) yarattığını gözlemledim.
5. Hata Ayıklama İçin Modülerlik ve Observability (Gözlemlenebilirlik): Bütün süreci tek bir devasa fonksiyon içine yazmanın çok kolay ama debug etmenin imkansız olduğunu anladım.

## 23. Yarın Agentic Workflow Hakkında Merak Ettiklerim
1. Sabit ve öngörülebilir bir RAG akışından çıkıp, AIın 'Önce veritabanında arama mı yapayım, yoksa doğrudan bir API'a (tool) mı gideyim?' kararına kendisinin vardığı o esnek karar noktalarını kodda nasıl güvenli bir şekilde inşa edeceğiz?
