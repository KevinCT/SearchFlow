import nltk

from crawler.mongodb import Connection

nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

top_search_db = Connection(db_name="StackOverflow", db_col="top_search")


def topSearch():
    list = []
    for item in top_search_db.db_col.find().sort("count", -1).limit(20):
        list.append(item.get("tag_name"))
    return list


def insertTop(data):
    stop = set(stopwords.words('english'))
    tokens = RegexpTokenizer(r'\w+').tokenize(data)
    for i in tokens:
        i = i.lower().strip()
        if i not in stop:
            if top_search_db.data_exist(data_type="tag_name", data=i):
                info = top_search_db.db_col.find_one({"tag_name": i})
                top_search_db.db_col.update_one({'tag_name': i}, {'$set': {'count': info.get("count") + 1}})
            else:
                top_search_db.db_col.insert_one({"tag_name": i, "count": 1})


data = "What is wrong with the java code present here. I need to complete number to text converter as my assignment How can I using this variable? Unable to iterate through POJO MessagePack Convert Float to String without losing precision - Java"
#insertTop(data)
#print(topSearch())
