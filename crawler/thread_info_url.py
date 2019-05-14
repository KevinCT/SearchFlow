import threading
import time

from crawler.debug import debug
from crawler.mongodb import Connection
from crawler.stackoverflowdata import StackOverflowInfo

db_connection = Connection(db_name="StackOverflow", db_col="Multi_Thread_URL")


def thread_info_url(question_id):
    debug(thread_info_url, flag=True).debug_print("Thread " + threading.current_thread().name + " starting")
    data_process_for_db(question_id=question_id)
    time.sleep(1)
    debug(thread_info_url, flag=True).debug_print("Thread " + threading.current_thread().name + " finishing")


def data_process_for_db(question_id):
    stackoverflow_info = StackOverflowInfo(question_id=question_id)
    data = stackoverflow_info.all_info()
    if len(data['Question'].get('question_title')) > 2:
        if db_connection.db_col.update_one({'Question.question_id': question_id, 'crawled': False}, {
            '$set': {'Question': data['Question'], 'Answer': data['Answer'], 'crawled': True}}):
            debug(data_process_for_db, flag=True).debug_print("Insert Done for question " + str(question_id))
        else:
            debug(data_process_for_db, flag=True).debug_print("Could not insert Done for question " + str(question_id))
    else:
        pass

if __name__ == '__main__':
    threads = list()
    time1 = time.time()
    while db_connection.db_col.find({'crawled': False}).count() > 0:
        mylist = db_connection.db_col.find({'crawled': False}).limit(3)
        data = [x['Question'].get('question_id') for x in mylist]
        t1 = threading.Thread(target=thread_info_url, args=(data[0],))
        t2 = threading.Thread(target=thread_info_url, args=(data[1],))
        t3 = threading.Thread(target=thread_info_url, args=(data[1],))

        threads.append(t1)
        threads.append(t2)
        threads.append(t3)

        t1.start()
        t2.start()
        t3.start()

        for index, thread in enumerate(threads):
            thread.join()
    print("Final Time:", time.time() - time1)
