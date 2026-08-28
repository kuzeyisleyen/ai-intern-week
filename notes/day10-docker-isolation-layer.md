Non-root user
Uygulamayı container içinde root olmayan, sınırlı yetkili bir kullanıcıyla çalıştırır.

--network none
Container’ın dış ağ bağlantısını kapatarak network üzerinden veri sızdırma riskini azaltır.

--read-only
Container’ın root filesystem’ine yazılmasını engeller.

--tmpfs /tmp
Uygulamaya yalnızca bellekte tutulan, geçici ve sınırlandırılabilir bir yazma alanı verir.

--memory
Container’ın kullanabileceği maksimum belleği sınırlandırır.

--cpus
Container’ın tüketebileceği CPU kapasitesini sınırlandırır.

--pids-limit
Container’ın oluşturabileceği process sayısını sınırlayarak fork/PID abuse riskini azaltır.

--cap-drop=ALL
Process’in ihtiyaç duymadığı Linux kernel yetkilerini kaldırır.

no-new-privileges
Process’in çalışma sırasında yeni veya daha yüksek yetki kazanmasını engellemeye yardımcı olur.

Default seccomp	
Riskli sistem çağrılarını filtreleyerek host kernel saldırı yüzeyini azaltır.

--rm
Container durduktan sonra geçici container filesystem’ini otomatik olarak kaldırır.

No secrets
Untrusted workload’a API key, token veya parola verilmesini engeller.

No host bind mount
Host dosyalarının untrusted workload tarafından okunmasını veya değiştirilmesini önler.

No Docker socket
Container’ın host Docker daemon’ını kontrol etmesini engeller.

No privileged mode
Container’ın host seviyesine yakın geniş yetkiler elde etmesini önler.

Rootless Docker
Docker daemon ve container’ları root olmayan kullanıcı bağlamında çalıştırarak olası açığın etkisini azaltır.