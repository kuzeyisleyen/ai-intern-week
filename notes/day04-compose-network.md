## 1. `localhost` neden Ollama'yı göstermiyor?
Local host kendi bilgisayarında çalıştığından app container içinden localhost a yapılan istek ollama ya gitmez.
## 2. `ollama` hostname'i nereden geliyor?
compose.yaml dosyasında services: ollama  kısmından geliyor.Buna farklı bir isimde verebilirdim.
## 3. Container IP'sini hard-code etmek neden kötü fikir?
çünkü servisin ip si değişebilir ve gönderdiğimiz bir istek eski ip adresine gidip ulaşamayabilir fakat service ismi verdiğimizde gidiceği adresi daime bulur.
## 4. Ollama portunu host'a publish etmeden app erişebilir mi?
Aynı docker compose ağı içinde bulunan app ve ollama containerları birbirlerinin protlarına erişebilirler.