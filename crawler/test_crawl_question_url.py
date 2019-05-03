import requests
from bs4 import BeautifulSoup
import time
import json

main_url = "https://stackoverflow.com"
sub_url ="/questions?sort=newest&page="
question_url = []
def crawl_question_url(main_url,sub_url):
    for i in range (1,2):
        page_url = requests.get(main_url+sub_url+str(i))
        print("Page", i, "Status:", page_url)
        soup = BeautifulSoup(page_url.content, "html.parser")
        all_question_url = soup.find_all("a",{"class":"question-hyperlink"})
        for q in all_question_url:
            if not str(q["href"]).__contains__("https"):
                #print(main_url+q["href"])
                q_url = main_url+q["href"]
            else:
                #print(q["href"])
                q_url = q["href"]
            question_url.append(q_url)
    with open("stack_"+time.time(), 'w', encoding='utf8') as outfile:
        json.dump(question_url, outfile)

def detail_question_info(url):
    url_request = requests.get(url)
    question_data ={}
    if url_request.status_code == 200:
        soup = BeautifulSoup(url_request.content, "html.parser")

        question_data['question'] = str(soup.find("title").text).split("-")[1].strip()

        question_data['asked_date'] = soup.find("time").get("datetime")

        views = soup.find("p", {"class":"label-key"}).text
        for v in views:
            if str(v).__contains__("times"):
                question_data['question_views'] = str(v).split(" ")[0]
            break

        question_data['question_upvote'] = soup.find("div", {"class":"js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"}).text

        tag_array = []
        tags = str(soup.find("div", {"class":"grid ps-relative d-block"}).text).strip().split(" ")
        for t in tags:
            tag_array.append(t)
        question_data['tags'] = tag_array

        related_question_array = []
        related_questions = soup.find_all("div", {"class":"spacer js-gps-track"})
        print(related_questions)
        for rq in related_questions:
            print(rq.text)
            related_question_array.append(rq.text)
        question_data['related_questions'] = related_question_array

        question_text = soup.find("div", {"class":"post-text"})
        question_data['question_text'] = str(question_text.text).strip()

        answers_array = []
        answers = soup.find("div",{"id":"answers"})
        answer_soup = BeautifulSoup(str(answers))
        total_answers = answer_soup.find("h2").get("data-answercount")
        question_data['total_answers'] = total_answers
        if int(total_answers)>=1:
            for ans in range(0,int(total_answers)):
                ans_dict = {}
                ans_dict['answer_upvote'] = answer_soup.find_all("div", {"class":"js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"})[ans].text
                ans_dict['answer'] = answer_soup.find_all("div", {"class":"post-text"})[ans].text
                #if answer_soup.find_all("div", {"class":"js-accepted-answer-indicator grid--item fc-green-500 ta-center p4"})[ans]:
                 #   ans_dict['accepted'] = True
                answers_array.append(ans_dict)
        question_data['answer_info'] = answers_array
    return question_data
#crawl_question_url(main_url,sub_url)
#print(question_url.__len__())
print(detail_question_info("https://stackoverflow.com/questions/2612548/extracting-an-attribute-value-with-beautifulsoup"))