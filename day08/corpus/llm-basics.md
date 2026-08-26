Büyük Dil Modeli Temelleri

Büyük dil modeli, verilen token dizisine dayanarak sıradaki token için olasılık dağılımı üretir. Model bu işlemi tekrar ederek metin oluşturur. Üretilen cevabın akıcı görünmesi, içindeki bütün bilgilerin doğru veya doğrulanmış olduğu anlamına gelmez.

Token ve context

Model metni doğrudan karakter veya kelime olarak değil, tokenizer tarafından oluşturulan token'lar üzerinden işler. Bir kelime tek token olabileceği gibi birden fazla token'a da ayrılabilir. Bu nedenle karakter sayısı ile token sayısı aynı değildir.

Context window, modelin tek istekte işleyebileceği toplam token miktarını sınırlar. System mesajı, kullanıcı sorusu, konuşma geçmişi, RAG context'i ve üretilen cevap bu bütçeyi birlikte tüketir. Çok sayıda belgeyi prompt'a eklemek yalnız maliyeti artırmaz; önemli bilginin ilgisiz içerik içinde kaybolmasına da neden olabilir.

Parametrik bilgi

Model, ön eğitim sırasında öğrendiği örüntüleri ağırlıklarında taşır. Bu bilgi parametrik bilgi olarak düşünülebilir. Model ağırlıkları bir veritabanı gibi doğrudan okunamaz ve belirli bir bilginin hangi eğitim kaynağından geldiği çoğunlukla gösterilemez.

Modelin eğitimden sonra gerçekleşen olayları bilmesi beklenmemelidir. Ayrıca eğitim sırasında gördüğü bir bilgiyi doğru zamanda ve doğru biçimde hatırlayacağı garanti değildir. RAG, çalışma anında harici bilgi getirerek bu sınırlamayı azaltmaya çalışır.

Halüsinasyon ve grounding

Halüsinasyon, modelin desteklenmeyen veya gerçeğe aykırı bir ifadeyi güvenli bir dille üretmesidir. Model, context yetersizken de cevap üretmeye eğilim gösterebilir. “Yalnız verilen context'e dayan” talimatı bu davranışı yönlendirir ancak fiziksel bir garanti oluşturmaz.

Grounded cevap, temel iddiaları verilen kanıtlarla desteklenen cevaptır. Bir cevabın kaynak etiketi içermesi tek başına grounded olduğunu kanıtlamaz. Kaynağın gerçekten ilgili iddiayı destekleyip desteklemediği ayrıca incelenmelidir.

Üretim ayarları

Temperature gibi ayarlar çıktı çeşitliliğini etkileyebilir. Düşük temperature daha tutarlı sonuçlar verebilir fakat doğruluk garantisi sağlamaz. Bilgi yoğun görevlerde model ayarlarını değiştirmeden önce retrieval sonuçları, context yapısı ve kaynak desteği kontrol edilmelidir.