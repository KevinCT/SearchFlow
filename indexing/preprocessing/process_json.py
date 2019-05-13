# find all tags
from crawler.mongodb import Connection
import json

import pymongo as pm
conn = Connection(db_name="StackOverflow", db_col="Test_Data")


def create_json():
    data_arr = []
    for i in conn.db_col.find({}):
        data_arr.append(i)
    return data_arr

def tag_processing(file):
    tags = set()
    data = []
    data2 = []
    with open("C:/SearchFlow/SearchFlow/crawler/test.json", encoding="utf8") as f:
        data2.append(json.load(f))
        print(data2[0])
        for line in f:
            data.append(json.loads(line))
            print(data[0])
            break

def tag_file_edit(tags):
    file = open('tags.txt', 'a')
    for tag in tags:
        file.write(tag + '\n')
        print(tag)
    file.close()


#tag_processing('C:\SearchFlow\SearchFlow\crawler\test.json')
print(create_json()[0])
#tag_file_edit(tag_processing('C:\SearchFlow\SearchFlow\crawler\demo_data.json'))
