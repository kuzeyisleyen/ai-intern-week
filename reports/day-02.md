---
day: 2
date: 2026-08-18
status: completed 
tests_passed: 5
tests_failed: 0
base_model_tested: true 
instruct_model_tested: true 
repo_reproducible: true 
blocker_count: 1
---

# Gün 2 — Çalışma Raporu

## 1. Gün Özeti

Bugün yaptığım en önemli çalışmalar:

1.Token, Token ID ve Embedding dönüşümlerini Hugging Face kütüphaneleri üzerinden kod yazarak test ettim.
2. SmolLM2-360M Base ve Instruct modellerini indirip, girdi formatları ve verdikleri yanıtlar arasındaki farkları inceledim.
3. Modelin yaratıcılığını kontrol eden parametreleri (Greedy, Sampling, Temperature) üzerine kontrollü bir kod deneyi yazdım.
4. Deney sonuçlarımı `json` kütüphanesi kullanarak kaydettim.
5. Projemi Git ile versiyonlayıp, `requirements.txt` ve `README.md` dosyalarını standartlara uygun hazırlayarak repomu tam anlamıyla çalıştırılabilir hale getirdim.


## 2. Python Çalışması

Bugün kodda yaptığım iyileştirmeler:

- if else yapısı ile kodu daha güvenli hale getirdim.
- Config ayarlarını (Greedy, Temp 0.7, Temp 1.2) hard-code yazmak yerine bir liste (`[]`) içinde sözlükler (`{}`) halinde tutarak `for` döngüsüyle dinamik hale getirdim.


Edge-case olarak ele aldığım durumlar:

-   if not isinstance(text, str):
       raise ValueError("Input must be a string")
   else:
       text = text.lower()
       text = re.sub(r'[^\w\s]', '', text)

       return text

`while`, exception veya function tasarımı hakkında öğrendiğim önemli şey:

Tek bir satırlık sözlük (dictionary comprehension) yapısının arka planda klasik bir `for/if` bloğuyla aynı işi yaptığını ve **kwargs (çift yıldız) operatörünün bir sözlüğün içindeki parametreleri fonksiyonun içine nasıl güvenle açtığını öğrendim.

## 3. Testler

Çalıştırdığım komut:

```bash
python -m pytest -v
```

Sonuç:

tests/test_text_utils.py::test_hello_world PASSED                                                                                                                      
tests/test_text_utils.py::test_empty_input PASSED                                                                                                                             
tests/test_text_utils.py::test_whitespace_input
PASSED 

Toplam:


Passed:3
Failed:0
```

En faydalı bulduğum test:

Boş string ve whitespace input (girdi) kontrolü yapan testler.

Neden:

Çünkü LLM modellerine veya Tokenizer'lara  boş bir metin gönderildiğinde sistemlerin çökmesine sebep olabiliriz. String manipülasyonunda giriş hijyeninin yapay zekadaki önemini daha iyi anladım.

## 4. Repository Düzeni

Bugün eklediğim / düzenlediğim şeyler:

- [x] `.gitignore`
- [x] `requirements.txt`
- [x] README
- [x] test klasörü
- [x] experiment çıktıları

Başka biri projeyi kurmak için şu adımları izleyebilir:

python -m venv .venv
# Windows için: .venv\Scripts\activate | macOS/Linux için: source .venv/bin/activate
python -m pip install -r requirements.txt
python day02/generation_experiment.py

## 5. Token / Token ID / Embedding

### Token

Metnin bölündüğü en küçük anlam veya hece parçalarıdır.

### Token ID

Bu stringlerin modelin hafızasında kaçıncı kelime olduğunu gösteren indeks.

### Embedding

Token ID nin kimliğinin ,anlamının ve diğer kelimelerle ilişkisini taşıyan çok boyutlu sayısal vektörler.

Deneyde aldığım shape'ler:

```text
Input IDs: torch.Size([1, 1])
Embedding tensor: torch.Size([1, 1, 768])
```

Bu deneyden çıkardığım ana fikir:

Yapay zeka aslında kelimeleri anlamaz. Tokenizer, metne bir numara verir. Model ise o numarayı embedding katmanına sorarak kelimenin anlamsal özelliklerini içeren matematiksel bir vektöre ulaşır.

## 6. Inference / Deployment / Hallucination

### Inference
Eğitilmiş modelin bir girdiden çıktı üretme işlemidir.

### Deployment
Modeli insanların veya başka sistemlerin kullansbilmesi için çalışan bir hizmet haline getirmektir.

### Hallucination
Modelin doğruymuş gibi sunduğu fakat aslında yanlış,asılsız veya teyit edilemeyen çıktılar.

## 7. Model Card Çalışması

### SmolLM2-360M

Önemli gözlemlerim:

1.Chat template'i (sohbet şablonu) yoktur, ham metin alır.

2.Bir asistan gibi cevap vermek yerine metnin devamını getirmeye çalışır.

3.360M parametreli olduğu için donanım dostudur ama karmaşık mantık yürütmede zayıf.

### SmolLM2-360M-Instruct

Önemli gözlemlerim:

1.Özel Chat Template'e ([{"role": "user", ...}]) ihtiyaç duyar.
2.Sorulara doğrudan cevap veren bir asistan gibi davranmak üzere ince ayar yapılmıştır.
3.Parametre sayısı (360M) düşük olduğu için halüsinasyon riski var. 


## 8. Base vs Instruct Model Deneyi

### Continuation prompt

Base çıktı:

You are a helpful AI assistant named SmolLM, trained by Hugging Face

Instruct çıktı:

Python is a versatile and widely-used programming language that is particularly well-suited for software development due to its simplicity, readability, and extensive libraries.

Gözlemim:

İkisi de bu tarzda (yarım bırakılmış cümle) iyi çalıştı ancak Instruct model daha toparlayıcı ve yapılandırılmış bir liste verdi.

### English instruction

Base çıktı:

• A list is a collection of items that can be of different types.
• A dictionary is a collection of key-value pairs.
• A dictionary is a collection of key-value pairs.

Instruct çıktı:

1. **Lists**: Lists are ordered collections of items that can be of any data type, including strings, integers, floats, and other lists. They are denoted by square brackets `[]` and are indexed by integers.
2. **Dictionaries**: Dictionaries are unordered

Gözlemim:

İkiside tam düzgün bir sonuç vermedi base model 2 maddeyi aynı sundu instruct modelse sadece 2 maddem sundu fakat içerik olarak isntruct biraz daha içi dolu bir yanıt verdi.

### Türkçe instruction

Base çıktı:

# 1.
# 1.1
# 1.1.1
# 1.1.1.1
# 1.1.1.1.1
# 1.1.1.1.1.1
# 1

Instruct çıktı:

1. List: Python'ye çevireceği ve liste çevireceği.
2. Dict: Python

Gözlemim:

Türkçe bir model değil ve doğru çalışmıyor.

### Sonuç

Base ve instruct farkını şu şekilde açıklıyorum:

Base model bir metin tamamlama makinesidir internetin bir yansımasıdır. Instruct model ise o yansımanın alınıp insan komutlarına  asistan rolü yapması için özel olarak eğitilmiş, sınırları çizilmiş halidir.Fakat bu gözlemi internetten edindiğim araştırmalar sonucu elde ettim deneyemlerken beklentimden farklı sonuçlar elde ettim.

## 9. Generation Deneyi

Kullandığım model:

HuggingFaceTB/SmolLM2-360M-Instruct

Kullandığım prompt:

"Bana yapay zekanın geleceği hakkında kısa, yaratıcı bir hikaye yaz."

Seed:
42

### Greedy

Config:

do_sample=False

Gözlem:

En olası kelimeleri seçtiği için robotik, sıradan ve yaratıcılıktan uzak (beklenen ve klişe) bir sonuç üretti. Güvenli ama sıkıcı.

### Temperature 0.7

Config:

do_sample=True, temperature=0.7

Gözlem:

Risk almaya başladı. Daha edebi kelimeler seçti, konu akışı gayet mantıklıydı. Yaratıcılık ile doğruluk arasında iyi bir denge kurdu.

### Temperature 1.2

Config:

do_sample=True, temperature=1.2

Gözlem:

Model tamamen risk aldı ve farklı kelimeler denedi. Yaratıcı olmaya çalışırken bağlamdan koptu, garip kelimeler seçti veya yazım hatalarına (halüsinasyonlara) meyilli hale geldi.

### Çıkardığım sonuç

Greedy; matematik veya kesin bilgi gerektiren görevlerde kullanılmalıdır. Temperature (Sampling) ise hikaye, pazarlama veya kodlama asistanı gibi yaratıcılık gerektiren işlerde ihtiyaca göre artırılıp azaltılmalıdır.

## 10. AI ile Çalışma

### ChatGPT / Codex

Bugün hangi işlerde kullandım:

1. Yol haritası çizdirme
2. Bazı kavramların araştırması

Kullandığım faydalı prompt:

Bir model kartı okumayı öğrenirken dikkat etmem gereken konular neler olur?

AI'nin önerdiği fakat değiştirdiğim / kabul etmediğim bir şey:

...

Neden:

...

### Claude / Claude Code

Bugün hangi işlerde kullandım:

1. Kod analizleri
2. Hata çözme

Kullandığım faydalı prompt:

Bu yapıyı kurabilmem için bana bir yol haritası çıkart .
Kaç adet fonksiyon kullanarak bu uygulamayı geliştirebilirim öneride bulun.
Kodlama yapmanı istemiyorum.

AI'nin önerdiği fakat değiştirdiğim / kabul etmediğim bir şey:

...

Neden:

...

---

## 11. Bugün AI Olmadan Yapabildiğim Şeyler

En az 3 madde:

1. Terminal komutları ile .venv ortamını başarıyla aktif edip requirements.txt bağımlılıklarını izole bir şekilde kurdum.
2. Model kartlarını kendi başıma inceleyerek Base ve Instruct arasındaki 360M parametreli modelin kullanım senaryolarını tablolaştırdım.
3. Projeyi lokalde git init ile başlatıp git push ile kendi repoma modeli boyut limitlerine takılmadan yükledim.

---

## 12. Hata ve Blocker'lar

Blocker yoksa:

`Yok.`

Varsa:

### Blocker

Problem:

Deney sonuçlarını JSON'a yazdırırken ve liste içindeki configleri dönerken crash aldım.

Hata mesajı:

FileNotFoundError: [Errno 2] No such file or directory
AttributeError: 'list' object has no attribute 'items'

Denediklerim:

Dosya yollarını kontrol ettim.

Config veri tiplerini manuel değiştirmeye çalıştım.

Çözüm:
JSON hatası için, Python'ın klasörü kendi kendine oluşturamayacağını öğrenip os.makedirs(os.path.dirname(output_file), exist_ok=True) ekledim. Attribute hatası için ise liste içindeki elemanları [] yerine {} ile sözlük formatına çevirdim.

Çözülmediyse ihtiyacım olan:
...

---

## 13. Bugünün En Önemli 5 Öğrenimi

1. Tokenizer anlam bilmez, sadece kimlik (ID) verir; embedding ise anlamı (vektörel matrisi) taşır.
2.Modeller projeye indirilmez (git'e yüklenmez), kod paylaşılır, model HuggingFace'in from_pretrained komutu ile otomatik çektirilir.
3.Base modeller sadece metin tamamlar, Instruct modellerin bir Chat Template yapısı vardır.
4.temperature arttıkça model risk alır (yaratıcı olur ama halüsinasyon artar), do_sample=False ise hep en güvenli/robotik yolu (greedy) seçer.
5.Embedding kavramının mantığını kavramsal boyutta tam olarak oturttum: Yapay zekanın kelimeleri sadece birer numara (Token ID) olarak görmediğini, asıl anlamı ve bağlamı onları çok boyutlu matematiksel uzaylara yerleştirerek (boyutlandırarak) kazandırdığını anladım.


## 14. Yarın İçin Sorularım

En az 2 soru:

1. Yarın öğlene kadarki programda ilk 2 gün öğrendiğim kavram ve kodlamaları tekrar edebiliceğim şekilde bir bölüm olma imkanı var mı?
2. Küçük boyutlu instruct modelin ingilizce komutlarda başarılıyken türkçede veya karmaşık görevlerde zorlandı.Gerçek projelerde küçük modelleri kendi dilimzide veya daha spesifik bir görevde daha başarılı hale getirmek için onları kendi verilerimizle nasıl eğitiyoruz?


## 15. Derinleşmek İstediğim Konular

1. API



# 5. Gün sonu kontrol listesi

Gün bitmeden:


[x] boş input güvenli şekilde yönetiliyor
[x] gereksiz recursion kaldırıldı
[x] kullanılmayan importlar temizlendi
[x] duplicate kod azaltıldı
[x] en az 3 pytest testi var
[x] testler çalıştırıldı
[x] .gitignore dolu
[x] requirements.txt dolu
[x] __pycache__ yeni commit'e girmiyor
[x] README başka geliştirici için anlaşılır
[x] token / ID / embedding deneyi tamamlandı
[x] base model çalıştırıldı
[x] instruct model çalıştırıldı
[x] en az 6 model karşılaştırma çıktısı kaydedildi
[x] generation deney config'leri kodda mevcut
[x] deney sonuçları kaydedildi
[x] reports/day-02.md tamamlandı