
import re
pattern = re.compile("[\W_]+")


def tokenize(line: str):
    """
    Method/Function: List<Token> tokenize(TextFilePath)
    Write a method/function that reads in a text file and returns a list of the tokens in that file. For the
    purposes of this project, a token is a sequence of alphanumeric characters, independent of capitalization
    (so Apple, apple are the same token).

    Complexity: O(N)
    """
    tokens = []
    try:
        tokens += pattern.sub(' ', line).lower().split()
    except Exception as err:
        print(err)
    finally:
        return [token for token in tokens if len(token) > 1]

print(tokenize('''[IDENTIFICATION]
# Set your user agent string here.
USERAGENT = 12345678

[CONNECTION]
HOST = styx.ics.uci.edu
PORT = 9000

[CRAWLER]
SEEDURL = https://www.ics.uci.edu,https://www.cs.uci.edu,https://www.informatics.uci.edu,https://www.stat.uci.edu
# In seconds
POLITENESS = 0.5

[LOCAL PROPERTIES]
# Save file for progress
SAVE = frontier.shelve

# IMPORTANT: DO NOT CHANGE IT IF YOU HAVE NOT IMPLEMENTED MULTITHREADING.
THREADCOUNT = 1
doesn't

'''))
