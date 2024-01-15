from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from bs4 import BeautifulSoup
import requests

model_name = "human-centered-summarization/financial-summarization-pegasus"

MAX_LEN_FOR_PEGASUS = 512;

#Encoding input for transformer model
tokenizer = PegasusTokenizer.from_pretrained(model_name)

model = PegasusForConditionalGeneration.from_pretrained(model_name)

url = "https://finance.yahoo.com/news/goldman-sachs-boosts-2024-sp-500-target-on-increased-confidence-for-fed-rate-cuts-in-march-162652453.html?guccounter=1"

r = requests.get(url)

s = BeautifulSoup(r.text, 'html.parser')
paras = s.find_all('p')
# print(paras)
text = [para.text for para in paras]
words = ' '.join(text).split(' ')
article = ' '.join(words)
# print(article)

input_ids = tokenizer.encode(article, return_tensors='pt')[:,:MAX_LEN_FOR_PEGASUS]
output = model.generate(input_ids, max_length=55, num_beams=5, early_stopping=True)
summary = tokenizer.decode(output[0], skip_special_tokens=False)
print(summary)