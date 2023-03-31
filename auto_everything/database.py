from typing import Any
from pymongo import MongoClient
import pymongo
from datetime import datetime
import json

class MongoDB:
    """
    MONGO_DB_URL is something like: "mongodb://yingshaoxo:yingshaoxo@127.0.0.1:27017/"

    #https://www.w3schools.com/python/python_mongodb_create_collection.asp
    """
    def __init__(self, url: str):
        from auto_everything.disk import Disk
        from auto_everything.terminal import Terminal
        from auto_everything.io import IO
        self.client = MongoClient(url) #type: ignore
        self._disk = Disk()
        self._terminal = Terminal()
        self._io = IO()

    @staticmethod
    def _get_mongodb_client_by_giving_arguments(host: str, port: str, user: str, password: str) -> pymongo.MongoClient: #type: ignore
        return MongoDB(f"mongodb://{user}:{password}@{host}:{port}") #type: ignore
    
    def delete_a_database(self, database_name: str):
        self.client.drop_database(database_name) #type: ignore
    
    def list_database(self): #type: ignore
        return self.client.list_database_names() #type: ignore
    
    def get_database(self, database_name: str): #type: ignore
        return self.client.get_database(database_name) #type: ignore
    
    def clear_mongodb(self, database_name: str|None = None, collection_name: str|None = None):
        database_name_list: list[str] = self.list_database()
        for a_database_name in database_name_list:
            if a_database_name in ["admin", "local", "config"]:
                continue

            if database_name == None and collection_name == None:
                self.client.drop_database(a_database_name) #type: ignore
            else:
                if database_name != None:
                    if database_name == a_database_name:
                        if collection_name != None:
                            self.client.get_database(name=a_database_name).get_collection(name=collection_name).delete_many({}) # type: ignore
                        else:
                            self.client.drop_database(name_or_database=a_database_name) # type: ignore

    # def backup_mongodb_safely(self, backup_folder_path: str, use_time_as_folder_name: bool=True):
    #     # save one object as a json_string per line in a txt file
    #     pass

    def backup_mongodb(self, backup_folder_path: str, use_time_as_folder_name: bool=True):
        """
        it saves files into this structure:
            ── 2023-03-31_09-30
            │   ├── __mongodb_info__.json      # can be used to save fake_folder_info inside
            │   │   database_name_1
            │   │   ├── collection_name_1.json
            │   │   ├── collection_name_2.json
            │   │   database_name_2
            │   │   ├── collection_name_1.json
            │   │   ├── collection_name_2.json
        """
        if not self._disk.exists(backup_folder_path):
            self._disk.create_a_folder(backup_folder_path)
        if not self._disk.exists(backup_folder_path):
            raise Exception(f"You should give me a valid backup_folder_path than '{backup_folder_path}'")
        
        if use_time_as_folder_name == True:
            now = datetime.now()
            today_string = now.strftime("%Y-%m-%m_%H-%M")
            backup_folder_path = self._disk.join_paths(backup_folder_path, today_string)
        
        database_name_list: list[str] = self.list_database()
        for database_name in database_name_list:
            if database_name in ["admin", "local", "config"]:
                continue

            a_database = self.get_database(database_name=database_name) #type: ignore

            database_folder_path = self._disk.join_paths(backup_folder_path, database_name)
            self._disk.create_a_folder(database_folder_path)

            collection_name_list = a_database.list_collection_names()
            for collection_name in collection_name_list:
                collection = a_database.get_collection(name=collection_name) #type: ignore
                object_list: list[Any] = []
                for one_object in collection.find(): #type: ignore
                    obj = dict(one_object) #type: ignore
                    del obj["_id"]
                    object_list.append(obj)
                json_string_of_an_collection = json.dumps(object_list, indent=4)

                collection_json_file_path = self._disk.join_paths(database_folder_path, collection_name + ".json")
                self._io.write(collection_json_file_path, json_string_of_an_collection)

        special_file_path = self._disk.join_paths(backup_folder_path, "__mongodb_info__.json")
        file_name_tree = self._disk.fake_folder_backup(backup_folder=backup_folder_path)
        self._io.write(special_file_path, json.dumps({
            "db_type": "mongodb",
            "backup_tool": "python, auto_everything",
            "author": "yingshaoxo@gmail.com",
            "file_tree": file_name_tree
        }, indent=4))

    def recover_mongodb(self, backup_folder_path: str, use_time_as_folder_name: bool=True):
        """
        it loads files from this structure:
            ── 2023-03-31_09-30
            │   ├── __mongodb_info__.json      
            │   │   database_name_1
            │   │   ├── collection_name_1.json
            │   │   ├── collection_name_2.json
            │   │   database_name_2
            │   │   ├── collection_name_1.json
            │   │   ├── collection_name_2.json
        """
        if (use_time_as_folder_name == True):
            date_folders = [one for one in self._disk.get_folder_and_files(folder=backup_folder_path, recursive=False) if one.is_folder == True]
            date_folders.sort(key=lambda one: one.name)
            if len(date_folders) > 0:
                backup_folder_path = date_folders[-1].path
            else:
                raise Exception(f"This folder does not contain any data: {backup_folder_path}")

        if not self._disk.exists(backup_folder_path):
            raise Exception(f"You should give me a valid backup_folder_path than '{backup_folder_path}'")
        if not self._disk.exists(self._disk.join_paths(backup_folder_path, "__mongodb_info__.json")):
            raise Exception(f"You should give me a valid backup_folder_path than '{backup_folder_path}'")
        
        self.clear_mongodb()
        
        database_folder_list = [one for one in self._disk.get_folder_and_files(folder=backup_folder_path, recursive=False) if one.is_folder]
        for database_folder in database_folder_list:
            database_name = database_folder.name
            a_database = self.get_database(database_name=database_name) #type: ignore

            collection_json_list = self._disk.get_folder_and_files(folder=self._disk.join_paths(backup_folder_path, database_name), recursive=False, type_limiter=[".json"])
            for collection_json_file in collection_json_list:
                collection_name = collection_json_file.name[:-len(".json")]
                json_content = self._io.read(collection_json_file.path)
                data_ = json.loads(json_content)
                for one in data_:
                    a_database.get_collection(collection_name).insert_one(one) #type: ignore


if __name__ == "__main__":
    pass
    # mongoDB = MongoDB(host="127.0.0.1", port="27017", user="root", password="yingshaoxo666")
    # databases = mongoDB.list_database()
    # print(databases)
    # db = mongoDB.get_database("test")
    # my_table = db.get_collection("my_table")
    # my_table.delete_many({"num": {"$gt": -1}})
    # for i in range(10):
    #     my_table.insert_one({"num": i})
    # for one in my_table.find({"num": {"$gt": -1}}):
    #     print(one)

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