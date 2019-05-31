import numpy as np
import queue
import copy

#do we consider the whole vector or only the terms from the query?
def cosineSimilarity(a, b):
    dot = np.dot(a, b)
    normalizeA = np.linalg.norm(a)
    normalizeB = np.linalg.norm(b)
    cos = dot / (normalizeA * normalizeB)
    return cos


def termFrequency(termsDictionary, document):
    document = document.split()
    frequencyDictionary = copy.deepcopy(termsDictionary)
    for term in document:
        if term in frequencyDictionary.keys():
            frequencyDictionary[term] += 1

    for term in frequencyDictionary:
        frequencyDictionary[term] = frequencyDictionary[term]/len(document)

    return frequencyDictionary


def tfidf(idfDictionary, document):
    termsDictionary = copy.deepcopy(idfDictionary)
    termsDictionary = dict.fromkeys(termsDictionary, 0)
    tfDictionary = termFrequency(termsDictionary, document)
    tempDictionary = {}
    for term in tfDictionary:
        tempDictionary[term] = tfDictionary[term] * idfDictionary[term]
    return tempDictionary



#document is a string containing the text (preprocessed)
#query is a list of strings containing the terms
def getScore(idfDictionary, document, query):
    documentDictionary = tfidf(idfDictionary, document)
    queryWord = ''.join(query)
    queryDictionary = tfidf(idfDictionary, queryWord)
    queryVector = list(queryDictionary.values())
    documentVector = list(documentDictionary.values())

    return cosineSimilarity(documentVector, queryVector)


def getDocScore(idfDictionary, documents, query):
    scoreQueue = queue.PriorityQueue()
    for document in documents:
        score = 0
        for term in query:
            if term in documents[document]:
                score += documents[document][term]*idfDictionary[term]
        scoreQueue.put((-score, document))
    return scoreQueue


def test():



    doc1 = "django is a web framework for python"
    doc2 = "bootstrap is a popular web framework"

    documents = {}
    documents['doc1'] = dict.fromkeys(doc1.split(), 1)
    documents['doc2'] = dict.fromkeys(doc2.split(), 1)
    print(documents)

    scores = getDocScore( {'a': 1.0, 'framework': 1.0, 'is': 1.0, 'django': 1.6931471805599454, 'web': 1.0,
                     'for': 1.6931471805599454, 'python': 1.6931471805599454, 'popular': 1.6931471805599454,
                     'bootstrap': 1.6931471805599454}, {'doc1': {'python': 1, 'java': 2, 'framework': 2}, 'doc2': {'python': 3, 'framework': 1}}, ["python", "framework", "h3"])
    while True:
        print(scores.get())


#print(getScore( {'a': 1.0, 'framework': 1.0, 'is': 1.0, 'django': 1.6931471805599454, 'web': 1.0, 'for': 1.6931471805599454, 'python': 1.6931471805599454, 'popular': 1.6931471805599454, 'bootstrap': 1.6931471805599454}
#,"bootstrap is a popular web framework", "python framework"))


#test()
