import pymongo
import nltk
from nltk.corpus import words
word_list = words.words()
# prints 236736

for word in word_list:
    print(word)
