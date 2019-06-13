import requests
from bs4 import BeautifulSoup

from crawler.ProxyChinese import pool_of_proxy
from crawler.debug import debug

MAIN_URL = "https://stackoverflow.com"
SUB_URL = "/questions?sort=newest&page="


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


# creates url for a page
def page_url_creator(page_id):
    return MAIN_URL + SUB_URL + str(page_id)


class LinkParser:
    """
    This is helper class.
    Helps to parse and process url.
    """

    def __init__(self):
        self.dbug = debug(name=self.__class__, flag=False)

    def link_info(self, url):
        """"
        :param url: string is an URL
        :return BeautifulSoup: as string of an URL
        """
        proxy = '104.248.7.88:8080'  # default proxy
        while True:
            try:
                proxies = {
                    'http': 'http://' + proxy,
                    'https': 'http://' + proxy,
                }
                s = requests.Session()
                s.proxies = proxies
                url_ = requests.get(url)
                if url_.status_code != 200:
                    self.dbug.debug_print(f"Error In Status Code: {url_.status_code} URL: {url}")
                    if url_.status_code == 404:
                        self.dbug.debug_print(f"Sorry the data was deleted from the page...")
                        return BeautifulSoup(url_.content, "html.parser")
                    if url_.status_code == 429:
                        raise Exception
                    raise Exception
                if BeautifulSoup(url_.content, "html.parser").find("body").text == "None":
                    raise Exception
                return BeautifulSoup(url_.content, "html.parser")
            except Exception as e:
                self.dbug.debug_print(str(e) + " URL: " + url)
                proxy = next(pool_of_proxy())  # next proxy in the list
                self.dbug.debug_print("Changed the proxy for " + " URL: " + url + ", Proxy: " + proxy)

    def question_id_extractor(self, page_url):
        """"
        :param page_url: string
        :return list: of question IDs
        """
        question_id_info = []
        soup = self.link_info(page_url)
        main_bar = BeautifulSoup(str(soup.find("div", {"id": "mainbar"})))
        for q_id in main_bar.find_all("div", {"class": "question-summary"}):
            question_id = int(str(q_id.get("id")).split("-")[2])
            question_id_info.append({"question_id": question_id})
        self.dbug.debug_print(question_id_info)
        return question_id_info


"""
All the test functions are here
"""


def Test_question_id_extractor():
    # expecting list of numbers as output
    lp = LinkParser()
    print(lp.question_id_extractor(page_url="https://stackoverflow.com/questions?sort=newest&page=10000"))

def Test_url_link_status(url="https://stackoverflow.com/questions/42310364/"):
    # expecting True as output
    print(url_link_status(url))


def Test_question_url_creator(question_id=2063184):
    # expecting url as output
    print(question_url_creator(question_id))


Test_question_id_extractor()
