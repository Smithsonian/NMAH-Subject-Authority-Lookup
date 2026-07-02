import requests
import urllib.parse

#pull subject codes from list - after workaround for earlier issues configured
#retrieve subject variant strings as array
#if the given variants match the LOC variant list, return LOC
#else, return NMAH

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

def getResourceURI(label):
    enc = urllib.parse.quote(label)
    url = f"https://id.loc.gov/authorities/subjects/label/{enc}"
    headers = {'accept':'application/json'}
    h = requests.head(url = url, headers = headers)
    json = h.headers
    uri = json["x-uri"].split("/")
    return uri[-1]


def getTermVariants(lbl):
    #where lbl is what it grabs from the csv
    idstr = getResourceURI(lbl)
    json = getData(idstr)
    allVars = []
    for i in json:
        if "http://www.loc.gov/mads/rdf/v1#Variant" in i["@type"]:
            varis = listVariants(i)
            if varis:
                for v in varis:
                    allVars.append(v)
    
    return allVars
