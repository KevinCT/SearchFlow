import copy
import queue

import numpy as np


# do we consider the whole vector or only the terms from the query?
def cosineSimilarity(a, b):
    dot = np.dot(a, b)
    normalizeA = np.linalg.norm(a)
    normalizeB = np.linalg.norm(b)

    cos = dot / (normalizeA * normalizeB)
    return cos


def termFrequency(termsDictionary, document):
    frequencyDictionary = copy.deepcopy(termsDictionary)
    for term in document:
        if term in frequencyDictionary.keys():
            frequencyDictionary[term] += 1

    for term in frequencyDictionary:
        frequencyDictionary[term] = frequencyDictionary[term] / len(document)

    return frequencyDictionary


def tfidf(idfDictionary, document, query, termsDictionary):
    tfDictionary = termFrequency(termsDictionary, document)
    tempDictionary = {}
    for term in tfDictionary:
        if term in idfDictionary:
            tempDictionary[term] = tfDictionary[term] * idfDictionary[term]
    #   elif term in document and term in query:
    #      tempDictionary[term] = 0
    return tempDictionary


# document is a string containing the text (preprocessed)
# query is a list of strings containing the terms
def getScore(idfDictionary, document, query):
    idfDictionary.pop('_id', None)
    print("-------------------getScore-----------------------")
    print(query)
    print(document)
    termsDictionary = dict((term, 0) for term in document)
    queryDictionary = tfidf(idfDictionary, query, query, termsDictionary)
    documentDictionary = tfidf(idfDictionary, document, query, termsDictionary)
    print(documentDictionary)
    print(queryDictionary)
    # print(documentDictionary)
    # print("QUERY")
    # print({x:y for x,y in queryDictionary.items() if y!=0})
    queryVector = list(queryDictionary.values())
    documentVector = list(documentDictionary.values())
    score = cosineSimilarity(documentVector, queryVector)
    print(score)
    # temp fix since rare terms are not added to idf in db
    # for term in termsDictionary:
    #     if term not in idfDictionary:
    #         if term in query:
    #             score += 0.05

    return score


# document is a dictionary of dictionaries containing the term frequency of each term related to the query
def getDocScore(idfDictionary, documents, query):
    idfDictionary.pop('_id', None)
    print("-------------------getDocScore-----------------------")
    print(documents)
    print(query)
    scoreQueue = queue.PriorityQueue()
    for document in documents:
        score = 0
        for term in query:
            if term in documents[document]:
                score += documents[document][term] * idfDictionary[term]
        scoreQueue.put((-score, document))
    #   scoreQueue.put((-1000, 0))
    return scoreQueue


def test():
    doc1 = "django is a web framework for python"
    doc2 = "bootstrap is a popular web framework"
    documents = {}
    documents['doc3'] = dict.fromkeys(doc1.split(), 1)
    documents['doc4'] = dict.fromkeys(doc2.split(), 1)
    print(documents)

    scores = getDocScore({'a': 1.0, 'framework': 1.0, 'is': 1.0, 'django': 1.6931471805599454, 'web': 1.0,
                          'for': 1.6931471805599454, 'python': 1.6931471805599454, 'popular': 1.6931471805599454,
                          'bootstrap': 1.6931471805599454},
                         {'doc1': {'python': 1, 'java': 2, 'framework': 2}, 'doc2': {'python': 3, 'framework': 1}},
                         ["python", "framework", "h3"])

    #  {'a': 1.0, 'framework': 1.0, 'is': 1.0, 'django': 1.6931471805599454, 'web': 1.0,
    #  'for': 1.6931471805599454, 'python': 1.6931471805599454, 'popular': 1.6931471805599454,
    #  'bootstrap': 1.6931471805599454}

    while True:
        print(scores.get())

# print(getScore( {'a': 1.0, 'framework': 1.0, 'is': 1.0, 'django': 1.6931471805599454, 'web': 1.0, 'for': 1.6931471805599454, 'python': 1.6931471805599454, 'popular': 1.6931471805599454, 'bootstrap': 1.6931471805599454}
# ,["django", "is", "a", "web", "framework", "for", "python"], ["python", "framework"]))


# ["bootstrap", "is", "a", "popular", "web", "framework"]

# test()
