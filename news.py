import requests
from bs4 import BeautifulSoup
import re


class News():
    def __init__(self):
        self.news_url = "https://www.google.com/search?q=yahoo+finance+{}&tbm=nws"

    def search_for_news(self, ticker):
        print("Searching for news articles for " + ticker)
        search_url = self.news_url.format(ticker)
        r = requests.get(search_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        atags = soup.find_all('a')
        hrefs = [link['href'] for link in atags]
        return hrefs

    def clean_urls(self, urls, exclude_list):
        clean_url = []
        idx = 1
        n = len(urls)
        for url in urls:
            print("Cleaning " + str((idx/n) * 100) + "% done")
            idx += 1
            if 'https://' in url and not any(exclude_word in url for exclude_word in exclude_list):
                # print("Reached here")
                res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
                clean_url.append(res)
        return list(set(clean_url))

    def process(self, urls, MAX_LEN_FOR_PEGASUS):
        articles = []
        idx = 1
        n = len(urls)
        for url in urls:
            print("Processing " + str((idx / n) * 100) + "% done")
            idx += 1
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            paragraphs = soup.find_all('p')
            text = [paragraph.text for paragraph in paragraphs]
            words = ' '.join(text).split(' ')[:MAX_LEN_FOR_PEGASUS]
            article = ' '.join(words)
            articles.append(article)
        return articles