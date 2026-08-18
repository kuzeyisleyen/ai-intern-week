


## Token 
Token Tokenizer ın ürettiği metinsel birimdir.Token metinsel ve sembolik bir kavramdır işlenebilmesi için bir sayıya dönüşmesi gerekir.
## Token ID 
Modelin sözlüğündeki her token a benzersiz bir sayı atanır ve sayılar arasında bir ilişki yoktur yani elma niçin armuttan 500 büyük gibi bir şey yoktur.
## Embedding 
Embedding tokenın model tarafından işlenebilen öğrenilmiş matematiksel temsilidir.
## Inference 
Eğitilen modelin bir girdiden çıktı üretmesi işlemidir.Tokenizasyon,Transformer,logit üretimi ve decoding aşamalarını kapsar.
## Deployment 
Modeli insanların veya başka sistemlerin kullanabiliceği çalışan bir sistem haline getirmektir.
## Hallucination 
Modelin doğruymuş gibi sunduğu fakat gerçekte yanlış,temelsiz veya doğrulanamayan çıktılardır.

## Token ID ile embedding arasındaki fark nedir?
Aslında tokenin farklı temsil şekilleridir.Token ID sözlükteki sıra numarası iken embedding tokenin öğrenilmiş sayısal vektörüdür.
Örneğin:
Token -> Ankara
TokenID -> 841
Embedding -> [0.65,-0.71,...]