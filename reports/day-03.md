day: 3
date: 2026-08-19
status: completed
compose_tests_passed: 5
compose_tests_failed: 0
docker_image_built: true 
compose_working: true 
output_bind_mount_working: true
blocker_count: 0


# Gün 3 — Çalışma Raporu

## 1. Gün Özeti

1. Python projemin bağımlılıklarını ve çalışma ortamını izole etmek için Dockerfile yazdım.
2. O uzun terminal komutlarından kurtulmak ve otomasyon sağlamak için projemi Docker Compose altyapısına taşıdım.
3. Bind Mount mantığını kavrayarak container içindeki geçici klasörleri kendi bilgisayarımdaki kalıcı output/ klasörüne bağladım
4. Tüm testlerimi kendi bilgisayarımda değil Docker containerınnın içinde çalıştırdım.
5. Benim bilgisayarımda çalışıyordu problemine son verdim.



## 2. Proje Sağlamlaştırma

Bugün düzenlediğim şeyler:

- `tests/test_text_utils.py` dosyasına 5 adet anlamlı (assert barındıran) test yazdım.
- Regex (`re.findall`) kullanarak noktalama işaretlerini ayıklayan temiz bir input akışı kurguladım.
- `requirements-docker.txt` dosyasını oluşturup gerekli kütüphaneleri sabitledim.



## 3. Docker'ı Şu An Nasıl Anlıyorum?

### Image

Uygulama ,bağımlılıklar ve çalışma ayarlarını içeren değişmez paket
### Container

image ın çalışan bağımsız örneği.

### Dockerfile

image ın nasıl hazırlanacağını anlatan metin dosyası.

### Build context

docker a imajı oluştururken içine katması için gönderdiğim çalışma klasörüm ve o anki tüm dosyalarım.

### Layer

Dockerfile'a yazdığım her bir copy veya run komutunun üst üste binerek oluşturduğu katmanlar

### Build cache

Değişiklik yapmadığım katmanların her seferinde baştan indirilmemesi için olan hafıza yapısı.

---

## 4. Dockerfile'ım


FROM python:3.9-slim

WORKDIR /app

COPY day03/requirements-docker.txt ./requirements-docker.txt
RUN python -m pip install --no-cache-dir -r requirements-docker.txt

COPY . .

CMD ["python", "day03/text_cli.py", "Docker icindeki varsayilan CMD calisti!"]

`FROM`
Temel ortamı seç
`WORKDIR`
Çalışma klasörünü belirle
`COPY`
Proje dosyalarını image e aktar
`RUN`
image çalışırken komut çalıştır
`CMD`
container başlayınca çalışcak komutu belirle
---
5. Docker Compose
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile

    environment:
      APP_MODE: compose

    volumes:
      - ./output:/app/output

    command:
      - python
      - day03/text_cli.py
      - Docker Compose uzerinden calisan Python
`services`
Compose un yönetecek olduğu uygulamaları tanımladığım ana başlık.
`build`
Compose a imajı hangi klasördeki hangi dosyaya bakarak inşa edeceğini gösteriyor
`environment`
Container ın içine benim dışarıdan APP_MODE=compose gibi çevresel değişkenler göndermemi sağlıyor
`volumes`
Bu kısım Bind Mount bilgisayarımdaki klasörle contaimner daki klasörü bağlıyor
`command`
Uygulamanın hangi argümanla çalışıcağını belirler
---
6. Testler
Bugün testleri host'ta değil Compose üzerinden çalıştırdım.
Komut:
```bash
docker compose run --rm app python -m pytest -v
```
Sonuç:
Passed: 5
Failed: 0
```
Bu yaklaşımın avantajını şöyle açıklıyorum:
Testlerimi artık sadece kendi bilgisayarımda değil uygulamanın gerçekten yaşayacağı standart ortamda kanıtlamış oluyorum. Her şey şeffaf ve tekrar edilebilir.
7. Host ve Container Ortamı
Host Python ortamıyla container Python ortamını neden ayırıyoruz?
Çünkü host ortamımda geçmişten kalan gereksiz kütüphaneler veya farklı sürümler olabilir. Container ise her seferinde temiz, beklentilerime uygun ve izole bir ortam sunuyor.
Aynı projenin başka makinede daha tutarlı çalışmasına Docker nasıl yardımcı olabilir?
Başkası projemi klonladığında "Hangi Python sürümünü kurmalıyım?" diye düşünmüyor. Sadece docker compose up yazıyor ve tam olarak benim test ettiğim mimarinin birebir aynısında kodları ayağa kaldırıyor.
8. Output Bind Mount
Compose satırım:
```yaml
- ./output:/app/output
```
Container içinde yazılan dosya:
/app/output/text-analysis.json (ve pytest-day03.txt)

Host'ta görüldüğü konum:

C:\Users\HP\ai-intern-week\output\
Container `--rm` ile silindikten sonra dosya kaldı mı?
Evet Kaldı.
Neden?
Çünkü dosya aslında containerın geçici hafızasına değil, aradaki bind mount sayesinde doğrudan benim host makinemin fiziksel hard diskine yazıldı. Container silinse bile dosya bende kaldı.
9. `.gitignore` ve `.dockerignore`
`.gitignore`
`output/` için kullandığım yapı:

output/*
!output/.gitkeep

`.dockerignore`
`output/` neden build context'e girmiyor?
Çünkü imajın içine önceki denemelerimden kalan gereksiz logların, metinlerin veya JSON dosyalarının kopyalanıp imajı boş yere şişirmesini istemiyorum
10. Bind Mount vs Named Volume
Bind mount
Dosya yolu önemlidir.Geliştirici dosyayı doğrudan kendi klasöründe görmek ister
Named volume
Verini kendisi önemlidir dosyanın fiziksel konumunu Dockerın kendi içinde yönetmesi tercih edilir.
Bugün output için neden bind mount kullandım?
Çünkü analiz sonucunu ve test raporunu kendi kod editörümde açıp anında incelemek istedim.
Yarın Ollama model verisi için neden named volume daha uygun olabilir?
Named Volume daha uygun olabilir çünkü gblarca büyüklükteki model verisini manuel olarak açıp okumayacağım veya düzenlemeyeceğim. Onları Docker'ın kendi kendine yönetmesi ve saklaması çok daha güvenli ve mantıklı.
---
11. Container Lifecycle
`docker ps`
O an canlı canlı çalışan, ayakta olan container'ları listeler
`docker ps -a`
Çalışması bitmiş, çökmüş veya durdurulmuş olanlar dahil projemin tüm geçmiş container'larını gösterir.
`--rm`
Container'a işini (örneğin testi bitirmeyi) tamamladığında arkasında çöp bırakmadan kendi kendini yok etmesini emreder.
Container silmek vs image silmek
Container silmek sadece çalışan o anki geçici programı kapatmaktır image silmek ise tüm projeyi şablonu tamamen bilgisayardan silmektir.Sınıf nesne ilişkisine benzetebiliriz.
---
12. Çalıştırdığım Önemli Komutlar
Komut	Ne yapıyor?
`docker compose build`	
Compose dosyasını okur imajı tarifime göre baştan inşa eder.
`docker compose run --rm app`	
Ayarlarımla containerı ayağa kaldırır varsayılan komutu koşturur ve silinir.
`docker compose run --rm app python -m pytest -v`	
Container içinde varsayılan kod yerine zorla testlerimi çalıştırır.
`docker compose ps`	
Sadece bu Compose projesine ait çalışan servisleri gösterir.
`docker images`	
Bilgisayarımdaki inşa edilmiş kalıcı imajların listesini ve boyutlarını verir.
`docker ps -a`	
Kapanmış veya çalışan tüm container kalıntılarını listeler.
---
13. Karşılaştığım Hatalar
Hata 1
Komut:
```bash
docker run --rm text-analyzer pytest

Hata:
```text
ModuleNotFoundError: No module named 'transformers'
Neden:
Dockerfile içine sadece pytest kurmuştum. Container temiz bir makine olduğu için benim test kodlarımın içindeki transformers paketini bulamayıp çöktü.
Denediklerim:
Hata logundaki "ImportError" kısmını incelemek.

Bağımlılıkların eksik olduğunu fark etmek.
Çözüm:
requirements-docker.txt dosyasına transformers'ı da ekleyerek imajı yeniden build ettim ve ortamı eşitledim.
Öğrendiğim:
Container varsayımlar üzerinden çalışmaz, benim bilgisayarımdaki her kütüphanenin orada da olduğunu düşünmemeliyim. Ne gerekiyorsa reçeteye yazmalıyım.
14. AI ile Çalışma
ChatGPT / Codex
Kullandığım görevler:
Kavram tanımları ve gerçek hayat örnekleriyle benzetme kurarak açıklama
Terminal komutlarının öğrenimi
Faydalı prompt:
```text
"Terminalde testleri yazdırmak için 'docker compose run --rm app sh -c "python -m pytest -v | tee /app/output/pytest-day03.txt"' şeklinde uzun bir komut kullandım. Bu komutun içindeki '--rm', 'sh -c' ve 'tee' parametrelerinin ne anlama geldiğini ve arkada tam olarak ne işe yaradığını adım adım açıklar mısın?"
Değiştirdiğim / reddettiğim öneri:
...
Neden:
...
Claude / Claude Code
Kullandığım görevler:
Alınan hataların karşısında çözüm önerileri
Kod analizi ve iyileştirmeler
Faydalı prompt:
"Yazdığım 'clean_text' fonksiyonunda noktalama işaretlerini temizlemek için 're.findall(r"\b\w+\b", "Hello World! This is a test.")' kullandım. Ancak metni dışarıdan dinamik almak yerine sabit  yazdığımı fark ettim ve regex bana liste döndüğü için sonraki aşamada hata alıyorum. Bu fonksiyonu string döndürecek şekilde, mantık ve veri tipi uyuşmazlığı hatalarını nasıl profesyonelce düzeltebilirim?"
```
Değiştirdiğim / reddettiğim öneri:
...
Neden:
...
---
15. Bugün AI Olmadan Açıklayabildiğim Şeyler
Dockerfile, Image ve Container arasındaki ilişki
Bind Mount ile dosyaların neden silinmediğinin fiziksel mantığı
compose.yaml dosyasının o uzun komutlarımızı nasıl otomatize ettiği
Testleri neden lokalimde değil Compose ortamında çalıştırdığım

---
16. Yarın İçin Sorularım
Ollama'nın devasa model dosyalarını çekerken Named Volume tam olarak diskin neresinde tutulacak?
---
17. Ollama İçin Merak Ettiklerim
Python kodu ile Ollama arasındaki iletişimi HTTP üzerinden kurarken özel bir port açacak mıyız yoksa localhost 8080 üzerinden mi işliycez?

---

# 6. Gün sonu kontrol listesi

```text
\\\[x] 5+ anlamlı pytest testi var
\\\[x] gereksiz recursion temizlendi
\\\[x] generation experiment tekrar üretilebilir
\\\[x] model comparison script bütün promptları işleyebiliyor
\\\[x] README güncel

\\\[x] .dockerignore mevcut
\\\[x] Dockerfile çalışıyor
\\\[x] compose.yaml mevcut
\\\[x] docker compose build çalışıyor

\\\[x] uygulama Docker Compose üzerinden çalışıyor
\\\[x] testler YALNIZCA Docker Compose üzerinden başarıyla çalıştırıldı
\\\[x] docker compose run --rm app python -m pytest -v PASS

\\\[x] output/ klasörü mevcut
\\\[x] output/.gitkeep mevcut
\\\[x] gerçek output dosyaları Git tarafından ignore ediliyor
\\\[x] output/ Docker build context'e alınmıyor

\\\[x] ./output:/app/output bind mount çalışıyor
\\\[x] uygulama container içinde output dosyası oluşturuyor
\\\[x] dosya host output/ klasöründe görünüyor
\\\[x] container silindikten sonra output dosyası hâlâ mevcut

\\\[x] bind mount ile named volume farkını açıklayabiliyorum
\\\[x] reports/day-03.md tamamlandı
