import nltk

from crawler.mongodb import Connection  # remove SearchFlow

nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
import csv


top_search_db = Connection(db_name="StackOverflow", db_col="top_search")
db = Connection(db_name="StackOverflow", db_col="final_processed_data_without_code")
tag_db = Connection(db_name="StackOverflow", db_col="tag_dictionary")

def topSearch():
    list = []
    for item in top_search_db.db_col.find().sort("count", -1).limit(10):
        list.append(item.get("tag_name"))
    return list


def insertTop(data):
    data = str(data).lower()
    tokens = RegexpTokenizer(r'\w+').tokenize(data)
    for i in tokens:
        i = i.lower().strip()
        if i in tag_db.get_distinct_data(data_type="TagName"):
            if top_search_db.data_exist(data_type="tag_name", data=i):
                info = top_search_db.db_col.find_one({"tag_name": i})
                top_search_db.db_col.update_one({'tag_name': i}, {'$set': {'count': info.get("count") + 1}})
            else:
                top_search_db.db_col.insert_one({"tag_name": i, "count": 1})


def save_to_excel_performance(results, query, query_type, time, flag):
    if flag:
        punc = [".", ",", "?"]
        for x in punc:
            if str(query).find(x):
                query = str(query).replace(x, "_")
        with open(query + '.csv', 'w', encoding="utf8", newline="") as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([query])
            for x in results:
                writer.writerow([x])
                writer.writerow([query_type])
            writer.writerow([time])
        writeFile.close()
