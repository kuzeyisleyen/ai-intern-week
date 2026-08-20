# Day 4 — Tool Use Literature Note

## Kaynak bilgileri

Title: Toolformer: Language Models Can Teach Themselves to Use Tools
Authors: Timo Schick ve diğerleri 
Year: 2023
URL: https://arxiv.org/abs/2302.04761

## Toolformer hangi problemi çözmeye çalışıyor?

Büyük dil modelleri çok iyi metin tamamlayabiliyor veya sohbet sürdürebiliyor fakat temel matematik ,bilgi arama gibi basit işlemlerde zorlanıyorlar.

## Temel yaklaşım

Bu basit işlemleride de yapabilmesi için daha fazla veriyle eğitilip ağırlığını büyütmektense modeller basit apiler aracılığıyla dış araçları kendi kendine kullanmayı öğrenebilirler.

## External tool neden kullanılıyor?

Büyük dil modelleri saatin kaç olduğunu,bir metnin çevirisini veya matematik hesaplamalarını yaparken zorlanıyor bu tarz işlemler için takvim ,hesap makinesi veya çeviri motoru gibi dış araçları(external tools) kullanıyor.

## Sunulan kanıtlar

Okuduğum makalede yazarlar bu modeli kendisinden devasa büyüklükteki modelle kıyaslıyorlar.

## Sınırlılıklar

Model bir apiyi çağırırken maliyet hesaplaması yapmıyor, modelin o api bağlantısını çekme kararını kullanıcının verdiği prompta duyarlı olduğunu sçylüyor ve api çağrıları birbirinden bağımsız çalışıyor bu yüzden bir aracın sonucunu diğer aracın girdisi olarak kullanan zincirleme tool kullanımını öğrenemiyor.

## Ollama function calling ile bağlantısı

Toolformer ile Ollama function calling arasındaki bağlantı, modelin hangi tool’u hangi argümanlarla kullanacağına karar vermesi ve tool sonucunu sonraki cevabında kullanmasıdır.

## Aynı olmayan noktalar

Toolformer modele tool kullanma davranışının nasıl öğretileceğine ilişkin bir eğitim yöntemidir.
Eğitilmiş Toolformer inference sırasında tool çağrısı üretir ve tool sonuçlarını kullanır.
Ollama function calling, zaten tool-use yeteneği bulunan bir modelle uygulamanın çalışma zamanında nasıl haberleşeceğini tanımlayan bir runtime api arayüzüdür.

## Anlamadığım terimler

Zero-shot
Self-supervised
Bootstrapping

## Kendi üç cümlelik özetim

Modelin büyütülerek tamamen ortadan kaldırılamayan matematik,zaman algısı ,güncel bilgi eksikliği ve halisünasyon gibi sorunları vardı.Toolformer bu sorunu modelin kendi yapamadığı işlemleri bu işlemlerde uzmanlaşmış apilere bırakıyor.Bugün yapıcağım uygulamada modele json şeması vererek bu görev için bir araç çağırma isteği alarak bunu deneyimleyeceğim.