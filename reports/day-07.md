day: 7
date: 2026-08-25
status: completed
embedding_model: embeddinggemma
vector_db: qdrant
qdrant_version: 1.19.0
collection: intern_documents
unit_tests_passed: 5
integration_tests_passed: 3
blocker_count: 0


# Gün 7 — Vector Database ve Qdrant

## 1. Day 6 Kapanışı

Embedding integration testlerinde ne eksikti?
Testlerin içinde dönen sonuçları matematiksel olarak doğrulayan gerçek `assert` ifadeleri yoktu sadece kodun çöküp çökmediğine bakıyordum.

Nasıl düzelttim?
Testlerin içine `assert` kontrollerini ekledim.

Semantic-search regression testleri:
Semantic search için ranking testi ekledim

Mental-model düzeltmem:
Embedding, insan dilindeki değişken uzunluktaki herhangi bir bilginin, yapay zeka süzgecinden geçirilerek, veritabanının matematiksel olarak kıyaslayabileceği sabit uzunlukta bir koordinata (vektöre) dönüştürülmesi sürecidir.

Dokümantasyon temizliği:
Test sayılarını total ve specific olarak ikiye ayırdım,markdown ifadelerini düzenledim.

## 2. Bugünkü Mimari
App:
Vektör oluşturma (ingestion), arama (search) ve test süreçlerini yürüten geçici Docker Python servisi.
Ollama:
Metinleri vektörlere dönüştüren `embeddinggemma` modelini koşturan yerel AI motoru.
Qdrant:
Üretilen vektörleri depolayan, filtreleme için metadataları saklayan ve semantic arama operasyonlarını yürüten veritaban.

## 3. Collection
Ad:
`intern_documents`
Dimension:
768
Distance:
COSINE
Dimension'ı nereden aldım?
Ollama üzerinden kullandığımız `embeddinggemma` modelinin sabit vektör boyutundan.

## 4. Dataset ve Payload
Document sayısı:
10 adet.
Payload alanları:
`document_id`, `text`, `category`, `source`, `day`, `topic`, `language`

## 5. Point Mental Model
Internal point ID:
Qdrant'ın indeksleme için zorunlu kıldığı tam sayı
Original document ID:
Kendi sistemimdeki referans metin kimliği
Vector:
768 adet ondalıklı (float) sayıdan oluşan matematiksel dizi.
Payload:
Vektörle eşleşen meta verileri içeren JSON (sözlük) objesi

## 6. İlk Semantic Query
Query:
Container silindiğinde dosyalarımın kaybolmasını nasıl engellerim?
Top-3:
"document_id": "doc-01",
"score": 0.6357,
"payload": 
"category": "docker",
"text": "Docker named volume kalıcı veri saklar. Container silinse bile veriler host makinede güvende kalır."
      
"document_id": "doc-02",
"score": 0.4144,
"payload": 
"category": "database",
"text": "Qdrant bir vektör veritabanıdır. Vektörleri bellek yerine diskte kalıcı olarak saklamamızı sağlar."
  
"document_id": "doc-08",
"score": 0.352,
"payload": 
"category": "docker",
"text": "Docker Compose ağında, aynı network içindeki servisler birbirlerine doğrudan servis isimleriyle ulaşabilir. Host portunun açılması zorunlu değildir."
    

## 7. Metadata Filtering
Filter:
category= docker
Filtresiz:
1. Skor: 0.6357 | Kategori: docker
   Metin: Docker named volume kalıcı veri saklar. Container silinse bile veriler host makinede güvende kalır.
2. Skor: 0.4144 | Kategori: database
   Metin: Qdrant bir vektör veritabanıdır. Vektörleri bellek yerine diskte kalıcı olarak saklamamızı sağlar.
3. Skor: 0.3520 | Kategori: docker
   Metin: Docker Compose ağında, aynı network içindeki servisler birbirlerine doğrudan servis isimleriyle ulaşabilir. Host portunun açılması zorunlu değildir.
Filtreli:
1. Skor: 0.6357 | Kategori: docker
   Metin: Docker named volume kalıcı veri saklar. Container silinse bile veriler host makinede güvende kalır.
2. Skor: 0.3520 | Kategori: docker
   Metin: Docker Compose ağında, aynı network içindeki servisler birbirlerine doğrudan servis isimleriyle ulaşabilir. Host portunun açılması zorunlu değildir.
Ne değişti?
Filtreli aramada kalıcı veriyle ilgili olsa dahi aktegorisi docker a girmeyen metni eledi.

## 8. Memory vs Qdrant
İkisi de birebir aynı skorları (0.6357) üretti.
Qdrant'ın asıl kazandırdığı:
Skor başarısı değil; veri kalıcılığı, arama hızı (brute-force yerine index kullanımı), meta veri filtreleme ve başka servislerden erişilebilir bir api sunması.

## 9. Persistence
docker compose down sonrası:
Konteynerler silindi ancak `qdrant_data` (Named Volume) host makinede güvende kaldı.
Tekrar ayağa kaldırınca:
Yeniden verileri yüklemeye gerek kalmadan arama scripti önceki id ve vektörleri aynı skorla döndürdü.

## 10. SQLite vs Qdrant
Exact ID:
Kesinlikle SQLite (veya klasik DB) kullanılmalı (`WHERE id = 'doc-07'`)
Category:
Her ikisi de kullanılabilir (SQL için `WHERE`, Qdrant için `Filter`).
Semantic query:
Kesinlikle Qdrant kullanılmalı SQL eşanlamlı kelimelerin matematiğini anlayamaz.

## 11. Index Mental Model
Brute-force:
Gelen sorguyu veritabanındaki tüm kayıtlarla tek tek karşılaştırma işlemi. Day 6da yazdığım bellek içi arama mantığı buydu. Kesin eşleşme sağlasa da veri seti büyüdükçe sistemi kilitleyecek kadar yavaşlayan ve ölçeklenemeyen bir yöntem.
ANN:
Kesin bir doğruluk yerine, kabul edilebilir bir hata payıyla işlem hızını artırma yaklaşımı. Birebir en doğru sonucu getirmeyi garanti etmiyor ancak en iyiye çok yakın sonuçları anında bularak sistemin büyük verilerde performanslı çalışmasını sağlıyor.
HNSW hakkında bugün anladığım:
Qdrantın yüksek hızlı arama yapmak için kullandığı indeksleme algoritması. Arama sırasında tüm veritabanını taramak yerine doğrudan ilgili veri gruplarına odaklanarak arama süresini ciddi oranda kısaltıyor.

## 12. Output
output/day07-vector-db-experiments.json
Deneyler kalıcı dosyaya başarıyla yazdırıldı

## 13. Testler
Unit Passed:5
Unit Failed:0
Integration Passed:3
Integration Failed:0

## 14. AI Araçları
Önce kendim yaptığım:
`ingest.py` dosyasında veritabanına yazılacak dokümanların uyması gereken katı doğrulama kurallarını tasarladım.
AI review:
AI'dan JSON'daki dokümanları Qdrant'a yükleyecek temel `ingest.py` iskeletini kurmasını istedim.
AI'nın önerdiği ama değiştirdiğim/reddettiğim öneri:
AI, hiçbir hata kontrolü içermeyen gelen veriyi körü körüne veritabanına basan oldukça zayıf ve junior seviyesinde bir döngü sundu. Bu yapıyı tamamen reddettim.
Neden:
Gerçek dünya senaryolarında eksik veya formatı bozuk bir payload geldiğinde bu basit kod sistemi anında çökertecekti.

## 15. Karşılaştığım Bir Hata
Problem:
App container içinde from qdrant_client import QdrantClient importu çalışmadı ve ModuleNotFoundError: No module named 'qdrant_client' hatası alındı. Dockerfile python:3.9-slim kullanırken qdrant-client==1.19.0 Python 3.10 veya üzerini gerektiriyordu.
İlk kontrolüm:
docker compose run --rm app python -m pip show qdrant-client komutunu çalıştırdım. Çıktıda Package(s) not found mesajını gördüm. Ardından requirements.txt ve Dockerfile’daki Python sürümünü kontrol ettim.
Kaynak:
Qdrant Client 1.19.0’ın resmî PyPI sayfasında paketin Python >=3.10 gerektirdiğini doğruladım: https://pypi.org/project/qdrant-client/1.19.0/
Çözüm:
requirements.txt dosyasına qdrant-client==1.19.0 eklendi ve Dockerfile temel image’ı python:3.9-slim yerine python:3.10-slim olarak güncellendi. Ardından docker compose build --no-cache app ile app image’ı yeniden oluşturuldu. Paket kurulumu ve Qdrant bağlantısı pip show, import testi ve client.get_collections() çağrısıyla doğrulandı.

## 16. Bugünün En Önemli 5 Öğrenimi
1.SQL ve Vektör Veritabanı İlişkisi: Vektör veritabanları ilişkisel  veritabanlarının yerine geçmez yapısal veri erişimi ile anlamsal arama farklı problemleri çözer ve birlikte kullanılır.
2.Qdrant'ın Asıl Sorumluluğu: Qdrant, bellekte yapılan hesaplamadan daha iyi bir score üretmek için değil retrieval mekanizmasına kalıcılık , indeksleme, filtreleme ve API sorumluluklarını kazandıran ayrı bir veri katmanı olduğu için tercih edilir.
3.Filtreleme ve Anlamın Birleşimi: Arama işlemleri sadece vektör benzerliği ile sınırlı kalmaz anlamsal yakınlık ile yapısal filtreler (örneğin category = docker) birleştirildiğinde çok daha hedeflenmiş sonuçlar elde edilir. 
4.Point ve Payload Modeli: Qdrantta veriler "Point" yapısıyla tutulur bu yapı sadece vektörü değil, integer/UUID formatında bir kimlik ile beraber dokümanın kendisini ve metadatasını barındıran "payload" alanını içerir.
5.Skorların Doğru Yorumlanması: Cosine similarity skoru bir sonucun "% doğruluk" oranı (örneğin 0.82 = %82 doğru) değildir yalnızca iki vektörün yön ilişkisini ölçer ve bu skorun yorumu modele ve veriye bağlıdır.

## 17. Yarın RAG Hakkında Merak Ettiklerim
1. Qdranttan filtreleyip çektiğimiz en yakın (top-k) dökümanları LLMe (context olarak) nasıl düzgünce formatlayıp vereceğiz?



