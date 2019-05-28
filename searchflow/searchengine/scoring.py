import numpy as np
import queue

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
        terms.update(documents[document].keys())
    termsDictionary = dict.fromkeys(terms, 0)
    for document in documents:
        tfDictionaries[document] = (termFrequency(termsDictionary, documents[document]))
    for dictionary in tfDictionaries:
        tfDictionary = tfDictionaries[dictionary]
        tempDictionary = {}
        for term in tfDictionary:
            tempDictionary[term] = tfDictionary[term] * idfDictionary[term]
        tfidfList.append((dictionary, tempDictionary))

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
    #scoreList = []
    queryScore = list(tfidfList.pop(-1)[1].values())
    scoreQueue = queue.PriorityQueue()

    for tpl in tfidfList:
        vectorList.append((tpl[0], list(tpl[1].values())))
    for tpl in vectorList:
        #scoreList.append((-cosineSimilarity(tpl[1], queryScore), tpl[0]))
        scoreQueue.put((-cosineSimilarity(tpl[1], queryScore), tpl[0]))
    return scoreQueue


def test():
    doc1 = "django is a web framework for python"
    doc2 = "bootstrap is a popular web framework"

    documents = {}
    documents['doc1'] = dict.fromkeys(doc1.split(), 1)
    documents['doc2'] = dict.fromkeys(doc2.split(), 1)

    scores = getScore( {'a': 1.0, 'framework': 1.0, 'is': 1.0, 'django': 1.6931471805599454, 'web': 1.0,
                     'for': 1.6931471805599454, 'python': 1.6931471805599454, 'popular': 1.6931471805599454,
                     'bootstrap': 1.6931471805599454}, documents, ["python", "framework"])
    while True:
        print(scores.get())

#test()
