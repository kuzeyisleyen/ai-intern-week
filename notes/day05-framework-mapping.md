| Native Yapımız | LangChain / LangGraph Kavramı |
|---|---|
| `messages` | agent state / messages |
| `AgentRunner.run()` | agent loop / invocation |
| dispatcher | tool execution |
| Python functions | tools |
| `MAX_ITERATIONS` | termination guard |
| trace JSON | tracing/observability fikri |
| explicit state dict | AgentState / graph state |
| validation | deterministic application step |
| model choice | agentic decision |

## Kendi yorumun

Şunları cevapla:

```text
Framework hangi boilerplate'i azaltıyor?
 bugün ajanın çalışması için koca bir while döngüsü kurdum, try-except blokları yazdım ve state adında bir dictionary oluşturdum. Eğer LangChain gibi bir framework kullansaydım, bu yorucu kısımlarını yazmayacaktım. Bizi bu uzun altyapı kodlarını tekrar tekrar yazmaktan kurtarıyor.
Hangi mekanizmayı görünmez hale getiriyor?
Ben bugün print(f"--- İterasyon {state['iteration']} ---") diyerek ajanın her adımını izledim. Hata yaptığında hatayı tool_history içine açıkça kaydettim. Framework kullansaydım tüm bunlar gizlice yapılacaktı. Yani ajan bir yerde takıldığında arka planda neyin bozulduğunu bulmak çok daha zor olacaktı.
Native yaklaşım neyi daha net gösterdi?
Yapay zekanın aslında sihirli bir varlık olmadığını sadece bizim kodumuza json ve metin gönderen basit bir araç olduğunu gösterdi. Ajanın sonsuz döngüye girmemek için yazdığım MAX_ITERATIONS gibi if-else bloklarına ihtiyacı olduğunu anladım. Yani yapay zekada olsada direksiyonun ve frenin tamamen bizim yazdığımız python kodlarında olduğunu gördüm.
Production'da framework ne zaman değerli olabilir?
Projeye sadece 2 tane araç (kargo ve analiz) ekledim ve bu kolaydı. Ama yarın büyük bir şirkette projeye google, veritabanı ve 50 tane daha araç bağlayacağız dediklerinde hepsini tek tek sıfırdan elde yazmak çok yorucu olur. İşte o zamaniçinde bu araçların hazır bulunduğu LangChain gibi frameworkleri kullanmak hız kazandırır.
