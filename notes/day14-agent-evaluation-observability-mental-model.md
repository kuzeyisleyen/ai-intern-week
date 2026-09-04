## Test vs Evaluation vs Observability
Test, kodun beklenen sözleşmeye uyup uymadığını kontrol ederken, değerlendirme (evaluation) sistemin genel kalite ve başarısını ölçer; gözlemlenebilirlik (observability) ise canlı bir çalışma anında arka planda tam olarak nelerin yaşandığını gösterir.

## Golden dataset nedir?
Sistemin davranışlarının ne zaman doğru kabul edileceğini önceden belirlediğimiz, yapay zekanın ezberlemesi için değil performansını test etmek için tasarlanmış, ideal senaryoları barındıran referans veri setidir.

## Gold label'ı kim belirlemeli?
Doğru kabul edilen etiketleri yapay zeka değil, sistemin mevcut kısıtlarını, kurallarını ve yeteneklerini en iyi bilen geliştirici belirlemelidir.

## Route accuracy
Sistemin, kendisine gelen sorguları doğru genel kategoriye (örneğin smalltalk, knowledge veya tool) ne oranda başarılı atadığını gösteren temel doğruluk oranıdır.

## Per-class accuracy
Genel başarı oranının yanıltıcı olmasını engellemek için, modelin her bir kategori özelinde (örneğin sadece kargo işlemlerinde veya sadece sohbetlerde) gösterdiği başarıyı ayrı ayrı ölçer.

## Confusion matrix
Beklenen ve tahmin edilen sonuçları yan yana koyarak, modelin hangi sınıfları birbiriyle karıştırdığını (örneğin bilgi sorgularını işlem sanması) ortaya çıkaran hata analiz tablosudur.

## Tool-selection accuracy
Yönlendirici doğru ana kategoriye gitse bile, içerideki spesifik araçlar arasından gerçekten doğru aracı seçip seçmediğini ölçer.

## Provider correctness
Seçilen aracın, uygulamanın mimarisinde tanımlandığı şekilde doğru sağlayıcı üzerinden (örneğin yerel bir fonksiyon mu yoksa dış bir MCP servisi mi) çalıştırılıp çalıştırılmadığını kontrol eder.

## Approval-policy correctness
Sistemin, kritik işlemler yapmadan önce kural gereği insandan onay istemesi (approval required) gereken durumlarda bu güvenlik politikasını başarılı bir şekilde işletip işletmediğini doğrular.

## Terminal-state correctness
Gidiş yolu doğru görünse bile, işlemin sonunda beklenen nihai duruma (tamamlandı, reddedildi veya hata verdi) ulaşıp ulaşmadığını kontrol eder.

## Neden final answer tek başına yeterli değil?
Sistem dışarıdan bakıldığında doğru cevabı vermiş gibi görünse de, arka planda gereksiz araçlar kullanmış, güvenlik adımlarını atlamış veya hatalı yollara sapmış olabileceği için süreç de sonuç kadar önemlidir.

## Trajectory evaluation
Sistemin sadece verdiği cevaba değil, LangGraph üzerinde hangi düğümleri (sınıflandırma, arama, kalite kontrol vb.) hangi sırayla ziyaret ettiğine bakarak izlediği yolu değerlendirir.

## Strict trajectory
Sistemin izlediği yolun, araya hiçbir ekstra adım girmeden veya eksik adım bırakılmadan, önceden tanımlanmış adımlarla birebir ve katı bir şekilde aynı olmasını bekler.

## Ordered / allowed trajectory
Ana kontrol adımlarının sırasını korumasına odaklanır, ancak araya sorgu düzeltme veya kalite kontrol gibi opsiyonel alt adımların girmesine esneklik tanıyan yörünge eşleştirmesidir.

## Keyword router baseline
Yeni ve akıllı bir modelin gerçekten ne kadar fayda sağladığını kanıtlamak için, kıyaslama yapabilmek adına basit kelime eşleştirme yönteminin (eski sistemin) mevcut performansını kaydetmektir.

## LLM semantic router
Yönlendirme kararını kelimelerin varlığına göre değil, kullanıcının cümlesinin ardındaki asıl niyeti ve anlamsal (semantik) bütünlüğü anlayarak veren yapay zeka modelidir.

## Structured output neden gerekli?
Yapay zekanın ürettiği kararın yazılım tarafından güvenle ayrıştırılıp bir sonraki adımın tetiklenebilmesi için, metnin serbest bir düz yazı değil, kesin kurallara bağlı bir JSON formatında olması şarttır.

## Router fallback
Yapay zeka modelinin bağlantı hatası, zaman aşımı veya bozuk çıktı üretmesi gibi durumlarda, sistemin tamamen çökmesini engellemek için tekrar basit kelime tabanlı yönlendiriciye dönme işlemidir.

## Accuracy vs latency trade-off
Daha büyük modeller kullanarak sistemin doğruluğunu (accuracy) artırırken, bunun karşılığında kullanıcının bekleyeceği sürenin (latency) uzaması arasındaki dengeyi ve mühendislik maliyetini ifade eder.

## Out-of-capability query neden taxonomy problemi olabilir?
Kullanıcının hava durumu gibi sistemde bulunmayan bir şeyi sorması durumunda, eldeki mevcut seçeneklerin (sohbet, bilgi, araç) yetersiz kaldığını ve sınıflandırmaya "desteklenmeyen" diye yeni bir yol eklenmesi gerektiğini gösterir.

## Route classification neden authorization değildir?
Yapay zekanın kullanıcının niyetini anlayıp "araç kullanılmalı" demesi, o aracın anında ve yetkisizce çalıştırılabileceği anlamına gelmez; sonrasında insan onayı ve kesin sistem kısıtlamaları devreye girmelidir.

## Observability span/event mental modeli
Sistemin çalışmasını devasa tek bir işlem olarak görmek yerine, yönlendirme, arama ve model yanıtı gibi küçük, bağımsız ve kendi süresi olan izleme parçalarına (span) bölerek analiz etmektir.

## run_id vs thread_id
Sistemdeki her bağımsız işlem denemesi yeni bir run_id alırken, kesintiye uğrayıp devam eden (resume) oturumların hepsini tek bir konuşma geçmişine bağlayan çatı kimlik thread_id'dir.

## Prompt/query logging neden riskli?
Kullanıcıların sorduğu soruları veya yüklediği dosyaları maskelemeden olduğu gibi loglara kaydetmek, özel hayatın gizliliğini ihlal edip ciddi veri sızıntılarına neden olabileceği için oldukça tehlikelidir.

## OpenTelemetry neyi standardize etmeye çalışıyor?
Farklı geliştiricilerin ve sistemlerin loglarını, sürelerini ve metriklerini tamamen ortak bir isimlendirme (telemetry modeli) altında birleştirerek hata ayıklamayı evrensel ve kolay hale getirmeyi amaçlar.

## LLM-as-judge ne zaman mantıklı?
Cevabın yeterince yararlı olup olmadığı veya kaynak dokümandaki tonu doğru yansıtıp yansıtmadığı gibi kesin bir doğrusu olmayan, anlamsal kalitenin değerlendirildiği durumlarda mantıklıdır.

## LLM-as-judge ne zaman gereksiz?
Onay istendi mi, doğru araç seçildi mi veya sistem tamamlandı durumuna geçti mi gibi, kod üzerinden doğrudan ve kesin olarak ölçülebilen deterministik olaylar için büyük dil modellerini kullanmak gereksiz ve maliyetlidir.
