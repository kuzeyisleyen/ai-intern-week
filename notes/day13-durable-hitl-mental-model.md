# Day 13 — Durable Workflow & HITL

## Process memory ile persistent state farkı
Process memory program açıkken vardır ve kapandığında tamamen silinir. Persistent state ise bir veritabanı dosyasına kaydedilir ve program yeniden başlasa bile sürecin kaldığı yerden devam etmesini sağlar.

## Checkpointer neyi çözer?
Bir iş akışının (workflow) hangi adımda kaldığını o anki durumuyla (state) birlikte ilgili iş parçacığına (thread) özel olarak kaydeder. Böylece süreç çöktüğünde veya bir insan onayı beklediğinde veriler kaybolmaz.

## Store neyi çözer?
Farklı iş akışlarının veya farklı kullanıcıların ortaklaşa paylaşabileceği, uzun vadeli genel uygulama verilerini saklar.

## Checkpointer vs Store
Checkpointer bu belirli işlem nerede kaldı? sorusuna yanıt ararken, Store uygulama genel ve uzun vadede neleri hatırlamalı? sorusuna çözüm sunar.

## thread_id nedir?
Bir iş akışının kimliğini, yani hangi işleme ait olduğunu belirten kalıcı bir takip numarasıdır.

## Aynı thread_id ile yeni thread_id farkı
Aynı ID kullanıldığında sistem önceki kaydedilmiş durumdan (checkpoint) uyanarak devam eder. Yeni bir ID verildiğinde ise hiçbir geçmişi olmayan tamamen yeni ve bağımsız bir iş akışı başlatılır.

## Checkpoint neden backup değildir?
Checkpoint sadece sürecin o anki çalışma durumunu geçici bir dosya üzerinde tutar ve dosya bozulursa bu durum silinir. Gerçek bir yedekleme (backup) ise verilerin güvenli ve uzun ömürlü arşivlenmesi anlamına gelir.

## interrupt ne yapar?
İş akışının çalışmasını kritik bir noktada geçici olarak durdurur ve durumu veritabanına kaydeder. Dışarıdan, geçerli bir onay kararı gelene kadar süreci askıda tutar.

## Command(resume=...) ne yapar?
Durdurulmuş bir iş akışına dışarıdan kullanıcının kararını ("approve" veya "reject") ileterek sürecin kaldığı yerden yeniden çalışmaya başlamasını sağlar.

## Resume sırasında interrupt node'u neden yeniden başlar?
LangGraph çalışma mantığı gereği, duraklatılan bir düğüm (node) devam komutu aldığında işlemlerini baştan aşağı tekrar çalıştırarak kaldığı yeri günceller.

## Side effect neden interrupt'tan önce olmamalı?
Düğüm devam komutuyla yeniden çalıştığında, duraklamadan önce yapılan işlemler (örneğin veritabanına yazma) baştan çalışarak aynı işin yanlışlıkla iki kere yapılmasına yol açabilir.

## Idempotency nedir?
Aynı işlemi veya komutu birden fazla kez çalıştırsanız bile, sonucun ve uygulanan kalıcı değişikliğin sadece bir kez gerçekleşmesi prensibidir.

## Idempotency neden retry/durable execution ile birlikte önemli?
Süreçler çöktüğünde veya yeniden başlatıldığında düğümler istemsizce tekrar çalışabilir. Bunu yönetmek için aynı işlemin ikinci kez yapılmasını engelleyen bir kontrol mekanizması kurmak kritik hataları önler.

## approve/reject neden structured olmalı?
Kullanıcının "belki" veya serbest metinler girmesi yerine, sadece belirli kurallara uyan net kararların (onayla veya reddet) sisteme girmesini sağlamak içindir.

## High-risk action approval policy neden modelden gelmemeli?
Yapay zeka modeli bir işlemi güvenli zannedip yanlış karar verebileceği için, onaya tabi kritik eylemler her zaman kesin kod kurallarıyla yönetilmelidir.

## MCP tool olması neden otomatik trusted veya approval-free demek değildir?
Bir aracın sisteme ekli ve bulunabilir (discovery) olması, onun her işlemi kontrolsüzce ve güvenle yapabileceği anlamına gelmez. Hangi aracın insan onayı gerektireceği, güvenlik politikalarıyla ayrı ayrı denetlenmelidir.

## Persistent state içine neden DB client / MCP client koymam?
Durum (state) dosyaları sadece metin veya sayı gibi seri hale getirilip kaydedilebilir basit verileri tutmalıdır. Canlı ağ bağlantıları veya servis nesneleri kayıt dosyasına yazılamaz ve süreç yeniden başladığında zaten bağlantılarını kaybederler

## SQLite checkpointer neden production ölçeği anlamına gelmez?
SQLite yerel, tek bir dosya üzerinde çalışan ve durumu anlamak için kullanılan basit bir eğitim/laboratuvar aracıdır. Büyük ölçekli canlı sistemlerde çökmeleri önlemek için dağıtık yapılı daha güçlü veritabanlarına ihtiyaç duyulur.

## Bugün process restart'ı nasıl gerçekten kanıtladım?
Komutu aynı açık program içinde çalıştırmak yerine, Docker üzerinden yeni terminal komutlarıyla sistemi başlattım ve aynı thread_id kullanıldığında akışın kaybolmadan durduğu yerden devam ettiğini izleme loglarında gördüm.
