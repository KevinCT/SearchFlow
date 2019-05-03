from pymongo import MongoClient, errors
from debug import debug

DEFAULT_MONGO_DB_PORT = 27017
DEFAULT_MONGO_DB_ADDRESS = 'localhost'
DEFAULT_MONGO_DB_NAME = 'Facebook_Public_Page'
DEFAULT_TARGET_COLLECTION_NAME = '_post'


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
        except errors as e:
            self.dbug.debug_print("MongoDb Connection error: " + e)

    def insert(self, data):
        """

        :param data: (json) is the data you want to insert
        if data is already existed then it will update the data
        """

        unique_query = {"question_id": data.get("question_id")}  # search for same title
        try:
            elements = self.db_col.find(unique_query)
        except errors as e:
            self.dbug.debug_print("Errors in finding MongoDb elements " + e)
        try:
            if elements.count() == 0:
                self.dbug.debug_print("Inserted Data...")
                self.db_col.insert_one(data)
            else:
                self.dbug.debug_print("Data Already Existed...")
        except errors as e:
            self.dbug.debug_print("Problem with insert or update...", e)
