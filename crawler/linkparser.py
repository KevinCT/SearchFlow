import requests
from bs4 import BeautifulSoup

from crawler.debug import debug

MAIN_URL = ""
SUB_URL = ""


class LinkParser:

    def __init__(self):
        self.dbug = debug(name=self.__class__, flag=True)

    def link_info(self, url, flag=False):
        try:
            url_ = requests.get(url)
            soup = BeautifulSoup(url_.content, "html.parser")
            if flag:
                return True, soup
        except Exception as e:
            self.dbug.debug_print(e + " URL: " + url)

    def question_id_extractor(self, page_url):
        question_id_info = []
        flag, soup = self.link_info(page_url, flag=True)
        main_bar = BeautifulSoup(str(soup.find("div", {"id": "mainbar"})))
        if flag:
            for q_id in main_bar.find_all("div", {"class": "question-summary"}):
                question_id = str(q_id.get("id")).split("-")[2]
                question_id_info.append({"question_id": question_id, "crawled_info": False})
        self.dbug.debug_print(question_id_info)


lp = LinkParser()
lp.question_id_extractor(page_url="https://stackoverflow.com/questions?sort=newest&page=10000")
