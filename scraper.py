import re
from urllib.parse import urlparse
from utils.response import Response
from bs4 import BeautifulSoup
from utils import get_logger

from urllib.request import Request
def scraper(url, resp):
    links = extract_next_links(url, resp)
    get_logger("scraper").info(f"Scrape from : {url}")
    return [link for link in links if is_valid(link)]

def extract_next_links(url: str, resp : Response):
    if resp.error:
        return list()

    parsed = urlparse(url)
    
    soup = BeautifulSoup(resp.raw_response.content, features='lxml')
    links = soup.find_all('a')
    result = list()
    for link in links:
        parsedLink = urlparse(link['href'])
        link = parsed.netloc if not parsedLink.netloc else parsedLink.netloc
        link += parsedLink.path
        if link == url:
            continue
        result.append(link)
        logger = get_logger("scraper")
        logger.info(f"Added URL: {link}")
    
    return result

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
        print ("TypeError for ", parsed)
        raise