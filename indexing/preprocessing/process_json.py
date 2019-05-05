# find all tags

import json

data = []
with open('C:\SearchFlow\SearchFlow\crawler\_Data.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

tags = []
for word in data:
    print(word['items'][0]['tags'])
    tags.append(word['items'][0]['tags'])

print(tags)