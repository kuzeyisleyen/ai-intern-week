
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

text = "Python"
print(f"\n--- Analiz Edilen Metin: '{text}' ---\n")

tokens = tokenizer.tokenize(text)
print(f"1. Tokenlar:\n{tokens}\n")

inputs = tokenizer(text, return_tensors="pt")
input_ids = inputs["input_ids"]
print(f"2. Token ID:\n{input_ids.tolist()[0]}\n")

print(f"3. Input Tensor Shape:\n{input_ids.shape}\n")

embedding_layer = model.get_input_embeddings()

embeddings = embedding_layer(input_ids)
print(f"4. Embedding Tensor Shape:\n{embeddings.shape}\n")

ilk_tokenin_ilk_5_degeri = embeddings[0, 0, :5]
print(f"5. İlk token'ın ilk 5 embedding değeri:\n{ilk_tokenin_ilk_5_degeri.tolist()}\n")
