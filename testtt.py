
import re
pattern = re.compile("[\W_]+")

from bs4 import BeautifulSoup
from tokenizer import tokenize, compute_word_frequencies



infile = open("/Users/ricardo/Downloads/wics_test.html", "r")

soup = BeautifulSoup(infile, features= "lxml")

words = compute_word_frequencies(tokenize(soup.text))

print(soup.find_all(text=True))

print(words)

