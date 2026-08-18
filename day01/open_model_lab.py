
from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="distilbert/distilgpt2"
)

prompt = "Once upon a time"

result = generator(
    prompt,
    max_new_tokens=30,
)

print(result[0]["generated_text"])


#Machine learning models can
#Once upon a time
#BU İKİ PROMPT İÇİN HER NE KADAR ANLAMLI CÜMLELELER OLUŞTURABİLSEDE DİĞER CÜMLELERDE
#DİL YAPISI OLARAK DOĞRU FAKAT PEK BİR ANLAMI OLMAYAN CÜMLELELER ORTAYA ÇIKARDI