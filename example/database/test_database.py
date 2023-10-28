from typing import Any
from auto_everything.database import Database_Of_Yingshaoxo

from auto_everything.disk import Disk
disk = Disk()


database_of_yingshaoxo = Database_Of_Yingshaoxo(
    database_name="test", 
    database_base_folder=disk.join_paths(disk.get_directory_path(__file__), "yingshaoxo_database"), 
    use_sqlite=True)


# database_of_yingshaoxo.add({"author": "yingshaoxo"})
# database_of_yingshaoxo.add({"author": "python"})
# database_of_yingshaoxo.add({"author": "vscode"})


# database_of_yingshaoxo.clear_database()


# def one_row_dict_handler(dict_: dict[str, Any]) -> dict[str, Any] | None:
#     return dict_
#     if "author" in dict_:
#         if dict_["author"] == "yingshaoxo":
#             return dict_
#         else:
#             return None
#     return None
# result_list = database_of_yingshaoxo.search(one_row_dict_handler=one_row_dict_handler)
# print(result_list)


# def one_row_dict_filter(dict_: dict[str, Any]) -> bool:
#    if dict_["author"] == "python":
#        return True
#    return False
# database_of_yingshaoxo.delete(one_row_dict_filter=one_row_dict_filter)


# def one_row_dict_handler(dict_: dict[str, Any]) -> dict[str, Any] | None:
#     if "author" in dict_:
#         if dict_["author"] == "vscode":
#             dict_["author"] = "..."
#             return dict_
#         else:
#             return None
#     return None
# database_of_yingshaoxo.update(one_row_dict_handler=one_row_dict_handler)