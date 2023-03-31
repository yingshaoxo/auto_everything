from auto_everything.database import MongoDB

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