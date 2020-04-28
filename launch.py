from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()
    print(f"Number of Unique Pages: {crawler.get_unique_pages()}")
    print(f"Longest Page: {crawler.get_longest_page()}")
    print("50 most common words: ")
    print(crawler.get_most_common_words())
    print("Subdomains of ics.uci.edu")
    print(crawler.get_subdomain_of_ics())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)

    