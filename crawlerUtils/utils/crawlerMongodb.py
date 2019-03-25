from pymongo import MongoClient

__all__ = ["Mongo"]
INVENTORY = []



class Mongo:

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def mongoConnect(cls, mongo_url="mongodb://localhost:27017",
                     mongo_db="crawler_db", username="", password=""):
        """ 连接mongo数据库 """
        cls.db_name = mongo_db
        cls.conn = MongoClient(mongo_url)
        cls.db = cls.conn[cls.db_name]
        if username or password:
            cls.db.authenticate(username, password)

    @classmethod
    def mongoInsert(cls, dict1, collection="crawler_collection"):
        """ 直接向mongo中插入数据 """
        cls.collection = cls.db[collection]
        cls.collection.insert_one(dict1)

    @classmethod
    def mongoClose(cls):
        global INVENTORY
        if INVENTORY:
            for i in range(len(INVENTORY)):
                cls.collection.insert_one(INVENTORY.pop(0))
        cls.conn.close()

    @classmethod
    def mongoInsertLength(cls, dict1, collection="crawler_collection", length=10000):
        """ 批量插入数据到mongo, 默认每1w条插入一次 """
        global INVENTORY
        INVENTORY.append(dict1)
        if len(INVENTORY) == length:
            cls.collection = cls.db[collection]
            for i in range(length):
                cls.collection.insert_one(INVENTORY.pop(0))

    @classmethod
    def mongoInsertAll(cls, list1, collection="crawler_collection",
                       mongo_url="mongodb://localhost:27017",
                       mongo_db="crawler_db", username="", password=""):
        """ 把一个字典列表插入mongo，自动创建和关闭连接 """
        cls.mongoConnect(mongo_url, mongo_db, username, password)
        cls.collection = cls.db[collection]
        if not isinstance(list1, list):
            raise ValueError("Parameter must be list object.")
        while list1:
            cls.collection.insert_one(list1.pop(0))
        cls.mongoClose()
