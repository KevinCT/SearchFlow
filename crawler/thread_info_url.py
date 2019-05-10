import threading
import time

from crawler.debug import debug
from crawler.mongodb import Connection
from crawler.stackoverflowdata import StackOverflowInfo

db_connection = Connection(db_name="StackOverflow", db_col="Multi_Thread_URL")


def thread_info_url(question_id):
    debug(thread_info_url, flag=True).debug_print("Thread %s: starting" + threading.current_thread().name)
    # debug(thread_info_url,flag=True).debug_print(str(question_ids))
    data_process_for_db(question_id=question_id)
    debug(thread_info_url, flag=True).debug_print("Thread %s: finishing" + threading.current_thread().name)


def data_process_for_db(question_id):
    stackoverflow_info = StackOverflowInfo(question_id=question_id)
    data = stackoverflow_info.all_info()
    if db_connection.db_col.update_one({'Question.question_id': question_id, 'crawled': False}, {
        '$set': {'Question': data['Question'], 'Answer': data['Answer'], 'crawled': True}}):
        debug(data_process_for_db, flag=True).debug_print("Insert Done for question " + str(question_id))
    else:
        debug(data_process_for_db, flag=True).debug_print("Could not insert Done for question " + str(question_id))


# def Test_data_process_for_db():
#     page_url = question_url_creator(page_id=1)
#     question_ids = LinkParser().question_id_extractor(page_url=page_url)
#     data_process_for_db(page_id=1, data=question_ids)


if __name__ == '__main__':
    threads = list()
    time1 = time.time()
    # data_process_for_db(56075703)
    count = 0
    while db_connection.db_col.find({'crawled': False}).count() > 0:
        mylist = db_connection.db_col.find({'crawled': False}).limit(4)
        data = [x['Question'].get('question_id') for x in mylist]
        t1 = threading.Thread(target=thread_info_url, args=(data[0],))
        t2 = threading.Thread(target=thread_info_url, args=(data[1],))
        t3 = threading.Thread(target=thread_info_url, args=(data[2],))
        t4 = threading.Thread(target=thread_info_url, args=(data[3],))

        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        threads.append(t4)

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        count += 1
        if count == 20:
            print("Going to sleep")
            time.sleep(1)
            count = 0
        for index, thread in enumerate(threads):
            thread.join()
    print("Final Time:", time.time() - time1)
