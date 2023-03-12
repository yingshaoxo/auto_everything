const _ygrpc_official_types = ["string", "number", "boolean"];

const _general_to_dict_function = (object: any): any => {
    let keys = Object.keys(object);
    keys = keys.filter((e) => !["_property_name_to_its_type_dict", "_key_string_dict"].includes(e));

    let new_dict: any = {}
    for (const key of keys) {
        if (Object.keys(object._key_string_dict).includes(key)) {
            let value = object[key];
            if (Array.isArray(value)) {
                let new_list: any[] = []
                for (const one of value) {
                    new_list.push(_general_to_dict_function(one))
                }
                new_dict[key] = new_list
            } else {
                if (_ygrpc_official_types.includes(typeof value)) {
                    new_dict[key] = value
                } else {
                    if ((typeof value).includes("class")) {
                        // custom message type
                        let new_value = _general_to_dict_function(value)
                        new_dict[key] = new_value
                    } else {
                        // enum
                        new_dict[key] = value
                    }
                }
            }
        }
    }

    return new_dict
};

const _general_from_dict_function = (old_object: any, new_object: any): any => {
    let keys = Object.keys(old_object);
    keys = keys.filter((e) => !["_property_name_to_its_type_dict", "_key_string_dict"].includes(e));

    let new_dict: any = {}
    for (const key of keys) {
        if (Object.keys(new_object).includes(key)) {
            let value = new_object[key];
            if (Array.isArray(value)) {
                let new_list: any[] = []
                for (const one of value) {
                    new_list.push(_general_from_dict_function(new (old_object._property_name_to_its_type_dict[key])(), one))
                }
                new_dict[key] = new_list
            } else {
                if (_ygrpc_official_types.includes(typeof value)) {
                    new_dict[key] = value
                } else {
                    if (value == null) {
                        new_dict[key] = null
                    } else if ((typeof value) == 'object') {
                        // custom message type
                        new_dict[key] = _general_from_dict_function(new (old_object._property_name_to_its_type_dict[key])(), value)
                    } else {
                        // enum
                        new_dict[key] = old_object._property_name_to_its_type_dict[key](value)
                    }
                }
            }
        }
    }

    return new_dict
}

enum UserStatus {
    OFFLINE = "OFFLINE",
    ONLINE = "ONLINE",
}

interface _User {
    id: number | null;
    name: string | null;
    user_status: UserStatus | null;
    user: User | null;
}

class User {
    id: number | null = null;
    name: string | null = null;
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

    from_dict(item: _User): User {
        let new_dict = _general_from_dict_function(this, item)

        if (new_dict == null) {
            return new User()
        }

        let an_item = new User()
        for (const key of Object.keys(new_dict)) {
            //@ts-ignore
            this[key] = new_dict[key]
            //@ts-ignore
            an_item[key] = new_dict[key]
        }

        return an_item
    }
}

let a_user = new User().from_dict({
    id: 3,
    name: "yingshaoxo",
    user_status: UserStatus.ONLINE,
    user: new User()
});

// console.log(a_user)

let a_user_dict = a_user.to_dict()
// console.log(a_user_dict)

let another_user = new User()

// console.log(String(UserStatus));
// console.log(String(User));
console.log(another_user.from_dict(a_user_dict).to_dict())
