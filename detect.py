from main import *

def suggestionSearch(unlinked, type):
    if type != "keyword" and type != "leftanchored":
        raise Exception("input type must be 'leftanchored' or 'keyword'")
    headers = {'Accept':'application/json'}
    keyw = urllib.parse.quote(str(unlinked))
    url = f"https://id.loc.gov/authorities%2Fsubjects/suggest2?q={keyw}&memberOf=http%3A%2F%2Fid.loc.gov%2Fauthorities%2Fsubjects%2Fcollection_LCSHAuthorizedHeadings&searchtype={type}&count=15&offset=0&sort=relevance&mime=json&usage=true&rawlist=true"
    r = requests.get(url = url, headers = headers)
    if r.status_code != 200:
        return "error code"
    return r.json()

def parseResults(dat, type):
    # messy; needs to just inherit the type from the original input but whatever
    results = []
    if dat == "error code":
        return "error code"
    hits = dat["hits"]
    if len(hits) >= 1:
        match type:
            case "keyword":
                for hit in hits:
                    authHeading = hit["suggestLabel"]
                    results.append(authHeading)
            case "leftanchored":
                for hit in hits:
                    results.append(hit)
    else:
        return "no matches found"
    return "; ".join(results)

def prim(inFile, outFile, type, filter):
    csv = pd.read_csv(inFile, encoding='utf-8')
    matches = []
    suggested = []
    if filter == True:
        csv = filterRows(csv)
    for i, row in csv.iterrows():
        # this is a typo from the csv that i didn't feel like dealing with, ignore
        r = suggestionSearch(row['Orginal XG Term'], type)
        match = parseResults(r, type)
        matches.append(match)
        # automatically updates with the first suggested term, saves some work on my end
        matchlist = match.split(";")
        suggested.append(matchlist[0])
        
    csv["LC Suggested Hits"] = matches
    csv["Updated Term"] = suggested
    csv.to_csv(outFile)

if __name__ == "__main__":
    # change to variables, command line args
    prim("../unlinked-subjects/unlinked-subjects-filtered-2.csv", "../unlinked-subjects/unlinked-term-hits2.csv", "leftanchored", filter=True)
