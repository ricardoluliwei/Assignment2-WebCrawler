import re
from collections import defaultdict

pattern = re.compile("[\W_]+")


def tokenize(line: str) -> list:
    tokens = []
    try:
        tokens += pattern.sub(' ', line).lower().split()
    except Exception as err:
        print(err)
    finally:
        return [token for token in tokens if len(token) > 1]


def compute_word_frequencies(tokens: list) -> defaultdict[str, int]:
    count = defaultdict(int)
    try:
        for token in tokens:
            count[token] += 1
    except:
        pass
    finally:
        return count



