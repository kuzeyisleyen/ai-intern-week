# Day 04: Model ve Servis Gözlemlerim (Terminal Çıktılarına Göre)

1. **Servis Kararlılığı:** `docker compose ps` çıktısından Ollama konteynerinin 5 saattir sorunsuz ve sağlıklı bir şekilde çalıştığını doğruladım. Sistem arka planda 11434 portu üzerinden isteklerimi dinlemeye hazır bekliyor.
2. **Küçük Modeller Bile Büyük Boyutlu:** `ollama list` komutunu çalıştırdığımda, görece "küçük" olarak geçen `qwen3:1.7b` modelinin bile 
diskimde 1.4 GB yer kapladığını gördüm. Yerel yapay zeka çalıştırmanın çok net bir depolama maliyeti var.
3. **Volume Kullanımının Önemi:** `docker volume ls` komutuyla `ai-intern-week_ollama_data` isimli alanın aktif olduğunu teyit ettim. Bu yapı sayesinde o 1.4 GB'lık devasa model dosyası Dockerın içinde güvenle saklanıyor konteyneri silip baştan kursam bile modeli tekrar indirmek zorunda kalmıyorum.