 ## 1. Bir kelime her zaman tek token mı?
Hayır bi kelime her zaman bir token değil.Kelimenin kökünü veya hecelerini ayırabiliyor.
 ## 2. Büyük/küçük harf sonucu etkileyebiliyor mu?
Token sayısı olarak sonucu etkilemiyor fakat büyük küçük harfe göre token ID değişiyor.
 ## 3. Noktalama tokenization'ı etkiliyor mu?
Noktalama işaretleri kendi başına token ID alıyor.
 ## 4. İngilizce için eğitilmiş bir tokenizer Türkçede farklı davranıyor mu?
Kesinlikle farklı davranıyor kelimleri hecelerine bölüyor ve neredeyse 2 veya 3 katı fazla token harcıyabiliyor.
 ## 5. Token sayısıyla kelime sayısı aynı mı?
Her cümle için aynısını söyleyemeyiz aynı olan cümlelerde kurulabilir fakat genellikle token sayısı kelime sayısından fazla.