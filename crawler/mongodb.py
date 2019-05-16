from pymongo import MongoClient

from crawler.debug import debug

DEFAULT_MONGO_DB_PORT = 27017
DEFAULT_MONGO_DB_ADDRESS = 'localhost'
DEFAULT_MONGO_DB_NAME = 'StackOverflow'
DEFAULT_TARGET_COLLECTION_NAME = 'test'


class Connection:

    def __init__(self, db_name=DEFAULT_MONGO_DB_NAME, db_col=DEFAULT_TARGET_COLLECTION_NAME,
                 db_address=DEFAULT_MONGO_DB_ADDRESS, db_port=DEFAULT_MONGO_DB_PORT):
        """
        :param db_name: string, Name of the database
        :param db_col: string, Name of the collection
        :param db_address:
        :param db_port:
        """

        try:
            self.client = MongoClient("mongodb://" + db_address + ":" + str(db_port) + "/")
            self.db_name = self.client[db_name]
            self.db_col = self.db_name[db_col]
            self.dbug = debug(name=self.__class__, flag=True)
        except Exception as e:
            self.dbug.debug_print("MongoDB Connection error: " + e)

    def insert(self, data, typical_query=None):
        """

        :param data: (json) is the data you want to insert
        if data is already existed then it will update the data
        """
        if typical_query is None:
            unique_query = {"Question.question_id": data.get("Question").get("question_id")}  # search for same title
        else:
            unique_query = {"TagName": data}
        try:
            elements = self.db_col.find(unique_query)
        except Exception as e:
            self.dbug.debug_print("Errors in finding MongoDB elements " + e)
        try:
            if elements.count() == 0:
                self.dbug.debug_print("Inserted Data...")
                self.db_col.insert_one(data)
            else:
                self.dbug.debug_print("Data Already Existed...")
        except Exception as e:
            self.dbug.debug_print("Problem with insert or update..." + str(e))

    # get all info based of the type
    # by default we give 100000 data
    def get_whole_info(self, data_type="", limit=100000):
        list = []
        for i in self.db_col.find({}, {data_type: 1, "_id": 0}).limit(limit):
            list.append(i)
        return list

    def get_distinct_element(self, tag_name=""):
        return self.db_col.distinct(tag_name)

    # conn = Connection(db_name="StackOverflow", db_col="Question_URL")
    # print(conn.get_distinct_element("Question.question_tags"))

    # be sure before you use this method
    def delete_null_text(self):
        total = self.db_col.delete_many({{"crawled": True, "Question.question_text": None}})
        self.dbug.debug_print("total deleted items: " + str(total))
        return total.deleted_count

    # data_type is the data that you want from DB
    # ex. 'Question.question_id', 'Question.question_text'
    def get_distinct_data(self, data_type=""):
        return self.db_col.distinct(data_type)

    def data_exist(self, data_type="", data=None):

        """
        :param data_type: string, The name/type of the data in mongoDB. Ex. Question.question_id, Answer.answer_upvote
        :param data: anytype, The value of the data
        :return: boolean
        """
        return self.db_col.find({data_type: data}).count() > 0

# conn = Connection(db_name="StackOverflow", db_col="Multi_Thread_URL")
# print(conn.data_exist(data_type="Question.question_id", data=56075703))
# var = conn.db_col.find({'crawled': 'True'})
# for x in var:
#     print(x['question_id'])
#     x["crawled"] = "False"
#     # conn.db_col.update_one({"question_id": x['question_id']}, {"$set": {"crawled":"True"}})
