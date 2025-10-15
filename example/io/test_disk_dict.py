from auto_everything.io import Redis_Style_Disk_String_Dict

#a_dict = Redis_Style_Disk_String_Dict("./test_dict_data", 1)
#a_dict["fine"] = "ok"
#print(a_dict["fine"])
#del a_dict["fine"]
#a_dict.clear()

from auto_everything.io import Disk_Dict

root_disk_dict = Disk_Dict("./test_dict_data")

root_disk_dict["hi"] = "you"
print(root_disk_dict["hi"])

root_disk_dict["hi"] = "okk"
print(root_disk_dict["hi"])

root_disk_dict["fine"] = "haha"
print(root_disk_dict["fine"])

del root_disk_dict["hi"]

root_disk_dict["fine"] = {"shit": "1", "nono": "2"}
print(root_disk_dict["fine"]["shit"])

#root_disk_dict.clear_all_data_for_all_dict_including_parent_dict()
