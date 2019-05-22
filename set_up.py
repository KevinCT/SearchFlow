from indexing.indexing import create_dictionary as cd
import csv

results = []
with open("crawler/QueryResults.csv") as file:
    reader = csv.reader(file)
    for wordi in reader:
        results.append(wordi[0])

cd.push_terms(results)
