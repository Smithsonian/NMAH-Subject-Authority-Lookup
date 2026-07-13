from detect import *
from main import *

def multiSearch(inFile, outFile):
    csv = pd.read_csv(inFile, encoding='utf-8')
    left_anchored_matches = []
    keyword_matches = []
    suggested = []
    for i, row in csv.iterrows():
        suggestions = []
        type="leftanchored"
        l = suggestionSearch(row['Orginal XG Term'], type)
        lr = parseResults(l, type)
        s1 = lr.split(";")
        suggestions.append(s1[0])

        type2 = "keyword"
        k = suggestionSearch(row['Orginal XG Term'], type2)
        kr = parseResults(k, type2)
        s2 = kr.split(";")
        suggestions.append(s2[0])

        left_anchored_matches.append(lr)
        keyword_matches.append(kr)
        suggested.append(";".join(suggestions))
    csv["Suggested Term"] = suggested
    csv["Left Anchored Matches"] = left_anchored_matches
    csv["Keyword Matches"] = keyword_matches

if __name__ == "__main__":
    # need to download separate filtered version for this
    multiSearch("../unlinked-subjects-web-current2.csv", "../unlinked-subjects/unlinked-deep-search-1.csv")
