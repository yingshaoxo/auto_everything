// yingshaoxo:
// Why to support some languages that you can't even input?
// The utf-8 chracter are actually bytes, process them like english words, show single character as pictures, just like what you do in micro_controller hardware project with led points.
//
#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>
#include <stdbool.h>
#include <string.h>

/*
String type
*/
typedef struct Type_Ypython_String Type_Ypython_String;
struct Type_Ypython_String {
    bool is_none;
    wchar_t *type;
    wchar_t *value;
    long long length;

    Type_Ypython_String* (*function_add)(Type_Ypython_String *self, Type_Ypython_String *another_string);
    bool (*function_is_equal)(Type_Ypython_String *self, Type_Ypython_String *another_string);
    // Add more wide character function pointers here for multilingual support
};

Type_Ypython_String *Ypython_String(wchar_t *value);
Type_Ypython_String *Type_Ypython_String_add(Type_Ypython_String *self, Type_Ypython_String *another_string) {
    Type_Ypython_String *new_string_value = Ypython_String(L"");

    if (self->is_none || another_string->is_none) {
        new_string_value->value = L"";
        new_string_value->length = wcslen(new_string_value->value);
        new_string_value->is_none = true;
    } else {
        new_string_value->is_none = false;

        size_t total_length = wcslen(self->value) + wcslen(another_string->value);
        wchar_t *new_wchars_value = (wchar_t *)malloc((total_length + 1) * sizeof(wchar_t));
        swprintf(new_wchars_value, total_length+1, L"%s%s", self->value, another_string->value);

        new_string_value->value = new_wchars_value;
        new_string_value->length = wcslen(new_string_value->value);
    }

    return new_string_value;
}

bool Type_Ypython_String_is_equal(Type_Ypython_String *self, Type_Ypython_String *another_string) {
    if (self->is_none && another_string->is_none) {
        return true;
    }
    else if ((!(self->is_none)) && (another_string->is_none)) {
        return false;
    }
    else if ((self->is_none) && (!(another_string->is_none))) {
        return false;
    } else {
        if (wcscmp(self->value, another_string->value) == 0) {
            return true;
        } else {
            return false;
        }
    }
}

// Add more wide character functions here for multilingual support

Type_Ypython_String *Ypython_String(wchar_t *value) {
    Type_Ypython_String *new_string_value;
    new_string_value = (Type_Ypython_String *)malloc(sizeof(Type_Ypython_String));

    new_string_value->is_none = false;
    new_string_value->type = L"string";

    new_string_value->value = value;
    new_string_value->length = wcslen(value);

    new_string_value->function_add = &Type_Ypython_String_add;
    new_string_value->function_is_equal = &Type_Ypython_String_is_equal;
    // Add more wide character function assignments here for multilingual support

    return new_string_value;
}

int main() {
    // Example usage of the modified code
    Type_Ypython_String *str1 = Ypython_String(L"Hello, ");
    Type_Ypython_String *str2 = Ypython_String(L"world!");
    
    Type_Ypython_String *result = str1->function_add(str1, str2);
    
    wprintf(L"%ls\n", result->value); // Output: Hello, world!

    return 0;
}
