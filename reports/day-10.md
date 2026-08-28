---
day: 10
date: 2026-08-28
status: completed 
unit_tests_passed: 50
integration_tests_passed: 15
failure_cases_verified: 7
blocker_count: 0
---

# Gün 10 — Reliability, Security Boundary ve Week 2 Review

## 1. Day 9 Kapanışı
Invalid route:
 invalid route'u her ikisinde de controlled `error` yapıldı.
Native/LangGraph terminal semantics:
Aynı workflow'un iki orchestration biçiminde terminal semantics sağlandı
Day 8 evaluation correction:
Top-k =3 kodlamadan çıkarıldı.
Day 8 evidence-language correction:
Yargılar düzenlendi.
README:
Güncellendi.
Actual test counts:
50 Unit, 15 Integration test başarıyla geçiyor.

## 2. Failure Matrix
Failure mode count:
7 temel hata senaryosu
Expected runtime failures:
Dış servislerin çökmesi (Qdrant), LLM API zaman aşımı, aracın çalışma zamanında patlaması.
Programmer/config bugs:
Parametre tiplerinin yanlış verilmesi (string yerine int beklenmesi), tanımlanmayan rotalar, hatalı mock konfigürasyonları.

## 3. Failure Injection

### Retriever unavailable
Detect: Qdrant'tan Exception dönmesi.
Contain: Akışın `error_type: DependencyUnavailableError` ile hata düğümüne alınması.
Recover: Kullanıcıya veya sisteme `error` statüsünde, sorunun nerede (`failed_node: retrieve`) koptuğunu belirten bir state dönülmesi.
Observe: Hatanın `errors` listesine ve `output/day10-failure-experiments.json` dosyasına kaydedilmesi.

### Model timeout
Detect: Ollama API çağrısında belirlenen sürenin aşılması (Timeout exception).
Contain: Sistemin kilitlenmesini önlemek için anında `DependencyTimeoutError` fırlatılması.
Recover: İş akışının `error` olarak sonlandırılması.
Observe: `failed_node: generate` ve trace kayıtlarının diske yazılması.

### Tool failure
Detect: Aracın iç mekanizmasından dönen beklenmedik hata (`RuntimeError`).
Contain: Dispatcher'ın hatayı `ToolRuntimeError` nesnesine çevirmesi.
Recover: `status: error` statüsüyle akışın sonlanması.
Observe: Hata kaydı ve patlayan arama aracının (`failed_node: execute_tool`) loglanması.
### Invalid route
Detect: Yönlendiricinin (classifier) izin verilen `smalltalk`, `knowledge`, `tool` dışında bir değer (örn. `banana_route`) dönmesi.
Contain: Koşullu kenarın (conditional edge) rotayı `WorkflowError` olarak yakalaması.
Recover: İşlemin devam ettirilmeden `error_node`'a düşürülmesi.
Observe: Hatanın trace listesine işlenmesi.
### Rewrite exhaustion
Detect: Arama motorunun sürekli zayıf sonuç dönmesi ve sayaç kontrolü (`rewrite_count > MAX_REWRITES`).
Contain: Döngünün zorla kırılarak `WorkflowLimitError` mantığıyla kısıtlanması.
Recover: Sistemin `fallback` düğümüne geçerek "Üzgünüm, bilgi bulamadım" diyebilmesi ve `status: completed` dönmesi.
Observe: JSON raporunda limit aşımının tespit edilmesi.

### Max-step
Detect: LangGraph state üzerindeki `step_count` değerinin `MAX_STEPS` (12) limitini aşması.
Contain: Yeni bir düğüm (node) çalıştırılmadan `WorkflowLimitError` fırlatılması.
Recover: Sistemin `status: stopped` statüsüne çekilmesi.
Observe: İzleme kayıtlarında `failed_node: next_step` olarak gözlemlenmesi.

### Invalid citation
Detect: Üretilen metindeki `[Sx]` etiketinin, sağlanan kaynakların (chunks) geçerli etiketleri arasında bulunmaması.
Contain: Validatörün `ResponseContractError` fırlatarak bu sahte kaynağın sisteme yayılmasını engellemesi.
Recover: İşlemin `error` durumuyla durdurulması.
Observe: JSON loglarında `invalid_citation` deneyi olarak başarıyla kaydedilmesi.

## 4. Error / Terminal State Policy
completed: İş akışı başarıyla hedefine ulaştığında veya kontrollü bir şekilde fallback mekanizmasıyla cevap üretildiğinde.
error: Dış bağımlılıkların çökmesi veya sistem içi kesin sözleşmelerin (geçersiz tool veya citation) ihlal edilmesi durumunda.
stopped: Sistem sonsuz döngüye girmek üzereyken `MAX_STEPS` gibi güvenlik kilitleri tarafından zorla durdurulduğunda.

## 5. Timeout Policy
Ollama: İş akışını tamamen tıkamaması için jenerasyon ve arama sorgusu yazdırma işlemlerinde belirlenen saniye sınırı (örn. 30s).
Qdrant: Vektör veritabanından veri çekerken kilitlenmeyi önleyecek saniye kısıtı.
Rewrite: Sorgu iyileştirme için modele gidilirken koyulan dış bağlantı zaman aşımı.

## 6. Retry Policy
Nerede retry var? Sadece okuma amaçlı (read-only) dış bağlantı denemelerinde veya yan etkisi olmayan retriever sorgularında (biz basit tuttuk ancak uygulanabilir).
Nerede özellikle yok? Araç çağrılarında (Tool calling - örneğin kargo veya sipariş işlemi).
Neden? Dış dünyada kalıcı değişiklik yapan işlemlerde (side-effect) hatanın kaynağını bilmeden tekrar denemek, bir müşteriye iki kez kargo fişi kesmek gibi kritik sonuçlar doğurabilir.

## 7. Trace
Yeni alanlar: `duration_ms` (kronometre), `error_type`, `failed_node` ve orjinal hata mesajını tutan `errors` listesi eklendi.
Secret/redaction yaklaşımı:

## 8. Sandbox Threat Model
Filesystem:
Kodun ana makinede kalıcı veya zararlı bir dosya oluşturma riski.
Network:
Kötü niyetli bir kodun dışarıya veya yerel ağa izinsiz veri sızdırma (exfiltration) ihtimali.
Secrets:
Ortam değişkenlerinin (ENV) ele geçirilmesi.
CPU/RAM/PID:
Sonsuz döngü veya fork bombaları ile makinenin kaynaklarının tüketilmesi (Denial of Service).
Persistence: 
Docker daemon: Uygulamanın `docker.sock` dosyasına ulaşıp ana sistemde yeni konteynerler başlatma tehlikesi.

## 9. Restricted Docker Demo
Image:
Kendi derlediğim sandbox-demo imajı

Run flags:
--network none --read-only --tmpfs /tmp --cpus="0.5" --memory="128m"

Normal execution result:
İzin verilen sınırlar içindeki asıl kod sorunsuz çalıştı ve ekrana "Merhaba. Restricted sandbox içinden çalışıyorum." çıktısını verdi.

Read-only observation:
Ana dosya sistemine dosya yazmaya veya değişiklik yapmaya çalıştığımda sistem bunu engelledi ve ekranda "write failure" (Read-only file system) hatasını gördüm.

tmpfs observation:
Kilitli sistemde yalnızca /tmp klasörüne dosya yazma işlemi başarılı oldu ("tmp write ok"). Bu alan sadece RAM'de tutulduğu için konteyner kapandığında tüm yazılanlar yok oldu.

CPU limit observation:
İşlemciyi %100 sömürmesi gereken kodu çalıştırdığımda docker stats üzerinden izledim; --cpus="0.5" sınırı sayesinde ana bilgisayarım kilitlenmedi ve işlem 5 saniye içinde kontrollü bir şekilde kapandı. 

## 10. Her Isolation Katmanını Neden Kullandım
network none:
Dış dünya ile bağlantıyı keserek, model kodunun içeriden dışarıya veri veya şifre sızdırmasını engellemek için.
read-only:
İçerideki dosya sistemine yazma yetkisini kapatarak zararlı kalıcı dosyaların oluşmasını önlemek için.
tmpfs: 
Uygulamanın sadece geçici (ephemeral) ve kapasitesi sınırlı bir bellekte işlem yapabilmesi için.
memory:
Uygulamanın host belleğini tamamen sömürüp ana sistemi çökertmesini önlemek için.
cpus:
Modelin veya kodun işlemcinin tamamını esir almasını kısıtlamak için.
pids:
Sonsuz `fork()` işlemleri ile process tablolarının taşmasını kırmak için.
cap-drop:
İşletim sistemi kernel seviyesinde gereksiz tüm ayrıcalıkları düşürmek (drop) için.
no-new-privileges:
Uygulamanın sonradan yetki tırmanışı (privilege escalation) yapmasını önlemek için.
non-root:
İşlemlerin süper yönetici (root) yerine sıradan ve kısıtlı bir kullanıcı (1000:1000) ile çalışmasını sağlamak için.
seccomp:
Uygulamanın doğrudan kernel üzerinde çalıştırabileceği tehlikeli sistem çağrılarını (syscall) filtrelemek için.
## 11. Docker'ın Sınırları
Docker standart yapısında hala ana işletim sisteminin çekirdeğini (kernel) paylaşır. Bu nedenle kernel seviyesinde bulunabilecek 
bir güvenlik açığı, konteyner içinden ana sisteme sıçrama yapılmasına sebep olabilir. Tam bir yalıtım sağlamaz.
## 12. gVisor / Firecracker Haritası
gVisor:
Uygulama ile host kernel'i arasına girip, sistem çağrılarını (syscall) engelleyen ve yönlendiren bir kullanıcı alanı (user-space) çekirdek katmanıdır.
Firecracker:
Çok hafif, çok hızlı ayağa kalkan donanım seviyesinde izole edilmiş mikro sanal makine (MicroVM) teknolojisidir.
Bugün neden kurmadım?
Mevcut bilgisayarımda yerel geliştirme (local dev) aşamasında konseptleri Docker argümanlarıyla kanıtlamak yeterli oldu.

## 13. Week 2 Architecture Review
LangGraph kullanılarak RAG ve Tool entegre bir yapay zeka ajanı inşa edildi. Sistemin kararları; model (yönlendirme/cevap üretme)
ve Python tabanlı deterministik kontroller (allowlist, MAX_STEPS, citation validasyonu) arasına dağıtılarak güvenilirlik sınırı (reliability boundary) güçlendirildi.

## 14. Week 2 Evidence
Total unit tests: 50
Total integration tests: 15
Hit@1: 6/6
Hit@3: 6/6
Chunk config: chunk_size=600, overlap=100
Top-k values: 1, 3, 5
Routes: smalltalk, knowledge, tool
MAX_REWRITES: 1
MAX_STEPS: 12

## 15. Known Limitations
1. Retrieval quality policy çok basit
2. Gerçek chunk-size re-ingestion experiment henüz yok
3. Citation validity semantic entailment değildir
4. Small deterministic classifier dil çeşitliliğinde kırılgan
5. LangGraph failure boundary henüz basit

## 16. AI Araçlarını Nasıl Kullandım
Threat model'i önce kendim çıkardım mı?
Evet. Hata yönetimini güçlendirmek için gereken özel hata sınıflarını (ResponseContractError vb.) önce kendim tasarladım.

AI'dan istediğim code review:
Bu yeni sınıfları, halihazırda çalışan agent_loop ve tool_dispatcher dosyalarıma nasıl entegre edeceğimi sordum.

AI'nın önerdiği ama değiştirdiğim/reddettiğim bir öneri:
AI, hata yapısı (paradigma) değiştiği için her iki dosyayı da sıfırdan baştan yazmayı teklif etti. Kesinlikle reddettim.

Neden?
Çalışan ve test edilmiş kodu sıfırdan yazdırmak yeni bug'lara (regression) yol açar. Dosyaları baştan yazdırmak yerine, sadece {"error": ...} dönen kısımları silip yerlerine raise koyarak (nokta atışı refactoring) proje riskini en aza indirdim.

Sistemle nasıl doğruladım?
Değişiklikleri manuel olarak uyguladım ve testlerimi pytest.raises mantığına uyarladım. Terminalde 50 birim testinin kayıpsız geçtiğini görerek bu minimal müdahalenin doğruluğunu kanıtladım.

## 17. Karşılaştığım Bir Hata
Problem:
Day 10'da hata yönetimini güçlendirip tool_dispatcher ve agent_loop için özel hata sınıfları (ResponseContractError, ToolRuntimeError) fırlatmaya başlayınca eski testlerimin hepsi patladı. Çünkü eski testler fonksiyonun geriye {"error": "mesaj"} formatında basit bir sözlük (dictionary) dönmesini bekliyordu.

Failure mı bug mı?
Bu bir bug (yazılımcı kaynaklı uyumsuzluk). Qdrant'ın veya Ollama'nın çökmesi gibi bir "failure" değildi; kodda değiştirdiğim yeni yapıyı (contract) test dosyalarıma yansıtmayı unuttuğum için kendi yazdığım kodun uyumsuzluğuydu.

Nasıl detect ettim?
Terminalde pytest komutunu çalıştırdığımda, tests/test_tool_dispatcher.py ve tests/test_agent.py dosyalarından fırlayan kırmızı AssertionError çıktıları ve yakalanmayan Exception logları sayesinde anında tespit ettim.

Nasıl contain ettim?
Pytest bu kilitlenmeleri test izolatöründe (test suite) yakalayıp süreci "Fail" olarak durdurduğu için, yeni eklediğim mimarinin doğrulanmadan bir sonraki aşamaya (veya canlıya) geçmesini engellemiş (contain etmiş) oldum.

Çözüm:
Testleri yeni mimariye göre baştan düzenledim. Hata döneceğini varsaydığım sözlük kontrollerini sildim; bunun yerine fırlatılan özel hataları yakalamak için pytest.raises(ResponseContractError) metodunu kullandım. Ajan testlerindeki hata mesajı kontrollerini de modern yapıya uygun olarak assert "Tool Error" in state["tool_history"] şeklinde string eşleştirmesine çevirdim.

## 18. Bugünün En Önemli 5 Öğrenimi
1. Modelin ürettiği kararları veya kodları deterministik Python sınırları içine almak güvenilirliğin temelidir.
2. Bir sistemde "bug" ile "failure" farklıdır; dış bağımlılıkların çökmesi olan failure durumları yutulmamalı, aksine detect -> contain -> recover -> observe döngüsüyle yönetilmelidir.
3. Tool çağırma (side effect) gibi işlemler körlemesine retry edilmemelidir, aksi takdirde felaket sonuçlar doğurabilir.
4. `pytest.mock` gibi araçlarla, üretim kodunu bozmadan hata senaryolarını simüle edip sistemin direncini kanıtlamak mümkündür.
5. Docker tek başına bir güvenlik kalesi değildir; yetkileri `--read-only`, `--network none`, `tmpfs` ile sınırlamak ve Firecracker/gVisor gibi yapıların gerekliliğini anlamak sistem güvenliği için şarttır.

## 19. İkinci Haftanın Sonunda Kendimi Nerede Görüyorum?
Kurulan sistemlerin mimari arka planını çok daha net görebilen, bir sonraki adımı öngörebilen ve bütünü düşünerek tasarım kararları alabilen bir noktadayım. Büyük resmi ve teorik altyapıyı zihnimde oturtmuş olsam da, bu tasarımları pratiğe dökme ve uygulama aşamasında henüz kas hafızamı yeterince geliştiremediğimi ve bazen geride kaldığımı fark ediyorum.

## 20. Üçüncü Haftada Öğrenmek İstediğim Konular
1.multi-agent
2.Daha esnek ve bağlamsal olarak duyarlı dinamik chunking/bölme algoritmaları entegre etmek.

