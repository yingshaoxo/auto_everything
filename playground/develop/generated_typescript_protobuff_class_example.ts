const _ygrpc_official_types = ["string", "number", "boolean"];

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
                new_list.push(_general_from_dict_function(old_object, one))
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
                            if ((typeof old_object._property_name_to_its_type_dict[key]) == "string") {
                                // default value type
                                old_object[key] = new_object[key]
                            } else {
                                // custom message type || enum
                                if ((typeof old_object._property_name_to_its_type_dict[key]).includes("class")) {
                                    // custom message type
                                    old_object[key] = _general_from_dict_function(new (old_object._property_name_to_its_type_dict[key])(), new_object[key])
                                } else {
                                    // enum
                                    old_object[key] = new_object[key]
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
        return structuredClone(this)
    }

    from_dict(item: _User): User {
        let new_dict = _general_from_dict_function(this, item)

        let an_item = new User()
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
