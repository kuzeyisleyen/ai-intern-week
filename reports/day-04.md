# Gün 4 — Çalışma Raporu Şablonu

```markdown
---
day: 4
date: 2026-08-20
status: completed
model: qwen3:1.7b
ollama_service_working: true 
named_volume_working: true
local_http_working: true 
structured_output_working: true 
unit_tests_passed: 3
integration_tests_passed: 1
blocker_count: 0
---

# Gün 4 — Çalışma Raporu

## 1. Gün Özeti
1. Güne kapsamlı bir repository temizliği yaparak başladım; test dosyalarını kendi klasörüne izole ettim, `pytest` ayarlarını yapılandırdım ve imajı hafifletmek için gereksiz bağımlılıkları sildim.
2. Ollama'yı Docker üzerinde `qwen3:1.7b` modeliyle tamamen yerel (local) bir servis olarak ayağa kaldırdım.
3. HTTP istekleriyle modelle haberleşen bir Python istemcisi (`OllamaClient`) yazdım ve modelin sadece metin değil, JSON (Structured Output) dönmesini sağladım.
4. Modelden gelen JSON verisini kendi yazdığım Python kurallarıyla doğruladım (Validation) ve hatalı cevapları kontrollü bir şekilde yakaladım.
5. Yapay zekaya bir Python fonksiyonunu (Kargo hesaplama) nasıl kullanacağını öğrettim (Tool Calling).

## 2. Başlangıç Cleanup

Bugün başlamadan önce yaptığım repository düzenlemeleri:

- Pytest'in sadece test dosyalarına odaklanması için ayarları yapılandırdım.
- Projede artık kullanmadığım gereksiz kütüphaneleri `requirements.txt`'den temizledim ve `requirements-lab.txt` içerisine aldım .

### Pytest discovery

`pytest.ini` içeriğim:

[pytest]
testpaths = tests
markers =
    integration: requires running Ollama service and local model

Bunun çözdüğü problem:

Bunun çözdüğü problem: Pytest'in proje içindeki alakasız Python dosyalarını (özellikle çalıştırılabilir scriptleri) test dosyası sanıp çalıştırmasını ve hata vermesini engelledi.

### Docker dependency

Kaldırdığım / eklediğim dependency'ler:
Kaldırdıklarım:
torch==2.13.0
transformers==5.15.0
Eklediklerim:
pytest== 9.1.1
requests== 2.32.5

Neden:

Uygulamanın imaj boyutunu küçültmek ve "Compose-first" yapısına sadık kalmak için.

## 3. Bugünkü Literatür Okuması

### Okuduğum araştırma çalışması

```text
Toolformer: Language Models Can Teach Themselves to Use Tools
```

Kaynak:

```text
https://arxiv.org/abs/2302.04761
```

### Paper'ı nasıl taradım?

- Abstract:Toolformer'ın kendi kendine API çağırmayı nasıl öğrendiğine odaklandım
- Introduction:LLM'lerin matematik veya güncel bilgi gibi konulardaki eksikliklerinin API/Tool'larla nasıl aşıldığına baktım.
- Figure / örnek:
- Conclusion:Modellerin dış araçları kullanarak performanslarını inanılmaz derecede artırdığını gördüm.
- Limitations:Hâlâ her aracı kusursuz kullanamadıkları veya gereksiz yere araç çağırma eğilimleri olduğunu not ettim.

### Çalışmanın çözmeye çalıştığı problem

Dil modellerinin temel zayıflıklarını (matematiksel hesaplama yapamamak, güncel veri eksikliği, halüsinasyon) dış dünya araçlarını kullanarak aşmak.

### Temel fikir

Modele sadece metin üretmeyi değil metnin içine özel tool_call tagleri koyarak dış sistemleri tetiklemeyi öğretmek.

### Sınırlılık

Çoklu araç kullanımlarında veya karmaşık argüman gerektiren araçlarda modelin kafasının karışabilmesi.

### Bugünkü Ollama function calling ile bağlantısı

Makaledeki modelin API çağırmayı öğrenmesi konseptini bugün Ollamanın sağladığı json tabanlı tools parametresi ile bizzat kendi bilgisayarımda kodlayarak deneyimledim.

### Aynı olmayan noktalar

Makale modelin nasıl "eğitileceği" üzerine odaklanıyor ben ise var olan bir modele tools şeması göndererek "çıkarım"  aşamasını kullandım.

Makalede model API çağrısını doğrudan metnin içine gömüyor, Ollamada ise bu bize özel bir JSON nesnesi olarak geliyor.

### Okuduğum resmî dokümantasyon

```text
https://docs.ollama.com/capabilities/tool-calling
```

Paper ile resmî runtime dokümantasyonu arasındaki farkı şöyle açıklıyorum:

Makale, işin teorik ve akademik mimarisini anlatırken, Ollama dökümantasyonu bana geliştirici olarak kodumda hangi JSON anahtarlarını (tools, messages, role: tool) kullanmam gerektiğini gösteren pratik bir rehberdi.

### AI'yı literatür okurken nasıl kullandım?

Kavramları basitleştirmek ve teorik makale ile kendi yazdığım Python kodu arasındaki köprüyü kurmak için fikir aldım.

AI'nın söylediğini doğrudan kabul etmeyip kaynaktan doğruladığım bir nokta:

...

### Literatür notum

```text
literature/day04-tool-use-reading.md
```

---

## 4. Bugünkü Mimari

Şu an sistemi kendi kelimelerimle şöyle açıklıyorum:

İki farklı kutum var biri zihnim (Ollama modeli), diğeri ise ellerim (Python uygulamam). Zihin karar veriyor, ellerim hesaplayıp (kargo fiyatı) sonucu tekrar zihne iletiyor. İkisi bir Docker köprüsü (network) üzerinden konuşuyor.

### `app`
Benim yazdığım Python kodlarının, iş mantığının ve arayüzün çalıştığı konteyner.

### `ollama`
sadece gelen promptları okuyup cevap (veya tool isteği) üreten yapay zeka motorunun koştuğu konteyner.

### `ollama_data`
Ollama'nın indirdiği model dosyasını güvenle saklayan konteyner çökse bile veriyi koruyan Docker Volume (disk alanı).

### `output/`
Modelden dönen yapılandırılmış cevapları dış dünyada görebilmem için Docker içinden kendi bilgisayarıma bağlanan (bind mount) klasör.

## 5. Ollama Container

Kullandığım image:
ollama/ollama:latest

Çalıştırma komutlarım:
docker compose up -d ollama

`docker compose ps` gözlemim:
Konteynerin saatlerdir "Up (healthy)" durumunda olduğunu ve 11434 portunu dinlediğini kendi gözlerimle teyit ettim.

## 6. Kullandığım Model

Model:
```text
qwen3:1.7b
```

Bu modeli neden kullandım?
...

Makinemde çalışma deneyimim:
- yükleme:Diskten RAM'e yüklenirken ilk istekte ufak bir gecikme oldu
- response süresi hakkında gözlem:Model uzun cevaplar verdikçe (token sayısı arttıkça) yanıt süresi belirgin şekilde uzadı.
- RAM / sistem hissi:Cihazımda aşırı bir kasma olmadı ama bir arka plan süreci çalıştığını hissettirdi.
- sorun:

Benchmark yapmadıysan uydurma değer yazma.

## 7. Named Volume Deneyi

Volume:
ai-intern-week_ollama_data

Container'ı kaldırdıktan sonra model kaldı mı?
Evet kaldı.

Bunu nasıl doğruladım?
Konteyneri silip baştan başlattığımda ollama list komutunu çalıştırdım model internetten tekrar inmek yerine anında oradaydı ve docker volume ls komutuyla gördüm.

Named volume'un görevini şöyle açıklıyorum:
Konteynerler geçicidir volümler ise kalıcıdır. Volüm, Dockerın içindeki veriyi bizim formatlamadığımız sürece güvenle tutan sanal bir hard disktir

## 8. `localhost` vs Service Name

### `localhost`
Her konteynerinkendisini ifade eder. Eğer App konteyneri içinde localhost dersem, Python kodu Ollamayı değil, App konteynerinin kendi içini aramaya başlar.

### `ollama`
Docker ağında diğer konteynerin ismidir. Dockerın yerleşik DNS'i sayesinde bu ismi doğrudan IP adresi gibi kullanabilirim.

App container'ın kullandığı adres:
http://ollama:11434

Neden doğrudan container IP'si kullanmadım?
Çünkü Docker konteynerleri her yeniden başlatıldığında IP adresleri değişebilir. İsim kullanmak IP'nin ne olduğuna bakılmaksızın iletişimin her zaman kopmadan çalışmasını sağlar.

## 9. HTTP API

### Endpoint
/api/chat

### Request
Sadece model adı, mesaj listesi ve stream: False gönderiyorum. Eğer Tool varsa tools dizisini de ekliyorum.

### Response
JSON formatında bir sözlük.

### JSON
Ollama apisi her zaman JSON kabul eder ve JSON döner. Python tarafında veriyi json.dumps ile stringe, geleni de json.loads ile dict'e çeviriyorum.
### Status code
Her şey yolundaysa 200 OK.

### Timeout

Python client'ımda timeout: timeout=30


Neden timeout kullandım?
Model bazen takılabilir kodumun sonsuza kadar Ollama'dan cevap beklemesini engellemek için.

## 10. Python Ollama Client

Dosya:
day04/ollama_client.py

Ana fonksiyon / metotlar:
1.__init__: Temel ayarları (URL, model) kurar.

2.chat: Parametreleri (prompt, messages, tools) alır, JSON'a çevirir, HTTP isteği atar ve dönen cevabı parse eder.

Client'ın sorumluluğu:
Sadece HTTP iletişimi yapmak. Gönderilen metnin veya kullanılan toolun ne anlama geldiğini umursamaz kurye görevi görür.

CLI'ın sorumluluğu:
Kullanıcıdan girdiyi (sys.argv) almak, ekrana print basmak, dosyaya kaydetmek ve iş akışını yönetmek.

## 11. İlk Local Model Çağrım

Prompt:
Bir restoran müşteri yorumlarından servis sorunlarını tespit etmek istiyor.

Model response:
JSON formatında kategori, özet, riskler ve ilk adımları içeren yapılandırılmış bir veri.

Response'un kaydedildiği host dosyası:
output/day04-problem-analysis.json

## 12. Structured Output

Beklediğim yapı:
```json
{
  "summary": "...",
  "category": "...",
  "risks": [],
  "next_step": "..."
}
```

Kullandığım schema:
{
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "category": {"type": "string"},
        "risks": {"type": "array", "items": {"type": "string"}},
        "next_step": {"type": "string"}
    },
    "required": ["summary", "category", "risks", "next_step"]
}

Modelden dönen sonuç:
```json
...
```

## 13. Parse ve Validation

### `json.loads`
Ne yapıyor?
Modelden dönen düz metni alıp, Python'ın anlayabileceği içinde rahatça gezinebileceğim bir Sözlüğe çeviriyor.

### Validation
Kontrol ettiğim şeyler:

Gerekli tüm anahtarlar (summary, category vb.) JSON içinde var mı?
Riskler bir liste (list) tipinde mi?

### Şu üç farkı açıklıyorum

#### Parse edilebilir
Modelin döndüğü metin teknik olarak süslü parantezlere ve tırnaklara sahip geçerli bir JSON'dur (Yani json.loads hata vermez).

#### Schema geçerli
Sadece JSON olması yetmez; benim istediğim başlıkların (summary, category) JSON'ın içinde var olmasıdır.
#### Semantik olarak doğru
Sözdizimi ve yapı doğru olsa bile, modelin "Özet" kısmına cidden özet mi yazdığı yoksa alakasız bir şiir mi yazdığıdır. Bunu kodla değil, okuyarak anlarız.
## 14. Geçersiz Output Davranışı

Geçersiz JSON / schema durumunda uygulamamın davranışı:
 kırmızı  hataları basıp çökmek yerine "HATA: Model geçerli bir JSON döndürmedi" yazdırıp programı güvenli şekilde (sys.exit(1)) sonlandırıyor.

Test ettiğim örnek:
Metni parse ederken yaşanabilecek bir hata senaryosunu try/except json.JSONDecodeError bloğuyla yakaladım.
## 15. Unit Test vs Integration Test

### Unit test
Dış dünyaya (Ollama'ya, internete) ihtiyaç duymadan, saf Python fonksiyonlarımın (örneğin kargo hesabı 50 + kilo*12 doğru mu yapıyor?) doğruluğunu test eder. Anında çalışır.

Bugün unit test ile kontrol ettiğim şeyler:

1.Dispatcher'daki validation kuralları (Eksik veya hatalı argümanları yakalıyor mu?)
2.OllamaClient'ın doğru JSON üretip üretmediği.

### Integration test
Parçaların birbirleriyle (örneğin App'in Ollama konteyneriyle) gerçek dünyada nasıl konuştuğunu test eder.

Integration test'in ihtiyaç duyduğu servis:
Arka planda Docker içinde koşan gerçek bir ollama servisi.

## 16. Compose Üzerinden Test Sonuçları

### Unit
```bash
docker compose run --rm app python -m pytest -v -m "not integration"
```

Sonuç:

Passed:5
Failed:0
```

### Integration
```bash
docker compose run --rm app python -m pytest -v -m integration
```

Sonuç:

Passed:1
Failed:0
```

## 17. Bind Mount vs Named Volume

### Output
```text
./output:/app/output
```

Neden bind mount?
Çünkü modelin ürettiği raporları (JSON dosyalarını) işim bittiğinde kendi bilgisayarımda, VS Code içinden klasörleri tıklayarak görebilmek istiyorum.

### Model storage
```text
ollama_data:/root/.ollama
```

Neden named volume?
Çünkü 1.4 GB'lık model dosyasının nerede saklandığını manuel olarak bilmeme gerek yok. Bunu Docker yönetsin ama ben konteyneri silsem bile o kocaman veriyi kaybetmeyeyim istiyorum.

## 18. Karşılaştığım Hatalar

### Hata 1

Komut / işlem:
python day04/problem_analyzer.py "Bir restoran..."

Hata:
ModuleNotFoundError: No module named 'day04'

Tahminim:
Python dosyasını doğrudan çalıştırdığım için içeriğindeki from day04... komutu patladı, çünkü script zaten o klasörün içinden çalışıyordu.

Denediklerim:
1.VS Code'dan o kelimeleri silip kaydettim.
2.Kodu tekrar çalıştırdım ama hata devam etti. Neden? Çünkü Docker imajını (eski resmi) build etmemiştim!

Çözüm:
day04. prefixlerini sildim ve en önemlisi Docker'a bu yeni kodları alması için docker compose build app diyerek imajı yeniledim.

Öğrendiğim:
Host makinemdeki kodda değişiklik yapınca, eğer bu kodlar içeriye COPY ile alınıyorsa her zaman Docker imajını build ederek güncellemem gerektiğini öğrendim.

## 19. AI ile Çalışma

### ChatGPT / Codex

Kullandığım görevler:
1. Araştırma
2. Kod analizi önerisi

İyi bir prompt:
```text
...
```

Değiştirdiğim / reddettiğim bir öneri:
...

Neden:
...

### Claude / Claude Code

Kullandığım görevler:
1. Kod iskeleti çıkartırma
2. Yeni öğrendiğim metodlarıjn nasıl kullanılıcağını araştırma

İyi bir prompt:
```text
...
```

Değiştirdiğim / reddettiğim bir öneri:
...

Neden:
...


## 20. Function Calling / Tool Use

### Tanımladığım tool

Tool adı:

calculate_shipping_cost

Python function:

def calculate_shipping_cost(city: str, weight_kg: float) -> dict:
    if city == "İstanbul":
        taban_fiyat = 50
    elif city == "Ankara":
        taban_fiyat = 60
    else:
        taban_fiyat = 75
        
    cost = taban_fiyat + (weight_kg * 12)
    return {"city": city, "weight_kg": weight_kg, "cost": cost, "currency": "TRY"}

Tool schema:

{
    "type": "function",
    "function": {
        "name": "calculate_shipping_cost",
        "description": "Calculate a synthetic shipping cost for training purposes...",
        "parameters": {
            "type": "object",
            "required": ["city", "weight_kg"],
            "properties": {
                "city": {"type": "string"},
                "weight_kg": {"type": "number"}
            }
        }
    }
}

### Modelin ürettiği tool call

{
  "function": {
    "name": "calculate_shipping_cost",
    "arguments": {
      "city": "Ankara",
      "weight_kg": 3
    }
  }
}

Model hangi argumentleri üretti?

Ben promptta "Ankara'ya 3 kg paket" dediğim için, model bunu anlayıp city: Ankara ve weight_kg: 3 değerlerini üretti.

### Dispatcher

Allowlist'im:

`AVAILABLE_TOOLS = {"calculate_shipping_cost": calculate_shipping_cost}

Argument validation kurallarım:

1.İstenen tool benim allowlistimde var mı?
2.city bilgisi boş mu geldi? (if not city)
3.weight_kg değeri 0'dan küçük veya eşit mi? (weight_kg <= 0)

### Python tool sonucu

{'city': 'Ankara', 'weight_kg': 3, 'cost': 96, 'currency': 'TRY'}`

### Tool sonucundan sonraki final model response

Ankara'ya 3 kg paket gönderildiğinde, işlem maliyeti **96 TL** olarak hesaplanmıştır.

### Güvenlik testi

Bilinmeyen tool adı verdiğimde ne oldu?

execute_tool fonksiyonu "error": "Tool ... bulunamadı veya izinsiz." döndürdü.

Geçersiz argument verdiğimde ne oldu?

Araya koyduğum if weight_kg <= 0: kontrolüne takıldı ve kodu çalıştırmak yerine kendi belirlediğim "error": "Geçersiz kilo..." hatasını döndürdü.

### Şu üç farkı açıklıyorum

**Tool schema:**  
Yapay zekanın sisteminizde hangi işlemleri yapabileceğini ve bu işlemler için hangi veri tiplerini sağlaması gerektiğini tanımlayan kurallar bütünüdür.

**Tool call:**  
Yapay zekanın kendisine sunulan şemaya dayanarak ilgili işlemin gerçekleşmesi için gerekli parametreleri doldurup sisteminize gönderdiği net bir çalıştırma talebidir.

**Tool execution:**  
Yapay zekanın ilettiği bu talebin bizzat sizin ortamınızda (örneğin Python'da) işlenip hesaplanması işlemidir ve yapay zeka hiçbir aşamada kodu kendisi çalıştırmaz.

---

## 21. Bugünün En Önemli 5 Öğrenimi

1. Yapay zeka benim bilgisayarıma sızıp kod çalıştırmaz; sadece hangi fonksiyonun hangi verilerle çağrılacağını tahmin eder. Çalıştırma ve güvenlik tamamen benim kodumun kontrolündedir.
2. Modelin belirsiz cevaplarını geleneksel koda entegre etmenin tek güvenli yolu onu katı bir JSON şemasına zorlamak ve çıkan sonucu doğrulamaktır .
3. Her API isteği bağımsızdır. Modelin diyalog akışını veya çağırdığı araçların sonucunu hatırlaması için tüm geçmişi (`messages` dizisini) her defasında baştan göndermek zorundayız.
4.Yerel modelde üretilen her kelime (token) doğrudan CPU ve zaman tüketir. Modeli uzun cümleler yerine sadece net bir JSON argümanı üretmeye zorlamak hayati bir optimizasyondur.
5. GB'larca büyüklükteki model dosyalarının her konteyner kapanışında silinmesini önlemek ve sistemi anında ayağa kaldırmak için Named Volume kullanmak şarttır.

## 22. Yarın İçin Sorularım

1. Tool kullanarak modelden dışarıdaki bir dosyayı okumasını (veya internetten API çekmesini) istesek, güvenlik açıklarını önlemek için ekstra nelere dikkat etmemiz gerekir?

## 23. Tool / Agent Konusunda Merak Ettiklerim

1.AI ajanlarının döngüye girip sonsuza kadar Tool çağırmasını (Loop) nasıl engelleriz?


# 6. Gün sonu kontrol listesi

```text
[x] Toolformer paper skim tamamlandı
[x] Ollama Tool Calling resmî dokümantasyonu okundu
[x] paper/preprint ile resmî runtime dokümantasyonu arasındaki fark düşünüldü
[x] literature/day04-tool-use-reading.md oluşturuldu
[x] literatür notu kendi cümlelerimle yazıldı
[x] AI özeti birincil kaynak yerine kullanılmadı

[x] .gitignore output davranışı doğru
[x] pytest yalnızca tests/ topluyor
[x] gereksiz Docker dependency temizlendi
[x] eski recursion temizlendi
[x] README Compose-first çalışma biçimini gösteriyor

[x] compose.yaml içinde app + ollama var
[x] ollama/ollama image çalışıyor
[x] ollama_data named volume var
[x] qwen3:1.7b indirildi
[x] model container recreate sonrasında volume'da kaldı

[x] app OLLAMA_BASE_URL=http://ollama:11434 kullanıyor
[x] container IP hard-code edilmedi
[x] localhost/service-name farkını açıklayabiliyorum

[x] requests app image dependency'si
[x] OllamaClient mevcut
[x] HTTP timeout kullanılıyor
[x] /api/chat çağrısı çalışıyor
[x] stream=false ile JSON response alınıyor
[x] model response host output/ klasörüne yazılıyor

[x] JSON schema tanımlı
[x] structured output çağrısı çalışıyor
[x] json.loads kullanılıyor
[x] application-side validation var
[x] geçersiz output kontrollü yönetiliyor

[x] unit ve integration test ayrımı var
[x] unit testler Compose üzerinden çalışıyor
[x] integration test Compose üzerinden çalışıyor
[x] host pytest kullanılmıyor


[x] en az 1 güvenli Python tool tanımlı
[x] tool JSON schema tanımlı
[x] tool schema Ollama request'e gönderiliyor
[x] message.tool_calls okunuyor
[x] yalnız allowlist'teki tool'lar çalıştırılıyor
[x] tool argumentleri validate ediliyor
[x] tool sonucu conversation'a role=tool ile geri ekleniyor
[x] tool result sonrasında final model response alınıyor
[x] unknown tool ve invalid argument unit testleri var
[x] tool testleri de Compose üzerinden çalışıyor

[x] reports/day-04.md tamamlandı
