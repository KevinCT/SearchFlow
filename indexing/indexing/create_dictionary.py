import time

from nltk.corpus import wordnet
from nltk.corpus import words
from spellchecker import SpellChecker

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

    def __init__(self, file):
        self.file = file

    def update_dict(self, key, posting_list):
        map[key] = posting_list

    def intersect(self, keys):
        '''
        lists = []
        list_score = []

        for key in keys:
            temp_node = map[key].start
            if temp_node is not None:
                lists.append(temp_node)
                list_score.append(temp_node.gap)

        min_score = list_score[0]
        min_index = 0
        current_score
        for x in range(1, len(list_score)):
            if list_score[x] < min_score:
                min_score = list_score[x]
                min_index

        while len(lists) != 0:



        query_dict = dict()

        for key in keys:
            score = 0
            posting_list = map[key]

            while posting_list is not None:
                score += test.gap
                print(score)
                test = test.next
        return map[keys[0]]
        '''

        doc_scores = dict()
        lists = []

        for key in keys:
            temp_node = map[key].start
            if temp_node is not None:
                lists.append(temp_node)
                # list_score.append(temp_node.gap)

        # could use a max heap
        for elem in lists:
            current_score = elem.gap
            while elem is not None:
                if doc_scores[current_score] is not None:
                    doc_scores[current_score] = doc_scores[current_score] + self.get_score(elem)
                else:
                    doc_scores[current_score] = self.get_score(elem)

    # return tf-idf score of element
    def get_score(self, elem):
        return 1


class PostingList:

    def __init__(self, start_position):
        self.start = PostingNode(start_position, None, None)

    def update(self, position):
        if position <= self.start.gap:
            self.start.prev = PostingNode(position, None, self.start)
            self.start.prev.next = self.start
            self.start.gap = self.start.gap - position
            self.start = self.start.prev
        else:
            self.start.update(position)


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


a = [5, 4, 6, 2, 1, 6, 91, 53, 3, 3, 3, 43, 1001, -8, 0]
test = PostingList(98)

for up in a:
    test.update(up)

score = 0
test = test.start
while test is not None:
    score += test.gap
    print(score)
    test = test.next
