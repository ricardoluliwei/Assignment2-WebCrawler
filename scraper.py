import re
from urllib.parse import urlparse
from utils.response import Response
from bs4 import BeautifulSoup

from utils import get_logger, get_urlhash
from collections import defaultdict

# key is the subdomain of ics.uci.edu, value is the pages' hash in the subdomain
global subdomains
subdomains = defaultdict(lambda: set())

# key is the url of longestPage, value is the length
global longestPage
longestPage = tuple()

# key is the words, value is the frequency
global wordsFrequency
wordsFrequency = defaultdict(lambda: 0)

# how many unique pages found
global uniquePages
uniquePages = int()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    uniquePages += len(links)
    return extract_next_links(url, resp)

def extract_next_links(url: str, resp: Response):
    if resp.error:
        return list()

    # logger = get_logger("scraper")
    # logger.info(f"Scrape from : {url}")
    print(f"scrape form {url}")
    rootURL = urlparse(url)
    
    soup = BeautifulSoup(resp.raw_response.content, features='lxml')
    links = soup.find_all('a')
    
    result = set()
    
    for l in links:
        try:
            #links are the urls found in this page
            link = l["href"]
            # defragement
            link = link.replace(r"#.*", "")
            
            linkParse = urlparse(link)
            domain = linkParse.netloc
            
            #count the subdomains in ics.uci.edu
            if re.match(r".*ics.uci.edu.*", domain):
                    subdomains[domain].add(get_urlhash(link))
                    
            #do content analysis here
            
            #get the original url
            if not linkParse.scheme:
                if not linkParse.netloc:
                    link = rootURL.netloc + link
                link = rootURL.scheme + link
            
            if is_valid(link):
                result.add(link)
                # logger = get_logger("scraper")
                # logger.info(f"New Found URL: {link}")
                print(f"new add : {link}")
        except:
            pass
    
    return list(result)


def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
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
