from utils import get_logger
from crawler.frontier import Frontier
from crawler.worker import Worker
import shelve
from collections import defaultdict


class Crawler(object):
    def __init__(self, config, restart, frontier_factory=Frontier,
                 worker_factory=Worker):
        self.config = config
        self.logger = get_logger("CRAWLER")
        self.frontier = frontier_factory(config, restart)
        self.workers = list()
        self.worker_factory = worker_factory
        
        self.count
    
    def start_async(self):
        self.workers = [
            self.worker_factory(worker_id, self.config, self.frontier)
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
        self.counter = shelve.open("count.shelve")
        
        # how many unique pages in a domain, only crawl a certain number of pages
        # in a domain in case of traps
        # dict key is the domain, value is the set of pages' url hash
        self.counter["PagesInDomain"] = self.counter.get("PagesInDomain",
                                                         defaultdict(str,
                                                                     set()))
        
        # longest page
        self.counter["longestPage"] = self.counter.get("longestPage", tuple(str,
                                                                            int))
    
    def get_unique_pages(self):
        pages = 0
        for k, v in self.counter["PagesInDomain"].items():
            pages += len(v)
        return
    
    def get_longest_page(self):
        self.