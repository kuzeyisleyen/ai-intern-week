---
day: 11
date: 2026-08-31
status: completed
dense_model: embeddinggemma
sparse_model: Qdrant/bm25
fusion: rrf
eval_cases: 20
unit_tests_passed: 6
integration_tests_passed: 2
---

# Gün 11 — Retrieval Quality Engineering

## 1. Week 2 Kapanışı

README Day 10 command:
Uygun hale getirildi.

README native-first wording:
Framework kullanıldığı eklendi.

Security wording:
Kesin yargı değiştirildi.

Week 3 üçüncü soru:
Eksik soru eklendi.

Baseline unit tests:
51

Baseline integration tests:
15

## 2. Technical Debt

Bugün çözmediğim ama görünür tuttuğum şeyler:
- Gerçek chunk-size re-ingestion experiment henüz yok.
- Citation validity semantic entailment (grounding) değildir.
- Small deterministic classifier dil çeşitliliğinde kırılgan.
- LangGraph failure boundary henüz basit.
- Python 3.10 lifecycle / upgrade planı eksik.
- ollama:latest image version pinning yapılmadı.
- CI/CD workflow yok.

## 3. Evaluation Dataset

Toplam case:
20

### Query Type Dağılımı

semantic:
6
exact_identifier:
4
command_or_code:
3
mixed:
4
unanswerable:
3

Her type neden var?
Genel başarı skorlarının arkasına saklanan sistem zafiyetlerini kategorik olarak tespit edebilmek ve arama motorlarının zayıf taraflarını izole etmek için var.

## 4. Metric Mental Model

Hit@1:
Sistemin getirdiği ilk 1. sıradaki dokümanın, kesin olarak beklenen doğru kaynak olup olmadığını ölçen en katı başarı metriğidir.

Hit@3:
Beklenen doğru dokümanın, sistemin aday gösterdiği ilk 3 sıradaki listeye girme potansiyelidir.

MRR:
Doğru dokümanın bulunduğu sıraya göre ceza keserek ortalama kaliteyi ölçer. 1. sıra ile 2. sıra veya daha alt sıralar arasındaki kalite farkını metriklere yansıtan en hassas araçtır.

Unanswerable policy:
Cevaplanamaz sorular sıralama metriklerine (Hit@k, MRR) dahil edilmez, kod seviyesinde "excluded from ranking metrics" olarak filtrelenerek sadece sistemin bunları nasıl işlediği test edilir.

## 5. Dense Baseline

Collection:
rag_chunks_hybrid

Embedding model:
embeddinggemma

Chunk config:
chunk_size: 600, overlap: 100

Hit@1:
0.8824

Hit@3:
1.0

MRR:
0.9314

## 6. Dense Failure Patternleri

### Failure 1
`command_or_code` tipindeki `down -v` (q15) sorgusunda Dense model, yeterli cümle bağlamı (semantic context) bulamadığı için "down" kelimesini genel konteyner 
konseptleriyle eşleştirmiş ve asıl beklenen `compose.md` dosyası yerine `docker.md` dosyasını 1. sıraya koyarak hedefi 3. sıraya itmiştir


### Failure 2
`exact_identifier` tipindeki `Cosine similarity` (q12) sorgusunda Dense model, beklenen `vector-database.md` dosyasını 2. sıraya iterek `embeddings.md` belgesini 
zirveye yerleştirmiştir[cite: 9]. Matematiksel olarak cosine similarity, embedding kavramıyla o kadar güçlü bir anlamsal bağa sahiptir ki, model bu çekim kuvvetine
 kapılarak kelimenin asıl geçtiği dökümanı kaçırmıştır

### Failure 3
Yok

## 7. Lexical / Sparse

Sparse model:
Qdrant/bm25

Collection design:
Hybrid arama için Dense vektörlere ek olarak Sparse (BM25) vektörlerin de aynı koleksiyonda (rag_chunks_hybrid) indekslenmesi.

Neden IDF modifier?
Qdrant'ın BM25 rehberiyle doğrulanarak, kelime frekansı tabanlı aramalarda kelimenin corpus içindeki nadirliğine ağırlık vermek için kullanıldı.

Hit@1:
0.5882

Hit@3:
0.7059

MRR:
0.6373

## 8. Hybrid

Fusion:
RRF

Prefetch limit:
5

Hit@1:
0.8824

Hit@3:
1.0

MRR:
0.9314

## 9. Query-Type Karşılaştırması

| Query Type | Dense | Lexical | Hybrid |
|---|---|---|---|
| semantic |Hit@1: 1.0, MRR: 1.0 |Hit@1: 0.6667, MRR: 0.8056 |Hit@1: 1.0, MRR: 1.0 |
| exact_identifier |Hit@1: 0.75, MRR: 0.875 |Hit@1: 0.25, MRR: 0.25 |Hit@1: 0.75, MRR: 0.875 |
| command_or_code |Hit@1: 0.6667, MRR: 0.7778| Hit@1: 0.3333, MRR: 0.3333| Hit@1: 0.6667, MRR: 0.7778|
| mixed |Hit@1: 1.0, MRR: 1.0|Hit@1: 1.0, MRR: 1.0 | Hit@1: 1.0, MRR: 1.0|

## 10. Üç Failure Analysis

### A — Dense yanlış / lexical doğru
Query: down -v (q15) ve Cosine similarity (q12)

### B — Lexical yanlış / dense doğru
Query: MAX_REWRITES (q11)

### C — Hybrid kötüleştirdi veya değiştirmedi
Query: down -v (q15)
Query Type: command_or_code
Expected Source: compose.md
Dense Rank: 3
Lexical Rank: Bulunamadı
Hybrid Rank: 3 (Değiştirmedi)
Benim hipotezim: Hybrid (RRF) harmanlaması iki modelin güçlerini birleştirmeyi amaçlar. Ancak down -v komutunda Lexical model belgeyi hiçbir şekilde bulamadığı için RRF algoritmasına bir sıralama katkısı verememiştir. Lexical'den destek gelmeyince Hybrid sistem yalnızca Dense modelin ürettiği hatalı sıralamaya (Ranking Failure) bağımlı kalarak doğru belgeyi 3. sırada bırakmış ve durumu düzeltememiştir.

## 11. Bugün Hangi Knob'u Özellikle Değiştirmedim?

Reranker:
Kullanılmadı

Query rewrite:
Kullanılmadı

Chunk size:
Değiştirilmedi; `chunk_size=600` ve `overlap=100` olarak bırakıldı.

Neden?
Bugün amaç yeni bir özellik eklemek değil, sistemin hangi aşamada (retrieval vs ranking) başarısız olduğunu ölçmek ve evaluation dataset kullanarak kararlar almaktı.

## 12. Output

output/day11-retrieval-benchmark.json
output/day11-retrieval-benchmark_lexical.json
output/day11-retrieval-benchmark_hybrid.json
output/day11-retrieval-benchmark_dense.json

Önemli config:

`dataset_size`: 20
`dense_model`: embeddinggemma
`sparse_model`: Qdrant/bm25
`chunk_size`: 600, `overlap`: 100

## 13. Testler

Unit:
6
Integration:
2

## 14. AI Araçlarını Nasıl Kullandım?

Eval dataset'i önce kendim tasarladım mı?
Evet yapısal olarak örneklerini hazırladım daha sonrasında hazır kalıplardan ai kullanımıyla çoğalttım.

AI'dan hangi review'u istedim?
Test başarısızlıklarının çapraz analizi, Qdrant entegrasyon testlerinde karşılaşılan vektör boyutu hatasının çözümü ve terminalden alınan bağımsız JSON metriklerinin yorumlanması.

AI'nın önerdiği ama değiştirdiğim/reddettiğim öneri:
AI ısrarla tüm test sonuçlarının tek bir `day11-retrieval-benchmark-all.json` dosyasında toplanmasını önerdi. Ben ise her strateji için izole edilmiş ayrı JSON dosyaları (`_dense.json`, `_lexical.json`, `_hybrid.json`) oluşturulması gerektiği fikrinde direttim ve AI'ın tek dosya yaklaşımını reddettim.

Neden?
AI'ın önerdiği tek dosya yaklaşımı, terminalde farklı stratejiler arka arkaya çalıştırıldığında önceki stratejinin verilerinin kaybolmasına (dosyanın üzerine yazılmasına) neden oluyordu. Veri izolasyonunu sağlamak, önceki benchmark sonuçlarını korumak ve her arama motorunun metriklerini birbirine karıştırmadan güvenli bir şekilde analiz edebilmek için bu kararı uygulamak zorundaydım.

## 15. Bugünün En Önemli 5 Öğrenimi
1.Sisteme yeni bir arama yöntemi eklemeden önce, mevcut yapının kalitesi ve zayıf yönleri mutlaka somut metriklerle ölçülmelidir.
2.Etkili bir değerlendirme veri seti, soru sayısının fazlalığıyla değil, farklı hata türlerini (anlamsal, kesin eşleşme vb.) barındıran senaryo çeşitliliğiyle kurulur.
3.Hit@k metriği aranan bilginin sonuçlar listesinde olup olmadığını gösterirken, MRR o bilginin sıralamada ne kadar üstte olduğunu ölçer. 
4.Hibrit arama, anlamsal ve sözcüksel arama puanlarını doğrudan toplamak yerine, bu farklı sinyalleri kontrollü bir yöntemle tek bir sıralamaya dönüştürür. 
5.Arama problemlerini çözmek için rastgele ayar değiştirmek yerine, öncelikle hatanın hangi katmanda (aday bulma, sıralama, sorgu veya veri) gerçekleştiği tespit edilmelidir. 


## 16. Salı MCP Hakkında Merak Ettiklerim

1.LangChain veya benzeri araçlar zaten varken, MCP (Model Context Protocol) tam olarak neyi çözmek veya kolaylaştırmak için ortaya çıktı?
2. Kurduğumuz Ollama ve Qdrant altyapısına MCP'yi dahil ettiğimizde, şu ana kadar yazdığımız entegrasyon kodlarını baştan mı tasarlamamız gerekecek, yoksa sistemimize kolayca uyum sağlayacak mı?
3. ...
```


