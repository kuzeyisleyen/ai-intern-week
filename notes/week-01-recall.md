User
↓
Docker 
↓
Ollama
↓
Model
↓
Response
```

Buraya Docker, app, Ollama, HTTP gibi bileşenleri nerede konumlandırdığını düşün.

### 2. Function calling

```text
User
↓
LLM
↓
Tool Call
↓
Python
↓
Tool Result
↓
LLM
```

Burada modelin neyi yaptığını, Python uygulamasının neyi yaptığını ayırmaya çalış.

### 3. Agent loop

```text
User
↓
State
↓
Model
↓
Tool Dispatcher / Validation
↓
State Updated
↓
Termination

##  Burada özellikle “tek bir tool call” ile “agent loop” arasındaki farkı düşün.

agent loop, tek seferlik tool çağrısını, state (durum) ve termination (bitiş) barındıran tekrar eden bir orkestrasyon akışına çevirir.

### Token, ID ve embedding

Şu akışı tamamla:

```text
text
→ Token
→ Token ID
→ vector representation (embedding)

Token ID ile embedding neden aynı şey değildir?
Token ıd tokenların modelin sözlüğündeki sıra numarasıdır,embedding ise bu id lerin sayısal vektörlere dönüştürülmesi işlemidir.

Base model:
Modelin sadece bir sonraki tokenı tahmin etmesi için eğitilmiş model

Instruct model:
Modelin soru-cevap ve talimatları yerine getirebilmesi için eğitilmiş modeldir.

Model dosyası container silinse de kalsın.
named volume

ve:

JSON output host klasöründe doğrudan görülsün.
bind mount

Hangisinde named volume, hangisinde bind mount kullanmak daha mantıklı?



`localhost` ve Compose service name

Şu soruyu kendi cümlenle açıkla:

> `app` container içinden Ollama'ya neden `http://ollama:11434` ile gidiyoruz da `http://localhost:11434` ile gitmiyoruz?

app container ı içinden local host isteği atarsak sadece kendi containerına bakar ama ollama farklı containerde çalışıyor o yüzden onu göremez bu yüzden docker compose ortamında ise containerlar birbirini aynı ağ üzerinden birbirlerini servis adlarıyla tanırlar.biz ollama ile istek attığımzıda dns adından ip adresini bulur ve bizi doğru yere götürür.

### Structured output ve function calling

Şunu tamamla:

```text
Structured output:
Modelden veriyi rastgele bir metin olarak değil önceden belirlediğimiz formata göre beklemektir.

Function calling:
Modelden sadece veriyi değil,sistemimizde çalışan bir kodu veya aracı çalıştırabilmemiz için bir aksiyon isteği üretmesini beklemektir.


1.Modele hangi tool'ların mevcut olduğu anlatılır.
2.Model hangi tool'u kullanmak istediğini söyler.
3.Python uygulaması gerçek fonksiyonu çalıştırır.