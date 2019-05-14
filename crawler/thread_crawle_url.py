import threading
import time

from crawler.debug import debug
from crawler.linkparser import LinkParser
from crawler.linkparser import page_url_creator
from crawler.mongodb import Connection

db_connection = Connection(db_name="StackOverflow", db_col="Multi_Thread_URL")
START_PAGE = 0
END_PAGE = 150000
TOTAL_PAGES = END_PAGE - START_PAGE
Thread_Num = 8

def thread_url(page_id):
    debug(thread_url, flag=True).debug_print("Thread %s: starting" + threading.current_thread().name)
    page_url = page_url_creator(page_id=page_id)
    question_ids = LinkParser().question_id_extractor(page_url=page_url)
    debug(thread_url, flag=True).debug_print(str(question_ids))
    data_process_for_db(page_id=page_id, data=question_ids)
    debug(thread_url, flag=True).debug_print("Thread %s: finishing" + threading.current_thread().name)


def data_process_for_db(page_id, data):
    for d in data:
        info = {"Question": d, "Answer": {}, "crawled": False}
        db_connection.insert(info)
    debug(data_process_for_db, flag=True).debug_print("Insert Done for page " + str(page_id))


if __name__ == '__main__':
    threads = list()
    time1 = time.time()
    for count in range(END_PAGE, START_PAGE, -8):
        t1 = threading.Thread(target=thread_url, args=(count - 1,))
        t2 = threading.Thread(target=thread_url, args=(count - 2,))
        t3 = threading.Thread(target=thread_url, args=(count - 3,))
        t4 = threading.Thread(target=thread_url, args=(count - 4,))
        t5 = threading.Thread(target=thread_url, args=(count - 5,))
        t6 = threading.Thread(target=thread_url, args=(count - 6,))
        t7 = threading.Thread(target=thread_url, args=(count - 7,))
        t8 = threading.Thread(target=thread_url, args=(count - 8,))

        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        threads.append(t4)
        threads.append(t5)
        threads.append(t6)
        threads.append(t7)
        threads.append(t8)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()

        for index, thread in enumerate(threads):
            thread.join()
        count += 1
    print("Final Time:", time.time() - time1)
