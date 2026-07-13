from main import *

def suggestionSearch(unlinked):
    headers = {'Accept':'application/json'}
    keyw = urllib.parse.quote(str(unlinked))
    url = f"https://id.loc.gov/authorities%2Fsubjects/suggest2?q={keyw}&memberOf=http%3A%2F%2Fid.loc.gov%2Fauthorities%2Fsubjects%2Fcollection_LCSHAuthorizedHeadings&searchtype=keyword&count=15&offset=0&sort=relevance&mime=json&usage=true&rawlist=true"
    r = requests.get(url = url, headers = headers)
    if r.status_code != 200:
        raise Exception(f"the request yielded a non-200 response: {r.status_code}")
    return r.json()

def parseResults(json):
    results = []
    hits = json["hits"]
    if len(hits) >= 1:
        for hit in hits:
            authHeading = hit["suggestLabel"]
            results.append(authHeading)
        return "; ".join(results)
    return "no matches found"

def main(inFile, outFile):
    csv = pd.read_csv(inFile, encoding='utf-8')
    matches = []
    for i, row in csv.iterrows():
        # this is a typo from the csv that i didn't feel like dealing with, ignore
        o = getResourceURI(row['Orginal XG Term'])
        if o == "not found":
            r = suggestionSearch(row['Orginal XG Term'])
        else:
            r = o
        match = parseResults(r)
        matches.append(match)
        
    csv["LC Suggested Hits"] = matches
    csv.to_csv(outFile)

if __name__ == "__main__":
    # change to variables, command line args
    main("../unlinked-subjects/unlinked-term-counts.csv", "../unlinked-subjects/unlinked-term-hits.csv")
