
## Container'ı kaldırdığımda

docker compose down
docker compose up -d ollama
docker compose exec ollama ollama list
Sırasıyla yaptığım bu işlemlerde containerları sildim ,ollamayı tekrar başlattım ve model içeri de mi olduğunu kontrol ettim.Model named volume içinde kaldı ve yeni ollama container ı başlattığımda aynı volume tekrar bağlandı.

## Model tekrar indirildi mi?

Hayır model silinmedi.

## Named volume neden kaldı?

Bu model dosyasını açıp düzenlemeyeceğimizden dosya yoluna ihtiyacımız yok ondan dolayı named volume kullandık ve kullanma sebebimizde container silindiğinde silinmesin güvenli birşekilde saklanmasını istememizdi.

## Bind mount ile farkı

Temel farkları dosyanın fiziksel olarak durduğu yer ve yönetimdir.