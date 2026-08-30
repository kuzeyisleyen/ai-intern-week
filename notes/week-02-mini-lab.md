Mikro Lab A — Top-k'yi Tekrar Gör
top_k=1 ile yaptığım aramada en yüksek skorlu tek bir chunk geldi ve temel tanımı yakaladı.
top_k=3 yaptığımda gelen ikinci ve üçüncü chunk'lar sisteme yeni teknik detaylar eklemek yerine çoğunlukla ilk chunk'ın tekrarını veya çok yakın varyasyonlarını getirdi.
Genişletilmiş arama her zaman yeni bir bilgi katmayıp bazen sadece bağlamı şişirerek modelin işlem yükünü artırabiliyor.

Mikro Lab C — Route'u Trace'ten Oku
"Merhaba" sorusunun trace çıktısında rota smalltalk, iz ise sadece ["classify_query", "direct_generate"] adımlarından oluştuğu için retrieve düğümü hiç tetiklenmemiştir.
"Named volume nedir?" sorusunda ise rota knowledge olarak belirlenmiş ve iz kaydına ["classify_query", "retrieve", "retrieval_quality", "generate", "validate_citations"] adımları eklenerek veritabanı taraması yapılmıştır.
Smalltalk sorularının veritabanında karşılığı olmadığı için arama maliyetinden kaçınmak adına retrieve adımına gitmemesi gerekirken, bilgi gerektiren sorular bağlam bulabilmek için mutlaka bu adımdan geçmelidir.