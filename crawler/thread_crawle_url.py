import threading
import time

from crawler.debug import debug
from crawler.linkparser import LinkParser
from crawler.linkparser import page_url_creator
from crawler.mongodb import Connection

db_connection = Connection(db_name="StackOverflow", db_col="Multi_Thread_URL")
START_PAGE = 201
END_PAGE = 400
TOTAL_PAGES = END_PAGE - START_PAGE


def thread_url(page_id):
    debug(thread_url, flag=True).debug_print("Thread %s: starting" + threading.current_thread().name)
    page_url = page_url_creator(page_id=page_id)
    question_ids = LinkParser().question_id_extractor(page_url=page_url)
    debug(thread_url, flag=True).debug_print(str(question_ids))
    data_process_for_db(page_id=page_id, data=question_ids)
    debug(thread_url, flag=True).debug_print("Thread %s: finishing" + threading.current_thread().name)


def data_process_for_db(page_id, data):
    all_link_data = []
    print(len(data))
    for d in data:
        info = {"Question": d, "Answer": {}, "crawled": False}
        db_connection.insert(info)
        # all_link_data.append(info)
    # db_connection.db_col.insert_many(all_link_data)
    debug(data_process_for_db, flag=True).debug_print("Insert Done for page " + str(page_id))


def Test_data_process_for_db():
    page_url = page_url_creator(page_id=1)
    question_ids = LinkParser().question_id_extractor(page_url=page_url)
    data_process_for_db(page_id=1, data=question_ids)


if __name__ == '__main__':
    threads = list()
    mylist = [x * 4 for x in range(int(START_PAGE / 4), int(END_PAGE / 4))]
    print(mylist)
    time1 = time.time()

    count = 0
    for index in mylist:
        t1 = threading.Thread(target=thread_url, args=(index + 1,))
        t2 = threading.Thread(target=thread_url, args=(index + 2,))
        t3 = threading.Thread(target=thread_url, args=(index + 3,))
        t4 = threading.Thread(target=thread_url, args=(index + 4,))

        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        threads.append(t4)

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        if count == 30:
            print("Going to sleep")
            time.sleep(2)
            count = 0
    for index, thread in enumerate(threads):
        thread.join()
    print("Final Time:", time.time() - time1)
