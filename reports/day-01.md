---
day: 1
date: 2026-08-17
status: completed 
python_confidence_before_10: 4
python_confidence_after_10: 7
llm_understanding_10: 6
vibe_coding_discipline_10: 7
open_model_status: completed 
blocker_count: 1
---

# Gün 1 — Çalışma Raporu

## 1. Bugün Ne Yaptım?

- List ,dict ve list compherension konularını tekrar ettim.
- LLM çalışma mantığını kavradım.
- Python veri yapılarını kullanarak metin analizi yapan analyze_text fonksiyonunu geliştirdim.
- Transformers kütüphanesiyle kelime/token farkını, boşlukların, büyük-küçük harflerin ve Türkçe ek yapısının tokenization üzerindeki etkilerini gözlemledim.
-Attention mekanizmasının önemini makaleden ve videolardan öğrendim.
-CLI üzerinden metin alıp kelime token sayısını hesaplayan ve devam metni üreten mini bir proje yazdım do_sample, temperature ve top_k parametrelerinin önemini öğrendim.

## 2. Python Çalışması

Bugün tekrar ettiğim / öğrendiğim konular:

-List ,dict , list compherension,try except ve exception konularını tekrar ettim.
-LLM çalışma mantığını öğrendim.
-Bir çok yeni kavramı açıklayabilicek seviyede öğrendim.

En zorlandığım Python konusu:

Sabahki Python çalışmasını LLM deneyiyle birleştirmek. Token & Generation Lab

## Bugün kendi başıma yazdığım kod:

def get_input() -> str:
    input_text = input("Enter a prompt for text generation: ")
    if not input_text.strip():
        print("Input cannot be empty. Please enter a valid prompt.")
        return get_input()
    return input_text

def count_words(text: str) -> int:
    return len(text.split())

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

---------------------------------------------

def analyze_text(text : str) -> dict:

    output = {
       "character count": 0,
       "word count": 0,
       "unique word count": 0,
       "longest word": "",
       "top words": []
    }
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation)) 
    output["character count"] = len(text)
    output["word count"] = len(text.split())
    output["unique word count"] = len(set(text.split()))
    output["longest word"] = max(text.split(), key=len)

## AI'nın yardımı olmadan açıklayabildiğim bölüm:

Çalışmamı tamamladıktan sonra ai yardımı olmadan açıklayabildiğim bölümler LLM çalışma mantığı,neden bugün agent docker konularına girmediğimiz,yeni öğrendiğim kavramlar ve kendim yazmış olduğum kod blokları.

## 3. Vibe Coding Deneyimim

Bugün AI'yı hangi geliştirme görevlerinde kullandım?

1. Yol haritası çıkartmada
2. Karşılaştığım bir problemi çözmekte
3. Elde ettiğim sonucu analiz ettirip öneri ve iyileştirme fikri almada

### İyi kullandığımı düşündüğüm bir prompt

Promp konusunda çok iyi olduğumu düşünmediğimden en faydalı geri dönüş aldığım prompt dökümanda var olan promptlardı.Zamanla bu konuda kendimi geliştirmeyi düşünüyorum.

Neden işe yaradı?

Aldığım yol haritası izlemem gereken yol ve önerilerden bir konu üzerinde uğraşırken daha fazla bilgi sahibi oldum.

### Kötü / yetersiz bulduğum bir prompt

kodumda bu parametrelersiz ve bu parametreleri kullanarak değişiklik yap farklı gözlemlemek istiyorum

Sorun neydi?

Günlük bir dil kullanımı ve gerekli kısıtlamaların olmadığını düşündüğüm ve daha detaylı promptlara göre yetersiz geri dönüş almam.

Nasıl daha iyi yazabilirdim?

DistilGPT2 modelinde metin üretimi (generation) parametrelerini test ediyorum. 

Mevcut `generate()` fonksiyonumu kullanarak bana iki farklı versiyon göster:
1. Parametresiz (varsayılan / Greedy Search haliyle)
2. `do_sample=True` ve `temperature=0.7` parametreleri eklenmiş hali.

Lütfen tüm kodumu yeniden yazma, sadece ilgili modeli çağırma bloğunu göster. 
Son olarak, bu parametrelerin eklenmesinin çıktıdaki çeşitliliği nasıl etkilemesini beklediğimi tek bir cümleyle açıkla.

Örneğin bu iyi cevap alamadığımda farklı bir ai kullanarak daha iyi bir geri dönüş aldığım aynı prompt.
Anlık cevaplar almak için özensiz ve hızlıca yazılan prompt alışkanlığındansa detaylı düşünülmüş promptlar yazabilirim.

## 4. ChatGPT / Codex Gözlemlerim

Hangi görevlerde kullandım?

-Öneride bulunma
-Analiz etme

En faydalı olduğu yer:

-Konuları veya kavramlar hakkında açıklamaları 

Yanlış / gereksiz / zayıf bulduğum bir önerisi:

...

## 5. Claude / Claude Code Gözlemlerim

Hangi görevlerde kullandım?

-Kod analizi
-Kod iyileştirmesi

En faydalı olduğu yer:

-Kod yazmak

Yanlış / gereksiz / zayıf bulduğum bir önerisi:

...

## 6. LLM'i Şu An Nasıl Anlıyorum?

Aşağıdakileri kendi kelimelerinle açıkla.

### Token
Yapay zekanın kelimeleri veya heceleri kendi anlayabileceği matematiksel değerlere dönüştürdüğü en küçük yapı.

### Tokenizer
Tokenizer kullanıcının girdiği metni bilgisayarın anlıyabiliceği sayı dizisine dönüştüren tercüman.

### Embedding
Yapay zeka modellerinin kelimeleri,  cümleleri  anlayabilmek için onları çok boyutlu bir uzaydaki matematiksel koordinatlara dönüştürme işlemi.

### Context
Modelin o anki cevabı üretirken aklında tutabildiği ve geçmişte görebildiği metinlerin sınırıdır.

### Transformer
Kelime kelime okuma yapmak yerine kuş bakışı bakarak hangi kelimenin hangi kelimeyle ilişkili olduğunu anlıyabilen bir yöntem.

### Attention
Yapay zekanın bir kelimenin anlamını çözerken transformer yöntemiyle bağlam için en ilişkili ve önemli olana dikkat kesilmesidir.

### Next-token prediction
Dizilime göre bir sonraki parçayı tahmin edip cümleleri uç uca eklemesiyle oluşuyor.

### Inference
Bir soruyu promptu alıp cevap üretmesi için geçen o anki çalışma ve düşünme süreci.

### Hallucination
İstatistiksel olarak biribirine uyumlu kelimeleri uç uca ekleyip anlamsız bir metin vermesi yani yalan uydurması.

## 7. Attention Is All You Need

Makalenin tamamını okumadan, bugün anladığın kadarıyla:

### Neden önemli?

Attenstion mekanizmasını standartlaştırdığı için yz tarihindeki önemli kırılma nhoktalarından biridir.

### Transformer neyi değiştirdi?

Sıralı işlemi zorunluluğunu kaldırarak paralel işlem yapmayı mümkün kıldı.

### Hâlâ anlamadığım kısım

Bütün kelimlere bakarken orjinal sırayı nasıl karıştırmadığı ve Attention skorlarının arka planda nasıl hesaplandığını tam olarak anlayamadım.

## 8. Tokenizer Deneyim

Denediğim örnekler:

Hello world
Merhaba Dünya
Artificial intelligence
artificial intelligence
Python

En şaşırtıcı gözlemim:

Dil olarak Türkçe kelimeler kullandığımdaki Token sayıları beni şaşırttı.

Kelime sayısı ile token sayısı arasındaki ilişki hakkında gözlemim:

Bazı kelimeler ile token sayısı aynı olsada kelimenin kök ve ek olarak ayrılıp her biri token sayısı olarak dönebiliyor.

## 9. Açık Model Deneyi

Kullandığım model:

`distilbert/distilgpt2`

Çalıştırdığım promptlardan bazıları:

The future of Python programming is
A software developer should always
Machine learning models can
Once upon a time

Model çıktısında gözlemlediğim şeyler:

Bazı tamamlamalarda güzel sonuç versede bazılarında verdiği cevaplar epey anlamsız olabiliyordu.

ChatGPT / Claude ile farkı:

ChatGPT veya Claude benimle bir insan gibi sohbet ediyor, sorularıma yanıt veriyor ve komutlarımı (instruction) yerine getiriyor.Yani  ikisinide kullandığım farklı alanlar var. Ancak distilgpt2 modeline bir metin verdiğimde bana bir asistan gibi yanıt vermek yerine, sadece sanki ben klavyede yazı yazarken yarım bırakmışım gibi cümleyi kaldığı yerden devam ettirmeye çalıştı.

Bunun nedenlerinden biri hakkında hipotezim:

Modeli araştırmam sonucunda bu kullandığım modelin saf bir base model olması. Bu model sadece internetteki metinleri okuyarak "sıradaki kelimeyi tahmin etmek" (next-token prediction) üzere eğitilmiş.

## 10. Generation Parametreleri

### `do_sample=False`
Gözlem:

Genellikle sıkıcı, robotik ve bir süre sonra aynı kelimelerin etrafında dönen (tekrara düşen) metinler üretti.

### `temperature=0.7`
Gözlem:

Konudan sapmadan tutarlı metin üretti.ChatBotlarda alışık olduğumuz dönüşler vardı.

### `temperature=1.2`
Gözlem:

Cümle tutarlı giderken biraz anlam karmaşası yaratıcak yöne doğru sapmalar yaptı.

Bunlardan çıkardığım sonuç:

Parametreleri ne kadar iyi kullanırsak aldığımız yanıt o kadar dengeli ve tatmin edici olur.

## 11. AI Code Review

AI'nın önerdiği ve kabul ettiğim değişiklik:

...

Neden:

...

AI'nın önerdiği fakat kabul etmediğim / ertelediğim değişiklik:

...

Neden:

...

## 12. Karşılaştığım Hatalar

### Hata 1

Hata:

Kullanıcının terminalden giriş yaparken hiçbir metin yazmadan Enter'a basması sonucu modelin boş girdi ("") alması ve programın çökmesi.

Muhtemel neden?

Boş veri girişine karşı başta bir koruma sağlamamam.

Denediklerim:
1. if-else bloğu 


Çözüm:

input_text = input("Enter a prompt for text generation: ")
    if not input_text.strip():
        print("Input cannot be empty. Please enter a valid prompt.")
        return get_input()
    return input_text


Öğrendiğim:

Kullanıcının her türlü hatayı yapabilceği ve buna karşı önlem almış olmak.

## 13. Blocker'lar

Blocker yoksa:

`Yok.`

Varsa:

### Blocker

Problem:
...

Denediklerim:
...

Hata mesajı:
...

Devam etmek için ihtiyacım olan:
...

## 14. Bugünün En Önemli 5 Öğrenimi

1. Vibe Coding disiplini
2. LLM yapısının nasıl çalıştığı
3. Tokenizasyon mantığını ve Türkçenin bunu nasıl değiştirdiği
4. transformer ve Attention mekanizması
5. Modelin davranışlarında parametrelerin önemi

## 15. Kendi Değerlendirmem

### Python

Gün başı: 4 / 10  
Gün sonu: 7 / 10

Bu puanı neden verdim?

Çoğu konuyu yeni öğrenmeye başladığımdan gün başından çok daha iyi bir noktadayım fakat bu yapıları tekrar ederek ve alıştırmalar yaparak daha iyi sindirmem gerekiyor.

### LLM çalışma mekanizmasını anlama

8 / 10

Neden?

Bazı yapılar soyut kalmış olsada genel çerçevesiyle çalışma mekanizmasını anladım.

### AI ile kontrollü kod geliştirme

6 / 10

Neden?

Prompt yazmayı geliştirerek vibe coding döngüsüne daha iyi alışıcağımı düşünüyorum.

## 16. Yarın İçin Sorularım



## 17. Derinleşmek İstediğim Konular



# 6. Gün sonunda kendini test et

AI araçlarını kapat.

Aşağıdaki sorulara sözlü cevap ver.

1. Python'da function neden kullanırız?
2. `list` ile `dict` arasındaki fark nedir?
3. Module neden kullanılır?
4. Exception nedir?
5. Token nedir?
6. Tokenizer ne yapar?
7. Kelime ve token aynı şey midir?
8. Context ne demektir?
9. Transformer kelimesi bugün senin için ne ifade ediyor?
10. Attention'ın sezgisel amacı nedir?
11. Bir LLM'in “next-token prediction” yapması ne demektir?
12. Inference ile training aynı şey midir?
13. Açık model deneyindeki model neden ChatGPT gibi davranmadı?
14. Temperature çıktıyı nasıl etkileyebilir?
15. AI'nın yazdığı bir kodun doğru olduğuna nasıl karar verirsin?

### Değerlendirme

- 0–5: Yarın bazı temelleri tekrar etmemiz gerekir.
- 6–10: Beklenen başlangıç düzeyi.
- 11–13: İyi ilerleme.
- 14–15: Çok iyi; 2. gün daha hızlı ilerleyebiliriz.

Bu bir sınav değildir.

