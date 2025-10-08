from auto_everything.io import Redis_Style_Disk_String_Dict

a_dict = Redis_Style_Disk_String_Dict("./test_dict_data")
a_dict["fine"] = "ok"
print(a_dict["fine"])
#del a_dict["fine"]

"""
from auto_everything.io import Disk_Dict

root_disk_dict = Disk_Dict("./test_dict_data")

root_disk_dict["hi"] = "you"
print(root_disk_dict["hi"])

root_disk_dict["hi"] = "okk"
print(root_disk_dict["hi"])

print("another_dict" in root_disk_dict)
#root_disk_dict["another_dict"] = {"1": "yi", "2": "er"}
"""
