import json

from crawler.mongodb import Connection

conn = Connection(db_name="StackOverflow", db_col="Multi_Thread_URL")


def get_json_data():
    data = []
    for i in conn.db_col.find({'crawled': True}).limit(100):
        db_data = {}
        db_data['Question'] = i.get("Question")
        data.append(i)

    with open("test.json", "w", encoding="utf8") as json_file:
        json.dump(data, json_file)


get_json_data()
