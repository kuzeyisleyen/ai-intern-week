## RAG hangi problemi çözüyor?
Büyük dil modellerinin 3 problemini çözüyor:
1.Halisünasyon,modelin bilmediği konularda uydurmasını engeller
2.Güncellik ,model eğitim verisinde kalır rag ile güncel bilgi verilebilir
3.Özel veriye erişim ,şirket içi dökümanlar özel veritabanları gibi modelin eğitim verisinde olmayan bilgilere dayanarak cevap verir.
## RAG fine-tuning değildir çünkü?
Fine tuning modelin ağırlıklarını değiştirirerek ona yeni bir davranış veya stil öğretmektir yani eğitimdir.

## Parametric memory ve retrieved knowledge sezgisi
Parametric memory
Modelin GPUda aylarca eğitilirken milyarlarca parametresinin içine gömdüğü ezberlediği statik bilgidir.
retrieved knowledge
Modelin dışındaki bir veritabanında (Qdrant) tutulan, runtime da aratılıp getirilen dinamik ve somut bilgidir.

## Ingestion-time ile query-time farkı
Ingestion-time
Belgelerin okunup chunklara bölünüp embeddinglerinin çıkarılarak Vektör Veritabanına (Qdrant) kaydedildiği arka plan sürecidir.
query-time
Kullanıcının soruyu sorduğu sorunun vektörleştirilip benzer chunkların bulunduğu ve LLMe context olarak verilip cevabın üretildiği anlık süreçtir.

## Chunk neden var?
Retrievalın hassasiyetini etkiler.

## Chunk size neyi etkiler?
- Çok küçük chunk size spesifik bir bilgiyi bulmak kolaylaşır ama cümlenin bağlamı kaybolabilir.
- Çok büyük chunk size bağlam tamdır ama içinde gereksiz çok fazla bilgi barındırdığı için LLMin kafasını karıştırabilir.

## Overlap neden var?
Metni bölerken kritik bir cümlenin veya fikrin tam ortadan ikiye ayrılmasını önlemek için vardır. Bir önceki chunkın son kelimelerini, bir sonraki chunk'ın başına koyarak anlamsal bütünlüğün kaybolmamasını garanti ederiz.

## Characters ile tokens neden aynı şey değil?
Karakterler tek bir harf veya semboldür. Tokenlar ise dil modellerinin kelimeleri anlama biçimidir (genelde heceler veya alt kelimeler)

## Retriever yanlış chunk getirirse generator ne olur?
LLM kendisine verilen yanlış bağlama bakarak mantıklı ama tamamen gerçek dışı (veya sorudan alakasız) bir cevap üretir.

## Top-k neden sınırsız büyütülmez?
Alakasız dökümanlar artacağı için LLM'in halüsinasyon görme riski artar.
Token maliyeti ve cevap süresi çok uzar.

## Context construction nedir?
Vektör veritabanından dönen  ham metin parçalarını, LLMin anlayabileceği düzenli bir formata dönüştürme işlemidir. Örneğin metinlerin başına `[S1] Kaynak: belge.md` gibi citation (atıf) etiketleri ekleyerek metni yapılandırmaktır.

## Grounded answer ne demek?
Üretilen cevabın %100 oranında kendisine sağlanan context içindeki gerçeklere dayandırılmasıdır.

## Source attribution ne sağlar?
Güvenilirlik ve doğrulanabilirlik  sağlar. Kullanıcı yapay zekanın verdiği cevabın sonundaki `[S1]` etiketine bakarak bilginin hangi dökümanın hangi satırından alındığını kendi gözleriyle kontrol edebilir.

## Source attribution neyi garanti etmez?
Kaynak dökümanın kendisinin Doğru/Gerçek olduğunu garanti etmez. Eğer veritabanınıza yanlış bilgilerle dolu bir metin koyarsanız RAG bunu mükemmel bir şekilde bularak grounded bir yalan söyler. Ayrıca modelin o cümleyi yanlış yorumlamadığını kesin olarak garanti etmez.

## Retrieval evaluation ile answer evaluation farkı
Retrieval evaluation 
Doğru dökümanları bulabildik mi? sorusunun cevabıdır. Sadece Qdrant'ın ve Embedding modelinin başarısını ölçer.
Answer evaluation
LLM bu dökümanları kullanarak soruyu doğru akıcı ve uydurmadan cevapladı mı? sorusunun cevabıdır. LLM'in başarısını ölçer.

## Day 8'de gördüğüm en şaşırtıcı retrieval failure
Arama sırasında çok spesifik kelimelerin olduğu sorularda anlamsal benzerliğin kelime eşleşmesini yenmesi. Bazen "Docker stop nedir?" dediğimde "Docker start" ile ilgili kısımları getirmesi.
