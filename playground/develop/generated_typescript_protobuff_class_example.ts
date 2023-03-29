// have to make sure enum key is in enum defination
const _ygrpc_official_types = ["string", "number", "boolean"];

export const clone_object_ = (obj: any) =>  JSON.parse(JSON.stringify(obj));

export const get_secret_alphabet_dict_ = (a_secret_string: string) =>  {
    const ascii_lowercase = "abcdefghijklmnopqrstuvwxyz".split("")
    const number_0_to_9 = "0123456789".split("")

    var new_key = a_secret_string.replace(" ", "").toLowerCase().split("")
    var character_list: string[] = []
    for (var char of new_key) {
        if ((/[a-zA-Z]/).test(char)) {
            if (!character_list.includes(char)) {
                character_list.push(char)
            }
        }
    }

    if (character_list.length >= 26) {
        character_list = character_list.slice(0, 26)
    } else {
        var characters_that_the_key_didnt_cover: string[] = []
        for (var char of ascii_lowercase) {
            if (!character_list.includes(char)) {
                characters_that_the_key_didnt_cover.push(char)
            }
        }
        character_list = character_list.concat(characters_that_the_key_didnt_cover) 
    }

    var final_dict = {} as Record<string, string>

    // for alphabet
    for (let [index, char] of ascii_lowercase.entries()) {
        final_dict[char] = character_list[index]
    }

    // for numbers
    var original_numbers_in_alphabet_format = ascii_lowercase.slice(0, 10) // 0-9 representations in alphabet format
    var secret_numbers_in_alphabet_format = Object.values(final_dict).slice(0, 10)
    var final_number_list = [] as string[]
    for (var index in number_0_to_9) {
        var secret_char = secret_numbers_in_alphabet_format[index]
        if (original_numbers_in_alphabet_format.includes(secret_char)) {
            final_number_list.push(String(original_numbers_in_alphabet_format.findIndex((x) => x===secret_char)))
        }
    }
    if (final_number_list.length >= 10) {
        final_number_list = final_number_list.slice(0, 10)
    } else {
        var numbers_that_didnt_get_cover = [] as string[]
        for (var char of number_0_to_9) {
            if (!final_number_list.includes(char)) {
                numbers_that_didnt_get_cover.push(char)
            }
        }
        final_number_list = final_number_list.concat(numbers_that_didnt_get_cover)
    }
    for (let [index, char] of final_number_list.entries()) {
        final_dict[String(index)] = char
    }

    return final_dict
};

export const encode_message_ = (a_secret_dict: Record<string, string>, message: string):string => {
    var new_message = ""
    for (const char of message) {
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {
            new_message += char
            continue
        }
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {
            new_char = new_char.toUpperCase()
        }
        new_message += new_char
    }
    return new_message
}

export const decode_message_ = (a_secret_dict: Record<string, string>, message: string):string => {
    var new_secret_dict = {} as Record<string, string>
    for (var key of Object.keys(a_secret_dict)) {
        new_secret_dict[a_secret_dict[key]] = key
    }
    a_secret_dict = new_secret_dict

    var new_message = ""
    for (const char of message) {
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {
            new_message += char
            continue
        }
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {
            new_char = new_char.toUpperCase()
        }
        new_message += new_char
    }
    return new_message
}

const _general_to_dict_function = (object: any): any => {
    let the_type = typeof object
    if (the_type == "object") {
        if (object == null) {
            return null
        } else if (Array.isArray(object)) {
            let new_list: any[] = []
            for (const one of object) {
                new_list.push(_general_to_dict_function(one))
            }
            return new_list
        } else {
            let keys = Object.keys(object);
            if (keys.includes("_key_string_dict")) {
                // custom message type
                let new_dict: any = {}
                keys = keys.filter((e) => !["_property_name_to_its_type_dict", "_key_string_dict"].includes(e));
                for (const key of keys) {
                    new_dict[key] = _general_to_dict_function(object[key])
                    // the enum will become a string in the end, so ignore it
                }
                return new_dict
            }
        }
    } else {
        if (_ygrpc_official_types.includes(typeof object)) {
            return object
        } else {
            return null
        }
    }
    return null
};

const _general_from_dict_function = (old_object: any, new_object: any): any => {
    let the_type = typeof new_object
    if (the_type == "object") {
        if (Array.isArray(new_object)) {
            //list
            let new_list: any[] = []
            for (const one of new_object) {
                new_list.push(structuredClone(_general_from_dict_function(old_object, one)))
            }
            return new_list
        } else {
            // dict or null
            if (new_object == null) {
                return null
            } else {
                let keys = Object.keys(old_object);
                if (keys.includes("_key_string_dict")) {
                    keys = Object.keys(old_object._property_name_to_its_type_dict)
                    for (const key of keys) {
                        if (Object.keys(new_object).includes(key)) {
                            // console.log((typeof old_object._property_name_to_its_type_dict[key]))
                            if ((typeof old_object._property_name_to_its_type_dict[key]) == "string") {
                                // default value type
                                old_object[key] = new_object[key]
                            } else {
                                // custom message type || enum
                                if (
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("class") || 
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("function")
                                ) {
                                    // custom message type || a list of custom type
                                    var reference_object = new (old_object._property_name_to_its_type_dict[key])()
                                    old_object[key] = structuredClone(_general_from_dict_function(reference_object, new_object[key]))
                                } else {
                                    // enum
                                    if (Object.keys(new_object).includes(key)) {
                                        old_object[key] = new_object[key]
                                    } else {
                                        old_object[key] = null
                                    }
                                }
                            }
                        } 
                    }
                } else {
                    return null
                }
            }
        }
    } 
    return old_object
}

export enum UserStatus {
    OFFLINE = "OFFLINE",
    ONLINE = "ONLINE",
}

export interface _User {
    id: number | null;
    name: string[] | null;
    user_status: UserStatus | null;
    user: User | null;
}

export class User {
    id: number | null = null;
    name: string[] | null = null;
    user_status: UserStatus | null = null;
    user: User | null = null;

    _property_name_to_its_type_dict = {
        id: "number",
        name: "string",
        user_status: UserStatus,
        user: User
    };

    _key_string_dict = {
        id: "id",
        name: "name",
        user_status: "user_status",
        user: "user"
    };

    to_dict(): _User {
        return _general_to_dict_function(this);
    }

    /*
    merge_from_dict(item: dict) {
        // when old dict has key in new dict, update it, include null
    }
    */

    _clone(): User {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
        // return structuredClone(this)
    }

    from_dict(item: _User): User {
        let an_item = new User()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}

/*
let a_user = new User().from_dict({
    id: 3,
    name: ["yingshaoxo", "yingjie.hu"],
    user_status: UserStatus.ONLINE,
    user: new User()
});

// console.log(a_user)

let a_user_dict = a_user.to_dict()
console.log(a_user_dict)

let another_user = new User()

// // // console.log(String(UserStatus));
// // // console.log(String(User));
console.log(another_user.from_dict(a_user_dict).to_dict())
*/

var secret_dict = get_secret_alphabet_dict_("yingshaoxo is the best")
console.log(secret_dict)

var source_message = "Hello, world, I'm yingshaoxo. Here is the test number: 9111108848."

var encrypted_message = encode_message_(secret_dict, source_message)
console.log(encrypted_message)

var decoded_message = decode_message_(secret_dict, encrypted_message)
console.log(decoded_message)

console.log(decoded_message === source_message )