| Alan | SmolLM2-360M | SmolLM2-360M-Instruct |
|---|---|---|
| Base / Instruct |Base | Instruct|
| Parametre ölçeği | 360M  | 360M  |
| License |Apache 2.0 |Apache 2.0 |
| Beklenen kullanım |Metin Tamamlama |Soru cevaplama ,ChatBot |
| Input formatı |Ham Metin |Chat Template |
| Chat template |yok |[{"role": "user", "content": "..."}] |
| Güçlü olduğu alan |Az yer kaplıyıp hızlı çalışması |talimatları takip edebilmesi ,diyalog kurabbilmesi |
| Limitasyon |cevap vermek yerine sorunun devamını getirmek |sınırlı parametre halisunasyon riski |

## Aynı model ailesindeki base ve instruct sürüm neden farklı davranabilir?
Parametreleri aynı olsa bile eğitim hedefleri farklıdır.Birisi kelimenin devamını getirmek için eğitilmişken diğeri soruya en faydalı cevabı üretip dialog sürdürmeye programlanmıştır.