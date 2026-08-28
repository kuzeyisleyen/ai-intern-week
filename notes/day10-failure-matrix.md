| Failure (Hata Durumu) | Nerede? (Düğüm/Katman) | Detect (Algıla) | Contain (Sınırla) | Recover/Fallback (Toparlan) | Observe (Gözlemle) | Kategori (Bug vs. Failure) |
|---|---|---|---|---|---|---|
| Ollama unavailable | generation | API Connection Error | Boş cevap üretmeyi engelle | "Model yanıt vermiyor" mesajı | failed_node=generate, error=api_timeout | expected runtime failure |

| Ollama timeout | generation/rewrite | Timeout Error | İşlemi iptal et | Retry (1 kez) veya Fallback | error=timeout | expected runtime failure |

| Qdrant unavailable | retrieval | Connection Error | Aramayı durdur | "Veritabanı ulaşılamıyor" | error=qdrant_down | expected runtime failure |

| empty retrieval | quality | Sonuç sayısı 0 | Kötü bağlamla modeli besleme | Rewrite veya doğrudan cevaplama | error=empty_result | expected runtime failure |

| malformed model response | model contract | JSON Decode Error / Regex Match Yok | Hatalı formatı akışa sokma | Modelden tekrar iste (retry) veya hata dön | error=bad_format | expected runtime failure |

| invalid route | router | Tanımsız rota stringi | Akışı yanlış yere yönlendirme | Hata durumuna (error_node) çek | failed_node=router | expected runtime failure |

| tool validation error | tool | Tool şemasında hata | Tool'u çalıştırma | "Parametreler hatalı" uyarısı | error=invalid_tool_args | expected runtime failure |

| tool runtime error | tool | Tool çalışırken exception | Çıktıyı bozma | "İşlem yapılamadı" | failed_node=tool | expected runtime failure |

| rewrite exhaustion | workflow | rewrite_count >= MAX | Sonsuz döngüyü kes | Fallback (Zayıf bağlamla cevapla) | error=max_rewrite | expected runtime failure |

| max-step reached | orchestration | step_count >= MAX | Çalışmayı tamamen durdur | Sistemi durdur (stopped) | error=max_steps | expected runtime failure |

| invalid citation | validation | Bağlamda olmayan kaynak kullanımı | Kullanıcıya yalan söyleme | Cevabı sil veya uyarı ekle | error=hallucination | expected runtime failure |

| empty/corrupt corpus | ingestion | Dosya okuma hatası | Boş veriyi veritabanına atma | İşlemi iptal et | error=corrupt_file | expected runtime failure |

| vector dimension mismatch | Qdrant/ingestion | Boyut uyuşmazlığı hatası | Veritabanını bozma | Indexlemeyi durdur | error=dim_mismatch | expected runtime failure |
