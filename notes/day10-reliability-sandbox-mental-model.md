# Day 10 — Reliability & Sandbox Mental Model

## Failure ile bug farkı
Failure, Qdrant'ın anlık çökmesi gibi sistem çalışırken yaşadığımız beklenen aksaklıklardır; bug ise kodu yazarken tamamen kendi yaptığım mantık veya yazım hatalarıdır.

## Detect → Contain → Recover → Observe
Bu bizim hata yönetim akışımızdır: Hatayı fark eder (detect), etrafa yayılmasını önler (contain), sistemi güvenli bir duruma döndürür (recover) ve ne olduğunu kaydederiz (observe).

## Timeout neden gerekir?
Dış servisler (örneğin Ollama) cevap vermediğinde sistemimizin sonsuza kadar bekleyip kilitlenmesini önleyen zorunlu bir süre sınırıdır.

## Retry ne zaman faydalı?
Veri okuma veya sistemin ayakta olup olmadığını kontrol etme gibi arkada kalıcı bir değişiklik yapmayan işlemlerde, anlık kopmaları atlatmak için işe yarayan bir yöntemdir.

## Retry ne zaman zararlı?
Kargo siparişi oluşturmak veya mail atmak gibi dış dünyada kalıcı etki bırakan işlemlerde tekrar denemek, aynı işlemi yanlışlıkla iki kez yapmamıza sebep olabileceği için risklidir.

## Fallback ile failure'ı gizlemek arasındaki fark
Hatayı gizlemek sorunu çözmez, sadece görünmez yapar fallback ise hatayı açıkça kaydedip kullanıcıya veya sisteme kontrollü ve şeffaf bir "B planı" sunmaktır.

## Model-generated code neden untrusted input?
Modelin ürettiği kodun sistemimde dosya okumayacağı, ağdan veri sızdırmayacağı ,veya makineyi kitlemeyeceği garanti olmadığı için onu dışarıdan gelen güvensiz bir girdi olarak görmek gerekir.

## Container neden tam güvenlik sandbox'ı değildir?
Standart container'lar ana makinenin çekirdeğini (kernel) paylaştıkları için tamamen yalıtılmış sayılmazlar ve tek başlarına kesin bir güvenlik garantisi sunmazlar.

## Network none neyi azaltır?
Container'ın dış dünya ile ağ bağlantısını tamamen kesen bir ayardır; böylece içerideki kodun dışarıya veya internete veri sızdırma riskini ortadan kaldırır.

## Read-only filesystem
Container'ın ana dosya sistemini sadece okunabilir yapan bir kısıtlamadır; içeride çalışan güvensiz kodun kalıcı dosyalar oluşturmasını veya sistemi bozmasını engeller.

## Non-root user
Container içindeki uygulamanın en yetkili kullanıcı (root) olarak çalışmasını engelleyen basit ama etkili bir güvenlik önlemidir.

## Linux capabilities
İşletim sisteminin sunduğu özel yetkilerdir; bunları gereksiz yere açık bırakmak yerine kısarak (drop) çekirdeğe yapılabilecek saldırı yüzeyini küçültürüz.

## seccomp
Uygulamanın işletim sistemi çekirdeğine yapabileceği çağrıları (syscall) sınırlayan ve sadece izin verilen işlemlerin yapılmasına olanak tanıyan bir güvenlik filtresidir.

## CPU / memory / PID limitleri
Çalışan kodun tüm işlemciyi sömürmesini, belleği taşırmasını veya sonsuz işlem (process) açmasını engelleyen, container'a koyduğumuz katı kaynak sınırlarıdır.

## Ephemeral workspace
Koda geçici olarak verdiğimiz, işlem bitince içindeki her şeyin silinip gittiği (örneğin /tmp) kısa ömürlü küçük bir çalışma alanıdır

## Docker socket neden agent'a verilmez?
Bu soket Docker'ın kalbidir; yapay zeka ajanına verirsek ana makinemizde kafasına göre yeni container'lar açıp tüm sistemi ele geçirme yetkisi vermiş oluruz.

## Trusted orchestrator / untrusted workload sınırı
Zaman aşımı gibi kuralları yöneten ana sistemimiz (trusted) ile, içeride ne yapacağı belli olmayan üretilmiş kodun (untrusted) birbirinden kesin bir çizgiyle ayrılmasıdır.

## gVisor mental model
Çalışan kod ile ana bilgisayarın çekirdeği arasına giren, doğrudan teması keserek güvenliği artıran ekstra bir yazılımsal güvenlik katmanıdır.

## Firecracker mental model
microVM/virtualization boundary ile klasik shared-kernel container'a kıyasla daha güçlü bir isolation boundary sağlar.

## Production multi-tenant sandbox neden daha güçlü isolation isteyebilir?
Yüzlerce farklı kullanıcının kodunu aynı ortamda çalıştırdığımız bir yapıda, standart container'ların sızıntı riskleri çok büyük olacağından sanal makine düzeyinde yalıtımlara (gVisor, Firecracker gibi) ihtiyaç duyulur.