import re
from typing import Any, Dict, Tuple

from numpy import double

from auto_everything.terminal import Terminal
from auto_everything.io import IO
from auto_everything.disk import Disk
from auto_everything.network import Network

t = Terminal(debug=True)
disk = Disk()
io_ = IO()
network = Network()


class GRPC:
    def __init__(self):
        pass

    def generate_python_code(self, python: str, input_folder: str, input_files: list[str], output_folder: str = "generated_grpc"):
        """
        python: like python3, python3.10 and so on...

        input_folder: where protobuff files was located

        input_files: it is a list, like ["english.proto", "pornhub.proto"]

        output_folder: where those generated code file was located
        """
        if not disk.exists(input_folder):
            raise Exception(f"'{input_folder}' does not exist!")

        if "Usage".lower() not in t.run_command(f"{python} -m grpc_tools.protoc --help").lower():
            t.run(f"""
            # # llvm
            # export LDFLAGS="-L/opt/homebrew/opt/llvm/lib"
            # export CPPFLAGS="-I/opt/homebrew/opt/llvm/include"
            # export LDFLAGS="-L/opt/homebrew/opt/llvm/lib -Wl,-rpath,/opt/homebrew/opt/llvm/lib"

            # # openssl
            # export CFLAGS="-I/opt/homebrew/opt/openssl/include"
            # export LDFLAGS="-L/opt/homebrew/opt/openssl/lib"
            # export C_INCLUDE_PATH=/opt/homebrew/include
            # export CPLUS_INCLUDE_PATH=/opt/homebrew/include
            # export LIBRARY_PATH=/opt/homebrew/lib

            # export PKG_CONFIG_PATH="/opt/homebrew/opt/zlib/lib/pkgconfig"
            # export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:"/opt/homebrew/opt/qt@5/lib/pkgconfig"
            # export CMAKE_PREFIX_PATH="/opt/homebrew/opt/zlib"
            # export CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH:"/opt/homebrew/opt/qt@5"

            source ~/.bashrc
            {python} -m pip install grpcio grpcio-tools
            """)
            raise Exception(
                f"You should install grpc_tools by using:\n{python} -m pip install grpcio grpcio-tools"
            )

        t.run(f"""
        {python} -m pip install "betterproto[compiler]==2.0.0b5"
        """)

        input_folder = input_folder.rstrip("/")
        input_command = ""
        if len(input_files) == 0:
            input_command = f'{input_folder}/*'
        else:
            input_command = " ".join(input_files)

        t.run(
            f"""
        mkdir -p {output_folder}
        {python} -m grpc_tools.protoc --proto_path '{input_folder}' --python_betterproto_out='{output_folder}' '{input_command}'
        """)
        #--experimental_allow_proto3_optional

    def generate_golang_code(self, input_folder: str, input_files: list[str], output_folder: str = "generated_grpc"):
        """
        input_folder: where protobuff files was located

        input_files: it is a list, like ["english.proto", "pornhub.proto"]

        output_folder: where those generated golang file was located
        """
        if not disk.exists(input_folder):
            raise Exception(f"'{input_folder}' does not exist!")

        if "not found" in t.run_command("protoc --version"):
            raise Exception(
                "You should install protobuf-compiler by using:\n\nsudo apt install -y protobuf-compiler"
            )

        input_folder = input_folder.rstrip("/")

        t.run(f"""
        go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
        go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
        """)

        input_command = ""
        if len(input_files) == 0:
            input_command = f'{input_folder}/*'
        else:
            input_command = " ".join(input_files)
        
        t.run(
            f"""
        mkdir -p {output_folder}
        protoc --proto_path '{input_folder}' --go_out='{output_folder}' --go-grpc_out='{output_folder}' {input_command}
        """
        )

    def generate_dart_code(self, input_folder: str, input_files: list[str], output_folder: str = "lib/generated_grpc"):
        """
        input_folder: where protobuff files was located

        input_files: it is a list, like ["english.proto", "pornhub.proto"]

        output_folder: where those generated code file was located
        """
        if not disk.exists(input_folder):
            raise Exception(f"'{input_folder}' does not exist!")

        if "not found" in t.run_command("protoc --version"):
            raise Exception(
                "You should install protobuf-compiler by using:\n\nsudo apt install -y protobuf-compiler"
            )

        if "" == t.run_command("which $HOME/.pub-cache/bin/protoc-gen-dart"):
            raise Exception(
                "You should install protoc-gen-dart by using:\n\ndart pub global activate protoc_plugin"
            )

        input_folder = input_folder.rstrip("/")
        input_command = ""
        if len(input_files) == 0:
            input_command = f'{input_folder}/*'
        else:
            input_command = " ".join(input_files)

        # protoc --dart_out=grpc:lib/src/generated -Iprotos protos/helloworld.proto
        # dart pub global activate protoc_plugin
        t.run(
            f"""
        mkdir -p {output_folder}
        export PATH="$PATH":"$HOME/.pub-cache/bin"
        protoc --proto_path '{input_folder}' --dart_out=grpc:{output_folder} {input_command}
        """
        )

    def generate_typescript_code(self, input_folder: str, input_files: list[str], project_root_folder: str, output_folder: str = "src/generated_grpc"):
        """
        input_folder: where protobuff files was located

        input_files: it is a list, like ["english.proto", "pornhub.proto"]

        project_root_folder: where the `package.json` file was located

        output_folder: where those generated golang file was located
        """
        if not disk.exists(input_folder):
            raise Exception(f"'{input_folder}' does not exist!")

        if not disk.exists(project_root_folder):
            raise Exception(f"'{project_root_folder}' does not exist!")

        files = disk.get_files(folder=project_root_folder, recursive=False)
        package_json_exists = False
        for file in files:
            if "package.json" in file:
                package_json_exists = True
                break
        if not package_json_exists:
            raise Exception(f"'{project_root_folder}' is not a npm/yarn project, because it doesn't have package.json file!")

        if "not found" in t.run_command("protoc --version"):
            raise Exception(
                "You should install protobuf-compiler by using:\n\nsudo apt install -y protobuf-compiler"
            )

        input_folder = input_folder.rstrip("/")

        t.run(f"""
cd {project_root_folder}

yarn add grpc-tools --ignore-scripts -D
yarn add ts-protoc-gen@next -D

# if [[ $OSTYPE == 'darwin'* ]]; then
#     # brew install protobuf@3
#     # brew link --overwrite protobuf@3
    pushd "{project_root_folder}/node_modules/grpc-tools"
    ./node_modules/.bin/node-pre-gyp install --target_arch=x64
    popd
# fi

yarn add @protobuf-ts/plugin
# yarn add @improbable-eng/grpc-web
        """)

        input_command = ""
        if len(input_files) == 0:
            input_command = f'{input_folder}/*'
        else:
            input_command = " ".join(input_files)
        
        t.run(
            f"""
mkdir -p {output_folder}

# --js_out="import_style=commonjs,binary:{output_folder}" \

protoc \
    --proto_path {input_folder} \
    --plugin="protoc-gen-ts={project_root_folder}/node_modules/.bin/protoc-gen-ts" \
    --plugin="protoc-gen-grpc={project_root_folder}/node_modules/.bin/grpc_tools_node_protoc_plugin" \
    --ts_out="service=grpc-web,mode=grpc-js:{output_folder}" \
    --grpc_out="grpc_js:{output_folder}" \
    {input_command}
""")

    def _get_raw_data_from_proto_file(self, proto_file_path: str):
        proto_string = io_.read(proto_file_path)
        found = re.findall(r"message\s+(?P<object_name>\w+)\s+\{(?P<properties>(\s*.*?\s*)+)\}", proto_string, re.DOTALL)
        return found
    
    def _get_data_from_proto_file(self, proto_file_path: str) -> Dict[str, Any]:
        proto_string = io_.read(proto_file_path)

        found = re.findall(r"message\s+(?P<object_name>\w+)\s+\{(?P<properties>(\s*.*?\s*)+)\}", proto_string, re.DOTALL)
        found = [
                    [string.strip() for string in one][:2]
                    for one in found
                ]

        data = {}
        for one in found:
            if len(one) == 2:
                class_name = one[0]
                property_text = one[1]
                if len(property_text) == 0:
                    continue
                property_list = re.findall(r"\w+\s+(?P<property>\w+)\s+=\s+\d+;", property_text)
                data[class_name] = property_list
        
        return data #type: ignore
    
    def generate_key_string_map_from_protocols(self, for_which_language:str , input_folder: str, input_files: list[str], output_folder: str|None = "grpc_key_string_maps"):
        #your name
        """
        for_which_language: 'rust', 'python', 'kotlin', 'go'...

        input_folder: where protobuff files was located

        input_files: it is a list, like ["english.proto", "pornhub.proto"]

        output_folder: where those generated code file was located
        """
        if not disk.is_directory(input_folder):
            raise Exception(f"The input_folder must be an directory.")

        if output_folder == None:
            output_folder_variable_name = [ k for k,v in locals().items() if v == output_folder][0]
            raise Exception(f"You must give '{str(output_folder_variable_name)}' paramater.")
        else:
            disk.create_a_folder(output_folder)

        if not disk.exists(input_folder):
            raise Exception(f"'{input_folder}' does not exist!")
        input_folder = input_folder.rstrip("/")
        files = disk.get_files(input_folder, recursive=False, type_limiter=[".proto"])

        new_files:list[str] = []
        for file in files:
            if any([one for one in input_files if file.endswith("/"+one)]):
                new_files.append(file)
        files = new_files.copy()

        if for_which_language == "python":
            for file in files:
                data_ = self._get_data_from_proto_file(file)
                filename,_ = disk.get_stem_and_suffix_of_a_file(file)
                target_file_path:str = disk.join_paths(output_folder, filename+".py")

                sub_class_container_list:list[str] = []
                for key, value in data_.items():
                    variable_list:list[str] = []
                    for one in value:
                        variable_list.append(f"""
    {one}: str = "{one}"
                        """.strip("\n").rstrip())
                    variable_list_text = "\n".join(variable_list).rstrip()
                    
                    sub_class_container_list.append(f"""
class {key}:
{variable_list_text}
    __property_list__: List[str] = [{", ".join(['"'+one+'"' for one in value])}]
                    """.strip("\n").rstrip())

                sub_class_container_list_text = "\n\n".join(sub_class_container_list)
                python_code = f"""
from typing import List

{sub_class_container_list_text}
                """.rstrip()

                io_.write(target_file_path, python_code)
        elif for_which_language == "rust":
            for file in files:
                data_ = self._get_data_from_proto_file(file)
                """
                    (VoiceRequest, ['uuid', 'timestamp', 'voice'])
                    (VoiceReply, ['uuid', 'timestamp', 'voice'])
                """
                filename,_ = disk.get_stem_and_suffix_of_a_file(file)
                target_file_path = disk.join_paths(output_folder, filename+".rs")

                kotlin_code = ""
                for key, value in data_.items():
                    kotlin_code += f"""
\n
pub struct {key} {{
}}
                    """

                    property_text = ''.join([f'    pub const {one}: &str = "{one}";\n' for one in value]).strip()

                    kotlin_code += f"""
impl {key} {{
    {property_text}
}}
                    """
                kotlin_code = kotlin_code.strip()
                io_.write(target_file_path, kotlin_code)

            mod_file_path = disk.join_paths(output_folder, "mod.rs")
            disk.delete_a_file(mod_file_path)
            for file in files:
                filename,_ = disk.get_stem_and_suffix_of_a_file(file)
                io_.append(mod_file_path, f"\npub mod {filename};\n")

        elif for_which_language == "kotlin":
            for file in files:
                data_ = self._get_data_from_proto_file(file)
                filename,_ = disk.get_stem_and_suffix_of_a_file(file)
                target_file_path = disk.join_paths(output_folder, filename+".kt")

                sub_class_container_list = []
                for key, value in data_.items():
                    variable_list = []
                    for one in value:
                        variable_list.append(f"""
                    var {one}: String = "{one}"
                        """.strip("\n").rstrip())
                    variable_list_text = "\n".join(variable_list).rstrip()
                    
                    sub_class_container_list.append(f"""
            class {key} {{
                companion object {{
                    @JvmField 
{variable_list_text}
                    val __property_list__: List<String> = listOf({", ".join(['"'+one+'"' for one in value])})
                }}
            }}
                    """.strip("\n").rstrip())

                sub_class_container_list_text = "\n\n".join(sub_class_container_list)
                kotlin_code = f"""
package grpc_key_string_maps

class {filename}_key_string_maps {{
    companion object {{
{sub_class_container_list_text}
    }}
}}
                """.rstrip()

                # var __column_key_list: List<String> = listOf<String>()
                io_.write(target_file_path, kotlin_code)

        elif for_which_language == "golang":
            for file in files:
                data_ = self._get_data_from_proto_file(file)
                filename,_ = disk.get_stem_and_suffix_of_a_file(file)
                sub_folder_path = disk.join_paths(output_folder, f"{filename}_grpc_key_string_maps")
                if not disk.exists(sub_folder_path):
                    disk.create_a_folder(sub_folder_path)
                target_file_path = disk.join_paths(sub_folder_path, filename+".go")

                sub_class_container_list = []
                for key, value in data_.items():
                    struct_property_declaration_list = [
                        f"""
    {one[0].upper() + one[1:]}    string
                        """.rstrip() for one in value
                    ]
                    struct_property_declaration_list_text = ''.join(struct_property_declaration_list)

                    struct_property_real_value_list = [
                        f"""
    {one[0].upper() + one[1:]}:    "{one}",
                        """.rstrip() for one in value
                    ]
                    struct_property_real_value_list_text = ''.join(struct_property_real_value_list)

                    column_key_list_text = ''.join([f'''
        "{one}",
                    '''.rstrip() for one in value])
                    one_part = f"""
var {key[0].upper() + key[1:]} = struct {{{struct_property_declaration_list_text}

    Column_key_list__    []string
}} {{{struct_property_real_value_list_text}

    Column_key_list__:    []string{{{column_key_list_text}
    }},
}}
                    """.rstrip()
                    sub_class_container_list.append(one_part)
                sub_class_container_list_text = "\n\n".join(sub_class_container_list)

                template = f"""
package {filename}_grpc_key_string_maps

{sub_class_container_list_text}
                """.strip()

                # var Column_key_list__: List<String> = listOf<String>()
                io_.write(target_file_path, template)
        else:
            raise Exception(f"We don't support '{for_which_language}' language.")


class YRPC:
    _yrpc_type_to_python_type_dict = {
        "string": "str",
        "bool": "bool",
        "uint32": "int",
        "int32": "int",
        "int64": "int",
        "uint64": "int",
        "bytes": "str",
        "float": "float",
        "double": "float"
    }

    # def _get_python_type_from_yrpc_type(self, type_string: str):
    #     if type_string in self._yrpc_type_to_python_type_dict:
    #         return self._yrpc_type_to_python_type_dict.get(type_string)
    #     else:
    #         return None

    def get_information_from_yrpc_protocol_code(self, source_code: str) -> Tuple[dict[str, Any], dict[str, Any]]:
        code_block_list = re.findall(r"(?P<type>\w+)\s+(?P<object_name>\w+)\s+\{(?P<properties>(\s*.*?\s*)+)\}", source_code, re.DOTALL)
        code_block_list = [
                    [string for string in one][:3]
                    for one in code_block_list
                ]

        new_parsed_object_list: list[Any] = []
        for one in code_block_list.copy():
            if len(one) == 3:
                type_ = one[0]
                class_name = one[1]
                content = one[2]

                if (type_ == "service"):
                    new_parsed_object_list.append([type_.strip(), class_name.strip(), content])
                else:
                    property_text = " " + content.strip()
                    if len(property_text) == 0:
                        continue

                    property_list = []
                    if (type_ == "message"):
                        property_list = re.findall(r"(?P<feature>\w*)\s+(?P<type>\w+)\s+(?P<property>\w+)\s+=\s+\d+;", property_text)
                    elif (type_ == "enum"):
                        property_list = re.findall(r"(?P<property>\w+)\s+=\s+\d+;", property_text)
                        property_list = [('','string', one) for one in property_list]

                    new_parsed_object_list.append([type_.strip(), class_name.strip(), property_list])
        
        class_name_list = [one[1].strip() for one in new_parsed_object_list]
        for one in class_name_list:
            if class_name_list.count(one) > 1:
                raise Exception("You must make sure there has no duplicated class/message name.")

        arguments_defination_tree:dict[str, Any] = {}
        for one in new_parsed_object_list.copy():
            code_block_type = one[0].strip()
            class_name = one[1].strip()
            variable_list = one[2]

            if code_block_type == "service":
                continue

            name_list = [one[2] for one in variable_list]
            for one in name_list:
                if name_list.count(one) > 1:
                    raise Exception("You must make sure there has no duplicated variable name.")

            arguments_defination_tree[class_name] = {
                "**type**": code_block_type
            }
            for one_variable in variable_list:
                feature = one_variable[0]
                type = one_variable[1]
                name = one_variable[2]

                arguments_defination_tree[class_name][name] = {
                    "type": type, 
                    "is_list": True if feature == "repeated" else False,
                    "name": name,
                    "feature": feature
                }

        rpc_defination_tree: dict[str, Any] = {}
        for one in new_parsed_object_list.copy():
            code_block_type = one[0].strip()
            class_name = one[1].strip()
            content = one[2]

            if code_block_type != "service":
                continue

            variable_list: list[Any] = re.findall(r"rpc\s+(?P<function_name>\w+)\s+\((?P<input_variable>[\w\s]+)\)\s+returns\s+\((?P<output_variable>[\w\s]+)\);", content)

            name_list = [one[0].strip() for one in variable_list]
            for one in name_list:
                if name_list.count(one) > 1:
                    raise Exception("You must make sure there has no duplicated variable name.")

            for one in variable_list:
                function_name = one[0].strip()
                input_variable = one[1].strip()
                output_variable = one[2].strip()

                rpc_defination_tree[function_name] = {
                    "input_variable": input_variable,
                    "output_variable": output_variable
                }

        return arguments_defination_tree, rpc_defination_tree

    def _convert_yrpc_code_into_python_code(self, source_code: str) -> str:
        arguments_dict, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        enum_code_block_list: list[str] = []
        dataclass_code_block_list: list[str] = []
        for class_name, class_info in arguments_dict.items():
            code_block_type = class_info["**type**"]
            del class_info["**type**"]

            if code_block_type == "enum":
                variable_list: list[str] = []
                for index, one in enumerate(class_info.values()):
                    name = one['name']
                    variable_list.append(f"""
    {name} = {index}
                    """.rstrip().lstrip('\n'))
                variable_list_text = "\n".join(variable_list)

                enum_class_text = f"""
class {class_name}(Enum):
{variable_list_text}
                """.rstrip().lstrip('\n')

                enum_code_block_list.append(enum_class_text)
            else:
                variable_list: list[str] = []
                property_name_to_its_type_dict_variable_list: list[str] = []
                key_string_dict_list: list[str] = []
                for index, one in enumerate(class_info.values()):
                    name = one['name']
                    type = self._yrpc_type_to_python_type_dict.get(one['type']) 
                    if type == None:
                        if one['type'] in arguments_dict.keys():
                            type = one['type']
                        else:
                            raise Exception(f"We don't support type of '{one['type']}'")
                    is_list = one['is_list']

                    if is_list == False:
                        variable_list.append(f"""
    {name}: {type} | None = None
                        """.rstrip().lstrip('\n'))
                    else:
                        variable_list.append(f"""
    {name}: list[{type}] | None = None
                        """.rstrip().lstrip('\n'))

                    property_name_to_its_type_dict_variable_list.append(f"""
        "{name}": {type},
                    """.rstrip().lstrip('\n'))

                    key_string_dict_list.append(f"""
        {name}: str = "{name}"
                    """.rstrip().lstrip('\n'))

                variable_list_text = "\n".join(variable_list)
                property_name_to_its_type_dict_variable_list_text = "\n".join(property_name_to_its_type_dict_variable_list)
                key_string_dict_list_text = "\n".join(key_string_dict_list)
                if len(key_string_dict_list_text.strip()) == 0:
                    key_string_dict_list_text = """
        pass
                    """.rstrip().lstrip('\n')

                dataclass_text = f"""
@dataclass()
class {class_name}(YRPC_OBJECT_BASE_CLASS):
{variable_list_text}

    property_name_to_its_type_dict_ = {{
{property_name_to_its_type_dict_variable_list_text}
    }}

    @dataclass()
    class key_string_dict_:
{key_string_dict_list_text}
                """.rstrip().lstrip('\n')

                dataclass_code_block_list.append(dataclass_text)

        enum_code_block_list_text = "\n\n\n".join(enum_code_block_list)
        dataclass_code_block_list_text = "\n\n\n".join(dataclass_code_block_list)

        template_text = f"""
from dataclasses import dataclass
from enum import Enum
from typing import Any


_ygrpc_official_types = [int, float, str, bool]


{enum_code_block_list_text}


def convert_dict_that_has_enum_object_into_pure_dict(value: Any) -> dict[str, Any] | list[Any] | Any:
    if type(value) is list:
        new_list: list[Any] = []
        for one in value: #type: ignore
            new_list.append(convert_dict_that_has_enum_object_into_pure_dict(value=one)) 
        return new_list
    elif type(value) is dict:
        new_dict: dict[str, Any] = {{}}
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
        new_dict: dict[str, Any] = {{}}
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

        
{dataclass_code_block_list_text}
        """.strip()
        return template_text.strip()

    def generate_python_code(self, input_folder: str, input_files: list[str], output_folder: str = "src/generated_yrpc"):
        """
        input_folder: where protobuff files was located

        input_files: it is a list, like ["english.proto", "pornhub.proto"]

        output_folder: where those generated code file was located
        """
        input_folder = input_folder.rstrip("/")

        if not disk.exists(input_folder):
            raise Exception(f"The input_forder '{input_folder}' does not exist!")

        if not disk.is_directory(input_folder):
            raise Exception(f"The input_folder '{input_folder}' must be an directory.")

        if not disk.is_directory(output_folder):
            disk.create_a_folder(output_folder)

        files = disk.get_files(input_folder, recursive=False, type_limiter=[".proto"])

        new_files:list[str] = []
        for file in files:
            if any([one for one in input_files if file.endswith("/"+one)]):
                new_files.append(file)
        files = new_files.copy()

        for file in files:
            filename,_ = disk.get_stem_and_suffix_of_a_file(file)
            target_file_path = disk.join_paths(output_folder, filename+".py")

            source_code = io_.read(file_path=file)
            final_code = self._convert_yrpc_code_into_python_code(source_code=source_code)

            io_.write(file_path=target_file_path, content=final_code)


if __name__ == "__main__":
    yrpc = YRPC()

    # source_code = io_.read("./playground/develop/test_protobuff_code.proto")
    # arguments_dict, rpc_dict = yrpc.get_information_from_yrpc_protocol_code(source_code=source_code)

    # print(arguments_dict)
    # print()
    # print(rpc_dict)

    yrpc.generate_python_code(
        input_folder="/Users/yingshaoxo/CS/auto_everything/playground/develop",
        input_files=["test_protobuff_code.proto"],
        output_folder="/Users/yingshaoxo/CS/auto_everything/playground/develop/build"
    )

    # grpc = GRPC()
    # grpc.generate_python_code(
    #     input_folder="/tmp/hi/protos/", output_folder="/tmp/hi/py_grpc"
    # )
    # grpc.generate_golang_code(
    #     input_folder="/tmp/hi/protos/", output_folder="/tmp/hi/go_grpc"
    # )
    # grpc.generate_dart_code(
    #     input_folder="/tmp/hi/protos/", output_folder="/tmp/hi/dart_grpc"
    # )
    # grpc.generate_key_string_map_from_protocols(
    #     for_which_language="golang",
    #     input_folder="/Users/yingshaoxo/CS/we_love_party/party_protocols/protocols",
    #     input_files=["management_service.proto"],
    #     output_folder="/Users/yingshaoxo/CS/we_love_party/management_system/golang_backend_service/grpc_key_string_maps",
    # )
    # grpc.generate_typescript_code(
    #     input_folder="/Users/yingshaoxo/CS/we_love_party/party_protocols/protocols",
    #     input_files=["management_service.proto"],
    #     project_root_folder="/Users/yingshaoxo/CS/we_love_party/management_system/react_web_client",
    #     output_folder="/Users/yingshaoxo/CS/we_love_party/management_system/react_web_client/src/generated_grpc",
    # )
