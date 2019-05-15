import re
import time

import pymongo
from nltk.corpus import wordnet
from nltk.corpus import words
from spellchecker import SpellChecker

from crawler.mongodb import Connection

conn = Connection(db_name="StackOverflow", db_col="Test_Data")
conn_title_test = Connection(db_name="StackOverflow", db_col="question_title_test")
connection = Connection(db_name="StackOverflow", db_col="id_to_url")
connection_url = Connection(db_name="StackOverflow", db_col="url_to_id")
conn_dictionary = Connection(db_name="StackOverflow", db_col="tag_dictionary")
conn_idf = Connection(db_name="StackOverflow", db_col="idf_scores")


def create_json():
    data = {}
    data_arr = []
    position = 0
    for i in conn.db_col.find({}):
        i["position"] = position
        data_arr.append(i)
        data[i["Question"].get("question_id")] = i
        position += 1

    return data_arr


# Do spell check in a different thread
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


def create_dict():
    word_list = words.words()
    dictionary = dict()

    for word in word_list:
        dictionary[word] = None
        # print(dictionary[word])

    #for

#create_dict()


class Index:

    def __init__(self, file):
        self.file = file
        self.map = dict()
        self.word_list = words.words()

    def update_dict(self, key, posting_list):
        self.map[key] = posting_list

    def get_posting_list(self, key):
        return self.map[key]

    def string_to_word_array(self, sentence, position):
        self.populate_index(re.compile('\w+').findall(sentence), position)

    def populate_index(self, sentence, position):
        for word in sentence:
            if word in self.word_list:
                if word in self.map:
                    self.map[word].update(position)
                else:
                    self.update_dict(word, PostingList(position))

    def intersect(self, keys):
        doc_scores = dict()
        lists = []

        for key in keys:
            if key in self.map:
                temp_node = self.map[key].start
                if temp_node is not None:
                    lists.append(temp_node)
                    #   list_score.append(temp_node.gap)

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

    def serialize(self):
        temp_node = self.start
        serialized_list = [temp_node.serialize()]

        while temp_node.has_next():
            temp_node = temp_node.next
            serialized_list.append(temp_node.serialize())
        return serialized_list


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

    def has_next(self):
        return self.next is not None

    def serialize(self):
        return {"gap": self.gap, "frequency": self.frequency}


def deserialize_node(node_dict):
    # print(node_dict.get("gap"))
    return PostingNode(node_dict.get("gap"), None, None, node_dict.get("frequency"))


def deserialize_list(posting_array):
    posting_list = PostingList(deserialize_node(posting_array[0]).gap)
    current_node = posting_list.start
    for i in range(1, len(posting_array) - 1):
        current_node.next = deserialize_node(posting_array[i])
        current_node.next.prev = current_node
        current_node = current_node.next
    current_node.next = deserialize_node(posting_array[len(posting_array) - 1])
    current_node.next.prev = current_node
    return posting_list


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


def clear_db():
    conn.db_col.delete_many({"Question.question_text": None})


def add_word_to_dictionary():
    for word in words.words():
        #conn_dictionary.insert({"TagName": word}, {"TagName": word})
        conn_dictionary.db_col.insert_one({"TagName": {word: get_idf()}})


# def get_idf():


def id_to_url():
    counter = 0
    for i in conn.db_col.find({}):
        connection.db_col.insert_one({str(counter): i["Question"].get("question_id")})
        counter += 1


def url_to_id():
    counter = 0
    for i in conn.db_col.find({}):
        connection_url.db_col.insert_one({str(i["Question"].get("question_id")): counter})
        counter += 1


def index_to_mongodb():
    question_title_index = Index("test")
    start_time = time.time()
    counter = 0
    for i in conn.db_col.find({}):
        question_title_index.string_to_word_array(i['Question']['question_title'], counter)
        counter += 1
    end_time = time.time()
    print(end_time - start_time)

    for word in question_title_index.map.keys():
        conn_title_test.db_col.insert_one({"PostingList": question_title_index.map.get(word).serialize(), "Term": word})


def deserialize_test():
    for i in conn_title_test.db_col.find({}):
        print(deserialize_list(i.get("PostingList")).start.gap)
        #print()


def static_intersect(keys, index):
    doc_scores = dict()
    term_posting = dict()
    index_connection = Connection(db_name="StackOverflow", db_col=index)
    tag_connection = Connection(db_name="StackOverflow", db_col="tag_dictionary")

    for key in keys:
        if tag_connection.db_col.count({"TagName": key}, limit=1) != 0:
            data = index_connection.db_col.find_one({"Term": key})
            print(data)
            if data is not None:
                temp_node = deserialize_list(data.get("PostingList")).start
                if temp_node is not None:
                    term_posting[key] = temp_node
                    #   list_score.append(temp_node.gap)

    # could use a max heap for ranking
    for key in term_posting.keys():
        elem = term_posting[key]
        current_score = elem.gap
        while elem is not None:
            if current_score in doc_scores:
                temp_dict = doc_scores.get(current_score)
                if temp_dict is None:
                    doc_scores[current_score][key] = static_get_score(elem)
            else:
                doc_scores[current_score] = dict()
                doc_scores[current_score][key] = static_get_score(elem)
            elem = elem.next
            if elem is not None:
                current_score += elem.gap

    return doc_scores


def static_get_score(elem):
    return elem.frequency


def find_idf(posting_node, total_docs):
    total = 1
    while posting_node.has_next():
        total += 1
        posting_node = posting_node.next
    return total / total_docs


def push_idf():
    total_docs = conn_title_test.db_col.count()
    for i in conn_title_test.db_col.find({}):
        idf = find_idf(deserialize_list(i.get("PostingList")).start, total_docs)
        conn_idf.db_col.insert_one({"Term": i.get("Term"), "IDF_Score": idf})


#push_idf()


def basic_search(query):
    # posting_lists = []
    # for word in query:
    #    posting_lists.append(deserialize_list(conn_title_test.db_col.find_one({"Term": word}).get("PostingList")))

    return static_intersect(query, "question_title_test")


print(basic_search(["and", "java", "on", "swift", "the"]))

'''




data_file = create_json()
question_title_index = Index("test")

start_time = time.time()
for line in data_file:
    question_title_index.string_to_word_array(line['Question']['question_title'], line['position'])
end_time = time.time()
print(end_time - start_time)

start = time.time()
for x in range(0, 2):
    question_title_index.intersect(["stop", "new", "list"])
end = time.time()

print(end - start)
print(data_file[189])
'''
