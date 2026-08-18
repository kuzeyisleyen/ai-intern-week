| Prompt | Base model gözlemi | Instruct model gözlemi |
|---|---|---|
| Continuation |Cümle anlamı farklı bir konuya kaymadı fakar robotsu ve sıradan bir cevap sundu |Daha detaycı bir şekilde cümleyi tamamladı |
| English instruction |Doğru ve tutarlı cevaplar vermiş olsa dahi 2 ve 3. maddeleri birebir aynı olarak çıktı verdi | Cevaplar daha kapsamlı ve ayrıntılı şekilde sunuldu fakat 2 madde ile özetledi yalnızca |
| Turkish instruction |Metinsel bir ifade döndürmedi,yalnızca sayı listesi gibi bir çıktı sundu | Her ne kadar metin döndürmüş olsa da mantıklı ve sorunun cevabına uygun cevap veremedi |
```

Ardından cevapla:

1. Hangi model continuation görevinde daha doğal davrandı?
her ne kadar base modelin görevi cümle tamamlamak olsa da instruct modelin daha doğal ve tatmin edici bir cevabı vardı.
2. Hangi model instruction'ı daha iyi takip etti?
instruct model kesinlikle daha iyidi.
3. Davranış farkının muhtemel nedeni nedir?
Parametreleri bir olsa da eğitilme şekilleri farklı olduğunu düşünüyorum.Farklı amaçlara fayda sağlamak.
4. Türkçe performansı hakkında ne gözlemledin?
Türkçe cevap veremedi
5. Yalnızca 3 prompt ile “bu model daha iyi” denebilir mi?
Kesinlikle denemez daha çok test edilmeli ve kullanıcağımız alana göre iyi oluşu göreceli olabilir.
