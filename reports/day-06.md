---
day: 6
date: 2026-08-24
status: completed 
embedding_model: embeddinggemma
embedding_dimension: 768
total_unit_tests_passed: 27
total_integration_tests_passed: 7
specific_unit_test_passed : 6
specific_integration_test_passed:3
blocker_count: 0
---

# Gün 6 — Embedding ve Semantic Retrieval

## 1. Week 1 Kapanışı
tool_name contract:
Tamamlandı.
run_agent smoke:
Tamamlandı.
Day 5 rapor senkronizasyonu:
Tamamlandı.
literatür/framework düzeltmeleri:
Tamamlandı.

## 2. 3Blue1Brown Video Notlarım
İzlediğim bölüm: 12:27–20:22

Bir token neden vector ile temsil ediliyor?
Çünkü bilgisayarlar kelimeleri anlamaz. Kelimeleri çok boyutlu bir uzayda koordinatlara çevirerek onların matematiksel olarak hesaplanabilir olmasını sağlarız.

Yakın vectors ne ifade edebilir?
Uzayda birbirine yakın olan vektörler anlamsal olarak benzer veya aynı bağlamda sıkça bir arada kullanılan kelimeleri veya cümleleri ifade eder.

Token ID ile embedding neden aynı şey değil?
Token ID, kelimenin sadece sözlükteki sıra numarasıdır hiçbir anlamsal bilgi taşımaz (A kelimesi 5, B kelimesi 6 olabilir ama alakaları olmayabilir). Embedding ise o kelimenin uzaydaki anlamsal haritası ve yönüdür.

## 3. Embedding Modeli
Model:
embeddinggemma

Gözlemlediğim dimension:
768

Generative modelden farkı:
Generative modeller promptu okuyup kelime kelime yeni bir metin üretir. Embedding modelleri ise yeni metin üretmez, metni okuyup onu temsil eden sabit boyutlu bir sayı (vektör) listesi döndürür.
## 4. İlk /api/embed Deneyim
Input:
Docker container içindeki veriyi kalıcı tutmak istiyorum.

İlk 5 değer:
İlk 5 Değer: [-0.10919785, 0.037083168, 0.0295148, 0.035536986, -0.014019868]

## 5. Cosine Similarity
Kendi açıklamam:
İki metnin çok boyutlu uzayda birbirine ne kadar paralel baktığını hesaplayan bir formül. Yönler aynıysa açı 0 dereceye, skor 1'e yaklaşır. Birbirlerine dik iseler açı 90 dereceye, skor 0'a yaklaşır.

## 6. Semantic Search Dataset
Document sayısı:
10

## 7. Semantic Search Deneyleri
Query 1:
Container silinse bile veriyi nasıl saklarım?
Top-3:
[0.7123] Docker named volume, container silinse bile kalıcı veri saklamak için kullanılabilir.
 [0.5232] Bind mount, host üzerindeki bir klasörü container içine doğrudan bağlar.
 [0.4677] Docker Compose, birden fazla container'ı aynı ağ üzerinde ayağa kaldırmak için YAML dosyası kullanır.

Query 2:
Modelin bir Python fonksiyonunu seçmesi nasıl çalışıyor?
Top-3:
[0.4530] Agent döngüsü (loop), modelin bir karar vermesini, araç çağırmasını ve sonucu değerlendirmesini sağlar.
 [0.3609] LLM'lerin function calling (araç kullanımı) yeteneği, onlara dış dünyadan veri çekme imkanı sunar.
 [0.3439] Büyük dil modellerine (LLM) system prompt ile belirli bir persona veya katı kurallar atanabilir.

Query 3:
Testlerimin gerçek LLM'e bağımlı olmasını istemiyorum.
Top-3:
[0.5389] Birim testlerinde dış servislere (API) bağımlılığı kesmek için mock objeleri kullanılır.
 [0.4111] Pytest unit testleri deterministic Python davranışlarını hızlı doğrulamak için kullanılabilir.
 [0.3613] Büyük dil modellerine (LLM) system prompt ile belirli bir persona veya katı kurallar atanabilir.
## 8. Keyword vs Semantic
Deney:
"pytest komutu nedir?" sorgusunda keyword eşleştirme test edildi

Çıkardığım ders:
Yapay zeka arama motorları her şeyin ilacı değildir. Kelimelerin anlamlarından ziyade doğrudan spesifik kelimelerin arandığı durumlarda Keyword arama daha iyi sonuç verir.

Semantic search'ün uygun olmadığı bir örnek:
Spesifik komutlar veya bir hata kodunun (Error 404 vb.) aranması.

## 9. Top-k
top_k=1:
Çok dar. Sistem, o konuyu farklı kelimelerle daha iyi açıklayan alternatif bir dokümanı gözden kaçırabilir.
top_k=3:
Benim veri setimdeki veri sayısına kıyasla ideal tutarlı yanıtları getirdi.
top_k=5:
Veri setimiz küçük olduğu için gereksiz gürültü üretmeye ve asıl konuyla alakası olmayan dokümanları da getirmeye başladı.

## 10. Output
output/day06-semantic-search.json

## 11. Testler
Unit Passed:6
Unit Failed:0

Integration Passed:3
Integration Failed:0

## 12. AI Araçlarını Nasıl Kullandım?
Kodu doğrudan yazdırmak yerine, önce algoritmaları ve mantığı araştırdım daha sonrasında kod iskeleti oluşturttum.Kodlamaların sonunda mamtık hatalarına karşı öneriler aldım ve kavramların araştırmasını yaptım.

AI'nın önerip benim değiştirdiğim/reddettiğim bir öneri:
...

Neden?
...

## 13. Karşılaştığım Bir Hata
Problem:
`JSONDecodeError: Expecting value: line 1 column 1 (char 0)`
Kendi kontrolüm:
Hatanın CLI kodundan değil, dosya okuma aşamasından (json.load) kaynaklandığını tespit ettim.
Kaynak:
`day06/data/documents.json` dosyasının içi boştu.
Çözüm:
Dosyanın içine JSON verilerini ekleyip dosyayı kaydederek tekrar çalıştırdım.

## 14. Bugünün En Önemli 5 Öğrenimi
1. Metinlerin uzaydaki yerini (vektör) bulmak için LLM'ler değil, özel Embedding modelleri kullanılır.
2. İki metnin benzerliği, vektörlerinin uzunluklarına değil, uzaydaki yönlerinin birbirine yakınlığına (Cosine Similarity) bağlıdır.
3. RAG sistemlerinde doğru belgenin çekilip çekilmediğini anlamak için (Retrieval Observability) skorları her zaman kayıt altına almalıyız.
4. Anlamsal arama (Semantic) ile kelime araması (Keyword) birbirinin rakibi değil, tamamlayıcısıdır.
5.RAG sistemlerinde LLM'e en iyi bağlamı sunmak ne kadar çok belge, o kadar iyi demek değildir doğru bir Top-K eşiği belirlemek sisteme gereksiz gürültü katılmasını önleyerek modelin odağını korur.

## 15. Yarın Vector Database Hakkında Merak Ettiklerim
1. Standart bir SQL veritabanı ile Vektör veritabanının indeksleme farkı tam olarak nedir?
