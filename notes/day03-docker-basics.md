## image
uygulama ,bağımlılıklar ve çalışma ayarlarını içeren değişmez pakettir.
## container
image ın çalışan bağımsız örneğidir.
## Dockerfile
image ın nasıl hazırlanacağını anlatan metin dosyasıdır.
## docker build
dockerfile ı okuyarak image üretir.
## docker run
hazırlanan imageden yeni bir container oluşturur ve çalıştırır.


Dockerfile
   │  Tarif
   ▼
docker build
   │  Tarifi uygular
   ▼
Image
   │  Hazır kalıp
   ▼
docker run
   │  Kalıptan çalıştırır
   ▼
Container
      Çalışan örnek
    