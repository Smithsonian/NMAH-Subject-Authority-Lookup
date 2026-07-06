import json
import requests
import sys
import urllib.parse

from main import *

#various functions to grab individual json files
def test(term):
    uri = getResourceURI(term)
    data = getData(uri)
    with open(f"{term}.json", "w") as f:
        json = json.dumps(data)
        f.write(json)

if __name__ == "__main__":
    test(sys.argv[1])
