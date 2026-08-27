# Day 9 — Agentic Workflow Mental Model

## Workflow ile agent loop arasındaki fark
Workflow önceden çizdiğim belirli ve kurallı bir yolda ilerlerken agent loop LLM in o anki duruma göre kendi kararlarını verip yön çizdiği yapıdır.

## Deterministic node ne zaman daha iyi?
Hata payının olmaması gereken maliyetin ve hızın kritik olduğu kural tabanlı işlemlerde daha iyi.

## LLM decision ne zaman değer katıyor?
Sorunun çok karmaşık olduğu kurallarla öngöremediğim veya bağlamı anlayıp yeni bir araç seçilmesi gereken dinamik durumlarda değer katıyor.

## Agentic = her şeyi LLM'e bırakmak neden değil?
Çünkü LLM halüsinasyon görebilir ve kendi kendine sonsuz döngülere girebilir önemli kararları ve sınırları yazdığım kodlarla güvenceye almam gerekir.

## State neden merkezi?
Sistemdeki her bir adım birbirine doğrudan veri aktarmak yerine merkezi statei güncellediği için veri kaybını önler ve izlenebilirliği sağlar.

## Node nedir?
İş akışımda belirli bir görevi (örneğin arama yapma, cevap üretme) yerine getiren mevcut statei alıp güncelleyerek döndüren bağımsız fonksiyonlardır.

## Edge nedir?
Nodeların hangi sırayla çalışacağını ve akışın hangi fonksiyondan hangisine geçeceğini belirleyen bağlantı yollarıdır.

## Conditional edge nedir?
Akışın sabit bir yoldan değil state içindeki değere bakarak dinamik olarak yön değiştirmesini sağlayan yapıdır.

## Cycle/retry neden guard ister?
Model inatla aynı hatayı yapıp sistemi sonsuz döngüye sokabileceği için maksimum adım sayısı (MAX_STEPS) gibi bir fren mekanizması koymak zorundayım.

## Query rewrite neyi çözmeye çalışıyor?
Kullanıcının eksik veya kapalı sorduğu soruları vektör veritabanının daha iyi anlayacağı net ve semantik arama sorgularına dönüştürmeyi sağlıyor.

## Query rewrite her zaman faydalı mı?
Hayır bazen basit soruları gereksiz yere karmaşıklaştırıp asıl bağlamı bozabiliyor ve fazladan api maliyeti yaratabilir.

## Smalltalk neden retrieval'a gitmemeli?
Merhaba nasılsın gibi sohbet soruları veritabanında bulunmadığı için arama maliyeti ve zaman kaybı yaratmasını engellemek istiyorum.

## Tool route neden allowlist ister?
LLM in rastgele fonksiyonları kendi başına tetiklemesini engellemek için sadece belirlediğim araçları listeliyorum.

## LangGraph native kodumda neyi soyutladı?
Benim manuel yazdığım karmaşık while döngülerini ve if/else zincirlerini düğümler ve kenarlar mantığıyla kendi altyapısına aldı.

## Framework hangi yeni maliyeti getirdi?
Projeme dışarıdan yeni bir kütüphane bağımlılığı ve LangGraphın kendi sözdizimini öğrenme zorunluluğu ekledi.

## Native ve LangGraph arasında bugün tercih yapmam gerekse hangi durumda hangisini seçerim?
Doğrusal ve basit akışlarda native Python kodunu seçerim, ancak döngülerin ve çoklu araçların olduğu karmaşık senaryolarda LangGraph kullanırım.
