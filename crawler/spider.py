import requests
from debug import debug
import crawler.mongodb as mongodb

page_url = "https://api.stackexchange.com/2.2/questions?page="+ +"&order=desc&sort=activity&site=stackoverflow"
class URLSpider:
    # Class variables (will be shared among all instance)
    project_name = ''
    base_url = ''
    domain_name = ''
    mongodb = mongodb.Connection(db_name="StackOverflow", db_col="Question_URL")
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        URLSpider.project_name = project_name
        URLSpider.base_url = base_url
        URLSpider.domain_name = domain_name
        self.dbug = debug(name=self.__class__, flag=True)
        self.boot()
        self.crawled_page('First Spider', URLSpider.base_url)

    @staticmethod
    def boot():
        URLSpider.queue = ""#mongodb.
        URLSpider.crawled =""#

    @staticmethod
    def crawled_page(thread_name, page_url):
        if page_url not in URLSpider.crawled:
            print(thread_name+ " now crawling "+page_url)
            print('Queue '+ str(len(URLSpider.queue)+' | Crawled '+ str(len(URLSpider.crawled))))
            URLSpider.add_links_to_queue(page_url)
            URLSpider.queue.remove(page_url)
            URLSpider.crawled.add(page_url)
            URLSpider.update_files()
    @staticmethod
    def add_links_to_queue(links):
        for page_id in links:
            if page_id in URLSpider.queue:
                continue
            if page_id in URLSpider.crawled:
                continue
            if URLSpider.domain_name not in page_id:
                continue
            URLSpider.queue.add(page_id)

    @staticmethod
    def update_files():
        # file same
        #set_to_file(URLSpider.queue, )
        #set_to_file(URLSpider.crawled, )
        pass