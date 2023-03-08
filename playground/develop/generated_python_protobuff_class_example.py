"""
"UserStatus": {
    "OFFLINE": {
        "type": "string",
        "is_list": false,
        "name": "OFFLINE",
        "feature": ""
    },
    "ONLINE": {
        "type": "string",
        "is_list": false,
        "name": "ONLINE",
        "feature": ""
    }
},
"hello_request": {
    "name": {
        "type": "string",
        "is_list": false,
        "name": "name",
        "feature": ""
    },
    "user_status": {
        "type": "UserStatus",
        "is_list": false,
        "name": "user_status",
        "feature": ""
    }
},
"""


from dataclasses import dataclass
from enum import Enum
from typing import Any


class UserStatus(Enum):
    OFFLINE = 0
    ONLINE = 1


def convert_dict_that_has_enum_object_into_pure_dict(a_dict: dict[str, Any]) -> dict[str, Any]:
    new_dict: dict[str, Any] = {}
    for key, value in a_dict.items():
        if str(type(value)).startswith("<enum"):
            new_dict[key] = value.name
        else:
            new_dict[key] = value
    return new_dict


def convert_pure_dict_into_a_dict_that_has_enum_object(pure_dict: dict[str, Any], target_dict: dict[str, Any], property_name_to_its_type_dict_: dict[str, Any]) -> dict[str, Any]:
    for key, value in target_dict.items():
        if key in pure_dict:
            if str(type(value)).startswith("<enum"):
                if key not in property_name_to_its_type_dict_:
                    value = None
                else:
                    possible_value = pure_dict[key]
                    the_enum_class = property_name_to_its_type_dict_[key]
                    for temp_index, temp_value in enumerate(the_enum_class._member_names_):
                        if temp_value == possible_value:
                            value = the_enum_class(temp_index) 
                            break

                target_dict[key] = value
            else:
                target_dict[key] = pure_dict[key]
    return target_dict


@dataclass()
class hello_request:
    name: str | None = None
    user_status: UserStatus | None = None
    property_name_to_its_type_dict_ = {
        "name": str,
        "user_status": UserStatus
    }

    @dataclass()
    class key_string_dict_:
        name: str = "name"
        user_status: str = "user_status"

    def to_dict(self, ignore_null: bool=False) -> dict[str, Any]:
        new_dict = convert_dict_that_has_enum_object_into_pure_dict(a_dict=self.__dict__)
        return new_dict

    def clone(self):
        return self.create_a_new_instance_from_dict(self.to_dict()) 

    def from_dict(self, dict: dict[str, Any]):
        new_dict = convert_pure_dict_into_a_dict_that_has_enum_object(pure_dict=dict, target_dict=self.__dict__, property_name_to_its_type_dict_=self.property_name_to_its_type_dict_)
        old_self_dict = self.__dict__.copy() 
        for key, value in new_dict.items():
            if key in old_self_dict:
                setattr(self, key, value)

    @staticmethod
    def create_a_new_instance_from_dict(dict: dict[str, Any]):
        an_object = hello_request()
        new_dict = convert_pure_dict_into_a_dict_that_has_enum_object(pure_dict=dict, target_dict=an_object.__dict__, property_name_to_its_type_dict_=an_object.property_name_to_its_type_dict_)
        for key, value in new_dict.items():
            if key in an_object.__dict__:
                setattr(an_object, key, value)
        return an_object
    


if __name__ == "__main__":
    object1 = hello_request(name="a", user_status=UserStatus.OFFLINE)
    object2 = hello_request(name="b", user_status=UserStatus.ONLINE)

    object1_dict = object1.to_dict()
    object2_dict = object2.to_dict()

    print(object1_dict)
    print(object2_dict)

    print("---------")

    object1.from_dict(object2_dict)
    object2.from_dict(object1_dict)

    print(object1.to_dict())
    print(object2.to_dict())

    print("---------")

    print(object1.clone())


