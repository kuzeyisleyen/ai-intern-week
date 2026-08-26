Vektör Veritabanı Temelleri

Vektör veritabanı, yüksek boyutlu embedding'leri saklamak ve bir sorgu vektörüne en yakın kayıtları bulmak için kullanılan bir veri sistemidir. RAG uygulamasında belge chunk'larının embedding'leri indekslenir; kullanıcı sorusunun embedding'i ile benzer olan chunk'lar retrieval aşamasında seçilir.

Collection, point ve payload

Qdrant'ta collection, benzer vektör yapılandırmasına sahip point'lerin mantıksal grubudur. Collection oluşturulurken vektör boyutu ve distance metriği tanımlanır. Vektör boyutu embedding modelinin gerçek çıktısıyla uyumlu olmalıdır.

Point genellikle kimlik, vector ve payload bileşenlerinden oluşur. Point kimliği internal integer veya desteklenen başka bir kimlik türü olabilir. docker:0 gibi uygulama düzeyindeki chunk kimliği payload içinde ayrıca korunabilir.

Payload, vektörle birlikte saklanan yapılandırılmış metadata'dır. RAG chunk'ında source, document_id, chunk_id, chunk_index, topic ve text alanları bulunabilir. Arama sonucu yalnız skor değil, context oluşturmak ve kaynak göstermek için gereken payload bilgisini de döndürmelidir.

Filtreleme

Metadata filtresi, aramanın hangi kayıtlar arasında yapılacağını sınırlar. Örneğin topic=docker filtresi yalnız Docker konulu chunk'ları aday yapabilir. Filtre performans optimizasyonundan ibaret değildir; retrieval aday kümesini değiştirdiği için recall ve cevap kalitesini doğrudan etkiler.

Yanlış filtre doğru kaynağı tamamen dışarıda bırakabilir. Kurumsal sistemlerde tenant, departman ve gizlilik seviyesi gibi filtreler aynı zamanda yetkilendirme sınırı oluşturur. Yetkisiz kayıtların önce getirilip daha sonra sonuçtan çıkarılmasına güvenilmemelidir.

Yaklaşık en yakın komşu araması

Büyük veri kümelerinde bütün vektörleri tek tek karşılaştırmak pahalıdır. HNSW gibi yaklaşık en yakın komşu indeksleri hız ile recall arasında denge kurar. İndeks ayarları sorgu gecikmesini, bellek kullanımını ve doğru komşuları bulma oranını etkileyebilir.

Top-k değerini büyütmek her zaman daha iyi değildir. Daha fazla sonuç, ilgili kanıtın yanında tekrarlı veya ilgisiz chunk'lar da getirerek context pollution oluşturabilir. Retrieval kalitesi gerçek sorular ve beklenen kaynaklarla ölçülmelidir.

Veri kaynağı ve indeks ayrımı

Vektör veritabanı her zaman asıl veri kaynağı değildir. Kaynak belgeler dosya sistemi, nesne depolama, SharePoint veya başka bir içerik sisteminde tutulabilir. Vektör veritabanı bu içeriğin aranabilir türevidir. Kaynak değiştiğinde ilgili embedding ve payload kayıtlarının senkronize edilmesi gerekir.