enum Status {
  offline,
  online,
}

class Key_string_dict_for_YingshaoxoInfo_ {
  final String id = "id";
  final String name = "name";
  final String status = "status";
}

class YingshaoxoInfo {
  int? id;
  String? name;
  Status? status;

  YingshaoxoInfo({this.id, this.name, this.status});

  final Map<String, dynamic> property_name_to_its_type_dict_ = {
    "id": int,
    "name": String,
    "status": Status
  };

  final key_string_dict_for_YingshaoxoInfo_ =
      Key_string_dict_for_YingshaoxoInfo_();

  Map<String, dynamic> to_dict() {
    return {
      'id': this.id,
      'name': this.name,
      'status': this.status?.name,
    };
  }

  dynamic from_dict(Map<String, dynamic>? json) {
    if (json == null) {
      return;
    }

    this.id = json['id'];
    this.name = json['name'];
    this.status =
        Status.values.map((e) => e.name).toList().indexOf(json['status']) == -1
            ? null
            : Status.values.byName(json['status']);

    return YingshaoxoInfo(
        id: json['id'],
        name: json['name'],
        status:
            Status.values.map((e) => e.name).toList().indexOf(json['status']) ==
                    -1
                ? null
                : Status.values.byName(json['status']));
  }
}

class Key_string_dict_for_Room_ {
  final String id = "id";
  final String title = "title";
  final String YingshaoxoInfo = "YingshaoxoInfo";
}

class Room {
  int? id;
  String? title;
  YingshaoxoInfo? user;

  Room({this.id, this.title, this.user});

  final Map<String, dynamic> property_name_to_its_type_dict_ = {
    "id": int,
    "title": String,
    "user": YingshaoxoInfo,
  };

  final key_string_dict_for_Room_ = Key_string_dict_for_Room_();

  Map<String, dynamic> to_dict() {
    return {
      'id': this.id,
      'title': this.title,
      'user': this.user?.to_dict(),
    };
  }

  dynamic from_dict(Map<String, dynamic>? json) {
    if (json == null) {
      return;
    }

    this.id = json['id'];
    this.title = json['title'];
    this.user = YingshaoxoInfo().from_dict(json['user']);

    return Room(
        id: json['id'],
        title: json['title'],
        user: YingshaoxoInfo().from_dict(json['user']));
  }
}

void main() {
  // print("hello, world.");

  // print(String == bool);

  // var room = Room(id: 0);

  // var class_info = reflect(room);
  // print(class_info.getField(new Symbol("id")).reflectee);
  // print(class_info.setField(new Symbol("id"), 2));
  // print(class_info.getField(new Symbol("id")).reflectee);
  // print(class_info.type);
  // print(class_info.reflectee.property_name_to_its_type_dict_);

  // Status? status = Status.offline;
  // print(reflect(status).type.isEnum);

  // print(reflectType(Status));
  // newInstance(Symbol(""), [], []).reflectee;

  // Map<String, dynamic> dict_1 = room.to_dict();
  // print(dict_1);

  // var room2 = room.from_json(dict_1);
  // print(room2.to_dict());

  // var room_1 = Room(
  //     id: 0,
  //     title: "a",
  //     user: YingshaoxoInfo(id: 1, name: "A", status: Status.offline));
  // var room_1_dict = room_1.to_dict();
  // print(room_1_dict);

  // var room_2 = Room();
  // room_2.from_dict(room_1_dict);
  // print(room_2.to_dict());
}







// ####################
// from_dict()

// const List<dynamic> _ygrpc_official_types = [String, int, bool];

// var this_object_info = reflect(this);

// for (MapEntry e in json.entries) {
//   if (this.property_name_to_its_type_dict_.keys.contains(e.key)) {
//     var the_refrence_type = this.property_name_to_its_type_dict_[e.key];

//     if (reflect(the_refrence_type).type.isEnum) {
//       //enum
//     } else {
//       if (_ygrpc_official_types.contains(the_refrence_type)) {
//         // default type: string, int, bool
//         this_object_info.setField(new Symbol(e.key), e.value);
//       } else {
//         // custom message type

//         // this_object_info.setField(
//         //     new Symbol(e.key), the_refrence_type.from_dict(e.value));
//       }
//     }
//   }
// }
