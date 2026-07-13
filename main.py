import chardet
import os
import pandas as pd
import requests
import urllib.parse

#pull subject codes from list - after workaround for earlier issues configured
#retrieve subject variant strings as array
#if the given variants match the LOC variant list, return LOC
#else, return NMAH
def getResourceURI(label):
    enc = urllib.parse.quote(str(label))
    url = f"https://id.loc.gov/authorities/subjects/label/{enc}"
    headers = {'accept':'application/json'}
    h = requests.head(url = url, headers = headers)
    json = h.headers
    if "x-uri" not in json:
        return "not found"
    uri = json["x-uri"].split("/")
    return uri[-1]

def getData(id):
    url = f"https://id.loc.gov/authorities/subjects/{id}.json"
    headers = {'Accept':'application/json'}
    r = requests.get(url = url, headers = headers)
    if r.status_code != 200:
        raise Exception(f"the request yielded a non-200 response: {r.status_code}")
    return r.json()

def listVariants(item):
    #where object is a single response item
    #if http://www.loc.gov/mads/rdf/v1#Variant in item["@type"]
    lbl = item["http://www.loc.gov/mads/rdf/v1#variantLabel"]
    labels = []
    for l in lbl:
        labels.append(l["@value"])
    return labels

def altAuthoritativeLabel(item, id):
    href = f"http://id.loc.gov/authorities/subjects/{id}"
    if item["@id"] == href:
        if "http://www.loc.gov/mads/rdf/v1#authoritativeLabel" in item.keys():
            sub = item["http://www.loc.gov/mads/rdf/v1#authoritativeLabel"]
            return sub[0]["@value"]
    return None


def getTermVariants(lbl):
    #where lbl is what it grabs from the csv
    idstr = getResourceURI(lbl)
    if idstr == "not found":
        return "string not found in LOC"
    json = getData(idstr)
    allVars = []
    for i in json:
        alts = altAuthoritativeLabel(i, idstr)
        if alts != None:
            allVars.append(alts)
        if "http://www.loc.gov/mads/rdf/v1#Variant" in i["@type"]:
            varis = listVariants(i)
            if varis:
                for v in varis:
                    allVars.append(v)    
    return "; ".join(allVars)

def matchVariants(inTerms):
    termsIn = inTerms.split(";")
    f = []
    for term in termsIn:
        found = "N"
        t = term.lstrip()
        sub = getResourceURI(t)
        if sub != "not found":
            found = "Y"
        f.append(found)
    return "; ".join(f)

def main():
    csv = "../unlinked-subjects/unlinked-term-counts.csv"
    out = "../unlinked-subjects/test_subjects_output.csv"
    #might mitigate some of the hiccups with accents
    with open(csv, 'rb') as f:
        enc = chardet.detect(f.read())
    term_vars = pd.read_csv(csv, encoding=enc['encoding'])
    variants = []
    checks = []
    for i, row in term_vars.iterrows():
        var = getTermVariants(row["Subject"])
        variants.append(var)

        varCheck = matchVariants(row["Variant Terms"])
        checks.append(varCheck)
    term_vars["LOC_Variants"] = variants
    term_vars["XG_Variants_in_LOC"] = checks
    term_vars.to_csv(out)

if __name__ == "__main__":
    main()