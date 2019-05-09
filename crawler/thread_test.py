import logging
import threading
import time

import requests
from bs4 import BeautifulSoup

main_url = "https://stackoverflow.com"
sub_url = "/questions?sort=newest&page="
all_data = []


def thread_function(name, num):
    logging.info("Thread %s: starting", name)
    url = url_process(main_url, sub_url, num)
    print(crawl_question_url(url), "page id ", num)
    logging.info("Thread %s: finishing", name)


def url_process(main_url, sub_url, page_id):
    return main_url + sub_url + str(page_id)


def crawl_question_url(url):
    question_url = []
    page_url = requests.get(url)
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
        question_url.append({'url': q_url, 'crawled_info': False})
    return question_url


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    mylist = [x * 3 for x in range(0, int(3 / 3))]
    print(mylist)

    time1 = time.time()
    for index in mylist:
        logging.info("Main    : create and start thread %d.", index)
        t1 = threading.Thread(target=thread_function, args=(1, index + 1))
        t2 = threading.Thread(target=thread_function, args=(2, index + 2))
        t3 = threading.Thread(target=thread_function, args=(3, index + 3))
        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        t1.start()
        t2.start()
        t3.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
