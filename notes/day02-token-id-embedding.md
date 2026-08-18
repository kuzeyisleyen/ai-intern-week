## 1. Token integer mıdır?
Token yaptığımız uygulama da deneyimlediğim şekilde String tipindedir.
## 2. Token ID ne işe yarar?
Model metin okuyamadığından dolayı embedding değerini bulmak için ID yi bir indeks gibi kullanır.
## 3. Embedding neden tek sayı değildir?
Kelimelerin anlamı,çoğul tekil olması veya diğer kelimelerle ilşkisi karmaşık olduğundan çok boyutlu anlamsal uzayda konumlandırılabilmesi için tek sayı değildir.
## 4. Token sayısı ile embedding tensor shape'i arasında nasıl ilişki var?
Embedding işleminden sonra ID büyük bir vektöre dönüşür fakat embedding matrisinin ortadaki boyutu cümledeki veya kelimedeki token sayısıyla birebirdir.
## 5. Model ile tokenizer'ın uyumlu olması neden önemlidir?
Herhangi bir uyumsuzluk yaşanmaması için önemlidir şöyle düşünebiliriz yanlış kullanılan tokenizer elma kelimesine atadığı ID modelin hafızasında farklı bir kelimesine denk gelebilir.