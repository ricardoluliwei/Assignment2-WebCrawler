import re
from urllib.parse import urlparse
from utils.response import Response
from bs4 import BeautifulSoup

from utils import get_logger

from tokenizer import tokenize
from tokenizer import compute_word_frequencies

import shelve

depth = 200

stop_words = open("stop_words.txt", "r").read()

def scraper(url, resp, counter: shelve.DbfilenameShelf):
    links = extract_next_links(url, resp, counter)
    return links


def extract_next_links(url: str, resp: Response,
                       counter: shelve.DbfilenameShelf) -> list:
    if resp.error:
        return list()
    
    logger = get_logger("scraper")
    logger.info(f"Scrape from : {url}")
    print(f"Scrape form {url}")
    rootURL = urlparse(url)
    
    soup = BeautifulSoup(resp.raw_response.content, features='lxml')
    links = soup.find_all('a')

    # do analysis here, get longest page and
    text = soup.text
    tokens = tokenize(text)
    # compute the longest page
    if len(tokens) > counter["longestPage"][1]:
        counter["longestPage"] = (url, len(tokens))

    # compute word frequencies
    new_tokens = [x for x in tokens if x not in stop_words]
    counter["WordFrequencies"] = compute_word_frequencies(new_tokens)

    result = set()
    for l in links:
        try:
            # links are the urls found in this page
            link = l["href"]
            # defragement
            link = link.replace(r"#.*", "")
            
            linkParse = urlparse(link)
            domain = linkParse.netloc
            
            # get the complete url
            if not linkParse.scheme:
                if not linkParse.netloc:
                    link = rootURL.netloc + link
                link = rootURL.scheme + link
            
            if is_valid(link, counter):
                result.add(link)
                logger = get_logger("scraper")
                logger.info(f"New Found URL: {link}")
                print(f"new add : {link}")
            
            # count the subdomains
            counter["PagesInDomain"][domain].add(link)
        
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
        
        # if we have found enough pages in a certain subdomain
        # all urls from the subdomain becomes invalid
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
