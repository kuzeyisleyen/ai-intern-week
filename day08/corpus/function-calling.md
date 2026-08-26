Function Calling ve Tool Kullanımı

Function calling, dil modelinin yalnız metin üretmek yerine uygulamanın tanımladığı bir aracı çağırmak için yapılandırılmış argümanlar önermesini sağlar. Model gerçek fonksiyonu doğrudan çalıştırmaz. Model araç adını ve argümanları üretir; uygulama bunları doğrular, yetki kontrolü yapar, fonksiyonu çalıştırır ve sonucu tekrar modele iletir.

Tool şeması

Her tool açık bir ad, açıklama ve argüman şemasına sahip olmalıdır. Açıklama, aracın hangi durumda kullanılacağını ve hangi durumda kullanılmaması gerektiğini belirtmelidir. Parametre adları belirsiz olmamalı; zorunlu alanlar, veri tipleri ve izin verilen değerler tanımlanmalıdır.

Çok geniş kapsamlı bir tool modele gereğinden fazla yetki verebilir. Küçük, amacı belirli ve doğrulanabilir araçlar daha güvenli bir tasarım oluşturur. Örneğin yalnız sipariş durumunu okuyan bir araç ile herhangi bir SQL ifadesi çalıştıran genel amaçlı araç aynı risk seviyesinde değildir.

Uygulamanın sorumluluğu

Modelin ürettiği tool argümanlarına güvenilmemelidir. Uygulama şema doğrulaması, kullanıcı yetkisi, kaynak sınırı, timeout ve hata yönetimi uygulamalıdır. Tool çağrısının başarılı dönmesi, dönen verinin kullanıcının sorusunu cevaplamak için yeterli olduğu anlamına gelmez.

Yan etkisi olan işlemlerde daha sıkı kontrol gerekir. Mesaj gönderme, ödeme başlatma, veri silme veya kayıt güncelleme gibi eylemler için kullanıcı onayı ve idempotency düşünülmelidir. Okuma araçları ile yazma araçları ayrı güvenlik politikalarına sahip olabilir.

Tool sonucu

Tool sonucu mümkün olduğunca yapılandırılmış, küçük ve açık olmalıdır. Gereksiz büyük çıktı context'i doldurabilir. Hata durumunda yalnız “başarısız” demek yerine hata türü ve yeniden denenebilirlik bilgisi verilmelidir. Gizli bilgiler ve dahili hata ayrıntıları modele kontrolsüz biçimde aktarılmamalıdır.

RAG ile ilişkisi

Retriever da bir tool olarak sunulabilir. Agent, sorunun kurum içi belge, SQL, web araması veya canlı API gerektirip gerektirmediğine karar verebilir. Ancak basit RAG akışında bu karar dinamik değildir; her soru önceden tanımlanmış retrieval adımından geçer.

