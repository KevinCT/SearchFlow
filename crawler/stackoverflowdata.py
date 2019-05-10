import dateutil.parser
from bs4 import BeautifulSoup

from crawler.debug import debug
from crawler.linkparser import LinkParser
from crawler.linkparser import question_url_creator
from crawler.mongodb import Connection


# import platform
# import sys
# if platform.system().lower() in ['linux', 'darwin']:
#     # sys.setdefaultencoding() does not exist, here!
#     reload(sys)  # Reload does the trick!
#     sys.setdefaultencoding('UTF8')

class StackOverflowInfo:

    def __init__(self, question_id):
        self.dbug = debug(name=self.__class__, flag=True)
        self.question_id = question_id
        self.page_soup = LinkParser().link_info(url=question_url_creator(self.question_id))

    def all_info(self):
        not_found = self.page_soup.find_all("h1", {"class": "fs-headline1 mb4"})
        self.dbug.debug_print("scraping question " + question_url_creator(self.question_id))
        if len(not_found) > 0:
            print("not found ", len(not_found))
            return {"Question": {"question_id": self.question_id, "question_text": None}, "Answer": {}}
        question_info = QuestionInfo(self.question_id).get_all_question_info(self.page_soup)
        answer_info = AnswersInfo(self.question_id).get_all_answer_info(self.page_soup)
        return {"Question": question_info, "Answer": answer_info}


class QuestionInfo:

    def __init__(self, question_id):
        self.dbug = debug(name=self.__class__, flag=True)
        self.question_id = question_id

    def get_all_question_info(self, page_soup):
        question_soup = BeautifulSoup(str(page_soup.find("div", {"class": "question"})))
        self.question_title = str(page_soup.find("title").text).split("-")[1].strip()
        self.question_ask_time = dateutil.parser.parse(str(page_soup.find("time").get("datetime")).strip())
        self.question_view = self.question_views(page_soup)
        self.question_tags = self.question_tags(question_soup)
        self.question_upvote = int(question_soup.find("div", {
            "class": "js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"}).text)
        self.question_text = str(question_soup.find("div", {"class": "post-text"}).text).strip()
        self.question_code = self.question_code(question_soup)
        self.related_questions = self.related_questions(page_soup)

        question_json = {"question_id": self.question_id, "question_title": self.question_title,
                         "question_asked_time": self.question_ask_time, "question_text": self.question_text,
                         "question_tags": self.question_tags, "question_views": self.question_view,
                         "question_upvote": self.question_upvote, "question_code": self.question_code,
                         "related_questions": self.related_questions}
        self.dbug.debug_print(question_json)
        return question_json

    def question_views(self, soup):
        views = soup.find_all("p", {"class": "label-key"})[3].text
        if str(views).split(" ")[0].strip().__contains__(','):
            return int(str(views).split(" ")[0].strip().replace(',', ''))
        return int(str(views).split(" ")[0].strip())

    def question_code(self, soup):
        question_code_arr = []
        for code in soup.find("div", {"id": "question"}).find_all("code"):
            question_code_arr.append(str(code.text).strip())
        return question_code_arr

    def question_tags(self, soup):
        tag_array = []
        tags = str(soup.find("div", {"class": "grid ps-relative d-block"}).text).strip().split(" ")
        for t in tags:
            tag_array.append(t)
        return tag_array

    def related_questions(self, soup):
        related_question_array = []
        related_questions_soup = BeautifulSoup(str(soup.find("div", {"class": "module sidebar-related"})))
        for rq in related_questions_soup.find_all("a", {"class": "question-hyperlink"}):
            related_question_array.append(
                {"related_question_id": int(str(rq.get("href")).split("/")[-2].strip()),
                 "related_question": str(rq.text).strip()})
        return related_question_array


class AnswersInfo:

    def __init__(self, question_id):
        self.dbug = debug(name=self.__class__, flag=True)
        self.question_id = question_id

    def get_all_answer_info(self, soup):
        answer_soup = BeautifulSoup(str(soup.find("div", {"id": "answers"})))
        self.total_answers = int(str(answer_soup.find("h2").get("data-answercount")).strip())
        self.answer_details, self.answer_code = self.answers_detail(self.total_answers, answer_soup)
        answer_json = {"total_answers": self.total_answers, "answer_code": self.answer_code,
                       "answers": self.answer_details}
        self.dbug.debug_print(answer_json)
        return answer_json

    def answers_detail(self, total_answers, answer_soup):
        answers_array = []
        answer_code_arr = []
        if int(total_answers) >= 1:
            for code in answer_soup.find_all("code"):
                answer_code_arr.append(str(code.text).strip())
            for ans in range(0, len(answer_soup.find_all("div", {"class": "answer"}))):
                ans_dict = {'answer_upvote': int(str(answer_soup.find_all("div", {
                    "class": "js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"})[
                                                         ans].text).strip()),
                            'answer': answer_soup.find_all("div", {"class": "post-text"})[ans].text}
                if answer_soup.find_all("div", {"class": "answer"})[ans].find("div", {
                    "class": "js-accepted-answer-indicator grid--item fc-green-500 ta-center p4"}) is not None:
                    ans_dict['answer_accepted'] = True
                else:
                    ans_dict['answer_accepted'] = False
                answers_array.append(ans_dict)
        return answers_array, answer_code_arr


def Test():
    connection = Connection(db_name="StackOverflow", db_col="Final_Test_Question_URL")
    test = StackOverflowInfo(56056337)
    info = test.all_info()
    print(info)
    connection.db_col.insert(info)
