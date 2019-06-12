import nltk

from crawler.mongodb import Connection  # remove SearchFlow

nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer

top_search_db = Connection(db_name="StackOverflow", db_col="top_search")
db = Connection(db_name="StackOverflow", db_col="final_processed_data_without_code")

def topSearch():
    list = []
    for item in top_search_db.db_col.find().sort("count", -1).limit(20):
        list.append(item.get("tag_name"))
    return list


def insertTop(data):
    tokens = RegexpTokenizer(r'\w+').tokenize(data)
    for i in tokens:
        i = i.lower().strip()
        if i in db.get_distinct_data(data_type="Question.question_tags"):
            if top_search_db.data_exist(data_type="tag_name", data=i):
                info = top_search_db.db_col.find_one({"tag_name": i})
                top_search_db.db_col.update_one({'tag_name': i}, {'$set': {'count': info.get("count") + 1}})
            else:
                top_search_db.db_col.insert_one({"tag_name": i, "count": 1})


def getValue(question_id, data_type):
    return Connection(db_col="Bigger_Test_Data",db_name="StackOverflow").get_data_of_question_id(question_id, data_type)