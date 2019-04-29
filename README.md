# Stoogle

tasks:
1. retrieve stack overflow data and propose logical data view (Pritom)
2. propose sample user queries matching the requirements; define page regions (relate results to task 1)
3. define ranking of answers
4. propose user experience (cmd, http, mobile app, whatever...)

to be discussed:
- what is a keyword (cf project description)?
- is our database static or dynamic? will we crawl in production? -> not necessary acording to project description

pm:
tuesdays 4.00 - 5.30 AND/OR
wednesdays 5.30 - 8.00 AND/OR
fridays after class

indexing and search technology  -- Apache Lucene (~ 83 MB)  -- Java	-- Python (Apache PyLucene)
	-- ElasticSearch (free trial) [basis of StackOverflow, sophisticated clustered solution -> possibly too much for our use case]
	-- Apache Solr [focus on distributed indexing -> maybe useful as a feature but not as basic functionality, however built on Apache Lucene]	-- IN: REST via JSON, XML, CSV or binary over HTTP / OUT: HTTP GET and receive JSON, XML, CSV or binary results
	
string matching capabilities	-- phrases, wildcards, joins, grouping	-- spell checking??	-- query suggestions??
