from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from tqdm import tqdm

class Summarize:

    def __init__(self):
        self.tokenizer = None;
        self.model = None;
    def set_up_model(self):

        MODEL_NAME = "human-centered-summarization/financial-summarization-pegasus"
        self.tokenizer = PegasusTokenizer.from_pretrained(MODEL_NAME, revision="main")
        self.model = PegasusForConditionalGeneration.from_pretrained(MODEL_NAME, revision="main")

    def summarize_all(self, articles, ticker):
        summaries = []
        # idx = 1
        # n = len(articles)
        # print("Summarizing articles for " + ticker)
        # for article in articles:
        for idx, article in enumerate(tqdm(articles, desc=f"Summarizing {ticker} articles")):
            # print("Summarizing {:.2f}% done".format((idx/n) * 100))
            idx += 1
            input_ids = self.tokenizer.encode(article, return_tensors='pt')
            output = self.model.generate(input_ids, max_length=55, num_beams=5, early_stopping=True)
            summary = self.tokenizer.decode(output[0], skip_special_tokens=True)
            summaries.append(summary)
        return summaries