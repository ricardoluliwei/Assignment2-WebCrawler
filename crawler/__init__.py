from utils import get_logger
from crawler.frontier import Frontier
from crawler.worker import Worker
import shelve
from collections import defaultdict
from re import match


class Crawler(object):
    def __init__(self, config, restart, frontier_factory=Frontier,
                 worker_factory=Worker):
        self.counter = shelve.open("count.shelve")
        self.load_counter()
        
        self.config = config
        self.logger = get_logger("CRAWLER")
        self.frontier = frontier_factory(config, restart)
        self.workers = list()
        self.worker_factory = worker_factory
    
    def start_async(self):
        self.workers = [
            self.worker_factory(worker_id, self.config, self.frontier,
                                self.counter)
            for worker_id in range(self.config.threads_count)]
        for worker in self.workers:
            worker.start()
    
    def start(self):
        self.start_async()
        self.join()
    
    def join(self):
        for worker in self.workers:
            worker.join()
    
    def load_counter(self):
        
        # Record how many unique pages in a domain, only crawl a certain number
        # of pages in a domain in case of traps.
        # Dict key is the domain, value is the set of pages' url
        self.counter["PagesInDomain"] = self.counter.get("PagesInDomain",
                                                         defaultdict(set))
        
        # longest page
        self.counter["longestPage"] = self.counter.get("longestPage",
                                                       ["", 0])
        
        # word frequencies
        self.counter["WordFrequencies"] = self.counter.get("WordFrequencies",
                                                           defaultdict(int))
    
    def get_unique_pages(self) -> int:
        count = 0
        for k, v in self.counter["PagesInDomain"].items():
            count += len(v)
        return count
    
    def get_longest_page(self) -> ():
        return self.counter["longestPage"]
    
    def get_subdomain_of_ics(self) -> dict:
        domains = self.counter["PagesInDomain"]
        return {k: domains[k] for k in sorted(domains) if
                match(
                    r".*ics.uci.edu.*", k)}
    
    def get_most_common_words(self) -> dict:
        word_frequencies = self.counter["WordFrequencies"]
        i = 0
        common_words = dict()
        for key in sorted(word_frequencies, key=word_frequencies.get,
                          reverse=True):
            if i >= 50:
                break
            common_words[key] = word_frequencies[key]
            i += 1
        return common_words
