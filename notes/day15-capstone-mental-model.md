# Day 15 — Capstone Mental Model

# Feature ile System farkı
Bir feature (özellik) sadece iyi gün senaryosunda çalışan kod parçasıyken; bir sistem, hataları izole eden, gözlemlenebilirlik (observability) sunan ve uç durumlarda ayakta kalan mimaridir. Bu projede kodu değil, bu sistemi inşa etmeye çalıştım.

# Contract Evidence
Bileşenler arası sözleşmelerin bozulmadığını, hızlı ve deterministik birim (unit) testlerimle kanıtladım. Dış sistemler devrede olmadan mimarinin mantık bütünlüğünü bu sayede güvenceye alıyorum.

# Quality Evidence
RAG ve arama (retrieval) süreçlerimin kalitesini, Hit@k ve MRR gibi metriklerle ölçerek belgelendirdim. Capstone senaryolarındaki 8/8 başarı oranım, kurduğum yapay zeka yönlendirme mimarisinin niyet anlama kalitesinin en net kanıtıdır.

# Runtime Evidence
Sistemin çalışma anındaki (runtime) sağlığını ve performansını; ağır bir OpenTelemetry stack'i kurmak yerine, OTel "Span" mental modelinden esinlenerek oluşturduğum gizlilik odaklı (privacy-safe) yerel JSON trace'leri ile anlık olarak takip edebiliyorum.

# Final Router Policy
Nihai yönlendirme kararı olarak, basit kural tabanlı bir hızlı yol (deterministic fastpath) ve ardından niyet tabanlı semantik yapay zeka (LLM router) kullanan "İki Aşamalı" (Two-Stage) politikayı benimsedim.

# Neden bu router policy'yi seçtim?
Gerçekleştirdiğim A/B testleri ve topladığım metrikler (evidence-driven), bu politikanın hem gecikmeyi (latency) sıfıra indirdiğini hem de karmaşık niyetleri yüksek doğrulukla çözdüğünü kanıtladığı için bu mimariyi seçtim.

# LLM route neden authorization değildir?
Yapay zeka sadece kullanıcının niyetini tahmin eder ve tavsiyede bulunur (intent routing). Gerçek yetkilendirmeyi ve kritik araçlara erişim iznini, kendi yazdığım deterministik beyaz liste (Tool Allowlist) belirler.

# Model / Provider Boundary
Yapay zeka modeli ile uygulamanın iş mantığını birbirine sıkı sıkıya bağlamaktan (hardcoding) kaçındım. Dış kaynakları ve araçları sisteme Model Context Protocol (MCP) adaptörleriyle entegre ederek modeli değiştirilebilir kıldım.

# CI'da ne otomatik?
Dış ağlara veya yapay zeka çıkarımına ihtiyaç duymayan, saniyeler içinde biten ve sözleşme bütünlüğünü doğrulayan deterministik birim ve entegrasyon testlerim (GitHub Actions gibi) CI sunucularında tamamen otomatiktir.

# CI'da ne otomatik değil?
Altyapı maliyeti yaratan ve doğası gereği olasılıksal (probabilistik) olan uçtan uca (E2E) LLM ve RAG değerlendirme testlerim bulutta otomatik değildir. Bunları yerel makinemde (Local CI) koşup sonuçlarını JSON statik kanıt dosyasına mühürlüyorum.

# Deterministic vs nondeterministic evaluation
Deterministik değerlendirmede if/else bloklarının ve sözleşmelerin kesin sonuçlarını test ederken; non-deterministik değerlendirmede yapay zekanın "niyet karmaşası" gibi olasılıksal çıktılarını Golden Dataset ile kalite standartlarına vuruyorum.

# Reproducibility
Geliştirdiğim sistemin sadece benim makinemde değil, her yerde aynı şekilde çalışabilmesi için tüm mimariyi Docker konteynerleriyle izole ettim ve altyapı bağımlılıklarını ortadan kaldırdım.

# Version pinning neden önemli?
LangGraph ve MCP gibi modern yapay zeka kütüphaneleri çok hızlı güncellendiğinden, sistemin gelecekteki bir sözleşme (contract) değişikliği yüzünden çökmesini engellemek adına kütüphane sürümlerini sıkıca sabitledim.

# Failure containment
Sistemdeki bir bileşenin (örneğin Ollama veya Qdrant) çökmesinin tüm uygulamayı yıkmasını engellemek için, hataları kendi sınırları içinde izole eden ve güvenli bir alternatif yola (graceful degradation) sapan güvenlik ağları kurdum.

# Trust boundaries
Yapay zekanın halüsinasyon görebileceği gerçeğini en başından kabul ettim. Bu yüzden modelin ürettiği kararlar ile sistemin çalıştırdığı kod arasına deterministik doğrulama ve insan onayı (HITL) gibi kesin güven sınırları (trust boundaries) çizdim.

# Checkpoint neden business DB / backup değildir?
Kurduğum SQLite Checkpointer mimarisi, kalıcı bir veri yedeği (backup) veya iş veritabanı değildir; sadece kesintiye uğrayan veya insan onayı bekleyen LangGraph iş akışlarının anlık durum (state) dökümünü tutan geçici bir hafızadır.

# Idempotency demo'sunun sınırı
İnsan onaylı süreçlerde duraklatılan işlemleri aynı thread_id üzerinden yanlışlıkla birden fazla kez tetiklesek bile, durum hafızası sayesinde aynı işlemin (side effect) mükerrer gerçekleşmeyeceğini ve sistemin kendini koruyacağını kanıtladım.

# Known limitations
Sistemin en büyük kısıtlaması, hızlı yerel geliştirme için seçtiğim küçük modelin (qwen3:1.7b) çok katmanlı senaryolarda niyet karmaşası yaşamasıdır; ancak bu limitasyon, mimarideki hata toleransımı ve geri dönüş yollarımı test etmek için harika bir fırsat oldu.

# Portfolio-ready repository ne demek?
Kodun sadece günü kurtarması değil; neden yazıldığının mimari kararlarla dokümante edildiği, test metrikleriyle kanıtlandığı, CI stratejisinin belirlendiği ve başka bir mühendisin tek komutla hatasız ayağa kaldırabileceği olgunluğa (production-ready) ulaşmasıdır.

# Üç haftada kurduğum sistemin hikâyesi
İlk hafta saf Python ile temelleri atıp, ikinci hafta LangGraph ve vektör veritabanlarıyla orkestrasyonu kurdum. Üçüncü haftanın sonunda ise; MCP, izlenebilirlik (observability) ve üretim kalitesindeki CI/CD pratikleriyle donatılmış, kriz anlarında çökmeyen uçtan uca, kalıcı ve otonom bir AI mimarisi inşa ettim.