Docker Temelleri

Docker, bir uygulamayı kodu, çalışma zamanı ve bağımlılıklarıyla birlikte taşınabilir bir container içinde çalıştırmayı sağlar. Container, image adı verilen değişmez bir şablondan başlatılır. Image uygulamanın dosyalarını ve başlangıç talimatlarını taşırken container bu image'ın çalışan örneğidir. Aynı image kullanılarak birden fazla bağımsız container oluşturulabilir.

Image ve container yaşam döngüsü

Image genellikle bir Dockerfile kullanılarak oluşturulur. Dockerfile içindeki her anlamlı adım image katmanlarına dönüşebilir. Katman önbelleği, değişmeyen adımların sonraki build işlemlerinde tekrar kullanılmasını sağlar. Bu nedenle bağımlılık dosyalarını önce kopyalamak, bağımlılıkları kurmak ve uygulama kodunu daha sonra eklemek build süresini azaltabilir.

Container silindiğinde container'ın yazılabilir katmanındaki veriler de kaybolabilir. Kalıcı tutulması gereken veriler container dosya sistemi yerine volume veya harici bir veri servisine yazılmalıdır. Uygulama logları da yalnız container içinde tutulmamalı; standart çıktıya veya merkezi bir log sistemine yönlendirilmelidir.

Named volume

Named volume, Docker tarafından yönetilen kalıcı bir veri alanıdır. Kullanıcı volume'a mantıksal bir ad verir; fiziksel konumu Docker yönetir. Veritabanı dosyaları veya Qdrant depolaması gibi container yeniden oluşturulduğunda korunması gereken veriler için uygundur.

Container'ın durdurulması veya silinmesi named volume'u otomatik olarak silmez. Bununla birlikte volume açıkça silinirse içindeki veriler de kaybedilebilir. Bu nedenle named volume kullanmak tek başına yedekleme stratejisi değildir.

Bind mount

Bind mount, host makinedeki belirli bir dosya veya klasörü container içine bağlar. Geliştirme sırasında kaynak kodda yapılan değişikliklerin container tarafından hemen görülmesi için kullanışlıdır. Host yolu doğrudan belirtildiği için named volume'a göre makinenin dizin yapısına daha bağımlıdır.

Named volume genellikle container tarafından üretilen kalıcı uygulama verisi için, bind mount ise geliştiricinin host üzerinde düzenlediği kaynak dosyaları paylaşmak için daha doğal bir seçimdir. Bu ayrım mutlak değildir; seçim veri sahipliği, taşınabilirlik, izinler ve operasyon gereksinimlerine göre yapılmalıdır.

Sağlıklı kullanım

Container içinde gizli bilgileri image katmanına gömmemek gerekir. Parolalar ve erişim anahtarları environment variable, secret yönetim sistemi veya platformun güvenli yapılandırma mekanizmasıyla verilmelidir. Image sürümleri mümkün olduğunda sabitlenmeli, healthcheck kullanılmalı ve container'ın gereksiz root yetkisiyle çalışması önlenmelidir.