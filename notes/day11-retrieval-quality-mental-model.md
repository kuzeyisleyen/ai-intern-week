# Day 11 — Retrieval Quality Mental Model

## Dense retrieval hangi sorularda güçlü olabilir?
Kullanıcının  nasıl, neden, farkı nedir gibi kavramsal veya dolaylı sorular sorduğu durumlarda güçlüdür. Eşanlamlı kelimeleri, farklı cümle yapılarını ve cümlenin genel bağlamını kavrayarak metinleri anlam düzeyinde eşleştirebilir.

## Dense retrieval hangi sorularda zayıf olabilir?
Bugünkü deneylerimde çok kısa komutlar (down -v), tam eşleşme (exact match) gerektiren spesifik ID'ler veya konfigürasyon anahtarları (volumes:) arandığında zayıftı. Yeterli bağlam bulamadığında kelimeyi genel konseptlerle eşleştirip alakasız dokümanları getirebilir.

## Lexical / sparse retrieval hangi sorularda güçlü olabilir?
Belgelerde birebir geçtiği bilinen spesifik terimlerin, kesin parametrelerin veya hata kodlarının arandığı durumlarda çok güçlüdür. Yalnızca kelime frekansına odaklandığı için nokta atışı kelime eşleşmelerini yakalar.

## Lexical / sparse retrieval hangi sorularda zayıf olabilir?
Soru ile belgedeki kavramlar eşanlamlı kelimelerle ifade edildiğinde zayuıflaşabilir. Soru kökündeki yaygın kelimelerin ("hangi", "neden", "için") alakasız bir dokümanda çok tekrar etmesine aldanarak yanlış pozitif (false positive) üretebilir. Ayrıca BM25 tokenizer'ının MAX_REWRITES gibi alt çizgili veya özel karakterli terimleri parçalaması/yok sayması durumunda tamamen çökebilir.

## Hybrid retrieval neden var?
Anlamsal aramanın (Dense) esnekliği ile kelime bazlı aramanın (Sparse) kesinliğini bir araya getirerek iki sistemin birbirinin zafiyetlerini örtmesi ve arama kalitesini maksimize etmesi için vardır.

## RRF sezgisi
Farklı arama motorlarından gelen sonuçları birleştirirken ham puanlara değil, sadece sıralamaya (rank) güvenir. 1 / (k + rank) mantığıyla çalışarak, her iki modelin de üst sıralara yerleştirdiği dokümanların skorunu katlayarak ödüllendirir ve ortak bir fikir birliği oluşturur.

## Raw dense ve sparse score'ları neden doğrudan toplamıyorum?
İki skor tamamen farklı matematiksel evrenlere aittir.Bunları doğrudan toplamak veya ortalamasını almak doğru bir sonuç elde ettirmez.

## Hit@1
Sistemin getirdiği ilk 1. sıradaki dokümanın, kesin olarak beklenen doğru kaynak olup olmadığını ölçen başarı metriği.

## Hit@3
Beklenen doğru dokümanın, sistemin aday gösterdiği ilk 3 sıradaki listede yer alıp almadığını ölçer. Sistemin hedefi genel olarak yakalama potansiyelini gösterir.

## MRR
Doğru dokümanın bulunduğu sıraya göre ortalama kaliteyi ölçer. 1. sıra ile 2. sıra arasındaki o kritik farkı metriklere yansıtan en hassas araçtır.

## Query type neden önemli?
Genel başarı skorlarının arkasına saklanan sistem zafiyetlerini tespit edebilmek içindir. Örneğin bir arama motoru genel MRR'da yüksek başarı gösterirken, sadece command_or_code sorgularında başarının düştüğünü ancak sorguları kategorize ederek görebiliriz.

## Aggregate metric yükselmesi her query'nin düzeldiği anlamına gelir mi?
Hayır. Hybrid model Hit@3 oranını %100'e çıkarsa bile, RRF algoritması Lexical modelden gelen güçlü fakat yanlış bir sinyali alıp, Dense modelin kusursuzca 1. sıraya koyduğu bir dokümanı 2. sıraya itebilir. Genel ortalama artarken bazı spesifik sorgular kötüleşebilir.

## Retrieval failure ile ranking failure farkı
Retrieval failure, beklenen dokümanın prefetch limitine hiç girememesi, adayın tamamen kaçırılması durumudur. Ranking failure ise dokümanın aday listesinde (örn. 5. sırada) bulunmasına rağmen arama motorunun onu zirveye taşıyamamasıdır.

## Ne zaman reranker düşünürüm?
Hit@3 oranımızın %100'e ulaşıp Hit@1'in %82.35'te kalması, belgeleri bulduğumuzu ancak zirveye yerleştiremediğimizi gösteren kusursuz bir reranker senaryosudur. Örneğin, down -v sorgusunda beklenen compose.md dosyasının 3. sırada kalması veya "Vector database..." sorgusunda hedefin 2. sıraya itilmesi tam birer sıralama hatasıdır.Bu gibi durumlarda düşünürüm

## Ne zaman query rewriting düşünürüm?
down -v gibi aşırı kısa, motorsuz ve bağlamsız sorgularda. Her iki modelin de ne aradığını anlayamadığı bu komutu "Docker compose down -v ne işe yarar?" şeklinde arka planda genişletmek sistemi rahatlatabilirdi.

## Ne zaman retrieval algorithm yerine chunking/corpus'a dönmeliyim?
Eğer Hit@3 listesinde veya genel retrieved_sources dizilerinde beklenen dosya hiçbir şekilde geçmiyorsa. Bu durum modelin hatası değil, bilginin parçalanırken ortadan ikiye kesilmesi (chunk boundary) veya Qdrant'a eksik aktarılmasından kaynaklanır.

## Bugün gördüğüm en şaşırtıcı failure
Lexical (BM25) modelden en yüksek performansı beklediğimiz MAX_REWRITES ve tool_calls gibi tam eşleşme stringlerinde, tokenizer kuralları yüzünden sıfır sonuç üretilmesiydi. Arama motorlarının teorik varsayımlarının, pratik uygulamada bir alt çizgi (_) yüzünden tamamen çökebileceğini gösterdi