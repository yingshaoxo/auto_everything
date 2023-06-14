from typing import Any, Callable, Iterator
from datetime import datetime
import json


class MongoDB:
    """
    MONGO_DB_URL is something like: "mongodb://yingshaoxo:yingshaoxo@127.0.0.1:27017/"

    #https://www.w3schools.com/python/python_mongodb_create_collection.asp
    """
    def __init__(self, url: str):
        from pymongo import MongoClient
        from auto_everything.disk import Disk
        from auto_everything.io import IO
        self.client = MongoClient(url) #type: ignore
        self._disk = Disk()
        self._io = IO()

    @staticmethod
    def _get_mongodb_client_by_giving_arguments(host: str, port: str, user: str, password: str): #type: ignore
        return MongoDB(f"mongodb://{user}:{password}@{host}:{port}") #type: ignore
    
    def delete_a_database(self, database_name: str):
        self.client.drop_database(database_name) #type: ignore
    
    def list_database(self): #type: ignore
        return self.client.list_database_names() #type: ignore
    
    def get_database(self, database_name: str): #type: ignore
        return self.client.get_database(database_name) #type: ignore

    def insert_or_update_item(self, database_name: str | None, collection_name: str | None, filter: dict[str, Any] | None, data: dict[str, Any]): #type: ignore
        pass

    def get_item(self, database_name: str | None, collection_name: str | None, filter: dict[str, Any] | None) -> dict[str, Any]: #type: ignore
        pass

    def get_item_list(self, database_name: str | None, collection_name: str | None, filter: dict[str, Any] | None) -> list[dict[str, Any]]: #type: ignore
        pass

    def delete_item(self, database_name: str | None, collection_name: str | None, filter: dict[str, Any] | None) -> dict[str, Any]: #type: ignore
        pass
    
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
    
    def backup_collection(self, database_name: str, collection_name: str, json_file_saving_path: str | None=None) -> list[dict[Any, Any]]:
        database_name_list: list[str] = self.list_database()
        if database_name not in database_name_list:
            raise Exception(f"database_name '{database_name}' not exists")
        the_database = self.get_database(database_name=database_name) #type: ignore
        if collection_name not in the_database.list_collection_names():
            raise Exception(f"collection_name '{collection_name}' not exists")
        the_collection = the_database.get_collection(name=collection_name) #type: ignore

        object_list: list[Any] = []
        for one_object in the_collection.find(): #type: ignore
            obj = dict(one_object) #type: ignore
            del obj["_id"]
            object_list.append(obj)
        
        if json_file_saving_path != None:
            if not json_file_saving_path.endswith(".json"):
                raise Exception(f"the json_file_saving_path you give me should be ended with '.json' other than '{json_file_saving_path}'")
            json_string_of_an_collection = json.dumps(object_list, indent=4)
            self._io.write(json_file_saving_path, json_string_of_an_collection)

        return object_list

    def recover_collection(self, database_name: str, collection_name: str, object_list: list[Any] | None = None, json_file_saving_path: str | None=None):
        if json_file_saving_path != None:
            if not self._disk.exists(json_file_saving_path):
                raise Exception(f"The json_file_saving_path you gave me does not exists: {json_file_saving_path}")
            json_text =  self._io.read(json_file_saving_path)
            object_list = json.loads(json_text)

        self.clear_mongodb(database_name=database_name, collection_name=collection_name)
        self.get_database(database_name=database_name).get_collection(name=collection_name).insert_many(object_list) #type: ignore

    # def backup_mongodb_safely(self, backup_folder_path: str, use_time_as_folder_name: bool=True):
    #     # save one object as a json_string per line in a txt file
    #     pass

    def backup_mongodb(self, backup_folder_path: str, use_time_as_sub_folder_name: bool=True):
        """
        backup_folder_path: str 
            the backup folder
        use_time_as_sub_folder_name: bool
            if it is true:
                it saves files into this structure:
                    ── 2023-03-31_09-30
                    │   ├── __mongodb_info__.json      
                    │   │   database_name_1
                    │   │   ├── collection_name_1.json
                    │   │   ├── collection_name_2.json
                    │   │   database_name_2
                    │   │   ├── collection_name_1.json
                    │   │   ├── collection_name_2.json
            else:
                it saves files into this structure:
                    ├── __mongodb_info__.json      
                    │   database_name_1
                    │   ├── collection_name_1.json
                    │   ├── collection_name_2.json
                    │   database_name_2
                    │   ├── collection_name_1.json
                    │   ├── collection_name_2.json
        """
        if not self._disk.exists(backup_folder_path):
            self._disk.create_a_folder(backup_folder_path)
        if not self._disk.exists(backup_folder_path):
            raise Exception(f"You should give me a valid backup_folder_path than '{backup_folder_path}'")
        
        if use_time_as_sub_folder_name == True:
            now = datetime.now()
            today_string = now.strftime(r"%Y-%m-%d_%H-%M")
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

    def recover_mongodb(self, backup_folder_path: str, use_time_as_sub_folder_name: bool=True):
        """
        backup_folder_path: str 
            the backup folder
        use_time_as_sub_folder_name: bool
            if it is true:
                it loads files from this structure:
                    ── 2023-03-31_09-30
                    │   ├── __mongodb_info__.json      
                    │   │   database_name_1
                    │   │   ├── collection_name_1.json
                    │   │   ├── collection_name_2.json
                    │   │   database_name_2
                    │   │   ├── collection_name_1.json
                    │   │   ├── collection_name_2.json
            else:
                it loads files from this structure:
                    ├── __mongodb_info__.json      
                    │   database_name_1
                    │   ├── collection_name_1.json
                    │   ├── collection_name_2.json
                    │   database_name_2
                    │   ├── collection_name_1.json
                    │   ├── collection_name_2.json
        """
        if (use_time_as_sub_folder_name == True):
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


class Redis:
    """
    Redis_DB_URL is something like: "redis://username:password@127.0.0.1:6379"
    """
    def __init__(self, redis_URL: str, database_name: str) -> None:
        import redis
        from auto_everything.disk import Disk
        from auto_everything.io import IO
        self._io = IO()
        self._disk = Disk()

        host, port, username, password = self._parse_redis_url(redis_URL=redis_URL)

        self.redis = redis.Redis(host=host, port=int(port), db=0, username=username, password=password)
        self.database_name = database_name
    
    @staticmethod
    def _parse_redis_url(redis_URL: str) -> tuple[str, str, str | None, str | None]:
        if not redis_URL.startswith("redis://"):
            raise Exception(f"the redis_URL is something like this: redis://127.0.0.1:6379")
        username = None
        password = None
        host = None
        port = None
        if "@" in redis_URL:
            splits = redis_URL.split("@")
            first_part = splits[0].split("://")[1]
            second_part = splits[1]

            splits = first_part.split(":")
            username = splits[0]
            password = splits[1]

            splits = second_part.split(":")
            host = splits[0]
            port = splits[1].split("/")[0]
        else:
            'redis://127.0.0.1:6379/0'
            ip_and_port = redis_URL.split("://")[1].split("/")[0]
            splits = ip_and_port.split(":")
            host = splits[0]
            port = splits[1]
        return host, port, username, password
    
    def _get_final_key_with_database_name_as_prefix(self, key: str) -> str:
        return f"{self.database_name}.{key}"

    def get(self, key: str) -> str | None:
        data = self.redis.get(
            self._get_final_key_with_database_name_as_prefix(key=key)
        )
        if data is None:
            return None
        else:
            return data.decode('utf-8')

    def set(self, key: str, value: str, expire_time_in_seconds: int | None = None) -> bool:
        result = self.redis.set(
            self._get_final_key_with_database_name_as_prefix(key=key),
            value, 
            ex=expire_time_in_seconds
        )
        if result is None:
            return False
        else:
            return result
    
    def delete(self, key: str) -> bool:
        result = self.redis.delete(
            self._get_final_key_with_database_name_as_prefix(key=key)
        )
        if result == 0:
            return False
        else:
            return True
    
    def delete_all(self):
        for key in self.redis.keys(
                self._get_final_key_with_database_name_as_prefix(key="*")
            ):
            self.redis.delete(key)
    
    def get_remaining_time_of_a_key(self, key: str) -> int:
        """
        The command returns -2 if the key does not exist.
        The command returns -1 if the key exists but has no associated expire.
        """
        return self.redis.ttl(
            self._get_final_key_with_database_name_as_prefix(key=key)
        )
    
    def backup_redis(self, json_file_saving_path: str | None = None) -> list[dict[str, str]]:
        value_list: list[dict[str, str]] = []
        for key in self.redis.keys(
                self._get_final_key_with_database_name_as_prefix(key="*")
            ):
            value = self.redis.get(key)
            if value != None:
                object = {
                    "key": key.decode("utf-8"), 
                    "value": value.decode("utf-8"),
                }
                ttl = self.get_remaining_time_of_a_key(key=key.decode("utf-8"))
                if ttl >= 1:
                    object["ttl"] = str(ttl)
                value_list.append(object)

        if json_file_saving_path != None:
            if not json_file_saving_path.endswith(".json"):
                raise Exception(f"the json_file_saving_path you give me should be ended with '.json' other than '{json_file_saving_path}'")
            json_string_of_an_collection = json.dumps(value_list, indent=4)
            self._io.write(json_file_saving_path, json_string_of_an_collection)

        return value_list

    def recover_redis(self, object_list: list[Any] | None = None, json_file_saving_path: str | None=None):
        if json_file_saving_path != None:
            if not self._disk.exists(json_file_saving_path):
                raise Exception(f"The json_file_saving_path you gave me does not exists: {json_file_saving_path}")
            json_text =  self._io.read(json_file_saving_path)
            object_list = json.loads(json_text)

        self.delete_all()
        for one in object_list: #type: ignore
            key, value, ttl = one.get("key"), one.get("value"), one.get("ttl")
            if ttl == None:
                self.set(key=key, value=value)
            else:
                self.set(key=key, value=value, expire_time_in_seconds=int(ttl))


class Database_Of_Yingshaoxo:
    """
                        r   r+   w   w+   a   a+
    ------------------|--------------------------
    read              | +   +        +        +
    write             |     +    +   +    +   +
    write after seek  |     +    +   +
    create            |          +   +    +   +
    truncate          |          +   +
    position at start | +   +    +   +
    position at end   |                   +   +
    """
    def __init__(self, database_name: str, database_base_folder: str = "./yingshaoxo_database") -> None:
        from auto_everything.disk import Disk
        from auto_everything.io import IO
        import json
        import subprocess
        import os
        self._disk = Disk()
        self._io = IO()
        self._json = json
        self._subprocess = subprocess
        self._os = os

        self.database_base_folder = database_base_folder
        if (not self._disk.exists(self.database_base_folder)):
            self._disk.create_a_folder(self.database_base_folder)

        self.database_txt_file_path = self._disk.join_paths(self.database_base_folder, f"{database_name}.txt")
        if (not self._disk.exists(self.database_txt_file_path)):
            self._io.write(self.database_txt_file_path, "")
    
    def add(self, data: dict[str, Any]):
        json_string = self._json.dumps(data).strip()
        with open(self.database_txt_file_path, "a+", encoding="utf-8", errors="ignore") as file_stream:
            file_stream.seek(0, self._os.SEEK_END) 
            file_stream.write(json_string + "\n")

    def raw_search(self, one_row_dict_handler: Callable[[str], dict[str, Any] | None]) -> Iterator[dict[str, Any]]:
        """
        one_row_dict_handler: a_function to handle search process. If it returns None, we'll ignore it, otherwise, we'll add the return value into the result list.
        """
        with open(self.database_txt_file_path, "r") as file_stream:
            previous_position = None
            while True:
                current_position = file_stream.tell()
                line = file_stream.readline()
                if previous_position == current_position:
                    # reach the end
                    break
                previous_position = current_position
                if (line.strip() == ""):
                    # ignore empty line
                    continue

                if (line.startswith('#')):
                    # ignore deleted line
                    continue

                result = one_row_dict_handler(line)
                if (result != None):
                    yield result
    
    def search(self, one_row_dict_handler: Callable[[dict[str, Any]], dict[str, Any] | None]) -> list[dict[str, Any]]:
        """
        one_row_dict_handler: a_function to handle search process. If it returns None, we'll ignore it, otherwise, we'll add the return value into the result list.
        """
        result_list = []
        with open(self.database_txt_file_path, "r") as file_stream:
            previous_position = None
            while True:
                current_position = file_stream.tell()
                line = file_stream.readline()
                if previous_position == current_position:
                    # reach the end
                    break
                previous_position = current_position
                if (line.strip() == ""):
                    # ignore empty line
                    continue

                if (line.startswith('#')):
                    # ignore deleted line
                    continue

                json_dict = self._json.loads(line)

                result = one_row_dict_handler(json_dict)
                if (result != None):
                    result_list.append(result)
        return result_list
    
    # def reverse_search(self):
    #     #https://stackoverflow.com/a/23646049/8667243
    #     #reverse search will speed up the search process in most of the cases
    #     pass

    def raw_delete(self, one_row_dict_filter: Callable[[str], bool]):
        """
        one_row_dict_filter: a_function to handle deletion process. If it returns False, we'll ignore it, otherwise, if it is True, we'll delete that row of data.
        """
        with open(self.database_txt_file_path, "r+") as file_stream:
            end_detection_counting = 1
            old_position_pair = None
            while True:
                previous_position = file_stream.tell()
                line = file_stream.readline()
                current_position = file_stream.tell()

                new_position_pair = (previous_position, current_position)
                if old_position_pair == new_position_pair:
                    end_detection_counting += 1 
                else:
                    old_position_pair = new_position_pair
                if end_detection_counting >= 3:
                    # We could make sure it is the end of the file
                    old_position_pair = None
                    break

                if (line.strip() == ""):
                    # ignore empty line
                    continue

                if (line.startswith('#')):
                    # ignore deleted line
                    continue

                result = one_row_dict_filter(line)
                if (result == True):
                    # replace the first character of the line with '#' symbol
                    file_stream.seek(previous_position)
                    file_stream.write("#"+line[1:])

    def delete(self, one_row_dict_filter: Callable[[dict[str, Any]], bool]):
        """
        one_row_dict_filter: a_function to handle deletion process. If it returns False, we'll ignore it, otherwise, if it is True, we'll delete that row of data.
        """
        with open(self.database_txt_file_path, "r+") as file_stream:
            end_detection_counting = 1
            old_position_pair = None
            while True:
                previous_position = file_stream.tell()
                line = file_stream.readline()
                current_position = file_stream.tell()

                new_position_pair = (previous_position, current_position)
                #print(new_position_pair)
                if old_position_pair == new_position_pair:
                    end_detection_counting += 1 
                else:
                    old_position_pair = new_position_pair
                if end_detection_counting >= 3:
                    # We could make sure it is the end of the file
                    old_position_pair = None
                    break

                if (line.strip() == ""):
                    # ignore empty line
                    continue

                if (line.startswith('#')):
                    # ignore deleted line
                    continue

                json_dict = self._json.loads(line)

                result = one_row_dict_filter(json_dict)
                #print(result)
                if (result == True):
                    # replace the first character of the line with '#' symbol
                    file_stream.seek(previous_position)
                    file_stream.write("#"+line[1:])

    def raw_update(self, one_row_dict_handler: Callable[[str], dict[str, Any] | None]):
        """
        one_row_dict_handler: a_function to handle update process. If it returns None, we'll ignore it, otherwise, we'll update the old value with the new value the handler function returns.
        """
        new_record_list = []

        def one_row_dict_filter(old_value: str) -> bool:
            result = one_row_dict_handler(old_value)
            if result == None:
                return False
            else:
                new_record_list.append(result)
                return True
        self.raw_delete(one_row_dict_filter=one_row_dict_filter)

        for one in new_record_list:
            self.add(one)

    def update(self, one_row_dict_handler: Callable[[dict[str, Any]], dict[str, Any] | None]):
        """
        one_row_dict_handler: a_function to handle update process. If it returns None, we'll ignore it, otherwise, we'll update the old value with the new value the handler function returns.
        """
        new_record_list = []

        def one_row_dict_filter(old_value: dict[str, Any]) -> bool:
            result = one_row_dict_handler(old_value)
            if result == None:
                return False
            else:
                new_record_list.append(result)
                return True
        self.delete(one_row_dict_filter=one_row_dict_filter)

        for one in new_record_list:
            self.add(one)

    def clear_database(self):
        self._io.write(self.database_txt_file_path, "")
    

if __name__ == "__main__":
    pass

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