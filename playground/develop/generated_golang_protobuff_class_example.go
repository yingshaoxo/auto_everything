// have to make sure enum key is in enum defination

// due to the stpid golang feature, we do not support enum and nested structure

// package test_protovuff_code
package main

import (
	"reflect"
	"strings"

	"github.com/yingshaoxo/gopython/built_in_functions"
	"github.com/yingshaoxo/gopython/dict_tool"
	"github.com/yingshaoxo/gopython/json_tool"
	"github.com/yingshaoxo/gopython/variable_tool"
)

// force all dict key and function name to be lowercase

// type User_Status struct {
// 	Enum_value_ variable_tool.Type_Nullable[string]
// 	Online      variable_tool.Type_Nullable[string]
// 	Offline     variable_tool.Type_Nullable[string]
// }

// func (self User_Status) New(value variable_tool.Type_Nullable[string]) User_Status {
// 	var item = User_Status{}
// 	item.Online = variable_tool.Nullable("Online")
// 	item.Offline = variable_tool.Nullable("Offline")
// 	item.Enum_value_ = value
// 	return item
// }

// func (self User_Status) To_dict() string {
// 	return self.Enum_value_.Value
// }

// func (self User_Status) From_dict(value string) User_Status {
// 	var item = User_Status{}.New(variable_tool.Nullable(value))
// 	return item
// }

var Null_value_identify_symbol string = "It's fucking null. The stupid golang doesn't support null value in map structure, which sucks!!! \nAnd golang don't support lower-case exported function name, bad. \nAnd golang don't support disableing the unused variable warning, which is super bad!"

type Is_It_OK_To_Be_Fool struct {
	Option variable_tool.Type_Nullable[bool]
}

type Get_Users_Request struct {
	Page_size   variable_tool.Type_Nullable[string]
	Page_number variable_tool.Type_Nullable[string]
	Okok        variable_tool.Type_Nullable[Is_It_OK_To_Be_Fool]
}

var Key_to_key_string_dict_for_Get_Users_Request = struct {
	Page_size   string
	Page_number string
	Okok        string
}{
	Page_size:   "page_size",
	Page_number: "page_number",
	Okok:        "Is_It_OK_To_Be_Fool",
}

func _get_key_to_value_type_dict_for_Get_Users_Request() map[string]any {
	return map[string]any{
		"page_size":   "string",
		"page_number": "string",
		"Okok":        Is_It_OK_To_Be_Fool{},
	}
}

func (self Get_Users_Request) To_dict() map[string]any {
	a_map, err := json_tool.Convert_struct_object_to_map(self)
	if err != nil {
		return map[string]any{}
	}
	return a_map
}

func (self Get_Users_Request) From_dict(a_dict map[string]any) Get_Users_Request {
	var item Get_Users_Request
	json_tool.Convert_map_to_struct_object(a_dict, &item)
	return item
}

func Check_if_key_in_struct_object(an_object_instance any, key string, lowercase_key bool) bool {
	object_key_representation := reflect.TypeOf(an_object_instance)

	for i := 0; i < object_key_representation.NumField(); i++ {
		var the_key = object_key_representation.Field(i).Name
		if lowercase_key == true {
			the_key = strings.ToLower(the_key)
		}

		if the_key == strings.ToLower(key) {
			return true
		}
	}

	return false
}

func is_the_variable_an_enum_class(a_variable any) bool {
	var yes = false

	object_key_representation := reflect.TypeOf(a_variable)
	object_value_representation := reflect.ValueOf(a_variable)

	for i := 0; i < object_value_representation.NumField(); i++ {
		var the_key = object_key_representation.Field(i).Name

		if the_key == "Enum_value_" {
			yes = true
			break
		}
	}

	return yes
}

// func Convert_nullable_struct_into_dict(an_object_instance any, lowercase_the_key bool) any {
// 	if an_object_instance == nil {
// 		return nil
// 	}

// 	if variable_tool.Is_the_variable_a_list_object(an_object_instance) {
// 		var new_list = make([]any, 0)
// 		switch t := an_object_instance.(type) {
// 		case []any:
// 			for _, value := range t {
// 				new_list = append(new_list, Convert_nullable_struct_into_dict(value, lowercase_the_key))
// 			}
// 		}
// 		return new_list
// 	}

// 	if !variable_tool.Is_the_variable_a_struct_object(an_object_instance) {
// 		return an_object_instance
// 	}

// 	if is_the_variable_an_enum_class(an_object_instance) {
// 		var new_object = variable_tool.Get_value_from_struct_object_by_name(an_object_instance, "Enum_value_")

// 		if variable_tool.Is_it_null(new_object) {
// 			return nil
// 		} else {
// 			var new_value = variable_tool.Get_value_from_nullable_variable(new_object).(string)
// 			if Check_if_key_in_struct_object(an_object_instance, new_value, true) {
// 				if lowercase_the_key == true {
// 					return strings.ToLower(new_value)
// 				} else {
// 					return new_value
// 				}
// 			} else {
// 				return nil
// 			}
// 		}

// 		return new_object
// 	}

// 	var new_dict = make(map[string]any)

// 	object_key_representation := reflect.TypeOf(an_object_instance)
// 	object_value_representation := reflect.ValueOf(an_object_instance)

// 	types := make([]any, object_key_representation.NumField())
// 	values := make([]interface{}, object_value_representation.NumField())
// 	for i := 0; i < object_value_representation.NumField(); i++ {
// 		var the_key = object_key_representation.Field(i).Name
// 		var the_type = object_key_representation.Field(i).Type.Name()
// 		var the_value = object_value_representation.Field(i).Interface()
// 		types[i] = the_type
// 		values[i] = the_value

// 		var is_nullable bool = false
// 		if strings.Contains(the_type, "Type_Nullable[") {
// 			is_nullable = true
// 		}

// 		var new_object any = nil
// 		if is_nullable {
// 			if variable_tool.Is_it_null(the_value) {
// 				new_object = nil
// 			} else {
// 				var new_value = variable_tool.Get_value_from_nullable_variable(the_value)
// 				new_object = Convert_nullable_struct_into_dict(new_value, lowercase_the_key)
// 			}
// 		} else {
// 			new_object = Convert_nullable_struct_into_dict(the_value, lowercase_the_key)
// 		}

// 		if lowercase_the_key == true {
// 			new_dict[strings.ToLower(the_key)] = new_object
// 		} else {
// 			new_dict[the_key] = new_object
// 		}
// 	}

// 	return new_dict
// }

// func Convert_struct_object_to_map(an_object any) (map[string]interface{}, error) {
// 	val := an_object

// 	var data map[string]interface{} = make(map[string]interface{})
// 	varType := reflect.TypeOf(val)

// 	if varType.Kind() != reflect.Struct {
// 		// Provided value is not an interface, do what you will with that here
// 		fmt.Println("Not a struct")
// 		return nil, nil
// 	}

// 	value := reflect.ValueOf(val)
// 	for i := 0; i < varType.NumField(); i++ {
// 		if !value.Field(i).CanInterface() {
// 			//Skip unexported fields
// 			continue
// 		}
// 		var fieldName string
// 		fieldName = varType.Field(i).Name
// 		if varType.Field(i).Type.Kind() != reflect.Struct {
// 			data[fieldName] = value.Field(i).Interface()
// 		} else {
// 			data[fieldName], _ = Convert_struct_object_to_map(value.Field(i).Interface())
// 		}

// 	}

// 	return data, nil
// }

func Convert_nullable_struct_into_dict(an_object_instance any, lowercase_the_key bool) any {
	if an_object_instance == nil {
		return nil
	}

	if variable_tool.Is_the_variable_a_struct_object(an_object_instance) {
		a_map, _ := json_tool.Convert_struct_object_to_map(an_object_instance)
		return Convert_nullable_struct_into_dict(a_map, lowercase_the_key)
	}

	if variable_tool.Is_the_variable_a_list_object(an_object_instance) {
		var new_list = make([]any, 0)
		switch t := an_object_instance.(type) {
		case []any:
			for _, value := range t {
				if variable_tool.Is_the_variable_a_dict_object(value) {
					if dict_tool.Check_if_a_key_is_in_the_dict(value.(map[string]any), "Is_null") {
						if dict_tool.Get_dict_value_by_giving_a_key(value.(map[string]any), "Is_null") == true {
							new_list = append(new_list, Null_value_identify_symbol)
						} else {
							new_list = append(new_list, dict_tool.Get_dict_value_by_giving_a_key(value.(map[string]any), "Value"))
						}
						continue
					}
				}
				new_list = append(new_list, Convert_nullable_struct_into_dict(value, lowercase_the_key))
			}
		}
		return new_list
	}

	if variable_tool.Is_the_variable_a_dict_object(an_object_instance) {
		var new_dict = make(map[string]any)
		for key, value := range an_object_instance.(map[string]any) {
			new_key := key
			if lowercase_the_key == true {
				new_key = strings.ToLower(key)
			}

			if variable_tool.Is_the_variable_a_dict_object(value) {
				if dict_tool.Check_if_a_key_is_in_the_dict(value.(map[string]any), "Is_null") {
					if dict_tool.Get_dict_value_by_giving_a_key(value.(map[string]any), "Is_null") == true {
						new_dict[new_key] = Convert_nullable_struct_into_dict(Null_value_identify_symbol, lowercase_the_key)
					} else {
						new_dict[new_key] = Convert_nullable_struct_into_dict(
							dict_tool.Get_dict_value_by_giving_a_key(value.(map[string]any), "Value"), lowercase_the_key,
						)
					}
					continue
				}
			}

			new_dict[new_key] = Convert_nullable_struct_into_dict(value, lowercase_the_key)
		}

		return new_dict
	}

	return an_object_instance
}

// func Convert_nullable_dict_into_json_string(an_dict any) string {
// 	if value == nil {
// 		return {
// 			key: null
// 		}
// 	} else {
// 		return {
// 			key: value
// 		}
// 	}
// }

func Convert_dict_into_nullable_struct(a_dict any, a_refrence_object_instance any) any {
	if a_dict == nil {
		return nil
	}
	if a_refrence_object_instance == nil {
		return nil
	}

	if variable_tool.Is_the_variable_a_list_object(a_dict) {
		var new_list = make([]any, 0)
		switch t := a_dict.(type) {
		case []any:
			for _, value := range t {
				// get child type or child object from empty list
				var type_of_an_element_in_a_list = reflect.TypeOf(a_refrence_object_instance).Elem()
				var instance_of_a_type = reflect.Zero(type_of_an_element_in_a_list).Interface()
				new_list = append(new_list, Convert_dict_into_nullable_struct(value, instance_of_a_type))
			}
		}
		return new_list
	}

	if !variable_tool.Is_the_variable_a_struct_object(a_refrence_object_instance) {
		// return nil if the basic element inside the tree is a dict than string, int, bool...
		if variable_tool.Is_the_variable_a_dict_object(a_dict) {
			return a_refrence_object_instance
		} else {
			return a_dict
		}
	}

	if is_the_variable_an_enum_class(a_refrence_object_instance) {
		return nil
		// return variable_tool.Nullable("").Set_to_null()
		// var real_value = dict_tool.Get_dict_value_by_giving_a_key(a_dict.(map[string]any), "Enum_value_")
		// if variable_tool.Get_variable_type_string_representation(real_value) == "string" {
		// 	return variable_tool.Nullable(real_value).Set_to_null()
		// } else {
		// 	if real_value == nil {
		// 		return variable_tool.Nullable("").Set_to_null()
		// 	} else {
		// 		var real_value2 = dict_tool.Get_dict_value_by_giving_a_key(real_value.(map[string]any), "Enum_value_")
		// 		if real_value2 == nil {
		// 			var result = Call_struct_object_function(a_refrence_object_instance, "New", []any{
		// 				variable_tool.Nullable(
		// 					a_refrence_object_instance,
		// 				),
		// 			})[0]
		// 			return result
		// 		} else {
		// 			var result = Call_struct_object_function(a_refrence_object_instance, "New", []any{
		// 				variable_tool.Nullable(
		// 					real_value2.(string),
		// 				),
		// 			})[0]
		// 			return result
		// 		}
		// 	}
		// }
	}

	var new_dict = make(map[string]any)

	object_key_representation := reflect.TypeOf(a_refrence_object_instance)
	object_value_representation := reflect.ValueOf(a_refrence_object_instance)

	types := make([]any, object_key_representation.NumField())
	values := make([]interface{}, object_value_representation.NumField())
	for i := 0; i < object_value_representation.NumField(); i++ {
		var the_key = object_key_representation.Field(i).Name
		var the_type = object_key_representation.Field(i).Type.Name()
		var the_reference_value = object_value_representation.Field(i).Interface()
		types[i] = the_type
		values[i] = the_reference_value

		var is_nullable bool = false
		if strings.Contains(the_type, "Type_Nullable[") {
			is_nullable = true
		}

		var new_object any = nil
		var new_value = dict_tool.Get_dict_value_by_giving_a_key(a_dict.(map[string]any), the_key)
		if is_nullable {
			the_reference_value = variable_tool.Get_value_from_nullable_variable(the_reference_value)

			if new_value == nil {
				new_object = variable_tool.Nullable(
					the_reference_value,
				).Set_to_null()
			} else {
				if dict_tool.Check_if_a_key_is_in_the_dict(new_value.(map[string]any), "Is_null") && dict_tool.Check_if_a_key_is_in_the_dict(new_value.(map[string]any), "Value") {
					new_value = dict_tool.Get_dict_value_by_giving_a_key(new_value.(map[string]any), "Value")
				}
				new_object = variable_tool.Nullable(
					Convert_dict_into_nullable_struct(
						new_value,
						the_reference_value,
					),
				)
			}
		} else {
			new_object = Convert_dict_into_nullable_struct(new_value, the_reference_value)
		}

		new_dict[the_key] = new_object
	}

	return new_dict
}

func Call_struct_object_function(an_object any, method_name string, input_arguments_list []any) []any {
	// if the object you give is from reflect.ValueOf(), you need to call reflect.ValueOf().Interface()
	var type_of_an_element = reflect.TypeOf(an_object)
	var instance_of_a_type = reflect.Zero(type_of_an_element)

	var arguments []reflect.Value
	for index := 0; index < len(input_arguments_list); index++ {
		arguments = append(arguments, reflect.ValueOf(input_arguments_list[index]))
	}
	var reflect_type_output_list = instance_of_a_type.MethodByName(method_name).Call(arguments)

	var outputs []any
	for index := 0; index < len(reflect_type_output_list); index++ {
		outputs = append(outputs, reflect_type_output_list[index].Interface())
	}

	return outputs
}

func main() {
	var item = Get_Users_Request{}.From_dict(
		map[string]any{
			"Page_size":   variable_tool.Nullable("2").Set_to_null(),
			"Page_number": variable_tool.Nullable("3"),
			"Okok": variable_tool.Nullable(
				Is_It_OK_To_Be_Fool{
					Option: variable_tool.Nullable(true),
				},
			).Set_to_null(),
		},
	)

	// built_in_functions.Print(item.Page_number)
	// built_in_functions.Print(item.To_dict())
	// built_in_functions.Print(Get_Users_Request{}.From_dict(item.To_dict()))

	abc := Convert_nullable_struct_into_dict(item, true)
	built_in_functions.Print(abc)
	built_in_functions.Print(
		json_tool.Convert_map_to_json_string(
			abc,
		),
	)

	built_in_functions.Print("\n-----------\n")

	cde := Convert_dict_into_nullable_struct(abc, Get_Users_Request{})
	built_in_functions.Print(cde)
	etf := Convert_nullable_struct_into_dict(item, false)
	built_in_functions.Print(etf)
	built_in_functions.Print(
		json_tool.Convert_map_to_json_string(
			etf,
		),
	)

	// var old_request, _ = json_tool.Convert_struct_object_to_map(item)
	// built_in_functions.Print(old_request)

	// var new_request = Convert_dict_into_nullable_struct(item.To_dict(), Get_Users_Request{})
	// built_in_functions.Print(new_request)
	// var new_request_map, _ = json_tool.Convert_struct_object_to_map(new_request)
	// built_in_functions.Print(new_request_map)

	// var a_dict = Convert_nullable_struct_into_dict(item, true)
	// fmt.Println(a_dict)

	// var json_string = json_tool.Convert_map_to_json_string(a_dict)
	// fmt.Println(json_string)

	/*
		// create array from type
		func CreateArray(t reflect.Type, length int) reflect.Value {
		var arrayType reflect.Type
		arrayType = reflect.ArrayOf(length, t)
		return reflect.Zero(arrayType)


		// create object from type
		var a_list = make([]Get_Users_Request, 0)
		var type_of_an_element_in_a_list = reflect.TypeOf(a_list).Elem()
		var instance_of_a_type = reflect.Zero(type_of_an_element_in_a_list)
		fmt.Println(type_of_an_element_in_a_list)
		fmt.Println(instance_of_a_type)
	*/
}
