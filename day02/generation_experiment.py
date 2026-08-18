import torch
import json
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

prompt = "Write a short, creative explanation about the future of artificial intelligence."
messages = [{'role':'user','content':prompt}]
prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(prompt_text, return_tensors="pt")

config=[
    {"name": "Config_A (Greedy)",
     "do_sample": False,
     },

     {"name": "Config_B (Sampling,Temperature= 0.7)",
      "do_sample": True,
      "temperature": 0.7
      },

    {"name": "Config_C (Sampling ,Temperature = 1.2)",
      "do_sample": True,
      "temperature": 1.2
      }
]

experiment_results = []


for cfg in config :
    torch.manual_seed(42) #tekrar üretim için aynı başlangıç noktası

    generation_parameters = {}

    for key , value in cfg.items():
        if key != "name":
            generation_parameters[key] = value

    generation_parameters["max_new_tokens"] = 100

    outputs = model.generate(**inputs, **generation_parameters)# ** işareti sözlükten parametreleri alıp fonksiyona gönderir
    result_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

#Sonucun kaydedileceği format
    experiment_results.append({
        "model": model_name,
        "prompt": prompt,
        "seed": 42,
        "config": cfg["name"],
        "config": generation_parameters,
        "output": result_text
    })



#Sonuçları json dosyasına eklme
output_file = "experiments/day02-generation-results.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(experiment_results, f, ensure_ascii=False, indent=4)