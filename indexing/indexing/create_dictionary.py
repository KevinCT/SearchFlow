import pymongo
import nltk
from nltk.corpus import words
from nltk.corpus import wordnet
from spellchecker import SpellChecker
import time
from vocabulary.vocabulary import Vocabulary as vb

spell = SpellChecker()


misspelled = spell.unknown(['jaka', 'is', 'hapenning', 'here'])

start = time.time()
syns = wordnet.synsets('car')
end = time.time()
print("first")
print(end - start)



for word in ['jaka', 'is', 'hapenning', 'here']:
    # Get the one `most likely` answer
    start = time.time()
    print(spell.correction(word))
    end = time.time()
    print("first")
    print(end - start)
    # Get a list of `likely` options

    start = time.time()
    print(spell.candidates(word))
    end = time.time()
    print("end")
    print(end - start)

word_list = words.words()
# prints 236736

print(word_list.index('base'))

# word_list.add(computer science terms)


class Dictionary:
    map = dict()


class PostingList:

    def __init__(self, start):
        self.start = start

    #def update(self, position):
    #    while


class PostingNode:

    def __init__(self, gap, prev=None, next=None):
        self.gap = gap
        self.prev = prev
        self.next = next

    def update(self, position):
        current_score = self.gap
        current = self

        if current.next is None and (position > current_score):
            current.next = PostingNode(position - current.gap, current)
            return

        if self.gap >= position:
            self.prev = PostingNode(position, None, current)
            self.gap = current_score - position
            return

        while current_score <= position:
            if current.next is not None:
                current = current.next
                current_score += current.gap
            else:
                current.next = PostingNode(position - current_score, current, None)
                return

        current.prev.next = PostingNode(position - current_score + current.gap, current.prev, current)
        current.prev = current.prev.next
        current.gap = current.gap - current.prev.gap


a = [5, 4, 6, 2, 1, 6, 91, 53, 3, 3, 3, 43, 1001]
test = PostingNode(98)

for up in a:
    test.update(up)
    while test.prev is not None:
        test = test.prev

currentscore = 0
while test is not None:
    currentscore += test.gap
    print(currentscore)
    test = test.next
