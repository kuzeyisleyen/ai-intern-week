

from transformers import AutoModelForCausalLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilbert/distilgpt2")
tokenizer.pad_token = tokenizer.eos_token



def get_input() -> str:
    input_text = input("Enter a prompt for text generation: ")
    if not input_text.strip():
        print("Input cannot be empty. Please enter a valid prompt.")
        return get_input()
    return input_text

def count_words(text: str) -> int:
    return len(text.split())

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

def generate_continuation(text: str, use_sampling: bool = False) -> str:
    inputs = tokenizer(text, return_tensors="pt")

    if use_sampling:
        output = model.generate(
            **inputs,
            max_new_tokens=30,
            do_sample=True,
            temperature=0.8,
            top_k=50
        )
    else:
        output = model.generate(
            **inputs,
            max_new_tokens=30
            # do_sample=False (varsayılan) -> greedy, parametresiz
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)


if __name__ == "__main__":
    prompt = get_input()

    greedy_result = generate_continuation(prompt, use_sampling=False)
    sampled_result = generate_continuation(prompt, use_sampling=True)

    print("--- Parametresiz (greedy) ---")
    print(greedy_result)
    print(f"Word count: {count_words(greedy_result)}")
    print(f"Token count: {count_tokens(greedy_result)}")

    print("\n--- Parametreli (sampling) ---")
    print(sampled_result)
    print(f"Word count: {count_words(sampled_result)}")
    print(f"Token count: {count_tokens(sampled_result)}")


"""def generate_continuation(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt")
    
    output = model.generate(
        **inputs, # input_ids ve attention_mask'i modele gönderir
        max_new_tokens=30,
        do_sample=True,   # Açgözlü aramayı kapatıp olasılıksal (yaratıcı) seçimi açar
        temperature=0.8,  # Yaratıcılık dozu (1.0 çok uçuk, 0.1 çok katı)
        top_k=50          # Sadece en mantıklı 50 kelime arasından seçim yap
    )
    
    return tokenizer.decode(output[0], skip_special_tokens=True)

    
if __name__ == "__main__":
    prompt = get_input()
    continuation = generate_continuation(prompt)
    print(f"Generated continuation: {continuation}")
    print(f"Word count: {count_words(continuation)}")
    print(f"Token count: {count_tokens(continuation)}")
"""