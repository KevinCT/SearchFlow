import math
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

def idf(termsDictionary, documents):
    countDictionary = termsDictionary.copy()
    idfDictionary = {}
    for document in documents:
        document = document.split()
        for term in document:
            countDictionary[term] += 1
    for term in countDictionary:
        idfDictionary[term] = math.log(len(documents))/countDictionary[term]
    return idfDictionary



def tfidf(documents):
    terms = set()
    for document in documents:
        terms.update(document.split())
    termsDictionary = dict.fromkeys(terms, 0)
    tfDictionaries = {}
    countDictionary = {}
    idfDictionary= {}
    tfidfList = []

    for document in documents:
        tfDictionaries[document] = (termFrequency(termsDictionary, document))
    for tfDictionary in tfDictionaries:
        tfDictionary = tfDictionaries[tfDictionary]

        for term in tfDictionary:
            if tfDictionary[term] > 0:
                if term in countDictionary:
                    countDictionary[term] += 1
                else:
                    countDictionary[term] = 1

    for term in countDictionary:
        idfDictionary[term] = 1 + math.log(len(documents) / countDictionary[term])
    for tfDictionary in tfDictionaries:
        tfDictionary = tfDictionaries[tfDictionary]
        tempDictionary = {}
        for term in tfDictionary:
            tempDictionary[term] = tfDictionary[term] * idfDictionary[term]
        tfidfList.append(tempDictionary)

    return [tfidfList, idfDictionary]


def test(query):
    documents = [ "django is a web framework for python", "bootstrap is a popular web framework"]
    result = tfidf(documents)
    tfidfList = result[0]
    idf = result[1]

    terms = set()
    for document in documents:
        terms.update(document.split())
    termsDictionary = dict.fromkeys(terms, 0)
    tf = termFrequency(termsDictionary, query)
    tfidfquery = {}
    for term in tf:
        tfidfquery[term] = tf[term] * idf[term]
    vectorList = []
    vectorList.append(list(tfidfquery.values()))
    for dictionary in tfidfList:
        vectorList.append(list(dictionary.values()))


 #   print(cosineSimilarity(np.array(vectorList[0]), np.array(vectorList[1])))
#    print(cosineSimilarity(np.array(vectorList[0]), np.array(vectorList[2])))

    return [cosineSimilarity(np.array(vectorList[0]), np.array(vectorList[1])), query]



#test('python framework')
