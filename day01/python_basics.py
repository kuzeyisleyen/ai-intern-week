import string
#List
from email.mime import text


fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
print(fruits.index("cherry"))
fruits.pop()
print(fruits)
#Dict
bos_sozluk = {}
bos_sozluk2 = dict()

ogrenci ={"ad" : "Ahmet","soyad" :"Yılmaz","yas" : 20,"bolum" : "BP"}

#VERİ ÇEKME
print (ogrenci["ad"])
print (ogrenci["soyad"])
print (ogrenci["yas"])
print (ogrenci["bolum"])

ogrenci2 ={"ad" : "Ahmet","soyad" :"Yılmaz","yas" : 20,"bolum" : "BP","dersler" : [207,205,281]}
print (ogrenci2["dersler"])
print (ogrenci2["dersler"][1])

dersler = ogrenci2["dersler"]
print (dersler[1])

print(ogrenci2.get("ad"))
print (ogrenci2.get("telefon","kayıtlı değil"))

#UPDATE
ogrenci2["ad"]="Kuzey"
print(ogrenci2)

#MULTİ UPDATE
ogrenci2.update({"ad" : "İpek" , "bolum" : "Mimarlık"})
print(ogrenci2)


#DELETE
ogrenci2.pop("yas")
print(ogrenci2)

ogrenci2.popitem() #sondaki veriyi siler
print(ogrenci2)

del ogrenci2["soyad"] 
print(ogrenci2)

ogrenci2.clear() #tüm veriler silinir
print(ogrenci2)

#SORGULAMA VE LİSTELEME
ogrenci3 ={"ad" : "Ahmet","soyad" :"Yılmaz","yas" : 20,"bolum" : "BP","dersler" : [207,205,281]}

print(ogrenci3.keys())
print(ogrenci3.values())
print(ogrenci3.items())

if "ad" in ogrenci3:
 print ("Bu key kullanılmaktadır")

#List Comprehension
#Ornek1
a =  list(range(51))
print(a)
bolunenler = [eleman for eleman in a if eleman %5 == 0]
print(bolunenler)
#Ornek2
b = list(range(16))
print (b)
tekCift = ["Çift" if eleman %2 == 0 else "Tek" for eleman in b]
print(tekCift)

#Dict Comprehension
#Ornek1
degerler = {i : i**3 for i in range(1,8)}
print(degerler)

#TEXT ANALYZE

#"character_count": 0,
#"word_count": 0,
#"unique_word_count": 0,
#"longest_word": "",
#"top_words": []

def analyze_text_basic(text : str) -> dict:

    output = {
       "character count": 0,
       "word count": 0,
       "unique word count": 0,
       "longest word": "",
       "top words": []
    }
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation)) #Noktalama işaretlerini kaldırmak için kullandım
    output["character count"] = len(text)
    output["word count"] = len(text.split())
    output["unique word count"] = len(set(text.split()))
    output["longest word"] = max(text.split(), key=len)
    wordsCount = {}
    for word in text.split():
        if word in wordsCount:
            wordsCount[word] += 1
        else:
            wordsCount[word] = 1
    output["top words"] = sorted(wordsCount.items(), key=lambda x: x[1], reverse=True)[:5]
   
    return output

print(analyze_text_basic("Yapay zeka yazılım geliştirme sürecini hızlandırabilir."))
print(analyze_text_basic("Yapay yapay zeka , yazılım geliştirme sürecini hızlandırabilir."))

    
