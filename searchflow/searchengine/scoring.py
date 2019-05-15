import numpy as np

#do we consider the whole vector or only the terms from the query?
def cosineSimilarity(a, b):
    dot = np.dot(a, b)
    normalizeA = np.linalg.norm(a)
    normalizeB = np.linalg.norm(b)
    cos = dot / (normalizeA * normalizeB)
    return cos


def termFrequency(termsDictionary, document):
    documentLength = sum(document.values())
    frequencyDictionary = termsDictionary.copy()
    for term in document:
        if term in frequencyDictionary.keys():
            frequencyDictionary[term] = document.get(term)/documentLength
    return frequencyDictionary


def tfidf(idfDictionary, documents):
    tfDictionaries = {}
    tfidfList = []
    terms = set()
    for document in documents:
        print(document)
        terms.update(documents[document].keys())
    termsDictionary = dict.fromkeys(terms, 0)
    for document in documents:
        tfDictionaries[document] = (termFrequency(termsDictionary, documents[document]))
    for tfDictionary in tfDictionaries:
        tfDictionary = tfDictionaries[tfDictionary]
        tempDictionary = {}
        for term in tfDictionary:
            tempDictionary[term] = tfDictionary[term] * idfDictionary[term]

        tfidfList.append(tempDictionary)

    return tfidfList

#documents is a dictionary of dictionary containing frequencies of each term
#query is a list of strings containing the terms
def getScore(idfDictionary, documents, query):
    queryDictionary = {}
    for term in query:
        if term in queryDictionary:
            queryDictionary[term] += 1
        else:
            queryDictionary[term] = 1

    documents['query'] = queryDictionary
    tfidfList = tfidf(idfDictionary, documents)
    vectorList = []
    scoreList = []
    for dictionary in tfidfList:
        vectorList.append(list(dictionary.values()))
    for vector in vectorList[:-1]:
        scoreList.append(cosineSimilarity(vector, vectorList[-1]))

    return scoreList


def test():
    doc1 = "django is a web framework for python"
    doc2 = "bootstrap is a popular web framework"

    documents = {}
    documents['doc1'] = dict.fromkeys(doc1.split(), 1)
    documents['doc2'] = dict.fromkeys(doc2.split(), 1)

    print(getScore( {'a': 1.0, 'framework': 1.0, 'is': 1.0, 'django': 1.6931471805599454, 'web': 1.0, 'for': 1.6931471805599454, 'python': 1.6931471805599454, 'popular': 1.6931471805599454, 'bootstrap': 1.6931471805599454}
    , documents, ["python", "framework"]))

#test()
