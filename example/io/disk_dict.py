from auto_everything.io import Redis_Style_Disk_String_Dict

a_dict = Redis_Style_Disk_String_Dict("./test_dict_data")
a_dict["fine"] = "ok"
print(a_dict["fine"])
#del a_dict["fine"]
