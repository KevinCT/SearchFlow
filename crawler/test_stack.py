import requests
import crawler.mongodb as mongodb


def get_page_id(main, sub):
    for i in range(1, 2):
        print(main + str(i) + sub)
        url = requests.get(main + str(i) + sub).json()
        for data in url['items']:
            # info of page
            info_url = "https://api.stackexchange.com/2.2/questions/" + str(data["question_id"]) + "?order=desc&sort=activity&site=stackoverflow&filter=!*1SgQGNUvZpJEMfhYZ7a01FlIQnNElOi7v2ulX1IL"
            data_info = requests.get(info_url).json()
            print(data["question_id"])
            print(data_info)
            question_id = {"question_id": data['question_id'], "page_id": i}
            url_connection.db_col.insert_one(question_id)
            data_connection.db_col.insert_one(data_info)


url_connection = mongodb.Connection(db_name="StackOverflow", db_col="Question_URL")
data_connection = mongodb.Connection(db_name="StackOverflow", db_col="Question_INFO")
question_id_url_main = "https://api.stackexchange.com/2.2/questions?page="
question_id_url_sub = "&order=desc&sort=activity&site=stackoverflow"
get_page_id(question_id_url_main, question_id_url_sub)
