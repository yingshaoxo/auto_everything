from typing import Callable

from generated_python_protobuff_class_example import *
from auto_everything.database import Database_Of_Yingshaoxo


def _search_function(self: Any, item_filter: Any, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
    search_temp_dict = {}
    search_temp_dict["_raw_search_counting"] = 0
    search_temp_dict["_search_counting"] = 0
    if (page_number!=None and page_size != None and start_from != None):
        search_temp_dict["_real_start"] = page_number * page_size
        search_temp_dict["_real_end"] = search_temp_dict["_real_start"] + page_size

    item_dict = item_filter.to_dict()

    def one_row_dict_filter(a_dict_: dict[str, Any]):
        search_temp_dict["_raw_search_counting"] += 1

        if (page_number!=None and page_size != None and start_from != None):
            if search_temp_dict["_raw_search_counting"] < start_from:
                return None

        result = True
        for key, value in item_dict.items():
            if value == None:
                # ignore None value because it is not defined
                continue
            if key not in a_dict_.keys():
                result = False
                break
            else:
                value2 = a_dict_.get(key)
                if value == value2:
                    continue
                else:
                    result = False
                    break

        final_result = None
        if result == True:
            search_temp_dict["_search_counting"] += 1
            final_result = a_dict_
        else:
            final_result = None

        if (page_number!=None and page_size != None and start_from != None):
            if search_temp_dict["_search_counting"] <= search_temp_dict["_real_start"]:
                return None
            if search_temp_dict["_search_counting"] > search_temp_dict["_real_end"]:
                return None

        return final_result

    return self.database_of_yingshaoxo.search(one_row_dict_handler=one_row_dict_filter)

def _raw_search_function(self: Any, one_row_json_string_handler: Callable[[str], dict[str, Any] | None], page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
    search_temp_dict = {}
    search_temp_dict["_raw_search_counting"] = 0
    search_temp_dict["_search_counting"] = 0
    if (page_number!=None and page_size != None and start_from != None):
        search_temp_dict["_real_start"] = page_number * page_size
        search_temp_dict["_real_end"] = search_temp_dict["_real_start"] + page_size

    def new_one_row_json_string_handler(a_json_string: str):
        search_temp_dict["_raw_search_counting"] += 1

        if (page_number!=None and page_size != None and start_from != None):
            if search_temp_dict["_raw_search_counting"] < start_from:
                return None

        result = one_row_json_string_handler(a_json_string)

        if result != None:
            search_temp_dict["_search_counting"] += 1

        if (page_number!=None and page_size != None and start_from != None):
            if search_temp_dict["_search_counting"] <= search_temp_dict["_real_start"]:
                return None
            if search_temp_dict["_search_counting"] > search_temp_dict["_real_end"]:
                return None

        return result

    return list(self.database_of_yingshaoxo.raw_search(one_row_json_string_handler=new_one_row_json_string_handler))

def _delete(self, item_filter: Any):
    item_dict = item_filter.to_dict()
    def one_row_dict_filter(a_dict_: dict[str, Any]):
        result = True
        for key, value in item_dict.items():
            if value == None:
                # ignore None value because it is not defined
                continue
            if key not in a_dict_.keys():
                result = False
                break
            else:
                value2 = a_dict_.get(key)
                if value == value2:
                    continue
                else:
                    result = False
                    break
        return result
    self.database_of_yingshaoxo.delete(one_row_dict_filter=one_row_dict_filter)


def _update(self, old_item_filter: Any, new_item: Any):
    item_dict = old_item_filter.to_dict()
    def one_row_dict_handler(a_dict_: dict[str, Any]):
        result = True
        for key, value in item_dict.items():
            if value == None:
                # ignore None value because it is not defined
                continue
            if key not in a_dict_.keys():
                result = False
                break
            else:
                value2 = a_dict_.get(key)
                if value == value2:
                    continue
                else:
                    result = False
                    break
        if result == True:
            new_object = {
                key:value for key, value
                in new_item.to_dict().items()
                if value != None
            }
            a_dict_.update(new_object)
            return a_dict_
        else:
            return None
    self.database_of_yingshaoxo.update(one_row_dict_handler=one_row_dict_handler)


class Yingshaoxo_Database_Yingshaoxo_info:
    def __init__(self, database_base_folder: str, use_sqlite: bool = False) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Yingshaoxo_info", database_base_folder=database_base_folder, use_sqlite=use_sqlite)

    def add(self, item: Yingshaoxo_info):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Yingshaoxo_info, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False) -> list[Yingshaoxo_info]:
        return [Yingshaoxo_info().from_dict(one) for one in _search_function(self=self, item_filter=item_filter, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)]

    def raw_search(self, one_row_json_string_handler: Callable[[str], dict[str, Any] | None], page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False) -> list[Yingshaoxo_info]:
        '''
        one_row_json_string_handler: a_function to handle search process. If it returns None, we'll ignore it, otherwise, we'll add the return value into the result list.
        '''
        return [Yingshaoxo_info().from_dict(one) for one in _raw_search_function(self=self, one_row_json_string_handler=one_row_json_string_handler, page_number=page_number, page_size=page_size, start_from=start_from, reverse=reverse)]

    def delete(self, item_filter: Yingshaoxo_info):
        return _delete(self=self, item_filter=item_filter)

    def update(self, old_item_filter: Yingshaoxo_info, new_item: Yingshaoxo_info):
        return _update(self=self, old_item_filter=old_item_filter, new_item=new_item)


class Yingshaoxo_Database_Excutor:
    def __init__(self, database_base_folder: str, use_sqlite: bool = False):
        self._database_base_folder = database_base_folder
        self.Yingshaoxo_info = Yingshaoxo_Database_Yingshaoxo_info(database_base_folder=self._database_base_folder, use_sqlite=use_sqlite)


if __name__ == "__main__":
    database_excutor = Yingshaoxo_Database_Excutor(database_base_folder="/home/yingshaoxo/CS/auto_everything/example/database/yingshaoxo_database")

    database_excutor.Yingshaoxo_info.add(Yingshaoxo_info(
        name="yingshaoxo",
        age=25
    ))
    database_excutor.Yingshaoxo_info.add(Yingshaoxo_info(
        name="google",
        age=25
    ))

    result = database_excutor.Yingshaoxo_info.search(Yingshaoxo_info(age=25))
    print(result)

    database_excutor.Yingshaoxo_info.update(Yingshaoxo_info(name="google"), Yingshaoxo_info(age=1000))
    result = database_excutor.Yingshaoxo_info.search(Yingshaoxo_info(name="google"))
    print(result)

    database_excutor.Yingshaoxo_info.delete(Yingshaoxo_info(name="yingshaoxo"))

    database_excutor.Yingshaoxo_info.database_of_yingshaoxo.refactor_database()

    result = database_excutor.Yingshaoxo_info.search(Yingshaoxo_info(name="google"), page_number=0, page_size=2)
    print(result)
