---
day: 13
date: 2026-09-03
status: completed
langgraph: 1.2.11
checkpointer: sqlite
checkpoint_package: 3.1.1
unit_tests_passed: 65
integration_tests_passed: 26
---

# Gün 13 — Durable Workflow + Human-in-the-Loop

## 1. Day 12 Kapanışı

MCP is_error:
Adapter içerisine response.is_error kontrolü eklendi

Resource read integration:
Dosya okuma işlemlerinde tüm metne bağlanmak yerine belirli bir başlığın kontrol edildiği entegrasyon testi eklendi.

Day 11 IDF integration:
Entegrasyon testindeki konfigürasyon, üretim ortamıyla eşleşecek şekilde Modifier.IDF kullanılarak düzeltildi.

MCP mental-model wording:
MCP'nin izole bir arka plan servisi olmadığı, ayrı sürecin bir güvenlik izolasyonu veya sandbox garantisi vermediği notlara yansıtıldı.

Raw query logging:
Sistemin ürettiği doğrudan sorgu logu kaldırılarak yerine güvenli loglama (redact) yapıldı.

README:
Test komutlarında gerçek modül isimleri kullanıldı ve hafta durumu "Week 3 devam ediyor" şeklinde güncellendi.

Day 12 report Overhead:
MCP kullanımıyla per-call stdio spawn + model initialization latency yaratıyor

## 2. Persistence Mental Model

Process memory:
Program çalıştığı sürece hafızada kalan ve süreç (process) kapanınca (crash) tamamen kaybolan geçici veridir

Persistent state:
Sürecin çalışma durumunu, veritabanı gibi kalıcı bir alana yazarak program yeniden başlatıldığında kaldığı yerden devam etmesini sağlayan yapıdır.

## 3. Checkpointer vs Store

Checkpointer:
Belirli bir iş parçacığının (thread) grafikte hangi adımda kaldığını ve o anki durumu kaydeder.

Store:
Farklı iş parçacıkları arasında paylaşılabilecek, kullanıcı tercihleri gibi uzun vadeli verileri saklar.

Bugün neden yalnız checkpointer kullandım?
Bugünkü amaç sadece sürecin kaldığı yerden yeniden başlatılabilmesidir.

## 4. SQLite Checkpointer

DB path:
`output/day13/checkpoints.sqlite`

Neden SQLite?
Durum yönetimini kalıcı, görünür ve yönetimi basit tek bir yerel dosya üzerinde kolayca test edebilmek için.

Production limitation:
Veritabanı dosyası bozulabilir, bu yüzden tek başına bir yedekleme çözümü değildir.

Serialization/security note:
Veritabanı objeleri veya ağ istemcileri (client) graf durumuna (state) kaydedilmemeli, sadece seri hale getirilebilir basit veriler kullanılmalıdır.

## 5. thread_id

Nasıl oluşturuyorum?
Komut satırından `--thread-id` parametresi ile (örneğin: `demo-009`) veriyoruz

Aynı thread:
Zaten var olan bir id ile başlatıldığında eski kaydedilmiş işleme erişilir ve süreç oradan devam eder.

Farklı thread:
Eski kayıtlardan bağımsız, tamamen farklı ve yeni bir iş akışı oluşturulur.

## 6. Gerçek Restart Experiment

İlk process command:
`docker compose run --rm app python -m day13.hitl_cli start --thread-id demo-009 --action publish_report`.

Interrupt öncesi state:
Kayıt dosyasında `status: "interrupted"` olarak güncellenir.

Process kapandı mı?
Evet, süreç duraklatıldıktan (interrupt) sonra komut sonlanır ve process kapanır.

İkinci process command:
docker compose run --rm app python -m day13.hitl_cli resume --thread-id demo-009 --decision approve

Aynı thread ile resume sonucu:
Duraklamış olan işlem başarılı bir şekilde `resumed: true` durumuna geçerek tamamlanır (`status: "completed"`).

## 7. Human-in-the-Loop

Hangi action approval istiyor?
`publish_report`

Policy nerede?
`day13.approval_policy` içindeki `ACTION_POLICIES` listesinde tanımlanmıştır.

Model bu policy'yi bypass edebilir mi?
Hayır, model güvenli olduğunu belirtse bile, süreç kesin bir kuralla onaya zorlanır.

## 8. Interrupt Payload
[demo-010] Güncel Durum:
{'request': 'start_demo', 'action_id': 'act-123', 'action_type': 'publish_report', 'status': 'prepared', 'node_trace': ['prepare']}
Next Node: ('approval',)

## 9. Approve Experiment

Decision:
`approve`

Terminal state:
`status: "completed"`

Side effect:
`output/day13/approved-actions.jsonl` log dosyasına {"action_id": "act-123", "action": "publish_report", "status": "executed"} oalrak yazılır


## 10. Reject Experiment

Decision:
`reject`

Terminal state:
`status: "completed"` olarak trace loglarına yansıdı

Side effect count:
Sıfır; onay verilmediği için dosyaya herhangi bir side effect yazılmadı.

## 11. Idempotency

action_id:
Kod içinde (prepare_node) eğitim amaçlı sabitlendiği için sürekli `act-123` değeri kullanıldı

İkinci execution sonucu:
`demo-009` numaralı işlem `act-123` için onay alıp işlemi tamamladığından, `demo-010` numaralı işlem `reject` yerine `approve` kararı alsaydı bile `execute_once` fonksiyonu `already_executed` döndürerek ikinci çalışmayı engelleyecekti

Business effect kaç kez oldu?
Farklı parçacıkları aynı aksiyon kimliği ile sisteme girmiş olsa da, koruma mekanizması sayesinde yan etki sadece 1 kez gerçekleşti.

## 12. Failure Experiments

Wrong thread:
Bir akış belirli bir kimlikle (`fail-001`) başlatıldıktan sonra farklı bir kimlikle (`fail-002`) devam ettirilmeye çalışıldığında, sistem eşleşen bir duraklatma kaydı bulamaz ve işlemi devralıp çalıştırmadı.

Invalid decision:
Sisteme geçerli seçenekler dışında bir argüman (`--decision maybe`) gönderildiğinde, komut satırı arayüzü doğrulama hatası fırlatarak geçersiz girdiyi reddeder ve akışın çalışmasını anında engeller.

Duplicate action:
Onaylanan ve başarıyla yürütülen akışlar, kayıt dosyasına `action_id` değeri ile birlikte yazılır. Aynı ID ile yeni bir işlem başlatıldığında, koruma mekanizması bu kaydı bularak yan etkinin (dosyaya tekrar yazmanın) ikinci kez gerçekleşmesini önler.

## 13. Trace

thread_id:
`demo-009` (Approve testi için) ve `demo-010` (Reject testi için)

action_id:
Her iki testte de `act-123`

interrupt_reason:
`publish_report` eyleminin politika gereği insan onayı gerektirmesi (loglara `interrupted` statüsü olarak yansıdı).

decision:
`approve` (demo-009) ve `reject` (demo-010)

terminal_status:
Her iki karar sonrasında da süreç başarılı bir şekilde akışını bitirip `completed` statüsünü aldı.

## 14. Tests

Unit:
3
Integration:
4

## 15. AI Araçlarını Nasıl Kullandım?

State/approval policy'yi önce kendim tasarladım mı?:
Evet. İş akışının duraklama noktalarını, durum şemasını ve mükerrer kayıtları önleyen (idempotency) kontrol mekanizmasını yapay zekaya yazdırmadan önce kendim kurguladım.

AI'dan hangi review'u istedim?:
Kurduğum grafiği ve `execute_once` fonksiyonumu yapay zekaya vererek, "Bu yapıda idempotency kuralını ihlal edecek veya aynı yan etkinin iki kez çalışmasına sebep olacak bir mantık hatası var mı?" diye sordum.

AI'nın önerdiği ama değiştirdiğim/reddettiğim öneri:
Yapay zeka kodumu incelerken `prepare_node` içinde `action_id` değerini `"act-123"` olarak sabit bıraktığımı fark etti. Gerçek dünya standartlarına (production) uyması için bu kısmı `uuid.uuid4()` kullanarak her işlemde dinamik ve benzersiz bir ID üretecek şekilde değiştirmemi önerdi. Bu öneriyi reddettim.

Neden?:
Çünkü bugünkü laboratuvar çalışmasının ana hedeflerinden biri sistemin hatalara karşı tepkisini ölçmekti. Eğer ID her seferinde dinamik üretilseydi, aynı işlemin ikinci kez çağrıldığında sistemin mükerrer kaydı nasıl engellediğini (`already_executed` durumunu) test etmem çok zorlaşırdı. Idempotency mekanizmasının gerçekten çalıştığını kanıtlayabilmek (Duplicate action senaryosu) için ID değerini bilinçli olarak `"act-123"` şeklinde sabit bıraktım.

## 16. Bugünün En Önemli 5 Öğrenimi

1. Bellekte tutulan süreçler (Process memory) program kapandığında kaybolur, ancak kalıcı durum (Persistent state) kaydedildiği dosyadan (SQLite checkpointer) yeniden yüklenerek süreci kaldığı yerden devam ettirebilir.
2. `interrupt()` fonksiyonu iş akışını duraklatır ve ancak `Command(resume=...)` ile geçerli bir karar iletildiğinde, duraklatılan node'u en baştan çalıştırarak süreci sürdürür.
3. İş akışları tekrar başlatılabildiğinden (idempotency prensibi), işlemlerde yan etkilerin (side effect) mükerrer gerçekleşmemesi için, yan etkinin olduğu düğümler daima `interrupt` sonrasında ayrı ve özel id'lerle çalıştırılmalıdır.
4. Yapay Zeka modeli risk analizi yapsa da kritik kararlar, insan onayına (Human-in-the-Loop) girmesi için kesin uygulama politikalarıyla sınırlandırılmalıdır.
5. Aynı iş akışının, işlem kapandıktan sonra dahi çalışabilmesi için kullanılan 'Checkpointer', aynı uygulamanın genel, uzun vadeli kullanıcı verilerini paylaştığı sistem olan 'Store' yapısından farklıdır.

## 17. Cuma — Evaluation / Semantic Router Hakkında Sorularım

1. Sistemin performansını değerlendirmeye başlarken şu anki mevcut durumumuzu tam olarak nasıl puanlaycaz?
2. Yaptığımız değişikliklerin sistemi gerçekten iyileştirdiğini kanıtlamak için doğruluk oranı (accuracy) dışında hangi metrikleri takip etmeliyiz?
3. Kullanıcı sistemde bulunmayan bir şey sorduğunda modelin yanlış bir araç seçmesini nasıl engelleyebiliriz?
```
