from indexing.indexing import create_dictionary as cd
import csv

# create databases StackOverflow: Test_Data, question_title_index, tag_dictionary

results = []
with open("crawler/QueryResults.csv") as file:
    reader = csv.reader(file)
    for word in reader:
        results.append(word[0])

cd.push_terms(results)

cd.index_to_mongodb()

# cd.search(['test','hey','java'])