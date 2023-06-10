import pymongo


def get_db_handle():
    connect_string = 'mongodb+srv://<user>:<password>@servicewebdb.gyy9vjg.mongodb.net/'
    client = pymongo.MongoClient(connect_string)
    return client
