# LLM-driven Kararlar

Answer generation 
Query rewrite 
Exploratory LLM classifier
Tool call proposal

# Deterministic (Python) Kontroller

Route allowlist 
Tool allowlist 
Citation label validation 
Max rewrite
Max steps 
Qdrant filter construction 
Test assertions 
Trace schema  

# Bu sistemde hangi kararı modelden Python'a taşımak reliability'yi artırdı?

Modelin kendi kendine sonsuz döngülere girmesini ve yetkisiz araçları çağırmasını engellemek 
için MAX_STEPS / MAX_REWRITES sınırlarını ve tool allowlist kontrolünü Python a taşımak 
sistemin güvenilirliğini doğrudan artırdı. Eğer döngüden çıkma veya hangi aracın 
çalıştırılacağı kararı tamamen modele bırakılsaydı, modelin halüsinasyon görmesi tüm iş 
akışını bozabilirdi. Citation label validation işleminin de modelin "Ben doğru kaynak 
kullandım" demesine güvenmek yerine Python tarafında kesin string eşleştirme ile yapılması,
sistemin kontrol ve güvenlik sınırlarını LLM'in esnekliğinden çıkarıp deterministik bir 
temele oturttu.


# -------------------------------------------------


| Evidence | Gerçek değer | Nereden geldi? |
|---|---:|---|
| Total unit tests passed |50 | pytest output |
| Total integration tests passed |15 | pytest output |
| Day 8 answerable eval questions | 6 | eval dataset |
| Day 8 unanswerable eval questions | 2 | eval dataset |
| Fixed ingestion chunk config |chunk_size=600, overlap=100 | actual code |
| Top-k experiment values |1, 3, 5 | actual runner |
| Hit@1 |6/6 | generated eval output |
| Hit@3 |6/6 | generated eval output |
| Workflow routes |smalltalk, knowledge, tool | code/state |
| MAX_REWRITES |1 | code |
| MAX_STEPS |12 | code |
| LangGraph version | 1.2.11 | requirements |
| Failure cases tested today |7| pytest/output |

# -------------------------------------------

# Known Limitations

Retrieval quality policy çok basit:
Geri çağrılan (retrieved) belgelerin kalitesini değerlendiren kuralımız, anlamsal bir 
uygunluk (relevance) ölçümünden ziyade yalnızca Qdrant'tan sonuç dönüp dönmediğine veya 
sabit bir skora dayanıyor.

Gerçek chunk-size re-ingestion experiment henüz yok:
Farklı parça boyutlarının (300/600/1000) arama kalitesine etkisini ölçerken veri tabanını 
bu boyutlara göre baştan oluşturup (re-ingestion) gömme (embedding) işlemlerini 
yenilemedik; sadece sorgu parametreleri üzerinden varsayımsal bir test yaptık. 
 
Citation validity semantic entailment değildir:
validate_citations fonksiyonumuz modelin ürettiği metindeki [S1], [S2] gibi etiketlerin
varlığını kontrol ediyor, ancak modelin o kaynaktaki bilgiyi gerçekten doğru ve destekli
(grounded) kullanıp kullanmadığını semantik olarak doğrulamıyor.

Small deterministic classifier dil çeşitliliğinde kırılgan:
İş akışındaki kural tabanlı (rule-based) yönlendirici, sadece belirli anahtar kelimeleri 
aradığı için eşanlamlı kelimelerde veya farklı cümle yapılarında kolayca yanlış rotaya 
(invalid route) düşebiliyor. 

Query rewrite gerçek production quality guarantee değildir:
Sorguyu LLM ile yeniden yazdırma (rewrite) işlemimiz arama sonuçları zayıf olduğunda bir 
kez deneniyor, ancak bu işlem her zaman arama kalitesini artırmıyor; bazen niyeti 
değiştirip sonuçları daha da bozabiliyor. 

LangGraph failure boundary henüz basit: 
Hata durumlarında döngüyü kırmak için yalnızca temel bir MAX_STEPS sınırı ve basit bir
fallback (geri çekilme) düğümü kullanıyoruz; sistemde üretim seviyesinde bir "circuit 
breaker" bulunmuyor. 

Sandbox demo production multi-tenant sandbox değildir: 
Kısıtlı kod çalıştırma sınırlarını (--network none, --read-only, tmpfs) yalnızca manuel 
Docker komutlarıyla, izole bir laboratuvar ortamında kanıtladık; sistemimiz henüz yüzlerce 
kullanıcının kodunu aynı anda güvenle çalıştırabilecek gVisor veya Firecracker mimarisine 
sahip değil.


# --------------------------------------------------------

# Bu Hafta En Çok Gelişen 5 Yetkinlik

1. Vektör Veritabanı ve Anlamsal Arama (Semantic Search) Yönetimi: Metinleri matematiksel dizilere (embeddings) dönüştürüp aralarındaki kosinüs benzerliğini hesaplamaktan, bu yapıyı Qdrant üzerinde 
metadata filtreleri ve kalıcılık (persistence) ile gerçek bir servis mimarisine taşımak.
2. RAG (Retrieval-Augmented Generation) Mimarisini Kurma ve Denetleme:
Verileri doğru boyutlarda (chunk) bölüp LLM'e bağlam (context) olarak sunmak ve modelin ürettiği metinlerin gerçekten arama motorundan gelen kaynaklara dayanıp dayanmadığını (citation validation) 
doğrulamak.
3. Ölçüme Dayalı Sistem Değerlendirme (Evaluation) Refleksi: Modelin ürettiği cevabın görünüşüne aldanmak yerine, doğru belgenin getirilip getirilmediğini Hit@1 ve Hit@3 gibi metriklerle ölçmeyi, 
ayrıca arama kalitesini artırmak için chunk-size ve top-k deneylerini verilerle yorumlamayı öğrenmek.
4. Durum Tabanlı (Stateful) İş Akışı Orkestrasyonu: Karar süreçlerini tamamen modele bırakmak yerine; deterministik kuralları, LLM'in yönlendirme (routing) esnekliğini ve döngü limitlerini LangGraph 
gibi bir yapı üzerinden "durum" (state) tutarak kontrol etmek.
5. Hata Yönetimi (Reliability) ve Güvenlik Sınırları (Sandboxing): Sistemin kusursuz çalışma senaryosundan (happy path) çıkıp; dış servis çökmelerini, zaman aşımlarını ve sonsuz döngüleri (detect, 
contain, recover, observe) yakalamak ve modele verilen kod çalıştırma yetkilerini Docker isolation katmanları (--network none, --read-only vb.) ile kısıtlamak.

# --------------------------------------------------------

# External Services
Ollama
Qdrant

# --------------------------------------------------------

# Observability

node_trace: İş akışının hangi düğümlerden (node) sırasıyla geçtiğini kaydeden liste.
step_count: Sonsuz döngüleri tespit edebilmek için atılan toplam adım sayısı.
duration_ms: Ana akışın başlangıcından bitişine kadar geçen sürenin kronometre kaydı.
errors ve error_type: Sistemde bir hata fırlatıldığında (WorkflowLimitError, DependencyUnavailableError vb.) hatanın türünü ve yutulmadan önceki orjinal mesajını tutan kayıtlar.

# --------------------------------------------------------

# Üçüncü Haftaya Taşınacak Teknik Borçlar

1.LangGraph'a Checkpointer mekanizması ekleyerek hafızayı (state) RAM'de uçucu olarak tutmak yerine bir veritabanına/diske kaydetmek ve önceki sohbetleri hatırlayabilmek.
2.Gelen metinleri sadece sabit karakter/kelime sayısına göre değil, anlam bütünlüğüne veya Markdown başlıklarına göre bölen dinamik bir chunking stratejisi araştırmak.
3.Sadece belirli anahtar kelimelere ("kargo", "merhaba") bakan basit (rule-based) classifier yerine, daha esnek çalışan ufak bir LLM tabanlı yönlendirici test etmek.


# --------------------------------------------------------

# Security Boundaries

1.--network none: Dış dünya ile bağlantıyı keserek veri sızdırmayı (exfiltration) engellemek.
2.--read-only: Ana dosya sistemini kilitli tutarak zararlı dosyaların kalıcı olarak yazılmasını önlemek.
3.--tmpfs /tmp: Sadece çalışma anında var olan, geçici ve boyut sınırlı bir bellek içi dosya sistemi vermek.
4.Non-root user (1000:1000): Uygulamanın sistem yöneticisi yetkileriyle çalışmasını engelleyerek olası yetki tırmanışlarını kırmak. 

# --------------------------------------------------------


[ 1. INGESTION PIPELINE ]

source documents
       │
       ▼
    chunking [D]                  Ollama [E]
       │                       ┌───────────────┐
       ▼                       │embeddinggemma │ [L]
   embeddings ◄────────────────┤               │
       │                       └───────────────┘
       ▼
    Qdrant [E][P]

────────────────────────────────────────────────────────

               [ 2. QUERY WORKFLOW ]

                   user query
                       │
                       ▼
             workflow routing [D]
              (classify_query)
        ┌──────────────┼──────────────┐
        │              │              │
    smalltalk      knowledge         tool
        │              │              │
        │              ▼              ▼
        │        ┌─► retrieval   allowlisted tool [D][S]
        │        │ (Qdrant [E][P])    │
        │        │     │              │
        │        │     ▼              │
        │   rewrite retrieval_quality [D]
        │     [L] ◄────┤              │
        │              │ good         │
        │              ▼              │
        │       context builder [D]   │
        │              │              │
        ▼              ▼              │
     direct         grounded          │
    generate        generate          │
   (qwen3 [L])     (qwen3 [L])        │
        │              │              │
        │              ▼              │
        │     citation validation [D] │
        │              │              │
        └──────────────┼──────────────┘
                       ▼
             trace / terminal state [D]
