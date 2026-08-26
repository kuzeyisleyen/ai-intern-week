Embedding Temelleri

Embedding, metin gibi bir girdiyi sabit boyutlu sayısal bir vektörle temsil eder. Benzer anlam taşıyan metinlerin vektör uzayında birbirine yakın olması hedeflenir. Bu temsil semantik arama, kümeleme, öneri ve sınıflandırma gibi görevlerde kullanılabilir.

Aynı embedding uzayı

Belgeler hangi embedding modeliyle vektörleştirildiyse kullanıcı sorgusu da aynı veya açıkça uyumlu modelle vektörleştirilmelidir. Farklı modellerin ürettiği aynı boyuttaki vektörler bile aynı koordinat anlamını paylaşmak zorunda değildir. Yalnız boyutların eşit olması uyumluluk sağlamaz.

Embedding modeli değiştirildiğinde mevcut belge vektörlerinin yeniden üretilmesi gerekir. Eski ve yeni model vektörlerini aynı collection içinde karşılaştırmak anlamsız sonuçlar oluşturabilir. Kullanılan model adı ve sürümü ingestion metadata'sında veya sistem yapılandırmasında takip edilmelidir.

Benzerlik

Cosine similarity, dot product ve Euclidean distance yaygın karşılaştırma yöntemleridir. Collection oluşturulurken kullanılan distance metriği embedding modelinin önerisiyle uyumlu olmalıdır. Daha yüksek skorun daha iyi eşleşme anlamına gelip gelmediği kullanılan metrik ve servis arayüzüne göre kontrol edilmelidir.

Vector search çoğu zaman mevcut kayıtlar arasından en yakın sonuçları döndürür. Sonuç bulunması, sonuçların soruyu gerçekten cevapladığı anlamına gelmez. Cevaplanamayan sorularda da matematiksel olarak en yakın fakat anlamsal olarak yetersiz chunk'lar gelebilir.

Chunking ile ilişkisi

Embedding modeli yalnız kendisine verilen metni temsil eder. Chunk çok büyükse birçok farklı konu tek vektörde birleşebilir. Çok küçükse gerekli anlam ve bağlam kaybolabilir. Bu nedenle retrieval kalitesi yalnız embedding modeline değil, chunk boyutuna ve overlap kararına da bağlıdır.

Boyut ve maliyet

Embedding dimension arttıkça her vektör için gereken depolama ve arama maliyeti artabilir. Daha büyük boyut her veri kümesinde otomatik olarak daha iyi retrieval sağlamaz. Model seçimi gerçek sorgularla oluşturulan değerlendirme kümesinde Hit@k, MRR veya benzeri ölçülerle karşılaştırılmalıdır.

Embedding bir şifreleme yöntemi değildir. Vektörler ve bunlarla birlikte saklanan payload kurumsal veri olarak korunmalı, yetkilendirme ve erişim politikalarına tabi tutulmalıdır.