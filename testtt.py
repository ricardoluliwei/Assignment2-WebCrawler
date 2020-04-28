from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlopen
from tokenizer import tokenize, compute_word_frequencies

html = urlopen("https://wics.ics.uci.edu/events/").read().decode("utf-8")


soup = BeautifulSoup(html, features='lxml')
tokens = tokenize(soup.get_text())


print(len(compute_word_frequencies(tokens)))