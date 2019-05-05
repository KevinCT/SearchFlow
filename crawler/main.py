import threading
from queue import Queue

from crawler.spider import URLSpider


Start_URL = ''
Queued_file = ''
Crawled_file = ''
Number_of_threads = 4
queue = Queue()
#first Spider
URLSpider()


# Create worked threads (die when main exits)
def create_workers():
    for _ in range(Number_of_threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# do the next job in the queue
def work():
    while True:
        url = queue.get()
        URLSpider.crawled_page(threading.current_thread().name, url)
        queue.task_done()

# Each queued link is a new job
def create_jobs():
    # set of links
   ##    queue.put(link)
    queue.join()
    crawl()

# Check the URL DB if there are items in the queue the scrawl it
def crawl():
    queued_links = ''#from db
    if len(queued_links) > 0:
        print(str(len(queued_links))+ ' links in the queue')
        create_jobs()

create_workers()
crawl()