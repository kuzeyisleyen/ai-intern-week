# Day 7 — Vector Database Mental Model

## Vector database hangi problemi çözüyor?
Çok sayıda yapılandırılmış veri arasında anlamsal yakınlık hesaplamasını çok hızlı şekilde yapılabilme zorluğunu çözer.

## Relational database'in yerine neden geçmiyor?
İlişkisel veri tabanlarında veri bütünlüğü ve kesin eşleşmeler gibi sorgular için kusursuzdur fakat vector databaseler ise anlamsal eşleşmeleri getirir.Bugünün deneylerinden elde ettiğim sonuçla yerine geçmesindense beraber kullanılabilir yapılardır. 

## Collection nedir?
Ortak özelliklere sahip vektörlerin bir arada tutulduğu çalışma alanlarıdır bir benzetmeyle geleneksel databaselerdeki tablo yapısına benzetilebilir.

## Point nedir?
Veritabanına kaydedilen her bir tekil öğedir.Mutlaka benzersiz id si olamk zorundadır.

## Vector nedir?
Kaydın anlamsal kaydını taşıyan sayısal dizi

## Payload nedir?
Vektörün yanında bir json yapısında tutulan ekstra meta verilerdir.(category ,text gibi)

## Metadata filter ne işe yarıyor?
Anlamsal arama yapmadan önce arama uzayını kesin kurallarla daraltır.Örneğin category = "docker" gibi.

## Vector index neden var?
Her vektörü tek tek aramanın getirdiği zaman kjaybını önlemek için vardır.Vektörleri zuayda gurplayarak sorgu süresini kısaltır.

## Persistence neden önemli?
Docker konteynırın kapandığında verilerin silinmemesi diskte volume üzerinde saklanarak sistemin kaldığı yerden devam etmesi için önemlidir.

## Day 6 memory search ile Qdrant arasındaki temel fark
Pyhton listesi veriyi ramde geçici tutar ve her kaydı tek tek tarar.Qdrant ise veriyi diskte saklar ve özel yapılarıyla çok sayıda kaydı hızlı bir şekilde sorgular.

## Exact query için relational DB'nin daha doğal olduğu bir örnek
Sistemde ID'si doc-07 olan kayıt nedir?

## Semantic query için Qdrant'ın daha doğal olduğu bir örnek
Konteyner silinince verilerim kaybolmasın

## Bugün beni şaşırtan bir sonuç
Sorguda geçen silince vekaybolmasın kelimelerinin hiçbiri belgede geçmemesine rağmen vektör matematiği sayesinde sistemin Docker named volume konusunu en yüksek skorla karşımıza çıkarması.