from transformers import AutoTokenizer

# Kullanacağımız modelin adı
model_name = "distilbert/distilgpt2"

# Tokenizer'ı internetten indirip yüklüyoruz
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Test edeceğimiz metin 
text = "Kodlama ve yapay zeka ile ilgili bir test metni."

# Metni token'lara  ayır
tokens = tokenizer.tokenize(text)

# Token'ları bilgisayarın anladığı Token ID (sayı) formatına çevir
token_ids = tokenizer.encode(text)

# Sonuçları terminale yazdır
print("Text:", text)
print("Tokens:", tokens)
print("Token IDs:", token_ids)
print("Token count:", len(token_ids))