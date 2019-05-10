import time

from nltk.corpus import wordnet
from nltk.corpus import words
from spellchecker import SpellChecker


def spell_check_test():
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


class Index:

    def __init__(self, file):
        self.file = file
        self.map = dict()

    def update_dict(self, key, posting_list):
        self.map[key] = posting_list

    def get_posting_list(self, key):
        return self.map[key]

    def populate_index(self, posts):

        # remove colons, dots etc
        for index in range(0, len(posts)):
            for word in posts[index].split():
                if word in self.map:
                    self.map[word].update(index)

    def intersect(self, keys):
        doc_scores = dict()
        lists = []

        for key in keys:
            temp_node = self.map[key].start
            if temp_node is not None:
                lists.append(temp_node)
                # list_score.append(temp_node.gap)

        # could use a max heap
        for elem in lists:
            current_score = elem.gap
            while elem is not None:
                if current_score in doc_scores:
                    doc_scores[current_score] = doc_scores[current_score] + self.get_score(elem)
                else:
                    doc_scores[current_score] = self.get_score(elem)
                elem = elem.next
                if elem is not None:
                    current_score += elem.gap

        return doc_scores

    # return tf-idf score of element
    def get_score(self, elem):
        return elem.frequency


class PostingList:

    def __init__(self, start_position):
        self.start = PostingNode(start_position, None, None)

    def update(self, position):
        if position < self.start.gap:
            self.start.prev = PostingNode(position, None, self.start)
            self.start.prev.next = self.start
            self.start.gap = self.start.gap - position
            self.start = self.start.prev
        elif position == self.start.gap:
            self.start.frequency += 1
        else:
            self.start.update(position)


class PostingNode:

    def __init__(self, gap, prev=None, next=None, frequency=1):
        self.gap = gap
        self.prev = prev
        self.next = next
        self.frequency = frequency

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
            if current_score == position:
                current.frequency = current.frequency + 1
                return
            if current.next is not None:
                current = current.next
                current_score += current.gap
            else:
                current.next = PostingNode(position - current_score, current, None)
                return

        current.prev.next = PostingNode(position - current_score + current.gap, current.prev, current)
        current.prev = current.prev.next
        current.gap = current.gap - current.prev.gap


def test_method():
    a = [5, 4, 6, -8, 1, 6, 91, 53, 3, 3, 3, 43, 1001, -8, 0]
    test_a = PostingList(53)
    for elem in a:
        test_a.update(elem)
    b = [5, 4, 6, 2, 1, 63, 911, 503, 437, 101, 8, 0]
    test_b = PostingList(91)
    for elem in b:
        test_b.update(elem)

    dictionary = Index("test")
    dictionary.update_dict("test_a", test_a)
    dictionary.update_dict("test_b", test_b)

    test = dictionary.intersect(["test_a", "test_b"])

    print(test)
    test_a = test_a.start
    current_score = 0
    while test_a is not None:
        current_score += test_a.gap
        print(current_score)
        print(test_a.frequency)
        test_a = test_a.next


test_method()
