# find all tags

import json

import pymongo as pm

print(pm.version)


def tag_processing(file):
    tags = set()
    data = []
    with open(file, encoding="utf8") as f:
        for line in f:
            data.append(json.loads(line))
    for word in data:
        for tag in word['items'][0]['tags']:
            tags.add(tag)

    return tags


def tag_file_edit(tags):
    file = open('tags.txt', 'a')
    for tag in tags:
        file.write(tag + '\n')
        print(tag)
    file.close()


tag_file_edit(tag_processing('C:\SearchFlow\SearchFlow\crawler\_Data.json'))
