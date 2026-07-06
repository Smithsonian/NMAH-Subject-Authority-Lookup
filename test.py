import json
import requests
import sys
import urllib.parse

from main import *

#various functions to grab individual json files
def test(term):
    uri = getResourceURI(term)
    data = getData(uri)
    j = json.dumps(data, indent=2)
    with open(f"{term}.json", "w") as f:
        f.write(j)

def findInLOC(name):
    enc = urllib.parse.quote(str(name))

if __name__ == "__main__":
    term = sys.argv[1]
    test(term)
