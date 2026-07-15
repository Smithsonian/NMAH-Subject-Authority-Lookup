from detect import *
from main import *

def filterHistory(label):
    if "History" in label or "Protestantism" in label or "Publications" in label or "American Indians" in label:
        lbl = label.split(",")
        term = lbl[-1]
        return term
    return label

def getBlanks(inDF):
    return inDF.loc[inDF["Source"] != "LC Subject Headings"]

def multiSearch(inFile, outFile):
    csv = pd.read_csv(inFile, encoding='utf-8')
    df = getBlanks(csv)
    left_anchored_matches = []
    keyword_matches = []
    suggested = []
    for i, row in df.iterrows():
        suggestions = []
        t = filterHistory(row['Orginal XG Term'])

        type="leftanchored"
        l = suggestionSearch(t, type)
        lr = parseResults(l, type)
        s1 = lr.split(";")
        suggestions.append(s1[0])

        type2 = "keyword"
        k = suggestionSearch(t, type2)
        kr = parseResults(k, type2)
        s2 = kr.split(";")
        suggestions.append(s2[0])

        left_anchored_matches.append(lr)
        keyword_matches.append(kr)
        suggested.append(";".join(suggestions))
    csv["LC Suggested Term"] = suggested
    csv["Left Anchored Matches"] = left_anchored_matches
    csv["Keyword Matches"] = keyword_matches
    csv.to_csv(outFile)

#if __name__ == "__main__":
#    multiSearch("../unlinked-subjects-current3.csv", "../unlinked-subjects/unlinked-deep-search-1.csv")
