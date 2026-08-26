Docker Compose Temelleri

Docker Compose, birden fazla container'dan oluşan uygulamayı tek bir YAML dosyasında tanımlamayı sağlar. Uygulama servisi, veritabanı, Qdrant ve Ollama gibi bileşenler ayrı servisler olarak ifade edilebilir. Compose dosyası servislerin image, build, port, environment, volume ve network ayarlarını birlikte yönetir.

Service-name networking

Aynı Compose projesindeki servisler varsayılan ağ üzerinde birbirlerine servis adlarıyla ulaşabilir. Örneğin uygulama container'ı Qdrant servisine localhost:6333 yerine qdrant:6333 adresiyle bağlanır. Container içindeki localhost, o container'ın kendisini gösterir; host makineyi veya başka bir servisi göstermez.

Host bilgisayardan erişim gerektiğinde port mapping kullanılır. Örneğin 6333:6333 eşlemesi, host üzerindeki 6333 portunu container'ın 6333 portuna bağlar. Servisler arası iletişim için her zaman host portu açmak gerekmez.

Bağımlılıklar ve hazır olma durumu

depends_on, servislerin başlatılma sırasını ifade etmeye yardımcı olur; ancak bir servisin uygulama isteği kabul etmeye tamamen hazır olduğunu her durumda garanti etmez. Veritabanı process'i başlamış olsa bile migration veya recovery işlemi sürüyor olabilir. Bu nedenle kritik bağımlılıklar için healthcheck, retry ve kontrollü timeout kullanmak gerekir.

Retry mekanizması sınırsız olmamalıdır. Maksimum deneme sayısı, gecikme ve hata mesajı açıkça tanımlanmalıdır. Böylece uygulama başlangıç problemi sessizce sonsuz döngüye dönüşmez.

Volume ve kalıcılık

Compose içindeki named volume tanımı, container yeniden oluşturulduğunda verinin korunmasını sağlar. Qdrant verisi için qdrant_data gibi bir volume kullanılabilir. docker compose down container ve ağı kaldırabilir; named volume varsayılan olarak korunur. Volume'u da kaldıran seçenekler kullanıldığında veri kaybı oluşabileceği için komutların etkisi bilinmelidir.

Geliştirme kaynak kodu bind mount ile bağlanabilir. Buna karşılık veritabanı ve arama indeksi gibi uygulama verileri için named volume daha uygun olabilir. Production ortamında volume yedekleme ve geri yükleme prosedürleri ayrıca tasarlanmalıdır.

Yapılandırma tutarlılığı

Uygulamanın kullandığı servis adı, port ve model adı Compose yapılandırmasıyla uyumlu olmalıdır. README'de verilen komutlar gerçekten çalışan servis ve modül isimlerini kullanmalıdır. Compose dosyasının çalışması, uygulamanın sağlıklı olduğu anlamına gelmez; servis health durumu ve uygulama smoke testleri ayrıca doğrulanmalıdır.