import copy
from dataclasses import dataclass
from enum import Enum
from typing import Any


_ygrpc_official_types = [int, float, str, bool]


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
                elif str(type(value)).startswith("<class"):
                    return convert_dict_that_has_enum_object_into_pure_dict(
                        value=value.to_dict()
                    )
    return None


def convert_pure_dict_into_a_dict_that_has_enum_object(pure_value: Any, refrence_value: Any) -> Any:
    if type(pure_value) is list:
        new_list: list[Any] = []
        for one in pure_value: #type: ignore
            new_list.append(
                convert_pure_dict_into_a_dict_that_has_enum_object(pure_value=one, refrence_value=refrence_value)
            ) 
        return new_list
    elif type(pure_value) is dict:
        if str(refrence_value).startswith("<class"):
            new_object = refrence_value()
            old_property_list = getattr(new_object, "_property_name_to_its_type_dict")
            for key in old_property_list.keys():
                if key in pure_value.keys():
                    setattr(new_object, key, convert_pure_dict_into_a_dict_that_has_enum_object(pure_value[key], old_property_list[key])) # type: ignore
            return new_object
        else:
            return None
    else:
        if str(refrence_value).startswith("<enum"):
            default_value = None
            for temp_index, temp_value in enumerate(refrence_value._member_names_):
                if temp_value == pure_value:
                    default_value = refrence_value(temp_value) 
                    break
            return default_value
        else:
            if refrence_value in _ygrpc_official_types:
                return pure_value
            else:
                return None


class YRPC_OBJECT_BASE_CLASS:
    def to_dict(self, ignore_null: bool=False) -> dict[str, Any]:
        old_dict = {}
        for key in self._property_name_to_its_type_dict.keys(): #type: ignore
            old_dict[key] = self.__dict__[key] #type: ignore
        new_dict = convert_dict_that_has_enum_object_into_pure_dict(value=old_dict.copy())
        return new_dict.copy() #type: ignore

    def from_dict(self, dict: dict[str, Any]) -> Any:
        new_object = convert_pure_dict_into_a_dict_that_has_enum_object(pure_value=dict.copy(), refrence_value=self.__class__)

        new_object_dict = new_object.__dict__.copy() 
        for key, value in new_object_dict.items():
            if key in self.__dict__:
                setattr(self, key, value)

        return new_object

    def _clone(self) -> Any:
        return copy.deepcopy(self)


class User_Type(Enum):
    # yingshaoxo: I strongly recommend you use enum as a string type in other message data_model
    # for example, `User_Type.admin.value`
    user = "user"
    admin = "admin"


@dataclass()
class Get_JSON_Web_Token_Request(YRPC_OBJECT_BASE_CLASS):
    email: str | None = None
    password: str | None = None
    invitation_code: str | None = None

    _property_name_to_its_type_dict = {
        "email": str,
        "password": str,
        "invitation_code": str,
    }

    @dataclass()
    class _key_string_dict:
        email: str = "email"
        password: str = "password"
        invitation_code: str = "invitation_code"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_JSON_Web_Token_Request = super().from_dict(dict)
        return new_variable


@dataclass()
class Get_JSON_Web_Token_Response(YRPC_OBJECT_BASE_CLASS):
    error: str | None = None
    json_web_token: str | None = None
    user_type: User_Type | None = None

    _property_name_to_its_type_dict = {
        "error": str,
        "json_web_token": str,
        "user_type": User_Type,
    }

    @dataclass()
    class _key_string_dict:
        error: str = "error"
        json_web_token: str = "json_web_token"
        user_type: str = "user_type"

    def from_dict(self, dict: dict[str, Any]):
        new_variable: Get_JSON_Web_Token_Response = super().from_dict(dict)
        return new_variable

