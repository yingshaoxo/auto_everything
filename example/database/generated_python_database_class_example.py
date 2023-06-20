from generated_python_protobuff_class_example import *
from auto_everything.database import Database_Of_Yingshaoxo


class Yingshaoxo_Database_Yingshaoxo_info:
    def __init__(self, database_base_folder: str) -> None:
        self.database_of_yingshaoxo = Database_Of_Yingshaoxo(database_name="Yingshaoxo_info", database_base_folder=database_base_folder)

    def add(self, item: Yingshaoxo_info):
        self.database_of_yingshaoxo.add(data=item.to_dict())

    def search(self, item_filter: Yingshaoxo_info, page_number:int|None=None, page_size:int|None=None, start_from:int=0, reverse:bool=False):
        self._raw_search_counting = 0
        self._search_counting = 0
        if (page_number!=None and page_size != None and start_from != None):
            self._real_start = page_number * page_size
            self._real_end = self._real_start + page_size

        item_dict = item_filter.to_dict()

        def one_row_dict_filter(a_dict_: dict[str, Any]):
            self._raw_search_counting += 1

            if (page_number!=None and page_size != None and start_from != None):
                if self._raw_search_counting < start_from:
                    return None
                if self._search_counting < self._real_start:
                    return None
                if self._search_counting > self._real_end:
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

            if result == True:
                self._search_counting += 1
                return a_dict_
            else:
                return None
        return self.database_of_yingshaoxo.search(one_row_dict_handler=one_row_dict_filter)

    def delete(self, item_filter: Yingshaoxo_info):
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
    
    def update(self, old_item_filter: Yingshaoxo_info, new_item: Yingshaoxo_info):
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


class Yingshaoxo_Database_Excutor:
    def __init__(self, database_base_folder: str):
        self._database_base_folder = database_base_folder
        self.Yingshaoxo_info = Yingshaoxo_Database_Yingshaoxo_info(database_base_folder=self._database_base_folder)


if __name__ == "__main__":
    database_excutor = Yingshaoxo_Database_Excutor(database_base_folder="/home/yingshaoxo/CS/auto_everything/example/database/yingshaoxo_database")

    # database_excutor.Yingshaoxo_info.add(Yingshaoxo_info(
    #     name="yingshaoxo",
    #     age=25
    # ))
    # database_excutor.Yingshaoxo_info.add(Yingshaoxo_info(
    #     name="google",
    #     age=25
    # ))

    #result = database_excutor.Yingshaoxo_info.search(Yingshaoxo_info(age=25))
    #print(result)

    # database_excutor.Yingshaoxo_info.update(Yingshaoxo_info(name="google"), Yingshaoxo_info(age=1000))
    # result = database_excutor.Yingshaoxo_info.search(Yingshaoxo_info(name="google"))
    # print(result)

    #database_excutor.Yingshaoxo_info.delete(Yingshaoxo_info(name="yingshaoxo"))

    #database_excutor.Yingshaoxo_info.database_of_yingshaoxo.refactor_database()
