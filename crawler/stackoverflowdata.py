from bs4 import BeautifulSoup

from crawler.debug import debug
from crawler.linkparser import LinkParser
from crawler.linkparser import question_url_creator


class StackOverflowInfo:

    def __init__(self, page_id):
        self.dbug = debug(name=self.__class__, flag=True)
        self.page_soup = LinkParser.link_info(question_url_creator(page_id))

    def question_info(self):
        return


class QuestionInfo:

    def __init__(self, question_id):
        self.dbug = debug(name=self.__class__, flag=True)
        self.question_id = question_id

    def get_all_question_info(self, page_soup):
        question_soup = BeautifulSoup(str(page_soup.find("div", {"class": "question"})))
        self.question_title = str(page_soup.find("title").text).split("-")[1].encode('utf-8').strip()
        self.question_ask_time = page_soup.find("time").get("datetime")
        self.question_views = self.question_views(page_soup)
        self.question_tags = self.question_tags(question_soup)
        self.question_upvote = int(question_soup.find("div", {
            "class": "js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"}).text)
        self.question_text = str(question_soup.find("div", {"class": "post-text"}).text).strip()
        self.question_code = self.question_code(question_soup)
        self.related_questions = self.related_questions(page_soup)

    def question_views(self, soup):
        views = soup.find("p", {"class": "label-key"}).text
        for v in views:
            if str(v).__contains__("times"):
                return str(v).split(" ")[0]

    def question_code(self, soup):
        question_code_arr = []
        for code in soup.find("div", {"id": "question"}).find_all("code"):
            question_code_arr.append(code.text)
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
                {"related_question_id": str(rq.get("href")).split("/")[-2], "related_question": rq.text})
        return related_question_array


class AnswersInfo:

    def __init__(self, question_id):
        self.dbug = debug(name=self.__class__, flag=True)
        self.question_id = question_id

    def get_all_question_info(self, soup):
        answer_soup = BeautifulSoup(str(soup.find("div", {"id": "answers"})))
        self.total_answers = answer_soup.find("h2").get("data-answercount")
        self.answer_details, self.answer_code = self.answers_detail(self.total_answers, answer_soup)

    def answers_detail(self, total_answers, answer_soup):
        answers_array = []
        if int(total_answers) >= 1:
            answer_code_arr = []
            for code in answer_soup.find_all("code"):
                answer_code_arr.append(code.text)
            answer_code_arr
            for ans in range(0, len(answer_soup.find_all("div", {"class": "answer"}))):
                ans_dict = {'answer_upvote': answer_soup.find_all("div", {
                    "class": "js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"})[ans].text,
                            'answer': answer_soup.find_all("div", {"class": "post-text"})[ans].text}
                if answer_soup.find_all("div",
                                        {"class": "js-accepted-answer-indicator grid--item fc-green-500 ta-center p4"})[
                    ans] != None:
                    ans_dict['accepted'] = True
                else:
                    ans_dict['accepted'] = False
                answers_array.append(ans_dict)
        return answers_array, answer_code_arr
