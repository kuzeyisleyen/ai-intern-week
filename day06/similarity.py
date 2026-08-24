from math import sqrt
from day06.embedding_client import EmbeddingClient

def cosine_similarity(a: list[float], b: list[float]) -> float:
    # TODO: İki listenin uzunlukları (len) eşit değilse ValueError fırlat ("Vectors must have the same dimension.")
    # TODO: Listeler boşsa (not a) ValueError fırlat ("Vectors must not be empty.")
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimension.")
    if not a and not b:
        raise ValueError("Vectors must not be empty.")
    

    # 1. Dot Product (Nokta Çarpımı) -> a ve b'nin karşılıklı elemanlarının çarpımlarının toplamı
    # İpucu: zip(a, b) kullanabilirsin.
    dot = sum(x * y for x, y in zip(a, b))
    
    # 2. Vektör Normları -> Her bir elemanın karesinin toplamının karekökü
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))

    # TODO: norm_a veya norm_b sıfır ise ValueError fırlat ("Zero vector is not valid.")
    if norm_a == 0 or norm_b == 0 :
        raise ValueError("Zero vector is not valid.")

    # 3. Sonuç -> Nokta çarpımının, normların çarpımına bölümü
    return dot / (norm_a * norm_b)

if __name__ == "__main__":
    # --- OYUNCAK TEST ---
    a = [1.0, 0.0]
    b = [1.0, 0.0]
    c = [0.0, 1.0]

    # TODO: Tahminlerini yorum satırı olarak yaz (Çalıştırmadan önce!)
    # cosine(a, b) sence ne çıkar?  yyüksek çıkar
    # cosine(a, c) sence ne çıkar?  düşük çıkar
    print(f"cosine(a, b): {cosine_similarity(a, b)}")
    print(f"cosine(a, c): {cosine_similarity(a, c)}")

    # --- GERÇEK METİN TESTİ ---
    # TODO: day06.embedding_client içerisindeki EmbeddingClient'ı import et.
    # TODO: A ("Docker container verilerini kalıcı saklamak istiyorum.") ve 
    #       B ("Container silinse bile dosyalarım kaybolmasın.") metinlerini embed et ve benzerliklerini ölç.
    # TODO: A ve C ("Kedim bugün pencerenin önünde uyuyor.") metinlerini embed et ve benzerliğini ölç.
    
    client = EmbeddingClient()
    texts = {
            "A": "Docker container verilerini kalıcı saklamak istiyorum.",
            "B": "Container silinse bile dosyalarım kaybolmasın.",
            "C": "Kedim bugün pencerenin önünde uyuyor."
        }
    #metinleri vektörlere çevirdim
    vec_A = client.embed(texts["A"])
    vec_B = client.embed(texts["B"])
    vec_C = client.embed(texts["C"])
    #benzerlikleri esapladım
    sim_AB = cosine_similarity(vec_A,vec_B)
    sim_AC = cosine_similarity(vec_A,vec_C)

    print(f"A ve B Benzerliği (Docker - Docker): {sim_AB:.4f}")
    print(f"A ve C Benzerliği (Docker - Kedi): {sim_AC:.4f}")



    