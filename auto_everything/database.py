from pymongo import MongoClient
from pymongo.database import Database

class MongoDB:
    #https://www.w3schools.com/python/python_mongodb_create_collection.asp
    def __init__(self, host: str, port: str, user: str, password: str):
        self.client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
    
    def delete_a_database(self, database_name: str):
        self.client.drop_database(database_name)
    
    def list_database(self) -> str:
        return self.client.database_names()
    
    def get_database(self, database_name: str) -> Database:
        return self.client[database_name]

if __name__ == "__main__":
    mongoDB = MongoDB(host="127.0.0.1", port="27017", user="root", password="yingshaoxo666")
    databases = mongoDB.list_database()
    print(databases)
    db = mongoDB.get_database("test")
    my_table = db.get_collection("my_table")
    my_table.delete_many({"num": {"$gt": -1}})
    for i in range(10):
        my_table.insert_one({"num": i})
    for one in my_table.find({"num": {"$gt": -1}}):
        print(one)

"""
import sqlalchemy

# Stupid MySQL can't be reasoned with
class MySQL:
    def __init__(self, host: str, port: str, user: str, password: str):
        self.engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}')
        self._block_list = ['mysql', 'performance_schema', 'sys']

    def create_a_database(self, database_name: str):
        self.engine.execute(f"CREATE DATABASE {database_name}")
        #self.engine.execute(f"USE {database_name}")

    def delete_a_database(self, database_name: str):
        if (database_name not in self._block_list):
            self.engine.execute(f"DROP DATABASE IF EXISTS {database_name};")
    
    def list_database(self) -> str:
        existing_databases = self.engine.execute("SHOW DATABASES;")
        return [d[0] for d in existing_databases if d[0] not in self._block_list]

    def is_database_exists(self, database_name: str) -> bool:
        existing_databases = self.list_database()
        return database_name in existing_databases

if __name__ == "__main__":
    mySQL = MySQL(host="127.0.0.1", port="3306", user="root", password="yingshaoxo666")

    for d in mySQL.list_database():
        mySQL.delete_a_database(d)
    print(mySQL.list_database())

    mySQL.create_a_database("test")
    print(mySQL.list_database())

    for d in mySQL.list_database():
        mySQL.delete_a_database(d)
    print(mySQL.list_database())
"""