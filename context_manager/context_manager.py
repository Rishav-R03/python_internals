class ContextManager:
    def __init__(self):
        print("init method is called")

    def __enter__(self):
        print("enter method is called")
        return self 
    def __exit__(selfm,exc_type, exc_value, exc_tracebac):
        print("exit method called")


with ContextManager() as manager:
    print("with statement block")

"""
Explanation:
__init__() initializes the object.
__enter__() runs at the start of the with block and returns the object.
The block executes (print statement).
__exit__() is called after the block ends to handle cleanup.
"""


from pymongo import MongoClient

class MongoDBConnectionManager:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.hostname, self.port)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()

with MongoDBConnectionManager('localhost', 27017) as mongo:
    collection = mongo.SampleDb.test
    data = collection.find_one({'_id': 1})
    print(data.get('name'))

"""
Explanation:

__enter__() opens MongoDB connection.
mongo inside with block is the client object.
You can perform database operations safely.
__exit__() closes the connection automatically.
"""