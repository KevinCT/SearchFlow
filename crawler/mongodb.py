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

        :param db_name:
        :param db_col:
        :param db_address:
        :param db_port:
        """

        try:
            self.client = MongoClient("mongodb://" + db_address + ":" + str(db_port) + "/")
            self.db_name = self.client[db_name]
            self.db_col = self.db_name[db_col]
            self.dbug = debug(name=self.__class__, flag=True)
        except Exception as e:
            self.dbug.debug_print("MongoDb Connection error: " + e)

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
            self.dbug.debug_print("Errors in finding MongoDb elements " + e)
        try:
            if elements.count() == 0:
                #self.dbug.debug_print("Inserted Data...")
                self.db_col.insert_one(data)
            else:
                self.dbug.debug_print("Data Already Existed...")
        except Exception as e:
            self.dbug.debug_print("Problem with insert or update..." + str(e))

    # def get_data(self, data_type="question_id"):
    def test_get_inf(self, data_type=""):
        list = []
        for i in self.db_col.find({}, {data_type: 1, "_id": 0}):
            list.append(i)
        return list

# conn = Connection(db_name="StackOverflow", db_col="Question_URL")
# print(conn.test_get_inf(data_type="question_id"))
# var = conn.db_col.find({'crawled': 'True'})
# for x in var:
#     print(x['question_id'])
#     x["crawled"] = "False"
#     # conn.db_col.update_one({"question_id": x['question_id']}, {"$set": {"crawled":"True"}})
