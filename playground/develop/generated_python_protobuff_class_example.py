from dataclasses import dataclass
from enum import Enum
from typing import Any


_ygrpc_official_types = [int, float, str, bool]


class UserStatus(Enum):
    OFFLINE = 0
    ONLINE = 1


def convert_dict_that_has_enum_object_into_pure_dict(value: Any) -> dict[str, Any] | list[Any] | Any:
    if type(value) is list:
        new_list: list[Any] = []
        for one in value: #type: ignore
            new_list.append(convert_dict_that_has_enum_object_into_pure_dict(value=one)) 
        return new_list
    elif type(value) is dict:
        new_dict: dict[str, Any] = {}
        for key_, value_ in value.items(): #type: ignore
            new_dict[key_] = convert_dict_that_has_enum_object_into_pure_dict(value=value_) #type: ignore
        return new_dict
    else:
        if str(type(value)).startswith("<enum"):
            return value.name
        else:
            if type(value) in _ygrpc_official_types:
                return value
            else:
                # handle custom message data type
                if value == None:
                    return None
                else:
                    return convert_dict_that_has_enum_object_into_pure_dict(
                        value=value.to_dict()
                    )


def convert_pure_dict_into_a_dict_that_has_enum_object(pure_value: Any, refrence_value: Any) -> Any:
    if type(pure_value) is list:
        new_list: list[Any] = []
        for one in pure_value: #type: ignore
            new_list.append(
                convert_pure_dict_into_a_dict_that_has_enum_object(pure_value=one, refrence_value=refrence_value)
            ) 
        return new_list
    elif type(pure_value) is dict:
        new_dict: dict[str, Any] = {}
        for key_, value_ in pure_value.items(): #type: ignore
            new_dict[key_] = convert_pure_dict_into_a_dict_that_has_enum_object( #type: ignore
                pure_value=value_, 
                refrence_value=refrence_value().property_name_to_its_type_dict_.get(key_)
            ) #type: ignore
        return new_dict
    else:
        if str(refrence_value).startswith("<enum"):
            default_value = None
            for temp_index, temp_value in enumerate(refrence_value(0)._member_names_):
                if temp_value == pure_value:
                    default_value = refrence_value(temp_index) 
                    break
            return default_value
        else:
            if refrence_value in _ygrpc_official_types:
                return pure_value
            else:
                return None


class YRPC_OBJECT_BASE_CLASS:
    def to_dict(self, ignore_null: bool=False) -> dict[str, Any]:
        new_dict = convert_dict_that_has_enum_object_into_pure_dict(value=self.__dict__.copy())
        return new_dict.copy() #type: ignore

    def from_dict(self, dict: dict[str, Any]):
        new_dict = convert_pure_dict_into_a_dict_that_has_enum_object(pure_value=dict.copy(), refrence_value=self.__class__)
        old_self_dict = self.__dict__.copy() 
        for key, value in new_dict.items():
            if key in old_self_dict:
                setattr(self, key, value)

    def clone(self):
        return self.create_a_new_instance_from_dict(self.to_dict()) 

    def create_a_new_instance_from_dict(self, dict: dict[str, Any]):
        an_object = self.__class__()
        new_dict = convert_pure_dict_into_a_dict_that_has_enum_object(pure_value=dict.copy(), refrence_value=an_object.__class__)
        for key, value in new_dict.items():
            if key in an_object.__dict__:
                setattr(an_object, key, value)
        return an_object


@dataclass()
class Yingshaoxo_info(YRPC_OBJECT_BASE_CLASS):
    name: str | None = None
    age: int | None = None
    sex: str | None = None
    super_power: bool | None = None

    property_name_to_its_type_dict_ = {
        "name": str,
        "age": int,
        "sex": str,
        "super_power": bool
    }

    @dataclass()
    class key_string_dict_:
        name: str = "name"
        age: str = "age"
        sex: str = "sex"
        super_power: str = "super_power"
    

@dataclass()
class hello_request(YRPC_OBJECT_BASE_CLASS):
    name: str | None = None
    user_status: UserStatus | None = None
    user_status_list: list[UserStatus] | None = None
    yingshaoxo_info: Yingshaoxo_info | None = None

    property_name_to_its_type_dict_ = {
        "name": str,
        "user_status": UserStatus,
        "user_status_list": UserStatus,
        "yingshaoxo_info": Yingshaoxo_info
    }

    @dataclass()
    class key_string_dict_:
        name: str = "name"
        user_status: str = "user_status"
        user_status_list: str = "user_status_list"
        yingshaoxo_info: str = "yingshaoxo_info"
    

if __name__ == "__main__":
    object1 = hello_request(name="a", 
                            user_status=UserStatus.OFFLINE, 
                            user_status_list=[UserStatus.OFFLINE, UserStatus.ONLINE],
                            yingshaoxo_info=Yingshaoxo_info(name="yingshaoxo", age=24, sex="male", super_power=True)
                            )
    object2 = hello_request(name="b", user_status=UserStatus.ONLINE)

    # print(object1.user_status_list)
    # print(type(object1.user_status_list))

    object1_dict = object1.to_dict()
    object2_dict = object2.to_dict()

    print(object1_dict)
    # print(object2_dict)

    print("---------")

    print(object2.to_dict())
    object2.from_dict(object1_dict)
    print(object2.to_dict())

    # print("---------")

    # print(hello_request.create_a_new_instance_from_dict(object2.to_dict()))


