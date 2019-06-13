import math
import queue as q
import re
import time

from bson.objectid import ObjectId
from nltk.corpus import stopwords

from crawler.mongodb import Connection
from indexing.indexing import scoring as sc

conn_title = Connection(db_name="StackOverflow", db_col="final_processed_data")
conn_new_idf_title = Connection(db_name="StackOverflow", db_col="new_idf")
conn_title_test = Connection(db_name="StackOverflow", db_col="question_text_index")
connection_title = Connection(db_name="StackOverflow", db_col="id_to_url")
conn_dictionary = Connection(db_name="StackOverflow", db_col="tag_dictionary")
conn_idf_title = Connection(db_name="StackOverflow", db_col="idf_scores")

conn = Connection(db_name="StackOverflow", db_col="final_processed_data_without_code")
conn_new_idf = Connection(db_name="Index", db_col="new_idf")
conn_text_test = Connection(db_name="StackOverflow", db_col="question_text_real_final_index")
connection = Connection(db_name="Index", db_col="id_to_url")
conn_idf = Connection(db_name="Index", db_col="idf_scores")

conn_tag = Connection(db_name="StackOverflow", db_col="final_processed_data_without_code")
conn_new_idf_tag = Connection(db_name="Index_tag", db_col="new_idf")
conn_text_test_tag = Connection(db_name="StackOverflow", db_col="question_tag_final_index")
connection_tag = Connection(db_name="Index_tag", db_col="id_to_url")
conn_idf_tag = Connection(db_name="Index_tag", db_col="idf_scores")

conn_code = Connection(db_name="StackOverflow", db_col="final_processed_data_without_code")
conn_new_idf_code = Connection(db_name="Index_code", db_col="new_idf")
conn_text_test_code = Connection(db_name="StackOverflow", db_col="question_code_final_index")
connection_code = Connection(db_name="Index_code", db_col="id_to_url")
conn_idf_code = Connection(db_name="Index_code", db_col="idf_scores")


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


class Index:

    def __init__(self, file):
        self.file = file
        self.map = dict()
        self.word_list = set()
        stop_words = set(stopwords.words('english'))
        for i in conn_dictionary.db_col.find({}):
            word = i.get("TagName")
            if word not in stop_words:
                self.word_list.add(word)

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
                    self.map[word].update(position, 1/len(sentence))
                else:
                    self.update_dict(word, PostingList(position, 1/len(sentence)))

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

    def get_score(self, elem):
        return elem.frequency


class PostingList:

    def __init__(self, start_position, frequency=1):
        self.start = PostingNode(start_position, None, None, frequency)

    def update(self, position, frequency):
        if position < self.start.gap:
            self.start.prev = PostingNode(position, None, self.start)
            self.start.prev.next = self.start
            self.start.gap = self.start.gap - position
            self.start = self.start.prev
        elif position == self.start.gap:
            self.start.frequency += frequency
        else:
            self.start.update(position, frequency)

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

    def update(self, position, frequency):
        current_score = self.gap
        current = self

        if current.next is None and (position > current_score):
            current.next = PostingNode(position - current.gap, current)
            return

        if self.gap >= position:
            self.prev = PostingNode(position, None, current, frequency)
            self.gap = current_score - position
            return

        while current_score <= position:
            if current_score == position:
                current.frequency = current.frequency + frequency
                return
            if current.next is not None:
                current = current.next
                current_score += current.gap
            else:
                current.next = PostingNode(position - current_score, current, None, frequency)
                return

        current.prev.next = PostingNode(position - current_score + current.gap, current.prev, current, frequency)
        current.prev = current.prev.next
        current.gap = current.gap - current.prev.gap

    def has_next(self):
        return self.next is not None

    def serialize(self):
        return {"gap": self.gap, "frequency": self.frequency}


def deserialize_node(node_dict):
    return PostingNode(node_dict.get("gap"), None, None, node_dict.get("frequency"))


def deserialize_list(posting_array):
    start_node = deserialize_node(posting_array[0])
    posting_list = PostingList(start_node.gap, start_node.frequency)
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
        test_a = test_a.next


def clear_db():
    conn.db_col.delete_many({"Question.question_text": None})


def id_to_url(id_url=connection, top_conn=conn):
    counter = 0
    for i in top_conn.db_col.find({}):
        id_url.db_col.insert_one({"Question_ID": str(i["_id"]), "DocumentCount": counter})
        counter += 1
    print(counter)


def index_to_mongodb():
    question_title_index = Index("test")
    start_time = time.time()
    counter = 0
    cursor = conn.db_col.find({}, no_cursor_timeout=True).batch_size(10)
    for i in cursor:
        if i['Question']['question_text'] is not None:
            question_title_index.string_to_word_array(i['Question']['question_text'].lower(), counter)
            counter += 1
            print(counter)
    end_time = time.time()
    print(end_time - start_time)
    cursor.close()

    for word in question_title_index.map.keys():
        conn_text_test.db_col.insert_one({"PostingList": question_title_index.map.get(word).serialize(), "Term": word})


def deserialize_test():
    for i in conn_text_test.db_col.find({}):
        deserialize_list(i.get("PostingList")).start.gap


def static_intersect(keys, index):
    doc_scores = dict()
    term_posting = dict()
    index_connection = index
    tag_connection = Connection(db_name="StackOverflow", db_col="tag_dictionary")

    for key in keys:
        print(key)
        if tag_connection.db_col.count({"TagName": key}, limit=1) != 0:
            data = index_connection.db_col.find_one({"Term": key})
            if data is not None:
                temp_node = deserialize_list(data.get("PostingList")).start
                if temp_node is not None:
                    term_posting[key] = temp_node

    for key in term_posting.keys():
        elem = term_posting[key]
        current_score = elem.gap
        while elem is not None:
            if current_score in doc_scores:
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
    return total_docs / total


def push_idf(idf_conn=conn_idf, top_conn=conn, index=conn_text_test):
    total_docs = top_conn.db_col.count()
    print(total_docs)
    total_docs = math.log(float(total_docs))
    for i in index.db_col.find({}):
        idf = find_idf(deserialize_list(i.get("PostingList")).start, total_docs)
        idf_conn.db_col.insert_one({"Term": i.get("Term"), "IDF_Score": idf})


def pull_idf(query):
    query_to_idf = dict()

    for key in query:
        temp = conn_idf.db_col.find({"Term": key}).limit(1)
        for word in temp:
            if word is not None:
                query_to_idf[key] = word.get("IDF_Score")
    return query_to_idf


def new_idf_index(new_idf=conn_new_idf, old_idf=conn_idf):
    dictionary = dict()

    for term in old_idf.db_col.find({}):
        dictionary[term["Term"]] = term["IDF_Score"]

    new_idf.db_col.insert_one(dictionary)


def basic_search(query, index):
    return static_intersect(query, index)


def push_terms(tags):
    for tag in tags:
        conn_dictionary.db_col.insert_one({"TagName": tag})


# id_to_url()
def get_search(query, docs, index=conn_text_test, area="question_text", idf_conn=conn_new_idf, data_conn=conn,
               id_url=connection, region="text"):
    if region == "title":
        index = conn_title_test
        area = "question_title"
        idf_conn = conn_new_idf_title
        id_url = connection_title
        data_conn = conn_title
    elif region == "tag":
        index = conn_text_test_tag
        area = "question_tags"
        idf_conn = conn_new_idf_tag
        id_url = connection_tag
        data_conn = conn_tag
    elif region == "code":
        index = conn_text_test_code
        area = "question_code"
        idf_conn = conn_new_idf_code
        id_url = connection_code
        data_conn = conn_code

    pq = sc.getDocScore(idf_conn.db_col.find_one({}), basic_search(re.compile('\w+').findall(query), index),
                        re.compile('\w+').findall(query))
    x = pq.get(False)
    new_pq = q.PriorityQueue()
    for a in range(0, docs):
        doc_id = id_url.db_col.find_one({"DocumentCount": x[1]}).get("Question_ID")
        doc = data_conn.db_col.find_one({'_id': ObjectId(doc_id)})  # .get("Question").get("question_text")
        if area == 'question_code' or area == 'question_tags':
            print('got here')
            text = re.compile('\w+').findall(' '.join(str(v) for v in doc.get("Question").get(area)).lower())
        else:
            text = re.compile('\w+').findall(doc.get("Question").get(area).lower())

        idfs = idf_conn.db_col.find_one({})
        views =doc.get("Question").get("question_views")
        upvotes = doc.get("Question").get("question_upvote")
        related_questions = doc.get("Question").get("related_questions")
        answers = doc.get("Answer").get("total_answers")
        if answers > 0:
            accepted_answer = doc.get("Answer")["answers"][0].get("answer_accepted")
        else:
            accepted_answer = False

        data_tuple = (views, upvotes, related_questions, accepted_answer)



        score = sc.getScore(idfs, text, re.compile('\w+').findall(query), area, data_tuple)
        new_pq.put([-score, a, doc])
        x = pq.get()
    return new_pq
