`reports/day-05.md`

```markdown
---
day: 5
date: 2026-08-21
status: completed
model: qwen3:1.7b
native_agent_working: true
max_iterations: 5
unit_tests_passed: 21
integration_tests_passed: 2
agent_scenarios_run: 4
literature_note_completed: true
framework_mapping_completed: true
blocker_count: 0
---

# Gün 5 — Çalışma Raporu

## 1. 4. Günden Düzelttiklerim

- Kargo aracına (shipping_tool) eksi değer veya metin (string) girilmesi gibi bug'lar giderildi ve bunlar yazılan yeni testlerle doğrulandı.
- `tool_dispatcher` için uç durum (edge-case) senaryoları eklendi. Olmayan bir araç çağrıldığında veya eksik argüman gönderildiğinde programın çökmesi (Exception) yerine kontrollü bir hata mesajı (`{"error": "..."}`) dönmesi sağlandı.
- shipping calculator içinde `if / if / else` akışının İstanbul branch'ini yanlışlıkla override edebilme riski giderildi.
-dispatcher için 4 farklı senaryolyu doğrudan doğrulayan testlerin eksikliği giderildi.

Gerçek test sonucu:

================================ short test summary info ================================
7 passed in 0.15s

## 2. Literatür Taraması

MRKL:
Ajanların sadece kendi bildikleriyle değil, dış uzman modüllere (hesap makinesi, hava durumu API'si vb.) bağlanarak çalışmasını savunan mimarilerinden biri.
ReAct:
Modelin bir aksiyon (tool) almadan önce mutlaka Reasoning yapmasını sağlayan yapı. Düşün -> Hareket Et -> Gözlemle döngüsüne dayanır.

Toolformer:
Modellerin dış araçları kullanmayı, zero-shot promptlar yerine doğrudan fine-tuning (kendi kendini eğitme) ile öğrenmesini sağlayan araştırma.

“En iyi agent hangisi?” sorusuna bugünkü cevabım:
En iyi agent, görevin karmaşıklığına göre değişir. Sabit ve belirli araçların olduğu senaryolarda ReAct tabanlı native while döngüleri fazlasıyla yeterliyken, API sayısının yüzleri bulduğu durumlarda Toolformer gibi aracı doğrudan tanıyan modeller daha avantajlı olabilir.

## 3. AI'dan Duyup Orijinal Kaynaktan Doğruladığım İddia

AI'nın söylediği:
AI'nın söylediği: "ReAct, otonom ajanlar için tek ve en standart yöntemdir."

Kontrol ettiğim kaynak:
MRKL ve Toolformer orijinal makaleleri.

Kaynakta gerçekten gördüğüm:
Kaynakta gerçekten gördüğüm: Ajan mimarilerinde tek bir standart yok. MRKL, ReActten daha önce benzer bir dış araç kullanımını önermiş. Toolformer ise prompt mühendisliğini tamamen ortadan kaldırıp modelin ağırlıklarına araç kullanmayı öğretiyor.

İlk ifade fazla güçlü müydü?
Evet, AI bu konuyu fazla basitleştirmiş ve ReAct'i sektörün tek kuralı gibi sunmuş.

## 4. Native Agent Mimarim

User 
 ↓
Agent Loop (While) -> System Prompt + Messages
 ↓
LLM (qwen3:1.7b) -> Yanıtı JSON/Tool Call olarak döner
 ↓
Termination Guard (Frenler) -> Çıkış şartı var mı?
 ↓
Tool Dispatcher -> İlgili Python fonksiyonunu çalıştır
 ↓
Result (Gözlem) -> Messages listesine "role: tool" olarak ekle ve başa dön

Kendi açıklamam:
Sistem tamamen bir while döngüsü üzerine kurulu. LLM sihirli bir iş yapmıyor, sadece metin ve fonksiyon çağrıları (JSON) üretiyor. Biz bu JSON'u yakalıyor, kodlarımızda çalıştırıyor ve sonucu tekrar modele veriyoruz. Olay tamamen "Mesaj Geçmişini" (State) doğru yönetmekten ibaret.

## 5. State / History

state = {
    "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}],
    "iteration": 0,
    "status": "running", 
    "errors": [],
    "tool_history": [],
    "final_response": None,
}

messages:
Ajanın LLM ile olan tüm diyalog geçmişi

iteration:
Ajanın döngüde kaçıncı turu attığını tutan sayaç (MAX_ITERATIONS için).

tool_history:
Hangi araçların, hangi parametrelerle çağrıldığını ve ne sonuç döndüğünü tutan sözlük listesi.

errors:
Döngü boyunca karşılaşılan exception veya kural ihlallerinin loglandığı liste

status:
Ajanın güncel durumu (running, completed, stopped, stuck).

## 6. Tool Orchestration

Tools:
1.calculate_shipping_cost: Ağırlık ve şehre göre kargo hesaplar.
2.analyze_text: Verilen metnin kelime/karakter analizini yapar.

Akış:
Model tool_calls döner -> Döngü içindeki for çalışır -> function name alınır -> execute_tool çalışır -> Sonuç state["messages"]'a role: tool olarak eklenir.

## 7. Termination

Stopping conditions:
1. tool_calls listesinin boş veya hiç gelmemiş olması (completed).
2. Döngü sayısının MAX_ITERATIONS değerine ulaşması (stopped).
3. Ajanın aynı aracı aynı argümanlarla tekrar çağırması (stuck).

max_iterations:
max_iterations: 5 olarak ayarlandı.

## 8. Repeated Tool Call

Nasıl tespit ediyorum?
Fonksiyon başında seen_signatures = set() tanımladım. Gelen araç adını ve parametrelerini json.dumps() ile string yapıp bir tuple oluşturuyorum. Eğer bu tuple daha önce sete eklenmişse tekrar edildiğini anlıyorum

Tekrarda ne oluyor?
state["status"] = "stuck" yapılıyor, hata listesine log düşülüyor ve while döngüsü break ile kırılarak sonsuz döngü engelleniyor.

## 9. Error Handling

Unknown tool:
tool_dispatcher Exception fırlatmak yerine {"error": "Bilinmeyen araç..."} döner. Bu hata ajana role: tool olarak bildirilir.

Invalid args:
Dispatcher içindeki Pydantic/manuel validasyon yakalar, program çökmez, model hatayı görüp düzeltmeye çalışır.

Tool exception:
agent_loop.py içindeki try-except bloğu unexpected hataları string'e çevirip state["errors"]'a kaydeder.

HTTP/model error:
Ollama bağlantısı koparsa if "error" in response bloğu tetiklenir ve statü stopped olur.

## 10. Agent Trace

Dosya:

output/trace_20260821_171826.json


Örnek iteration:
{
            "iteration": 1,
            "tool_name": "calculate_shipping_cost",
            "arguments": {
                "city": "İzmir",
                "weight_kg": 5
            },
            "result": {
                "city": "İzmir",
                "weight_kg": 5,
                "cost": 135,
                "currency": "TRY"
            },
            "status": "success"
        }

Trace sayesinde fark ettiğim şey:
Modelin kaputun altında nasıl karar aldığını açıkça görebilmek. Hata yaptığında, o hatayı role: tool olarak geri beslediğimizde modelin bunu okuyup diğer iterasyonda farklı bir parametre ile tekrar denemesi harikaydı.

## 11. Unit Test

Komut:
```bash
docker compose run --rm app python -m pytest -v -m "not integration"
```

Passed:7
Failed:0

Senaryolar:
no tool: Ajan doğrudan cevap verip iterasyon 1'de tamamlandı.
single tool: Ajan aracı çağırdı, cevabı aldı ve iterasyon 2'de bitirdi.
unknown tool: Dispatcher "error" döndü, ajan hatayı alıp işlemi bitirdi.
invalid args: Hatalı string ("iki kilo") gönderildi, dispatcher hatayı yakaladı.
tool exception: Try-except bloğunun çökmeden döngüyü tamamlaması test edildi.
max iteration: Farklı argümanlarla 6 kez istek atıldı, status stopped oldu.
repeated tool: Aynı argümanlarla 3 kez istek atıldı, fren mekanizması stuck verdi.

## 12. Integration Test

Komut:
docker compose run --rm app python -m pytest tests/integration/ -v

Passed:1
Failed:0

## 13. Gerçek Model Scenario Runs

### No tool
Prompt:
 Merhaba, sen kimsin ve neler yapabilirsin?
Gözlem:
Merhaba! Ben bir AI yardımcıımımınım. Bilgiye ulaşmak, soru cevap yapmak, yazım yapmak, kod yazmak, açıklamalar yapmak, öneriler vermek gibi birçok şey yapabilirim. Ne konuda yardımcı olabilirim? 🌟
Status: completed, iteration: 1.

### Shipping
Prompt:
Ankara'ya 3 kg paket göndereceğim. Eğitim kargo maliyetini hesapla.
Tool call:
calculate_shipping_cost(city="Ankara", weight_kg=3)
Gözlem:
Aracı doğru seçti, parametreleri doğru çıkardı. Dispatcher sonucu başarıyla geri döndü ve model final cevabında maliyeti belirtti. Status: completed, iteration: 2.
### Text analysis
Prompt: 'Docker AI Agent ve Python' metnini analiz et.
Tool call: analyze_text(text="Docker AI Agent ve Python")
Gözlem: Kargo aracıyla hiç ilgilenmeden doğrudan metin analiz aracına yöneldi. Kelime ve karakter sayılarını JSON'dan okuyup derledi. Status: completed, iteration: 2.

### Multiple tools
Prompt: Önce 'Otonom Sistemler' metnini analiz et, sonra İzmir'e 5 kg kargo hesapla. İki sonucu da bana özetle.
Tool calls: Önce analyze_text, sonra calculate_shipping_cost.
Gözlem: Orchestration yeteneği harikaydı. İterasyonlar arasında kaybolmadan iki ayrı tool'u sırayla çalıştırdı ve en sonunda iki veriyi birleştirip kusursuz bir final metni yazdı. Status: completed, iteration: 3.

## 14. Agent = LLM + While Loop mu?

Cevabım:
Kesinlikle evet. Olay modeli çağıran API'de değil, onu çerçeveleyen mantıkta.

Model: Sadece prompt alan ve metin/JSON döndüren bir tahmin makinesi.
State: LLM'in kendisinde hafıza olmadığı için bizim dışarıda tuttuğumuz liste.
Tools: Modele "eller" veren Python fonksiyonlarımız.
Orchestration: Gelen JSON'u parse edip fonksiyonu çağıran köprü.
Validation: LLM'in uydurma ihtimaline karşı veri tipi koruyucumuz.
Termination: Sistemin sonsuza kadar para harcamasını engelleyen if-else frenleri.
Observability: Ajanın kara kutu olmasını engelleyen trace kayıtları.

## 15. Native vs Framework

Native yaklaşımda açıkça gördüğüm şeyler:
1. Yapay zekanın sihirli bir varlık olmadığını, sadece kodumuza JSON gönderdiğini anladım.
2. Sistemin sonsuz döngüye girmemek için bizim yazdığımız basit if bloklarına (Frenlere) muhtaç olduğunu gördüm.
3. Arka planda while döngüsünün ve state taşımanın aslında ne kadar standart bir algoritma işi olduğunu fark ettim.

LangChain neyi soyutluyor?
Ana while döngüsünü kurmayı, API bağlantılarını, gelen veriyi parse etmeyi ve hata yakalama (try-except) uğraşını tek satıra (agent.invoke()) indirgiyor.

LangGraph neye odaklanıyor?
Ajanın düşünme ve araç kullanma sırasını daha kompleks, dallanıp budaklanan bir akış şeması (workflow) olarak tasarlamaya odaklanıyor.

Framework hangi boilerplate'i azaltıyor?
Manuel state sözlüğü oluşturma, araç şemalarını API formatına dönüştürme ve hata loglama kodlarını azaltıyor.

Framework hangi mekanizmayı gizleyebilir?
Ajanın adım adım nasıl düşündüğünü, hatayı modele nasıl geri beslediğimizi ve döngü mekanizmasını bir kara kutu içine hapseder. Hata çıktığında nerede takıldığını anlamak zorlaşır.

## 16. Literatür ile Kod Bağlantısı

MRKL'e benzeyen taraf: Ajanın dışarıdaki (kargo, metin analizi) uzman modülleri çağırması.

ReAct'e benzeyen taraf: Modelin önce aracı seçip, dönen sonuca (Observation) bakarak final cümlesini kurması.

Toolformer'a benzeyen / benzemeyen taraf: Biz aracı prompt ve sistem komutu ile tanıttık (benzemeyen taraf). Toolformer ise aracı doğrudan fine-tuning ile modelin ağırlıklarına öğretir.

## 17. AI Coding Araçları

ChatGPT/Codex:
Kod analzileri 
Makale parçalamaları

Değiştirdiğim/reddettiğim öneri:
...

Claude/Claude Code:
Test kodlarının ve agent döngüsünün kod iskeletini oluşturma
Hata Çözümleme ve iyileştirme önerileri

Değiştirdiğim/reddettiğim öneri:
...

## 18. Bugünün En Önemli 5 Öğrenimi

1. Otonom bir ajan aslında sihirli bir zeka değil, modele soru sorup dönen cevaba göre fonksiyon çalıştıran basit bir `while` döngüsüdür.
2. Yapay zekanın sonsuz döngüye girmesini engellemek için, maksimum iterasyon ve aynı aracı tekrar kullanma gibi manuel frenler yazmak zorunludur.
3. Bir araçta hata çıktığında programı çökertmek yerine hatayı modele metin olarak geri göndermek, modelin kendi hatasını görüp düzeltmesini sağlar.
4. Sürekli farklı cevaplar üreten bir yapay zekayı test edebilmek için, dışarıdan sahte cevaplar (`FakeClient`) vererek sistemi kandırmak en güvenli yoldur.
5. LangChain gibi popüler framework'ler aslında arka planda sadece bizim bugün yazdığımız bu döngü ve hafıza (state) sistemini çalıştırır, mucizevi bir iş yapmazlar.

## 19. Sonraki Hafta Geliştirmek İstediğim Konular

1. LangGraph kullanarak, ajanın kararlarına "İnsan Onayı (Human-in-the-loop)" eklemek

## 20. Açık Sorularım

1. Madem framework'ler (LangChain/LangGraph) arka planda bizim bugün sıfırdan kurduğumuz bu native motoru kullanıyor; haftaya ve sonraki projelerde yolumuza bu native kodlarla mı devam edeceğiz, yoksa artık mantığını anladığımız için LangChain/LangGraph'a tam geçiş yapacak mıyız?
`

---

# 7. Gün Sonu Kontrol Listesi

```text
[x] 4. gün kritik cleanup tamamlandı
[x] shipping bug test ile doğrulandı
[x] dispatcher edge-case testleri var
[x] OllamaClient env + timeout + health kullanıyor
[x] dependency yapısı tutarlı
[x] package/import yapısı tutarlı
[x] rapor gerçek test çıktısıyla senkron

[x] literature/day05-agent-comparison.md mevcut
[x] MRKL skim tamamlandı
[x] ReAct skim tamamlandı
[x] Toolformer karşılaştırıldı
[x] en az bir AI iddiası orijinal kaynaktan doğrulandı
[x] tek doğru agent mimarisi sonucu çıkarılmadı

[x] native AgentRunner mevcut
[x] explicit state/history mevcut
[x] max_iterations mevcut
[x] no-tool stop condition var
[x] repeated-tool koruması var
[x] unknown tool kontrollü
[x] invalid argument kontrollü
[x] tool exception kontrollü
[x] multiple tool çağrıları işlenebiliyor

[x] trace host output/ altına yazılıyor
[x] trace iteration/tool/result/final response içeriyor
[x] trace'e secret yazılmıyor

[x] agent unit testleri Compose üzerinden çalışıyor
[x] Ollama integration testi var
[x] en az 4 gerçek model scenario run yapıldı
[x] host pytest kullanılmadı

[x] notes/day05-framework-mapping.md mevcut
[x] LangChain Agents docs okundu
[x] LangGraph overview okundu
[x] framework/native farkı kendi cümlelerimle yazıldı

[x] README güncellendi
[x] reports/day-05.md tamamlandı
