# Weekend Review

## Cumartesi

Bugün düzelttiğim 3 şey:
1. **Çift Çalıştırma Bug'ı (agent_cli.py):** Ajanın aynı input için iki kere çalışması ve trace (log) kaydıyla terminal çıktısının farklı paralel run'lardan gelmesi sorununu düzelttim.
2. **Observability Hatası (agent_loop.py):** Ajanın çağırdığı tool başarısız olmasına rağmen (JSON ile hata dönmesi), loglara `status: success` olarak düşmesi (sahte başarı) mantığını düzelttim.
3. **Resmi Tool Sözleşmesi Uyumsuzluğu:** Ajanın `tool_calls` sonuçlarını tekrar modele geri yollarken, Ollama'nın resmi sözleşmesindeki gereklilik olan `"name": tool_name` parametresinin eksikliğini giderdim.

Bugün tekrar netleştirdiğim 3 kavram:
1. **Trace ve Execution Uyumu:** Observability (gözlemlenebilirlik) sadece veriyi yazmak değil, o loglanan verinin sistemin gerçeğiyle birebir örtüşmesi gerektiğidir.
2. **Regresyon Testlerinin Amacı:** Modelin ne zaman hata yapacağını (hallucination) bilemeyeceğimiz için, hatalı durumları zorla simüle eden sahte istemciler (FakeClient) yazıp koda güvenlik ağları (safety net) kurmanın önemini anladım.

İstasyon 1 — LLM Temeli
Temperature: Modelin yaratıcılık ayarıdır. Düşükse hep en garanti kelimeyi seçer (sıkıcı ama net), yüksekse risk alır, farklı kelimeler dener.

Seed: Rastgeleliği sabitleme ayarıdır. Aynı soruda hep aynı cevabı almak (test yapmak) istiyorsam seed kullanırım.

Aynı prompt neden farklı cevap verir?: Çünkü arka planda kesin bir hesap değil, olasılıksal bir zar atma (sampling) işlemi dönüyor.

Yanlışın Düzeltilmesi: "Embedding, token ID'nin diğer adıdır" demek tamamen yanlıştır. Token ID kelimenin sözlükteki sıra numarasıdır (örn: 543). Embedding ise o kelimenin anlamsal uzaydaki haritası/koordinatıdır (duygu ve anlam içerir).

İstasyon 2 — Docker / Compose
Model cache kalıcı olsun -> named volume 
JSON output host'ta doğrudan görülsün -> bind mount 
app container Ollama'ya erişsin -> service name 

Problem: OLLAMA_BASE_URL=http://localhost:11434 neden patlar?
Çünkü Docker içindeki bir uygulamanın "localhost"u kendisidir. Kendi içine bakar, orada Ollama'yı bulamaz. Doğrusu http://ollama:11434 olmalıdır.

İstasyon 3 — Structured Output ve Function Calling
"Mesajı analiz et (summary, category)" -> Sadece belirli formatta JSON dönmesi yeterli. (Structured Output)

Kargo ücretini hesapla" -> Dışarıda matematik/kod çalışması lazım. (Function Calling)

tool schema: Modele sunduğumuz restoran menüsü. "Bak bende bu araçlar var."
tool call: Modelin sipariş vermesi. "Bana şu parametrelerle şu aracı çalıştır."
tool execution: Garsonsun (Uygulama/Python), siparişi alıp mutfakta (Dispatcher) gerçekten çalıştırıp sonucu getirmendir.

Mini Hata Nerede Durdurulmalı?
{"weight_kg": "çok"} formatı Type Validation (Tip Doğrulaması) aşamasında durdurulmalıdır. Kilo bir sayı olmalıdır, metin (string) değil

İstasyon 4 — Agent Loop
Trace (Sürekli aynı aracı çağırma):

Ne zaman stuck (takıldı) deriz?: Model aynı aracı, aynı parametrelerle üst üste hiçbir ilerleme kaydetmeden çağırıyorsa takılmıştır.

max_iterations neden var?: Model takılırsa sonsuza kadar dönüp api faturamızı veya sunucu zamanını bitirmesin diye "acil fren" sistemidir.

repeat policy neden gerekir?: Modelin aynı şeyi boş yere tekrar edip etmediğini kontrol etmek için.

Formül: Agent = Model + Durum/Bellek (State) + Tools + Dispatcher + Validation + Döngü (Loop) + Observability.

İstasyon 5 — Literatür

MRKL: Basitçe, yapay zekaya dış sistemleri (hesap makinesi, hava durumu API'si) bağlama fikridir.

ReAct: Yapay zekanın kuru kuru cevap vermesi yerine, önce sesli düşünmesi (Reasoning) sonra harekete geçmesi (Acting) mantığıdır.

Toolformer: Modelin API kullanmayı kendi kendine (eğitilerek) öğrenmesidir.

"ReAct her zaman en iyisidir" iddiası: Kesinlikle yanlıştır. Sadece hava durumunu soruyorsam ReActa gerek yoktur, normal Function Calling daha ucuz ve hızlıdır. ReAct karmaşık problemlerde işe yarar.

