// have to make sure enum key is in enum defination

// due to the stpid golang feature, we do not support enum and nested structure

// package test_protovuff_code
package main

import (
	"github.com/yingshaoxo/gopython/built_in_functions"
	"github.com/yingshaoxo/gopython/json_tool"
	"github.com/yingshaoxo/gopython/variable_tool"
)

// force all dict key and function name to be lowercase

// var Null_value_identify_symbol string = "It's fucking null. The stupid golang doesn't support null value in map structure, which sucks!!! And golang doesn't support lower-case exported function name, bad. And golang doesn't support disableing the unused variable warning, which is super bad!"
var Null_value_identify_symbol *string = nil

type Fuck_it_structure struct {
	Nice string
	Bad  string
}

type Is_It_OK_To_Be_Fool struct {
	Option            []variable_tool.Type_Nullable[bool]
	Fuck_it_structure Fuck_it_structure
}

type Get_Users_Request struct {
	Page_size   variable_tool.Type_Nullable[string]
	Page_number variable_tool.Type_Nullable[int64]
	Okok        variable_tool.Type_Nullable[Is_It_OK_To_Be_Fool]
}

var Key_to_key_string_dict_for_Get_Users_Request_ = struct {
	Page_size   string
	Page_number string
	Okok        string
}{
	Page_size:   "page_size",
	Page_number: "page_number",
	Okok:        "Is_It_OK_To_Be_Fool",
}

func Get_key_to_value_type_dict_for_Get_Users_Request_() map[string]any {
	return map[string]any{
		"page_size":   "string",
		"page_number": "int64",
		"Okok":        Is_It_OK_To_Be_Fool{},
	}
}

func (self Get_Users_Request) To_dict() map[string]any {
	return variable_tool.Convert_nullable_struct_into_dict(self, true).(map[string]any)
}

func (self Get_Users_Request) From_dict(a_dict map[string]any) Get_Users_Request {
	// var item Get_Users_Request
	variable_tool.Convert_dict_into_nullable_struct(a_dict, &self)
	// return item
	return self
}

// func is_the_variable_an_enum_class(a_variable any) bool {
// 	var yes = false

// 	object_key_representation := reflect.TypeOf(a_variable)
// 	object_value_representation := reflect.ValueOf(a_variable)

// 	for i := 0; i < object_value_representation.NumField(); i++ {
// 		var the_key = object_key_representation.Field(i).Name

// 		if the_key == "Enum_value_" {
// 			yes = true
// 			break
// 		}
// 	}

// 	return yes
// }

func main() {
	var option_list = [...]variable_tool.Type_Nullable[bool]{
		variable_tool.Nullable(true).Set_to_null(),
		variable_tool.Nullable(true).Set_to_null(),
	}
	var item = Get_Users_Request{}.From_dict(
		map[string]any{
			"Page_size":   variable_tool.Nullable("2").Set_to_null(),
			"Page_number": variable_tool.Nullable(3),
			"Okok": variable_tool.Nullable(
				Is_It_OK_To_Be_Fool{
					Option:            option_list[:],
					Fuck_it_structure: Fuck_it_structure{Nice: "hi", Bad: "bad"},
				},
			),
		},
	)

	original_dict := variable_tool.Convert_nullable_struct_into_dict(item, true)
	built_in_functions.Print(original_dict)

	// json_string := _convert_nullable_dict_into_json_string(
	// 	original_dict,
	// )
	// built_in_functions.Print(json_string)
	json_string := json_tool.Convert_map_to_json_string(original_dict)
	built_in_functions.Print(json_string)

	built_in_functions.Print("\n-----------\n")

	var an_object Get_Users_Request
	variable_tool.Convert_json_string_into_nullable_struct(json_string, &an_object)
	built_in_functions.Print(an_object.Page_size.Is_null)
	built_in_functions.Print(an_object)
	built_in_functions.Print(json_tool.Convert_struct_object_to_json_string(an_object))
}
