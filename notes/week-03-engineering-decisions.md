## Native-First'ten LangGraph'a Geçiş
Context
Başlangıçta ajan orkestrasyonunu ve durum yönetimini (state management) standart Python kodlarıyla kendim yazmıştım. Ancak sisteme tool calling (araç çağırma) özellikleri ekledikçe, döngüleri ve state'i manuel olarak yönetmek spagetti koda dönüşmeye ve hata toleransını düşürmeye başladı.

Decision
Ajan orkestrasyonu ve döngüsel yönlendirme işlemleri için LangGraph çatısına geçmeye karar verdim.

Evidence
LangGraph'ın yapısı, ajanlar arası geçişleri deterministik düğümler ve kenarlar (nodes/edges) olarak modellememi sağladı. Bu sayede LLM'in kendi içindeki karar döngüsünü kesintiye uğramadan yönetebildim. Ayrıca debug yaparken sadece log okumak yerine sistemin state makinesi gibi görselleştirilebilir olması işimi çok kolaylaştırdı.

Trade-off / Limitation
Sistemi LangChain/LangGraph ekosistemine sıkı sıkıya bağlamış oldum. Öğrenmesi biraz zordu ama sağladığı hazır state yönetimi, kendi orkestrasyon motorumu yazıp sürdürme zahmetinden kurtardığı için bu bedeli ödemeye değerdi.

## Dense'den Hibrit Arama Modeline Geçiş
Context
Qdrant üzerinde sadece yoğun vektör (dense embedding - Gemma) kullandığımda, sistem anlamsal sorularda çok iyi çalışıyordu. Ancak kullanıcı spesifik bir komut veya tam eşleşme gerektiren özel bir isim aradığında modelin bunları kaçırdığını veya halüsinasyon gördüğünü fark ettim.

Decision
Qdrant aramalarını saf vektörden Hibrit Arama'ya geçirdim. Anlamsal yakınlık için Dense vektörleri, anahtar kelime/tam eşleşmeler için ise Sparse (BM25) indeksini aynı anda kullanıp sonuçları RRF ile birleştirdim.

Evidence
Yaptığım testlerde sistemin "Kargo ücreti ne kadar?" gibi kavramsal sorulardaki başarısı aynen devam ederken, "down -v" gibi spesifik komutlar barındıran sorgularda hedefi tam isabetle vurduğunu gördüm.

Trade-off / Limitation
Qdrant artık hem yoğun hem de seyrek indeksleri aynı anda tuttuğu için depolama alanı ihtiyacı arttı. Ayrıca iki arama birden yapıldığı için arama gecikmesinde ufak bir artış oldu.

## Yetenek Sınırı (Capability Boundary) Olarak MCP
Context
Dış servisleri ve API'ları doğrudan router'ın veya ana kodun içine gömmek hem güvenlik riski yaratıyordu hem de kodları birbirine çok sıkı bağlı hale getiriyordu.

Decision
Model Context Protocol (MCP) yapısını sistemde sadece bir "Yetenek Sınırı" olarak konumlandırdım. Router sadece "niyeti" belirliyor; araçların yetkilendirmesi, çalıştırılması ve güvenlik kontrolleri tamamen MCP sınırları içindeki deterministik uygulama katmanına bırakılıyor.

Evidence
Bu yapıyla "LLM'in düşünmesi" ile "sistemin çalıştırması" birbirinden tamamen izole oldu. Biri prompt injection ile router'ı kandırıp "tool" rotasına düşürse bile, execution katmanındaki deterministik kurallarım (allowlist vb.) sayesinde riskli işlemlerin çalışması engelleniyor.

Trade-off / Limitation
Basit bir API çağrısı eklemek istesem bile MCP standartlarına uygun bir arayüz yazmak zorunda kalırım. Bu da yeni bir özellik eklerken geliştirme hızımı bir miktar yavaşlatır.

## Lokal Ortam İçin SQLite Checkpointer
Context
LangGraph'ın adımlar arasındaki state'i hatırlayabilmesi için kalıcı bir denetleme noktasına (checkpointer) ihtiyacı vardı.

Decision
Kendi bilgisayarımdaki yerel geliştirme ortamım için SQLite Checkpointer kullanmayı seçtim.

Evidence
SQLite sıfır yapılandırma gerektirdiği için Docker Compose ortamıma anında uyum sağladı. Sırf LangGraph state'ini tutmak için ağır bir konteynerini ayağa kaldırma yükünden ve RAM tüketiminden kurtulmuş oldum.

Trade-off / Limitation
Bu çözüm kesinlikle sadece lokal ortamım için geçerli. SQLite yüksek eşzamanlı istekleri kaldıramayacağı için, proje production'a  çıkacağı zaman bu modülü kesinlikle Postgres gibi güçlü bir veritabanıyla değiştirmem gerekecek.

## Final Semantic Router Policy (Yönlendirici Politikası)
Context
Sistemde kullanıcıdan gelen mesajları doğru yere (smalltalk, bilgi tabanı veya araçlar) yönlendirmek için Qwen3:1.7b modelini kullanıyordum. Ancak her mesajı doğrudan modele gönderdiğimde, modelin karar vermeden önce uzun uzun kendi kendine düşünme süreci (reasoning) yüzünden sistem inanılmaz yavaşlıyordu. Kullanıcının basit bir "Merhaba" cevabı için bile bazen 10-20 saniye beklemesi gerekiyordu ve bu bir yönlendirici için kabul edilemezdi.

Decision
"İki Aşamalı (Two-Stage) Yönlendirici" mimarisine geçmeye ve modele istek atarken think=false (düşünme özelliğini kapatma) parametresini kullanmaya karar verdim. Sistem artık önce çok hızlı, deterministik kurallara (anahtar kelimelere) bakıyor. Orada net bir eşleşme bulamazsa işi LLM'e devrediyor ama modelden "düşünmeden" hızlıca bir karar vermesini istiyor.

Evidence
Kendi yazdığım test scriptiyle (router_experiment) yaptığım ölçümlerde, varsayılan (düşünen) modun ortalama 11 saniye sürdüğünü, think=false modunun ise bu süreyi 569 milisaniyeye indirdiğini kanıtladım. İlginç bir şekilde, model düşünmeyi bıraktığında "küçük sohbet" gibi basit niyetleri aşırı karmaşıklaştırıp yanlış rotaya atmaktan kurtuldu.

Trade-off / Limitation
Model düşünmeden anlık refleksle karar verdiği için, "çalışma notlarımda ara" gibi bazı karmaşık araç (tool) isteklerini bazen yanlışlıkla bilgi tabanına (knowledge) yönlendirebiliyor. Ayrıca şu anki yapımda "Bugün hava nasıl?" gibi mevcut yeteneklerimizi aşan sorular için özel bir "desteklenmiyor" rotası yok; sistem böyle durumlarda elindeki rotalardan birini uydurmaya çalışıyor. Ancak yanıt süresini 11 saniyeden yarım saniyeye düşürmenin getirdiği devasa kullanıcı deneyimi kazancı, bu küçük kusurları fazlasıyla telafi ediyor.