from auto_everything.database import MongoDB
from auto_everything.database import Redis

my_mongodb = MongoDB(url="mongodb://yingshaoxo:yingshaoxo@127.0.0.1:27017/")

def test_mongodb_backup():
    my_mongodb.client.get_database("yingshaoxo").get_collection("friend1").insert_one({#type: ignore
        "name": "1",
        "superpower": "you name it"
    })
    my_mongodb.client.get_database("yingshaoxo").get_collection("friend1").insert_one({#type: ignore
        "name": "2",
        "superpower": "you name it"
    })
    my_mongodb.client.get_database("yingshaoxo").get_collection("friend2").insert_one({#type: ignore
        "name": "1",
        "superpower": "you name it"
    })
    my_mongodb.client.get_database("yingshaoxo").get_collection("friend2").insert_one({#type: ignore
        "name": "2",
        "superpower": "you name it"
    })
    my_mongodb.client.get_database("god").get_collection("friend1").insert_one({#type: ignore
        "name": "yingshaoxo",
        "superpower": "you name it"
    })
    my_mongodb.client.get_database("god").get_collection("friend2").insert_one({#type: ignore
        "name": "robot",
        "superpower": "you name it"
    })
    my_mongodb.backup_mongodb(backup_folder_path="/tmp/test")


def test_mongodb_recover():
    my_mongodb.recover_mongodb(backup_folder_path="/tmp/test")

def test_mongodb_collection_backup():
    data = my_mongodb.backup_collection(database_name="yingshaoxo", collection_name="friend1", json_file_saving_path="/tmp/test/ok.json")
    print(data)

def test_mongodb_collection_recover():
    # my_mongodb.recover_collection(database_name="yingshaoxo", collection_name="friend1", json_file_saving_path="/tmp/test/ok.json")
    my_mongodb.recover_collection(database_name="yingshaoxo", collection_name="friend1", object_list=[{
        "author": "yingshaoxo"
    }])

def test_redis_url_parsing():
    data = Redis._parse_redis_url(redis_URL="redis://hi:you@127.0.0.1:6379/")
    print(data)

    data = Redis._parse_redis_url(redis_URL="redis://0.0.0.0:6379/0")
    print(data)

    data = Redis._parse_redis_url(redis_URL="redis://0.0.0.0:6379")
    print(data)