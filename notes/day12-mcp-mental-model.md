## MCP neden var?
Yapay zeka modellerinin dış veri kaynakları ve araçlarla her seferinde özel kod yazmaya gerek kalmadan standart ve güvenli bir dille iletişim 
kurabilmesi için var.

## Host
İstemciyi ve yapay zeka modelini barındıran LangGraph gibi orkestrasyonları ve kullanıcı etkileşimini yöneten ana uygulamadır.

## Client
Host uygulamasının içinde çalışan ve standartlaştırılmış MCP protokolü üzerinden sunuculara istek gönderip veri alan iletişim katmanıdır.

## Server
MCP stdio server ayrı bir process boundary oluşturabilir; bu security isolation veya sandbox garantisi değildir.

## Tool
Yapay zeka modelinin dış dünyada bir eylem gerçekleştirmesine (hesaplama, API çağrısı, veritabanı yazması vb.) olanak tanıyan çalıştırılabilir 
fonksiyonlardır.

## Resource
Modelin okuması veya bağlam olarak kullanması için sunucu tarafından sağlanan, genellikle salt okunur veri kaynaklarıdır.

## Prompt
Sunucu tarafında tanımlanmış modelin belirli görevleri daha iyi yapmasını sağlayan yeniden kullanılabilir ve şablonlanmış talimat kalıplarıdır.

## Transport
İstemci ve sunucu arasındaki veri paketlerinin nasıl taşınacağını belirleyen ve genellikle stdio veya SSE (Server-Sent Events) tabanlı olan iletişim 
kanalıdır.

## Discovery
İstemcinin bağlandığı sunucunun hangi araçları kaynakları veya promptları desteklediğini otomatik olarak öğrenme ve listeleme yeteneğidir.

## Native dispatcher vs MCP
Native dispatcher araçları doğrudan ajanın kodu içinde aynı bellekte çalıştırarak çökme riski yaratırken, MCP bu araçları ayrı bir sunucu sürecine izole 
ederek sistemi korur ve dilden bağımsızlık sağlar.

## Resource vs Tool
Resource modelin sadece okuyup bağlamına kattığı pasif verilerken, Tool modelin aktif olarak çalıştırıp parametre gönderdiği fonksiyonlardır.

## stdio neden iyi bir başlangıç?
Ağ yapılandırması, port çakışmaları veya HTTP sunucusu kurma karmaşası olmadan işletim sistemi düzeyinde standart girdi/çıktı akışları üzerinden anında 
ve güvenli iletişim kurmayı sağlar.

## stdout neden protocol wire?
stdio taşıma mekanizmasında JSON-RPC mesajları doğrudan terminalin standart çıktısı (stdout) üzerinden akıtıldığı için, bu kanal fiziksel bir ağ kablosu 
görevi görür.

## Schema / validation
Şema doğrulaması yalnızca verinin tipini ve yapısını kontrol eden yapısal bir sözleşmedir; iş kuralları, yetkilendirme ve risk onay süreçleri şemanın değil, uygulamanın ayrı katmanlarının sorumluluğundadır.

## Type hint neden tek başına runtime validation değildir?
Pythondaki type hint'ler sadece geliştiriciye ve araçlara statik ipucu verir kod çalışırken gelen verinin tipini zorlamaz veya yanlış veri tipini 
engellemez.

## MCP neden sandbox değildir?
Araçlara standart bir erişim arayüzü sunar ancak bu araçların işletim sisteminde dosya silme veya veritabanı değiştirme gibi işlemleri yapmasını 
kısıtlayan bir güvenlik duvarı veya yalıtım sağlamaz.

## Tool listelenmesi neden trusted demek değildir?
Bir sunucunun discovery ile araçlarını anons etmesi, o araçların ajan tarafından doğrudan ve güvenle çalıştırılabileceği anlamına gelmez sistemin açık
bir onay listesine (allowlist) ihtiyacı vardır.

## Resource content neden instruction sayılmaz?
Kaynak içerikleri sadece modelin okuyacağı bağlamsal verilerdir modelin davranışını, kişiliğini veya hangi adımları izleyeceğini dikte eden sistem 
talimatları değillerdir.

## MCP workflow'umda hangi coupling'i azalttı?
Ajanın temel karar alma yapısı (LangGraph) ile kullanılan dış araçların (Qdrant, Kargo hesaplama) teknik entegrasyon detayları arasındaki sıkı bağı 
kopardı.

## Hangi yeni failure surface'i ekledi?
Ajan ve araçlar artık ayrı süreçler olduğu için süreçler arası iletişim kopmaları, stdout kirlenmesi veya sunucunun yanıt verememesi gibi yeni iletişim 
noktası hataları eklendi.

## MCP hangi problemi çözmedi?
MCP failure'ların standart bir boundary üzerinden ifade edilmesini kolaylaştırır; containment ve recovery application/runtime tasarımına bağlıdır.