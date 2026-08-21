## Çözdüğü temel problem
## MRKL : 
LLM in güncel ve özel bilgiye erişememesi ,kesinlik gerektiren işlemlerde güvenilir olamaması ve her görev için ayrı model ihtiyacı. 
## ReAct :
Reasoning işlemlerin dış dünyaya kapalı olması,acting işlemlerin ise plansız kalması
## Toolformer : 
Tool kullanımının  çok insan etiketi veya göreve özel promp gerektirmesi.,

## Modelin rolü 
## MRKL : 
Girdiyi anlamak ve router olarak expert seçmek.
## ReAct :
Mevcut bağlama göre thougt veya action üretmek.
## Toolformer : 
Tool gerekip gerekmediğini ,tool adını ,argümanları ve kullanım yerini üretmek.

## External tool/module 
## MRKL : 
Bağımsız Uzmanlar (Experts): Hesap makinesi, hava durumu apisi vb. modüller.
## ReAct :
Etkileşim Ortamı (Environment): Aksiyon alınıp gözlem yapılan bir dış dünya
## Toolformer : 
Metne Gömülü Çağrılar: Metin içine yerleştirilmiş özel api etiketleri (örn. [Calc(5+5)]).

## Reasoning yaklaşımı 
## MRKL :
 Sınıflandırma ve yönlendirme odaklı bir akıl yürütme kullanır. Gelen metni adım adım bir analizden ziyade işi doğru adrese teslim etme mantığıyla düşünür.
## ReAct :
 Akıl yürütme (Thought) süreci kullanır. Ajan eyleme geçmeden önce durumu analiz etmek zorundadır.Örneğin kullanıcı Türkiye'nin başkentinin nüfusunu soruyor. Önce başkenti bulmalıyım sonra o şehrin nüfusunu aramalıyım şeklinde kendi iç mantığını metin olarak üreterek adım adım düşünür.
## Toolformer : 
Açık bir düşünme (reasoning) süreci yoktur. Dil modelinin klasik sıradaki kelimeyi tahmin etme mantığıyla çalışır. Model normal bir metin üretirken, eğitiminde öğrendiği kalıplara dayanarak bağlamın uygun olduğunu hissettiği an araya otonom olarak bir api çağrısı yerleştirir

## Acting yaklaşımı 
## MRKL :
Seçilen uzman sisteme (API, Veritabanı vb.) girdiyi göndermek ve onun çalışmasını sağlamak.
## ReAct :
Düşünce (Thought) aşamasından hemen sonra, sistemin anlayacağı özel bir formatta komut üretmek.
## Toolformer : 
Metni oluştururken araya özel api etiketleri (örn. [Calculator(5+5)]) basarak aracı tetiklemek.

## State/history fikri
## MRKL :
Yok istek uzmana gider cevap döner. Çok adımlı bir geçmiş (hafıza) tutma mekanizması kurgulanmamıştır.
## ReAct :
Var düşünce -> eylem -> gözlem döngülerinin tamamı belleğe (context) yazılır. Ajan tüm geçmiş adımlarına bakarak hareket eder.
## Toolformer : 
Sadece metşn geçmişi, ayrı bir ajan belleği yoktur. O ana kadar üretilen metin ve içine gömülen api sonuçları geçmişi oluşturur.

## Planning varmı?
## MRKL :
Hayır,görevi anında ilgili uzmana paslar.
## ReAct :
Evet,dönen sonuca (Observation) bakar ve bu bilgi yetmedi, şimdi şu aracı kullanmalıyım diyerek planını günceller
## Toolformer : 
Hayır,kelime kelime metin üretirken anlık ihtiyaç duyduğunda araç kullanır, stratejik bir adım planlaması yapmaz.

## Tool nasıl seçiliyor? 
## MRKL :
Router, elindeki sabit uzmanlar listesinden gelen isteğe en uygun olanı eşleştirerek seçer.
## ReAct :
Ajan, kendisine verilen araçların açıklamalarını okur. Duruma göre hangi aracı ve hangi parametreleri kullanması gerektiğini kendi belirler.
## Toolformer : 
Model bunu eğitim aşamasında öğrenmiştir. Metnin bağlamına göre hangi aracı çağırması gerektiğine metin üretimi sırasında otonom karar verir.

## Observation/result nasıl kullanılıyor? 
## MRKL :
Uzmandan dönen kesin sonuç, genellikle bir doğal dil üreticisine verilip doğrudan kullanıcıya iletilecek son mesaja dönüştürülür.
## ReAct :
Araçtan dönen yanıt bir observation olarak sisteme girer. Model bu yeni veriyi, sıradaki adımını düşünmek için hammadde olarak kullanır.
## Toolformer : 
Dönen yanıt, modelin ürettiği metnin içine doğrudan gömülür ve model sanki o bilgiyi en başından beri biliyormuş gibi cümlenin kalanını yazar

## Termination (bitiş) fikri
## MRKL :
Çoğunlukla tek adımlıdır. Uzman çalışır, cevap alınır ve süreç orada sonlanır.
## ReAct :
Model, problemi çözecek yeterli veriyi topladığına karar verdiğinde döngüyü kıracak özel bir Final Answer komutu üreterek bitirir
## Toolformer : 
Klasik LLM mantığıdır model yazacağı metni bitirdiğinde doğal olarak sonlanır.

## Training gerekiyor mu?
## MRKL :
Yönlendirici sistemin uzmanları doğru tanıması için bazen ince ayar (fine-tuning) gerekebilir.
## ReAct :
Hayır.
## Toolformer : 
Evet.

## Runtime/inference mekanizması mı?
## MRKL :
Çalışma zamanında (runtime) işleri dağıtan bir orkestrasyon mekanizmasıdır
## ReAct :
Çalışma zamanında (inference) çalışan, prompt ve döngü tabanlı bir mekanizmadır.
## Toolformer : 
Hem modele işlenmiş mimari bir eğitim yöntemi hem de bir inference mekanizmasıdır.

## Güçlü yön
## MRKL :
Matematik veya kod gibi işler, o işin gerçek "uzmanına" (hesap makinesi vs.) bırakıldığı için halüsinasyon riski düşüktür.
## ReAct :
Modelin "Neden bu kararı verdiğini" ve "Nerede hata yaptığını" Thought (Düşünce) adımlarını okuyarak net şekilde görebiliriz.
## Toolformer : 
Araç kullanımı modele sonradan yamalanmamış, modelin metin üretme doğasına işlenmiş olduğu için çok daha pürüzsüz çalışır.

## Sınırlılık
## MRKL :
Esnekliği düşüktür. Yeni bir özellik veya uzman eklemek sistemin mimarisini değiştirmeyi gerektirir. Karmaşık mantık yürütmede zorlanır.
## ReAct :
Sürekli düşünce ve gözlem üretmek, modelin hem daha yavaş çalışmasına hem de context penceresini çok hızlı doldurmasına sebep olur.
## Toolformer : 
Sisteme yepyeni bir araç/API eklemek için, veri setini güncelleyip modeli yeniden eğitmek (fine-tune) gerek

##  Bizim native agent'a benzeyen taraf
## MRKL :
Araçları projemizde ayrı bağımsız fonksiyonlar (tools.py) olarak tanımlamamız ve modeli sadece buralara parametre göndermek için kullanmamız.
## ReAct :
Yazacağımız ajan döngüsünün (while loop) "Araç çalıştır -> Sonucu modele geri ver -> Tekrar düşün" şeklindeki yapısı doğrudan ReAct'in yaklaşımıdır.
## Toolformer : 
Modelin aracı kullanma isteğini, harici bir prompt hilesi yerine, Ollama'nın Native Tool Calling özelliği sayesinde kendi yapısı içinde doğal olarak (JSON) üretmesi.

## Bizim agent'tan farklı taraf
## MRKL :
taraf	Bizde gelen isteği yönlendiren sabit/kural bazlı bir router (yönlendirici) yok; hangi aracı seçeceğine model otonom karar veriyor.
## ReAct :
ReAct modelindeki though action gibi uzun uzun metin tabanlı prompt formatları yerine, biz doğrudan api seviyesinde modern tool calling şemaları kullanıyoruz.
## Toolformer : 
Biz modeli araçları öğrenmesi için sıfırdan eğitmiyoruz. Hazır bir modele, mevcut araçların listesini çalışma anında veriyoruz.



## AI'dan Duyup Orijinal Kaynaktan Doğruladığım İddia

AI'nın iddiası:
Toolformer modeli, hiçbir insan yardımı olmadan API kullanmayı tamamen kendi kendine öğreniyor.

Kontrol ettiğim orijinal kaynak:
Meta'nın Toolformer (2023) makalesi.

Paper'ın gerçekten söylediği:
Ortada sihir yok. Geliştiriciler modele önce birkaç örnek veriyor. Model buna bakıp bir sürü deneme API çağrısı yapıyor. Sadece işine yarayan çağrıları filtreleyip kendi eğitim setini oluşturuyor. Yani sıfırdan öğrenmiyor, kendi eğitim verisini hazırlıyor.

İlk ifade fazla güçlü müydü?:
Evet bayağı abartılı. AI "sıfır insan müdahalesi" diye söylüyor ama arkada kurgulanmış çok iyi bir veri filtreleme algoritması var. Sihir değil bildiğimiz mühendislik ve otomasyon.