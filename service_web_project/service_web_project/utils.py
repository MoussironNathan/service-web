import pymongo


def get_db_handle():
    # connect_string = 'mongodb+srv://nmoussiron:passworddb@servicewebdb.gyy9vjg.mongodb.net/'
    connect_string = 'mongodb://localhost:27017/'
    client = pymongo.MongoClient(connect_string)
    return client
