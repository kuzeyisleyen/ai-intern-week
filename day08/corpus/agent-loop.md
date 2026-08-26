Agent Loop Temelleri

Agent loop, modelin bir hedefe ulaşmak için durum değerlendirmesi yapması, uygun aracı seçmesi, araç sonucunu gözlemlemesi ve gerekirse yeni bir adım planlamasıdır. Basit bir chatbot yalnız cevap üretirken agent dış sistemlerle etkileşim kurabilir.

Temel döngü

Tipik akış kullanıcı isteğinin alınmasıyla başlar. Model mevcut durumu ve kullanılabilir araçları inceler. Bir tool çağrısı gerekiyorsa araç ve argümanları seçer. Uygulama çağrıyı doğrulayıp çalıştırır. Sonuç agent durumuna eklenir ve model hedefin tamamlanıp tamamlanmadığını yeniden değerlendirir.

Döngü yalnız başarılı cevapla sona ermez. Cevabın elde edilemediği, kullanıcının onayının gerektiği veya güvenli şekilde devam edilemediği durumlar da açık durma koşullarıdır.

Max iterations

max_iterations, agent'ın sınırsız tool çağrısı yapmasını engelleyen güvenlik ve maliyet sınırıdır. Model aynı başarısız sorguyu tekrar tekrar deneyebilir veya iki araç arasında döngüye girebilir. Maksimum iterasyon sayısı aşıldığında sistem kontrollü bir sonuç üretmeli ve hangi noktada durduğunu kaydetmelidir.

Yalnız iterasyon sınırı yeterli değildir. Toplam süre, token kullanımı, tool maliyeti ve belirli araçların çağrı sayısı için de bütçeler tanımlanabilir. Kritik işlemler için kullanıcı onayı ayrı bir durma noktasıdır.

State

Agent state, kullanıcının hedefini, önceki mesajları, tool çağrılarını, tool sonuçlarını ve ara kararları taşır. State'in kontrolsüz büyümesi context maliyetini artırır. Uzun süreçlerde gerekli bilgilerin özetlenmesi veya kalıcı belleğe aktarılması gerekebilir.

Tool sonucu ile modelin yorumu birbirinden ayrılmalıdır. Böylece gözlemin gerçekten tool tarafından mı döndüğü, yoksa model tarafından mı çıkarıldığı takip edilebilir.

Deterministik ve agentic akış

Deterministik workflow'da adımlar önceden bellidir. Örneğin her soru için retrieve → generate uygulanabilir. Agentic workflow'da ise model retrieval gerekip gerekmediğine, hangi kaynağın kullanılacağına veya yeniden deneme yapılıp yapılmayacağına karar verebilir.

Her probleme agent eklemek gerekmez. Sabit ve denetlenebilir iş akışlarında deterministik yapı daha basit ve güvenli olabilir. Agent, gerçekten dinamik karar noktaları bulunduğunda değer sağlar.