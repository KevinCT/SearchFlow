import requests
from bs4 import BeautifulSoup
import time
import json
import crawler.mongodb as mongodb
# encoding=utf8
import sys

#reload(sys)
sys.setdefaultencoding('utf8')

main_url = "https://stackoverflow.com"
sub_url = "/questions?sort=newest&page="
question_url = []

# just crawl the url
def crawl_question_url(main_url, sub_url):
    for i in range(1, 30000):
        page_url = requests.get(main_url + sub_url + str(i))
        print("Page", i, "Status:", page_url)
        soup = BeautifulSoup(page_url.content, "html.parser")
        all_question_url = soup.find_all("a", {"class": "question-hyperlink"})
        for q in all_question_url:
            if not str(q["href"]).__contains__("https"):
                # print(main_url+q["href"])
                q_url = main_url + q["href"]
            else:
                # print(q["href"])
                if not str(q_url).__contains__("stackoverflow.com"):
                    continue
                q_url = q["href"]
            question_url.append(q_url)
            url_connection.insert({'url': q_url, 'crawled_info': False})

    # with open("stack.json", 'a+') as outfile:
    #    json.dump(question_url, outfile)


def detail_question_info(url):
    if not str(url).__contains__("https://"):
        url = main_url + url
        print('after fix ', url)
    url_request = requests.get(url)
    question_data = {}
    try:
        if url_request.status_code == 200:
            soup = BeautifulSoup(url_request.content, "html.parser")
            try:
                question_data['question'] = str(soup.find("title").text).split("-")[1].encode('utf-8').strip()
            except Exception as e:
                question_data['question'] = "No question found"

            question_code_arr = []
            for code in soup.find("div", {"id": "question"}).find_all("code"):
                question_code_arr.append(code.text)

            question_data['question_code'] = question_code_arr
            try:
                question_data['asked_date'] = soup.find("time").get("datetime")
            except Exception as e:
                question_data['asked_date'] = "No asked date found"

            views = soup.find("p", {"class": "label-key"}).text
            for v in views:
                if str(v).__contains__("times"):
                    question_data['question_views'] = str(v).split(" ")[0]
                break

            question_data['question_upvote'] = soup.find("div", {
                "class": "js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"}).text

            tag_array = []
            tags = str(soup.find("div", {"class": "grid ps-relative d-block"}).text).strip().split(" ")
            for t in tags:
                tag_array.append(t)
            question_data['tags'] = tag_array

            related_question_array = []
            related_questions = soup.find_all("div", {"class": "spacer js-gps-track"})
            print(related_questions)
            for rq in related_questions:
                print(rq.text)
                related_question_array.append(rq.text)
            question_data['related_questions'] = related_question_array

            question_text = soup.find("div", {"class": "post-text"})
            question_data['question_text'] = str(question_text.text).strip()

            answers_array = []
            answers = soup.find("div", {"id": "answers"})
            answer_soup = BeautifulSoup(str(answers))
            total_answers = answer_soup.find("h2").get("data-answercount")
            question_data['total_answers'] = total_answers
            if int(total_answers) >= 1:
                for ans in range(0, len(answer_soup.find_all("div", {"class": "answer"}))):
                    ans_dict = {'answer_upvote': answer_soup.find_all("div", {
                        "class": "js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"})[ans].text,
                                'answer': answer_soup.find_all("div", {"class": "post-text"})[ans].text}
                    # if answer_soup.find_all("div", {"class":"js-accepted-answer-indicator grid--item fc-green-500 ta-center p4"})[ans]:
                    #   ans_dict['accepted'] = True

                    answer_code_arr = []

                    for code in answer_soup.find_all("code"):
                        answer_code_arr.append(code.text)

                    ans_dict['answer_code'] = answer_code_arr

                    answers_array.append(ans_dict)
            question_data['answer_info'] = answers_array
        return question_data
    except Exception as e:
        print(e)


def json_to_mongodb(file_name):
    json_file = open(file_name, 'r')
    data = json.loads(json_file.read())
    for d in data:
        url_connection.db_col.insert_one({'url': d, 'crawled_info': False})
    # print(d)
    print('finished')


def all_info():
    count = 1
    x = url_connection.db_col.delete_many({"url": {"$regex": ".stackexchange.com|mathoverflow.com|superuser.com"}})
    print("deleted data ", x.deleted_count)
    for info in url_connection.db_col.find({}):
        if not info['crawled_info']:
            print(count, info['url'])
            data = detail_question_info(info['url'])
            url_connection.db_col.update_one({'url': info['url']}, {'$set': {'info': data, 'crawled_info': 'true'}})
            print(item for item in url_connection.db_col.find({'url': info['url']}))
            count += 1


# crawl_question_url(main_url,sub_url)
# print(question_url.__len__())
url_connection = mongodb.Connection(db_name="StackOverflow", db_col="Test_Question_URL")
# print(detail_question_info("/questions/55990000/run-the-savina-code-https-github-com-shamsimam-savina"))
# json_to_mongodb("stack.json")
all_info()

