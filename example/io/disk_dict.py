from auto_everything.io import Disk_Dict

a_dict = Disk_Dict("./test_dict_data")
a_dict["fine"] = "ok"
print(a_dict["fine"])
#del a_dict["fine"]
