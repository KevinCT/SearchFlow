import numpy as np

#do we consider the whole vector or only the terms from the query?
def cosineSimilarity(a, b):
    dot = np.dot(a, b)
    normalizeA = np.linalg.norm(a)
    normalizeB = np.linalg.norm(b)
    cos = dot / (normalizeA * normalizeB)
    return cos


def termFrequency(termsDictionary, document):
    document = document.split()
    frequencyDictionary = termsDictionary.copy()
    for term in document:
        if term in frequencyDictionary.keys():
            frequencyDictionary[term] += 1

    for term in frequencyDictionary:
        frequencyDictionary[term] = frequencyDictionary[term]/len(document)
    return frequencyDictionary


def tfidf(idfDictionary, documents):
    tfDictionaries = {}
    tfidfList = []
    terms = set()
    for document in documents:
        terms.update(document.split())
    termsDictionary = dict.fromkeys(terms, 0)
    for document in documents:
        tfDictionaries[document] = (termFrequency(termsDictionary, document))
    for tfDictionary in tfDictionaries:
        tfDictionary = tfDictionaries[tfDictionary]
        tempDictionary = {}
        for term in tfDictionary:
            tempDictionary[term] = tfDictionary[term] * idfDictionary[term]
        tfidfList.append(tempDictionary)

    return tfidfList

#documents is a list of strings where each string is the text.
def getScore(idfDictionary, documents, query):
    documents.append(query)
    tfidfList = tfidf(idfDictionary, documents)
    vectorList = []
    scoreList = []
    for dictionary in tfidfList:
        vectorList.append(list(dictionary.values()))
    for vector in vectorList[:-1]:
        scoreList.append(cosineSimilarity(vector, vectorList[-1]))

    return scoreList




#print(getScore( {'a': 1.0, 'framework': 1.0, 'is': 1.0, 'django': 1.6931471805599454, 'web': 1.0, 'for': 1.6931471805599454, 'python': 1.6931471805599454, 'popular': 1.6931471805599454, 'bootstrap': 1.6931471805599454}
#, ["django is a web framework for python", "bootstrap is a popular web framework"], "python framework" ))
