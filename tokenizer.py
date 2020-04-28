import re
import sys
from collections import defaultdict
from typing import List, Dict

pattern = re.compile("[\W_]+")


def tokenize(line: str) -> List[str]:
    tokens = []
    try:
        tokens += pattern.sub(' ', line).lower().split()
    except Exception as err:
        print(err)
    finally:
        return [token for token in tokens if len(token) > 1]


def compute_word_frequencies(tokens: List[str]) -> Dict[str, int]:
    count = defaultdict(int)
    try:
        for token in tokens:
            count[token] += 1
    except:
        pass
    finally:
        return count



