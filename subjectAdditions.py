from main import *
from detect import *

#pull identified list of terms where LC Subject Headings
#make columns for variants 1-10, pop name, variant, and source
#make columms (at end) for URI, name, etc

def pullLOC(inDF):
    df = inDF.loc[inDF["Source"] == "LC Subject Headings"]
    return df

def pullWikidat(inDF):
    df = inDF.loc[inDF["Source"] == "Wikidata"]

def varsLOC(inFile, outFile):
    inDF = pd.read_csv(inFile)
    lc = pullLOC(inDF)
    df = pd.DataFrame(data={"Updated Term":lc["Updated Term"][1:], "Source":lc["Source"][1:]})
    uri = []
    variant1 = []
    variant2 = []
    variant3 = []
    variant4 = []
    variant5 = []
    variant6 = []
    variant7 = []
    variant8 = []
    variant9 = []
    variant10 = []
    variants = [variant1, variant2, variant3, variant4, variant5, variant6, variant7, variant8, variant9, variant10]

    for i, row in df.iterrows():
        u = getResourceURI(row["Updated Term"])
        uri.append(f"http://id.loc.gov/authorities/subjects/{u}")
        vars = getTermVariants(row["Updated Term"])
        if ";" in vars:
            vars = vars.split(";").lstrip()
        else:
            a = vars
            vars = []
            vars.append(a)
        n = 0
        if len(vars) < 10:
            l = 10 - len(vars)
            for i in range(l):
                vars.append('')
        for v in vars:
            if n == 10:
                break
            variants[n].append(v)
            n += 1
        
    df["URI"] = uri
    df["Variant 1"] = variants[0]
    df["Variant 2"] = variants[1]
    df["Variant 3"] = variants[2]
    df["Variant 4"] = variants[3]
    df["Variant 5"] = variants[4]
    df["Variant 6"] = variants[5]
    df["Variant 7"] = variants[6]
    df["Variant 8"] = variants[7]
    df["Variant 9"] = variants[8]
    df["Variant 10"] = variants[9]

    df.to_csv(outFile)

if __name__ == "__main__":
    varsLOC("../unlinked-terms-matched3.csv", "../matched-to-LOC3.csv")