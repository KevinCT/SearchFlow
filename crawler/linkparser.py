import requests
from bs4 import BeautifulSoup

from crawler.debug import debug

MAIN_URL = "https://stackoverflow.com"
SUB_URL = ""


# given the question id this function creates the url
def question_url_creator(questionID):
    """
    :param questionID:
    :return: string URL
    """
    url = MAIN_URL + "/questions/" + str(questionID)
    return url


# check if a link is working or not
def url_link_status(url):
    """
    :param url:
    :return: boolean
    """
    return requests.get(url).status_code == 200


class LinkParser:
    """
    This is helper class.
    Helps to parse and process url.
    """

    def __init__(self):
        self.dbug = debug(name=self.__class__, flag=True)

    def link_info(self, url):
        """"
        :param url: string is an URL
        :return BeautifulSoup: as string of an URL
        """
        try:
            url_ = requests.get(url)
            return BeautifulSoup(url_.content, "html.parser")
        except Exception as e:
            self.dbug.debug_print(e + " URL: " + url)

    def question_id_extractor(self, page_url):
        """"
        :param page_url: string
        :return list: of question IDs
        """
        question_id_info = []
        flag, soup = self.link_info(page_url, flag=True)
        main_bar = BeautifulSoup(str(soup.find("div", {"id": "mainbar"})))
        if flag:
            for q_id in main_bar.find_all("div", {"class": "question-summary"}):
                question_id = str(q_id.get("id")).split("-")[2]
                question_id_info.append({"question_id": question_id, "crawled_info": False})
        self.dbug.debug_print(question_id_info)
        return question_id_info


"""
All the test functions are here
"""


def Test_question_id_extractor():
    # expecting list of numbers as output
    lp = LinkParser()
    lp.question_id_extractor(page_url="https://stackoverflow.com/questions?sort=newest&page=10000")


def Test_url_link_status(url="https://stackoverflow.com/questions/42310364/"):
    # expecting True as output
    print(url_link_status(url))


def Test_question_url_creator(question_id=2063184):
    # expecting url as output
    print(question_url_creator(question_id))
