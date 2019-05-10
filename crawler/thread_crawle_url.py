import threading

from crawler.debug import debug
from crawler.linkparser import LinkParser
from crawler.linkparser import page_url_creator
from crawler.mongodb import Connection

db_connection = Connection()
json_data = "{'Question': {'question_id': 56056337, 'question_title': 'How can I check if the date already exists using code Behind?', 'question_asked_time': '2019-05-09T09:34:28', 'question_tags': ['c#', 'sql-server'], 'question_views': 'None', 'question_upvote': 0, 'question_text': 'I have a date just one " 'DateOfyear' " and i want to check before inserting the date in the textbox is already exists in DB but using Code Behind in c#.\nI will give a example like what i want to do, i know is not the right code or what i need, but is just a example because i don\'t want peoples to past or give solution with SQLCommand /SqlServer and other thing i want something like that code and thanks.\n            DateTime InvoiceDateTo = new DateTime();\n            InvoiceDateFrom = Convert.ToDateTime(txtDatRiferiment.Text);\n            InvoiceDateTo = Convert.ToDateTime(txtDatRiferiment.Text);\n            if (InvoiceDateFrom == InvoiceDateTo)\n            {\n                errorMessage = vea.ErrorMessage;\n            }', 'question_code': ['            DateTime InvoiceDateTo = new DateTime();\n            InvoiceDateFrom = Convert.ToDateTime(txtDatRiferiment.Text);\n            InvoiceDateTo = Convert.ToDateTime(txtDatRiferiment.Text);\n            if (InvoiceDateFrom == InvoiceDateTo)\n            {\n                errorMessage = vea.ErrorMessage;\n            }\n'], 'related_questions': [{'related_question_id': '18932', 'related_question': 'How can I remove duplicate rows?'}, {'related_question_id': '52797', 'related_question': 'How do I get the path of the assembly the code is in?'}, {'related_question_id': '113045', 'related_question': 'How to return only the Date from a SQL Server DateTime datatype'}, {'related_question_id': '133031', 'related_question': 'How to check if a column exists in a SQL Server table?'}, {'related_question_id': '167576', 'related_question': 'Check if table exists in SQL Server'}, {'related_question_id': '659051', 'related_question': 'Check if a temporary table exists and delete if it exists before creating a temporary table'}, {'related_question_id': '1293330', 'related_question': 'How can I do an UPDATE statement with JOIN in SQL?'}, {'related_question_id': '11790710', 'related_question': 'If not exists then insert else show message “Already exists”'}, {'related_question_id': '13513932', 'related_question': 'Algorithm to detect overlapping periods'}, {'related_question_id': '21692193', 'related_question': 'Why not inherit from List<T>?'}]}, 'Answer': {'total_answers': '1', 'answer_code': ['if(InvoiceDateFrom.CompareTo(InvoiceDateTo) == 0){\n    errorMessage = vea.ErrorMessage;\n}\n'], 'answers': [{'answer_upvote': '0', 'answer': '\nYou can use the DateTime.compareTo method:\nif(InvoiceDateFrom.CompareTo(InvoiceDateTo) == 0){\n    errorMessage = vea.ErrorMessage;\n}\n\nMore info here.\n', 'answer_accepted': 'False'}]}}"
TOTAL_PAGES = 280000


def thread_url(page_id):
    debug(thread_url).debug_print("Thread %s: starting", threading.current_thread().name)
    page_url = page_url_creator(page_id=page_id)
    question_ids = LinkParser.question_id_extractor(page_url)
    debug(thread_url).debug_print(str(question_ids))
    debug(thread_url).debug_print("Thread %s: finishing", threading.current_thread().name)


def data_process_for_db(data):
    all_link_data = []
    print(len(data))
    for d in data:
        info = {"Question": {}, "Answer": {}, "crawled": False}
        info["Question"] = d
        # print(info)
        all_link_data.append(info)
    print(all_link_data[0])


def Test_data_process_for_db():
    page_url = page_url_creator(page_id=1)
    question_ids = LinkParser().question_id_extractor(page_url=page_url)
    data_process_for_db(question_ids)

if __name__ == '__main__':
    threads = list()
    mylist = [x * 4 for x in range(0, int(TOTAL_PAGES / 4))]

    print(len(mylist))

    Test_data_process_for_db()
    # time1 = time.time()
    # for index in mylist:
    #     t1 = threading.Thread(target=thread_url, args=(1, index + 1))
    #     t2 = threading.Thread(target=thread_url, args=(2, index + 2))
    #     t3 = threading.Thread(target=thread_url, args=(3, index + 3))
    #     t4 = threading.Thread(target=thread_url, args=(4, index + 4))
    #
    #     threads.append(t1)
    #     threads.append(t2)
    #     threads.append(t3)
    #     threads.append(t4)
    #
    #     t1.start()
    #     t2.start()
    #     t3.start()
    #     t4.start()
    #
    # for index, thread in enumerate(threads):
    #     thread.join()
