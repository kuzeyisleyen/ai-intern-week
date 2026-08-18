import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def base_model(prompt):
    model_name = "HuggingFaceTB/SmolLM2-360M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    inputs = tokenizer(prompt,return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens = 60,
        do_sample = False
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"PROMPT: {prompt}\nÇIKTI: {result}\n")


def instruct_model(prompt):
    model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    message = [{"role": "user", "content": prompt}]

    prompt_text = tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=True)#sözlüğü modele uygun formata getiren fonksiyon
    inputs = tokenizer(prompt_text, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens = 60,
        do_sample = False
    )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"PROMPT: {prompt}\nÇIKTI: {result}\n")

if __name__ == "__main__":
   
    prompt_A = "Python is useful for software development because"
    prompt_B = "Explain the difference between a Python list and dictionary in exactly three bullet points."
    prompt_C = "Python'da list ve dict arasındaki farkı tam olarak 3 maddede açıkla."

    base_model(prompt_C)
    instruct_model(prompt_C)