```markdown
# Day 6 — Embedding Mental Model

## Token ID nedir?
Token ID,tokenların modelin hafızasındaki sıra numarasıdır.Sayının büyüklüğü küçüklüğüyle tokenlar arasında bir ilşki yoktur.

## Embedding nedir?
Embedding, tokeni modelin matematiksel olarak işleyebilceği çok boyutlu sayı vektöre dönüştüren temsil.

## Token ID ile embedding neden aynı şey değildir?
Token ID sadece embedding tablosunda hangi satırın alınıcağını belirleyen indeks numarasıdır.

## Neden bir vector?
Tokenları sadece bir sayı ile ifade edemeyiz çünkü tokenın birçok anlamı taşıması gerekir örneğin dil bilgisel kullanımı,olumlu olumsuz bağlamı veya diğer kelimelerle kullanılma biçimi bunları tek sayıyla anlamlandıramayız

## 3Blue1Brown videosundan çıkardığım 3 şey
1. Bir tokenin neden tek bir sayı yerine çok boyutlu vektörletemsil edildiği
2. Vektör uzayında birbirine yakın temsiller sezgisel olarak neyi ifade ettiği örneğin queen =king+men+women
3. token ıd ile embedding farkı

## Cosine similarity neyi ölçüyor?
Kosinüs benzerliği kelimlerin uzunluğuna veya metnin boyuna bakmaz.Çok boyutlu örenğin bugünkü örneğimiz 768 boyut uzayda iki vektör arasındaki açıyı ölçer.Bu vektörler aynı yöne bakıyorsa skor 1.0(mükemmel benzerlik) eğer vektörler birbirine dik alakasız konumlardaysa skor 0.0 a yaklaşır.

## Keyword search ile semantic search farkı
Keyword serach metinlerin içindeki kelimelerin birebir örtüşüp örtüşmediğine bakar.Örneğin pytest komutu nedir? gibi bir prompta iyi cevap verir.Fakat semantic search kelimlere değil cümlenin bütününe bakar.Örneklerde de gördüğümüz gibi Kullanıcı dosyalarım silinmesin dediğinde kalıcı veriyi aynı konsept olduğunu bilir ve eşleştirir.

## Generative model ile embedding model farkı
Generative model girdi oalrak metinalır ve bir sonraki kelimeyi tahmin ederek insan okuyabiliceği yeni meti üretir.Embedding model ise girdi olarak metin alır ancak yeni kelime üretmez sadece metni okur ve onu makinenin anlıcağı bir sayı vektörüne çevirir.

## Bugün beni şaşırtan bir retrieval sonucu

## Query:

Container silinince verim kaybolmasın.

## Beklentim:
İçinde doğrudan "container" kelimesi geçen dokümanların keyword eşleşmesinden dolayı en yüksek skorla 1. sıraya yerleşmesi.

## Gerçek top-3:
1.Docker named volume, container silinse bile kalıcı veri saklamak için kullanılabilir.
2.Bind mount, host üzerindeki bir klasörü container içine doğrudan bağlar.
3.Docker Compose, birden fazla container'ı aynı ağ üzerinde ayağa kaldırmak için YAML dosyası kullanır.

## Neden şaşırdım?
Query içerisindeki verim kaybolmasın ksımını semantic search ile kalıcı veri ile eşleştirmesine şaşırdım.
