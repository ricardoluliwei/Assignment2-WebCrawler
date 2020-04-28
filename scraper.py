import re
from urllib.parse import urlparse
from utils.response import Response
from bs4 import BeautifulSoup

from tokenizer import tokenize
from tokenizer import compute_word_frequencies

import shelve

depth = 200

low_words_limit = 50
high_token_limit = 20000

stop_words = open("stop_words.txt", "r").read()


def scraper(url, resp, counter: shelve.DbfilenameShelf):
    links = extract_next_links(url, resp, counter)
    return links


def extract_next_links(url: str, resp: Response,
                       counter: shelve.DbfilenameShelf) -> list:
    if resp.error:
        return list()
    
    print(f"extract: {url}")
    soup = BeautifulSoup(resp.raw_response.content, features='lxml')
    
    # text is the pure text that we extract from the page excluding html tags
    text = soup.get_text()
    tokens = tokenize(text)
    
    # compute word frequencies
    new_tokens = [x for x in tokens if x not in stop_words]
    word_frequencies = compute_word_frequencies(new_tokens)
    
    # if the page has low value skip it
    if len(word_frequencies) < low_words_limit:
        return list()
    
    # if the page is too large skip it
    if len(tokens) > high_token_limit:
        return list()
    
    compute_longest_page(url, tokens, counter)
    count_word_frequenies(word_frequencies, counter)
    count_pages_in_domain(url, counter)
    
    return get_url_from_page(url, soup, counter)


# compute the longest page
def compute_longest_page(url, tokens, counter):
    if len(tokens) > counter["longestPage"][1]:
        counter["longestPage"] = [url, len(tokens)]


# add the word_frequencies to the total WordFrequencies
def count_word_frequenies(word_frequencies, counter):
    WordFrequencies = counter["WordFrequencies"]
    for k, v in word_frequencies.items():
        if k in WordFrequencies.keys():
            WordFrequencies[k] += v
        else:
            WordFrequencies[k] = v
    
    counter["WordFrequencies"] = WordFrequencies


# count the pages in a domain
def count_pages_in_domain(url: str, counter):
    parse = urlparse(url)
    domain = parse.netloc
    
    PagesInDomain = counter["PagesInDomain"]
    PagesInDomain[domain].add(url)
    counter["PagesInDomain"] = PagesInDomain


# extract all url from a page
def get_url_from_page(url: str, soup: BeautifulSoup, counter) -> list:
    parse = urlparse(url)
    links = soup.find_all('a')
    result = set()
    for l in links:
        try:
            # links are the urls found in this page
            link = l["href"]
            # defragement
            link = link.replace(r"#.*", "")
            
            linkParse = urlparse(link)
            
            # get the complete url
            if not linkParse.scheme:
                if not linkParse.netloc:
                    link = parse.netloc + link
                link = parse.scheme + link
            
            if is_valid(link, counter):
                result.add(link)
                print(f"get: {link}")
        except:
            pass
    
    return list(result)


def is_valid(url, counter: shelve.DbfilenameShelf):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # if we have added this page, this page becomes invalid
        if url in counter["PagesInDomain"][domain]:
            return False
        
        # if we have found enough pages in a certain domain
        # all urls from the domain becomes invalid
        if len(counter["PagesInDomain"][domain]) > depth:
            return False
        
        if parsed.scheme not in {"http", "https"}:
            return False
        
        if not re.match(
            r".*ics.uci.edu.*|"
            + r".*cs.uci.edu.*|"
            + r".*informatics.uci.edu.*|"
            + r".*stat.uci.edu.*|"
            + r"today.uci.edu/department/information_computer_sciences.*",
            parsed.netloc.lower()):
            return False
        
        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False
        
        return True
    
    except TypeError:
        print("TypeError for ", parsed)
        raise
