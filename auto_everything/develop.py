from typing import Any, Dict, Tuple

import re
import os
from pprint import pprint

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
            raise Exception(f"We don't support '{for_which_language}' language. You can @yingshaoxo in social media or send him an email for support.")


class YRPC:
    _yrpc_type_to_python_type_dict = {
        "string": "str",
        "bytes": "str",

        "bool": "bool",

        "uint32": "int",
        "uint64": "int",
        "sint32": "int",
        "sint64": "int",
        "fixed32": "int",
        "fixed64": "int",
        "sfixed32": "int",
        "sfixed64": "int",
        "int32": "int",
        "int64": "int",
        "uint64": "int",

        "float": "float",
        "double": "float"
    }

    _yrpc_type_to_dart_type_dict = {
        "string": "String",
        "bytes": "String",

        "bool": "bool",

        "uint32": "int",
        "uint64": "int",
        "sint32": "int",
        "sint64": "int",
        "fixed32": "int",
        "fixed64": "int",
        "sfixed32": "int",
        "sfixed64": "int",
        "int32": "int",
        "int64": "int",
        "uint64": "int",

        "float": "double",
        "double": "double"
    }

    _yrpc_type_to_typescript_type_dict = {
        "string": "string",
        "bytes": "string",

        "bool": "boolean",

        "uint32": "number",
        "uint64": "number",
        "sint32": "number",
        "sint64": "number",
        "fixed32": "number",
        "fixed64": "number",
        "sfixed32": "number",
        "sfixed64": "number",
        "int32": "number",
        "int64": "number",
        "uint64": "number",

        "float": "number",
        "double": "number"
    }

    _yrpc_type_to_golang_type_dict = {
        "string": "string",
        "bytes": "string",

        "bool": "bool",

        "uint32": "int64",
        "uint64": "int64",
        "sint32": "int64",
        "sint64": "int64",
        "fixed32": "int64",
        "fixed64": "int64",
        "sfixed32": "int64",
        "sfixed64": "int64",
        "int32": "int64",
        "int64": "int64",
        "uint64": "int64",

        "float": "float64",
        "double": "float64"
    }

    def _capitalize_the_first_char_of_a_string(self, text: str) -> str:
        if len(text) == 0:
            return text
        return text[0].capitalize() + text[1:]

    def get_information_from_yrpc_protocol_code(self, source_code: str) -> Tuple[dict[str, Any], dict[str, Any]]:
        source_code = "\n".join(line for line in source_code.split("\n") if (not line.strip().startswith("//")))
        source_code = re.sub(r"/\*([\s\S]*?)\*/", "", source_code, flags=re.MULTILINE) 

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
                raise Exception(f"You must make sure there has no duplicated class/message name. (the duplicated one: '{one}')")

        enum_class_name_list = [one[1].strip() for one in new_parsed_object_list if one[0].strip() == "enum"]

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
                    raise Exception(f"You must make sure there has no duplicated variable name. (the duplicated one: '{one}')")

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
                    "is_enum": True if (type in enum_class_name_list) else False,
                    "is_custom_message_type": True if ((type in class_name_list) and (type not in enum_class_name_list)) else False,
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

            variable_list: list[Any] = re.findall(r"rpc\s+(?P<function_name>\w+)\s*\((?P<input_variable>[\w\s]+)\)\s+returns\s+\((?P<output_variable>[\w\s]+)\);", content)

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

    def _convert_yrpc_code_into_python_objects_code(self, source_code: str) -> str:
        arguments_dict, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        enum_code_block_list: list[str] = []
        dataclass_code_block_list: list[str] = []
        for class_name, class_info in arguments_dict.items():
            code_block_type = class_info["**type**"]
            del class_info["**type**"]

            if code_block_type == "enum":
                variable_list: list[str] = []
                a_temp_name = ""
                for index, one in enumerate(class_info.values()):
                    name = one['name']
                    a_temp_name = name
                    variable_list.append(f"""
    {name} = "{name}"
                    """.rstrip().lstrip('\n'))
                variable_list_text = "\n".join(variable_list)

                enum_class_text = f"""
class {class_name}(Enum):
    # yingshaoxo: I strongly recommend you use enum as a string type in other message data_model
    # for example, `{class_name}.{a_temp_name}.value`
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
                            raise Exception(f"We don't support type of '{one['type']}', have you defined this type in your protocol code?")
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

    _property_name_to_its_type_dict = {{
{property_name_to_its_type_dict_variable_list_text}
    }}

    @dataclass()
    class _key_string_dict:
{key_string_dict_list_text}

    def from_dict(self, dict: dict[str, Any]):
        new_variable: {class_name} = super().from_dict(dict)
        return new_variable
                """.rstrip().lstrip('\n')

                dataclass_code_block_list.append(dataclass_text)

        enum_code_block_list_text = "\n\n\n".join(enum_code_block_list)
        dataclass_code_block_list_text = "\n\n\n".join(dataclass_code_block_list)

        template_text = f"""
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
        old_dict = {{}}
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


{enum_code_block_list_text}

        
{dataclass_code_block_list_text}
        """.strip()
        return template_text.strip()

    def _convert_yrpc_code_into_auto_everything_based_python_rpc_code(self, identity_name: str, source_code: str) -> str:
        _, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        service_class_function_list: list[str] = []
        service_api_calling_code_list: list[str] = []
        for function_name, parameter_info in rpc_dict.items():
            input_variable: str = parameter_info["input_variable"]
            output_variable: str = parameter_info["output_variable"]

            if " " in input_variable:
                input_variable = re.split(r"\s+", input_variable)[1]
            if " " in output_variable:
                output_variable = re.split(r"\s+", output_variable)[1]

            service_class_function_list.append(f"""
    def {function_name}(self, headers: dict[str, str], item: {input_variable}) -> {output_variable}:
        default_response = {output_variable}()

        try:
            pass
        except Exception as e:
            print(f"Error: {{e}}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response
            """.rstrip().lstrip('\n'))

            service_api_calling_code_list.append(f"""
        elif (request_url == "{function_name}"):
            correct_item = {input_variable}().from_dict(item)
            return json.dumps((service_instance.{function_name}(headers, correct_item)).to_dict())
            """.rstrip().lstrip('\n'))

        
        service_class_function_list_text = "\n\n".join(service_class_function_list)
        service_api_calling_code_list_text = "\n\n".join(service_api_calling_code_list)

        template_text = f"""
from .{identity_name}_objects import *


from typing import Any
import json
from auto_everything.http_ import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request


class Service_{identity_name}:
{service_class_function_list_text}


def run(service_instance: Service_{identity_name}, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    def handle_get_url(sub_url: str, headers: dict[str, str]) -> str:
        return 'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

    def handle_post_url(sub_url: str, headers: dict[str, str], item: dict[str, Any]) -> dict | str:
        sub_url = sub_url.strip("/")
        sub_url = sub_url.replace("{identity_name}", "", 1)
        sub_url = sub_url.strip("/")
        request_url = sub_url.split("/")[0].strip()

        if (request_url == ""):
            return f"Request url '{{request_url}}' is empty"
{service_api_calling_code_list_text}

        return f"No API url matchs '{{request_url}}'"

    def general_handler(request: Yingshaoxo_Http_Request) -> dict | str:
        response = f"No handler for {{request.url}}"
        if request.method == "GET":
            response = handle_get_url(request.url, request.headers)
        elif request.method == "POST":
            response = handle_post_url(request.url, request.headers, json.loads(request.payload))
        return response

    router = {{
        r"(.*)": general_handler,
    }}

    yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router)
    yingshaoxo_http_server.start(host="0.0.0.0", port=int(port), html_folder_path=html_folder_path, serve_html_under_which_url=serve_html_under_which_url)


if __name__ == "__main__":
    service_instance = Service_{identity_name}()
    run(service_instance, port="6060")
        """.strip()

        return template_text


    def _convert_yrpc_code_into_pure_python_rpc_code(self, identity_name: str, source_code: str) -> str:
        _, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        service_class_function_list: list[str] = []
        service_api_calling_code_list: list[str] = []
        for function_name, parameter_info in rpc_dict.items():
            input_variable: str = parameter_info["input_variable"]
            output_variable: str = parameter_info["output_variable"]

            if " " in input_variable:
                input_variable = re.split(r"\s+", input_variable)[1]
            if " " in output_variable:
                output_variable = re.split(r"\s+", output_variable)[1]

            service_class_function_list.append(f"""
    def {function_name}(self, headers: dict[str, str], item: {input_variable}) -> {output_variable}:
        default_response = {output_variable}()

        try:
            pass
        except Exception as e:
            print(f"Error: {{e}}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response
            """.rstrip().lstrip('\n'))

            service_api_calling_code_list.append(f"""
        elif (request_url == "{function_name}"):
            correct_item = {input_variable}().from_dict(item)
            return json.dumps((service_instance.{function_name}(headers, correct_item)).to_dict())
            """.rstrip().lstrip('\n'))

        
        service_class_function_list_text = "\n\n".join(service_class_function_list)
        service_api_calling_code_list_text = "\n\n".join(service_api_calling_code_list)

        template_text = f"""
from .{identity_name}_objects import *


from typing import Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import os
from time import sleep


class Service_{identity_name}:
{service_class_function_list_text}


def _get_headers_dict_from_string(headers: str) -> dict:
    dic = {{}}
    for line in headers.split("\\n"):
        if line.startswith(("GET", "POST")):
            continue
        point_index = line.find(":")
        dic[line[:point_index].strip()] = line[point_index+1:].strip()
    return dic


def run(service_instance: Service_{identity_name}, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    # allow_origins=['*'],
    # allow_credentials=True,
    # allow_methods=["*"],
    # allow_headers=["*"],

    def handle_get_url(sub_url: str, headers: dict[str, str]) -> bytes:
        return b'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

    if (html_folder_path != ""):
        if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
            def handle_get_url(sub_url: str, headers: dict[str, str]) -> bytes:
                sub_url = sub_url.strip("/")
                sub_url = sub_url.lstrip(serve_html_under_which_url)
                if sub_url == '':
                    sub_url = 'index.html'
                real_file_path = f"{{os.path.join(html_folder_path, sub_url)}}"
                if os.path.exists(real_file_path) and os.path.isfile(real_file_path):
                    with open(real_file_path, mode="rb") as f:
                        the_data = f.read()
                else:
                    #return b"Resource not found\\n\\n(This web service is using YRPC (Yingshaoxo Remote Procedure Call))"
                    sub_url = 'index.html'
                    real_file_path = f"{{os.path.join(html_folder_path, sub_url)}}"
                    with open(real_file_path, mode="rb") as f:
                        the_data = f.read()
                return the_data

            print(f"The website is running at: http://127.0.0.1:{{port}}/")
        else:
            print(f"Error: You should give me an absolute html_folder_path than {{html_folder_path}}")

    def handle_post_url(sub_url: str, headers: dict[str, str], item: dict[str, Any]) -> str:
        sub_url = sub_url.strip("/")
        sub_url = sub_url.replace("{identity_name}", "", 1)
        sub_url = sub_url.strip("/")
        request_url = sub_url.split("/")[0].strip()

        if (request_url == ""):
            return f"Request url '{{request_url}}' is empty"
{service_api_calling_code_list_text}

        return f"No API url matchs '{{request_url}}'"

    class WebRequestHandler(BaseHTTPRequestHandler):
        def do_OPTIONS(self):
            self.send_response(200, "ok")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', '*')
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()

        def do_GET(self):
            sub_url = self.path
            headers = _get_headers_dict_from_string(self.headers.as_string())

            self.send_response(200)

            self.send_header("Access-Control-Allow-Origin", "*")

            if sub_url.endswith(".html"):
                self.send_header("Content-Type", "text/html")
            elif sub_url.endswith(".css"):
                self.send_header("Content-Type", "text/css")
            elif sub_url.endswith(".js"):
                self.send_header("Content-Type", "text/javascript")

            response = handle_get_url(sub_url, headers)

            self.end_headers()
            self.wfile.write(response)

        def do_POST(self):
            sub_url = self.path
            headers = _get_headers_dict_from_string(self.headers.as_string())

            content_length = headers.get('Content-Length')
            if content_length is None:
                self.wfile.write("What you send is not json".encode("utf-8"))
                return
            else:
                content_length = int(content_length)
            
            if content_length == 0:
                self.wfile.write("What you send is not json".encode("utf-8"))
                return

            request_json_dict = json.loads(self.rfile.read(content_length))

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = handle_post_url(sub_url, headers, request_json_dict)

            self.wfile.write(response.encode("utf-8"))

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        pass
    
    # Setting TCP Address
    server_address = ('0.0.0.0', int(port))
    
    # invoking server
    http = ThreadedHTTPServer(server_address, WebRequestHandler)
    
    http.serve_forever()


def run_with_hot_load(watch_path: str, service_instance: Service_{identity_name}, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    import multiprocessing
    from auto_everything.develop import Develop
    develop = Develop()

    the_running_process = multiprocessing.Process(target=run, args=(service_instance, port, html_folder_path, serve_html_under_which_url))
    the_running_process.start()

    while True:
        changed = develop.whether_a_folder_has_changed(folder_path=watch_path, type_limiter=[".py", ".html", ".css", ".js"])
        if (changed):
            print("Source code get changed, doing a reloading now...")
            the_running_process.kill()
            while the_running_process.is_alive():
                sleep(1)
            the_running_process = multiprocessing.Process(target=run, args=(service_instance, port, html_folder_path, serve_html_under_which_url))
            the_running_process.start()
        sleep(1)


if __name__ == "__main__":
    service_instance = Service_{identity_name}()
    run(service_instance, port="6060")
        """.strip()

        return template_text

    def _convert_yrpc_code_into_python_fastapi_rpc_code(self, identity_name: str, source_code: str) -> str:
        _, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        service_class_function_list: list[str] = []
        service_api_function_list: list[str] = []
        for function_name, parameter_info in rpc_dict.items():
            input_variable: str = parameter_info["input_variable"]
            output_variable: str = parameter_info["output_variable"]

            if " " in input_variable:
                input_variable = re.split(r"\s+", input_variable)[1]
            if " " in output_variable:
                output_variable = re.split(r"\s+", output_variable)[1]

            service_class_function_list.append(f"""
    async def {function_name}(self, headers: dict[str, str], item: {input_variable}) -> {output_variable}:
        default_response = {output_variable}()

        try:
            pass
        except Exception as e:
            print(f"Error: {{e}}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response
            """.rstrip().lstrip('\n'))

            service_api_function_list.append(f"""
    @router.post("/{function_name}/", tags=["{identity_name}"])
    async def {function_name}(request: Request, item: {input_variable}) -> {output_variable}:
        item = {input_variable}().from_dict(item.to_dict())
        headers = dict(request.headers.items())
        return (await service_instance.{function_name}(headers, item)).to_dict()
            """.rstrip().lstrip('\n'))


        service_class_function_list_text = "\n\n".join(service_class_function_list)
        service_api_function_list_text = "\n\n".join(service_api_function_list)

        template_text = f"""
from .{identity_name}_objects import *


from fastapi import APIRouter, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os


class Service_{identity_name}:
{service_class_function_list_text}


def init(service_instance: Any, router: Any):
{service_api_function_list_text}


def run(service_instance: Any, port: str, html_folder_path: str="", serve_html_under_which_url: str="/", only_return_app: bool = False):
    router = APIRouter()

    init(service_instance=service_instance, router=router)

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        router,
        prefix="/{identity_name}",
    )

    if (html_folder_path != ""):
        if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
            app.mount(serve_html_under_which_url, StaticFiles(directory=html_folder_path, html = True), name="web")
            @app.get(serve_html_under_which_url, response_model=str)
            async def index_page():
                return FileResponse(os.path.join(html_folder_path, 'index.html'))
            @app.exception_handler(404) #type: ignore
            async def custom_404_handler(_, __): #type: ignore
                return FileResponse(os.path.join(html_folder_path, 'index.html'))
            print(f"The website is running at: http://127.0.0.1:{{port}}/")
        else:
            print(f"Error: You should give me an absolute html_folder_path than {{html_folder_path}}")

    if only_return_app == True:
        return app

    print(f"You can see the docs here: http://127.0.0.1:{{port}}/docs")
    uvicorn.run( #type: ignore
        app=app,
        host="0.0.0.0",
        port=int(port)
    )


if __name__ == "__main__":
    service_instance = Service_{identity_name}()
    run(service_instance, port="6060")
        """.strip()

        return template_text

    def _convert_yrpc_code_into_pure_python_rpc_client_code(self, identity_name: str, source_code: str) -> str:
        _, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        client_function_list: list[str] = []
        for function_name, parameter_info in rpc_dict.items():
            input_variable: str = parameter_info["input_variable"]
            output_variable: str = parameter_info["output_variable"]

            if " " in input_variable:
                input_variable = re.split(r"\s+", input_variable)[1]
            if " " in output_variable:
                output_variable = re.split(r"\s+", output_variable)[1]

            client_function_list.append(f"""
    def {function_name}(self, item: {input_variable}, ignore_error: bool | None=None) -> {output_variable} | None:
        result = self._get_reponse_or_error_by_url_path_and_input("{function_name}", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return {output_variable}().from_dict(result)
            """.rstrip().lstrip('\n'))

        client_function_list_text = "\n\n".join(client_function_list)

        template_text = f"""
from .{identity_name}_objects import *

from typing import Any, Callable
import json
from urllib import request


def _send_a_post(url: str, data: dict, headers: dict | None=None) -> str:
    a_request = request.Request(url, method="POST")
    a_request.add_header('Content-Type', 'application/json')
    if headers != None:
        for key, value in headers.items():
            a_request.add_header(key, value)
    data = json.dumps(data, indent=4)
    data = data.encode("utf-8", errors="ignore")
    r_ = request.urlopen(a_request, data=data)
    content = r_.read().decode("utf-8", errors="ignore")
    return content


class Client_{identity_name}:
    def __init__(self, service_url: str, headers: dict[str, Any] | None = None, error_handle_function: Callable[[str], None] | None = None, special_error_key: str = "__yingshaoxo's_error__", interceptor_function: Callable[[dict], None] | None = None):
        if (service_url.endswith("/")):
            service_url = service_url[:-1]
        self._service_url = service_url 

        if headers == None:
            headers = {{}}
        self._header = headers

        def _default_error_handle_function(error_message: str):
            print(f"errors: {{error_message}}")
        if error_handle_function == None:
            error_handle_function = _default_error_handle_function
        self._error_handle_function = error_handle_function

        self._special_error_key = special_error_key

        def _default_interceptor_function(data: dict):
            pass
        if interceptor_function == None:
            interceptor_function = _default_interceptor_function
        self._interceptor_function = interceptor_function

    def _get_reponse_or_error_by_url_path_and_input(self, sub_url: str, input_dict: dict[str, Any]):
        the_url = f"{{self._service_url}}/{identity_name}/{{sub_url}}/"
        try:
            response = _send_a_post(url=the_url, data=input_dict, headers=self._header)
            json_response = json.loads(response)
            self._interceptor_function(json_response)
            return json_response
        except Exception as e: 
            return {{self._special_error_key: str(e)}}

{client_function_list_text}
        """.strip()

        return template_text

    def _convert_yrpc_code_into_dart_objects_code(self, source_code: str) -> str:
        arguments_dict, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        enum_code_block_list: list[str] = []
        dataclass_code_block_list: list[str] = []
        for class_name, variable_info in arguments_dict.items():
            code_block_type = variable_info["**type**"]
            del variable_info["**type**"]

            if code_block_type == "enum":
                variable_list: list[str] = []
                for index, one in enumerate(variable_info.values()):
                    name = one['name']
                    variable_list.append(f"""
  {name},
                    """.rstrip().lstrip('\n'))
                variable_list_text = "\n".join(variable_list)

                enum_class_text = f"""
enum {class_name} {{
    // yingshaoxo: I strongly recommend you use enum as a string type in other message data_model
{variable_list_text}
}}
                """.rstrip().lstrip('\n')

                enum_code_block_list.append(enum_class_text)
            else:
                variable_list: list[str] = []
                constructor_variable_list: list[str] = []
                property_name_to_its_type_dict_variable_list: list[str] = []
                key_string_dict_list: list[str] = []

                to_dict_function_variable_list: list[str] = []

                from_dict_function_variable_list_1: list[str] = []
                from_dict_function_variable_list_2: list[str] = []

                for index, one in enumerate(variable_info.values()):
                    name = one['name']
                    type = self._yrpc_type_to_dart_type_dict.get(one['type']) 
                    if type == None:
                        if one['type'] in arguments_dict.keys():
                            type = one['type']
                        else:
                            raise Exception(f"We don't support type of '{one['type']}', have you defined this type in your protocol code?")
                    is_list = one['is_list']
                    is_enum = one['is_enum']
                    is_custom_message_type = one['is_custom_message_type']

                    if is_list == False:
                        variable_list.append(f"""
  {type}? {name};
                        """.rstrip().lstrip('\n'))
                    else:
                        variable_list.append(f"""
  List<{type}>? {name};
                        """.rstrip().lstrip('\n'))
                    
                    constructor_variable_list.append(f"""
                    this.{name}
                    """.strip())

                    property_name_to_its_type_dict_variable_list.append(f"""
    "{name}": {type},
                    """.rstrip().lstrip('\n'))

                    key_string_dict_list.append(f"""
  final String {name} = "{name}";
                    """.rstrip().lstrip('\n'))

                    if is_enum:
                        if is_list:
                            to_dict_function_variable_list.append(f"""
      '{name}': this.{name}?.map((e) => e.name).toList(),
                            """.rstrip().lstrip('\n'))
                        else:
                            to_dict_function_variable_list.append(f"""
      '{name}': this.{name}?.name,
                            """.rstrip().lstrip('\n'))
                    elif is_custom_message_type:
                        if is_list:
                            to_dict_function_variable_list.append(f"""
      '{name}': this.{name}?.map((e) => e.to_dict()).toList(),
                            """.rstrip().lstrip('\n'))
                        else:
                            to_dict_function_variable_list.append(f"""
      '{name}': this.{name}?.to_dict(),
                            """.rstrip().lstrip('\n'))
                    else:
                        to_dict_function_variable_list.append(f"""
      '{name}': this.{name},
                        """.rstrip().lstrip('\n'))

                    if is_enum:
                        if is_list:
                            from_dict_function_variable_list_1.append(f"""
    this.{name} = json['{name}']?.map((e1) {{
      return {type}.values
                  .map((e2) => e2.name)
                  .toList()
                  .indexOf(e1) ==
              -1
          ? null
          : {type}.values.byName(e1);
    }})
    ?.toList()
    .cast<{type}>() ?? null
    ;
                            """.rstrip().lstrip('\n'))
                        else:
                            from_dict_function_variable_list_1.append(f"""
    this.{name} =
        {type}.values.map((e) => e.name).toList().indexOf(json['{name}']) == -1
            ? null
            : {type}.values.byName(json['{name}']);
                            """.rstrip().lstrip('\n'))
                    elif is_custom_message_type:
                        if is_list:
                            from_dict_function_variable_list_1.append(f"""
    this.{name} = json['{name}']
            ?.map((e) => {type}().from_dict(e))
            ?.toList()
            ?.cast<{type}>() ??
        null;
                            """.rstrip().lstrip('\n'))
                        else:
                            from_dict_function_variable_list_1.append(f"""
    this.{name} = {type}().from_dict(json['{name}']);
                            """.rstrip().lstrip('\n'))
                    else:
                        from_dict_function_variable_list_1.append(f"""
    this.{name} = json['{name}'];
                        """.rstrip().lstrip('\n'))

                    if is_enum:
                        if is_list:
                            from_dict_function_variable_list_2.append(f"""
      {name}: json['{name}']?.map((e1) {{
        return {type}.values
                    .map((e2) => e2.name)
                    .toList()
                    .indexOf(e1) ==
                -1
            ? null
            : {type}.values.byName(e1);
      }})
      ?.toList()
      .cast<{type}>() ?? null
      ,
                            """.rstrip().lstrip('\n'))
                        else:
                            from_dict_function_variable_list_2.append(f"""
      {name}:
        {type}.values.map((e) => e.name).toList().indexOf(json['{name}']) == -1
            ? null
            : {type}.values.byName(json['{name}']),
                            """.rstrip().lstrip('\n'))
                    elif is_custom_message_type:
                        if is_list:
                            from_dict_function_variable_list_2.append(f"""
      {name}: json['{name}']
              ?.map((e) => {type}().from_dict(e))
              ?.toList()
              ?.cast<{type}>() ??
          null,
                            """.rstrip().lstrip('\n'))
                        else:
                            from_dict_function_variable_list_2.append(f"""
      {name}: {type}().from_dict(json['{name}']),
                            """.rstrip().lstrip('\n'))
                    else:
                        from_dict_function_variable_list_2.append(f"""
      {name}: json['{name}'],
                        """.rstrip().lstrip('\n'))

                variable_list_text = "\n".join(variable_list)
                constructor_variable_list_text = ", ".join(constructor_variable_list) 
                if (len(constructor_variable_list_text) != 0):
                    constructor_variable_list_text = "{" + constructor_variable_list_text + "}"
                property_name_to_its_type_dict_variable_list_text = "\n".join(property_name_to_its_type_dict_variable_list)
                key_string_dict_list_text = "\n".join(key_string_dict_list)

                to_dict_function_variable_list_text = "\n".join(to_dict_function_variable_list)

                from_dict_function_variable_list_1_text = "\n".join(from_dict_function_variable_list_1)
                from_dict_function_variable_list_2_text = "\n".join(from_dict_function_variable_list_2)

                dataclass_text = f"""
class _Key_string_dict_for_{class_name} {{
{key_string_dict_list_text}
}}

class {class_name} {{
{variable_list_text}

  {class_name}({constructor_variable_list_text});

  final Map<String, dynamic> _property_name_to_its_type_dict = {{
{property_name_to_its_type_dict_variable_list_text}
  }};

  final _key_string_dict_for_{class_name} =
      _Key_string_dict_for_{class_name}();

  Map<String, dynamic> to_dict() {{
    return {{
{to_dict_function_variable_list_text}
    }};
  }}

  {class_name} from_dict(Map<String, dynamic>? json) {{
    if (json == null) {{
      return {class_name}();
    }}

{from_dict_function_variable_list_1_text}

    return {class_name}(
{from_dict_function_variable_list_2_text}
    );
  }}
}}
                """.rstrip().lstrip('\n')

                dataclass_code_block_list.append(dataclass_text)
        
        enum_code_block_list_text = "\n\n\n".join(enum_code_block_list)
        dataclass_code_block_list_text = "\n\n\n".join(dataclass_code_block_list)

        template_text = f"""
// ignore_for_file: unused_field

{enum_code_block_list_text}

{dataclass_code_block_list_text}
        """.strip()

        return template_text

    def _convert_yrpc_code_into_dart_rpc_code(self, identity_name: str, source_code: str) -> str:
        _, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        client_function_list: list[str] = []
        for function_name, parameter_info in rpc_dict.items():
            input_variable: str = parameter_info["input_variable"]
            output_variable: str = parameter_info["output_variable"]

            if " " in input_variable:
                input_variable = re.split(r"\s+", input_variable)[1]
            if " " in output_variable:
                output_variable = re.split(r"\s+", output_variable)[1]

            client_function_list.append(f"""
  Future<{output_variable}?> {function_name}(
      {{required {input_variable} item, bool ignore_error = false}}) async {{
    Map<String, dynamic> response_dict = await this
        ._get_reponse_or_error_by_url_path_and_input(
            "{function_name}", item.to_dict());
    if (response_dict.containsKey(this._special_error_key)) {{
      if (!ignore_error) {{
        this._error_handle_function!(response_dict[this._special_error_key]);
      }}
      return null;
    }} else {{
      return {output_variable}().from_dict(response_dict);
    }}
  }}
            """.rstrip().lstrip('\n'))

        client_function_list_text = "\n\n".join(client_function_list)

        template_text = f"""
import "./{identity_name}_objects.dart";

import 'dart:convert';
import 'dart:io';

class Client_{identity_name} {{
  /// [_service_url] is something like: "http://127.0.0.1:80" or "https://127.0.0.1"
  /// [_header] http headers, it's a dictionary, liek {'content-type', 'application/json'}
  /// [_error_handle_function] will get called when http request got error, you need to give it a function like: (err: String) {{print(err)}}
  String _service_url = "";
  Map<String, String> _header = Map<String, String>();
  final _special_error_key = "__yingshaoxo's_error__";
  Function(String error_message) _error_handle_function =
      (String error_message) {{}};
  Function() _function_before_request = () {{}};
  Function() _function_after_request = () {{}};

  Client_{identity_name}(
      {{required String service_url,
      Map<String, String>? header,
      Function(String error_message)? error_handle_function,
      Function()? function_before_request,
      Function()? function_after_request}}) {{
    if (service_url.endsWith("/")) {{
      service_url =
          service_url.splitMapJoin(RegExp(r'/$'), onMatch: (p0) => "");
    }}
    this._service_url = service_url;

    if (header != null) {{
      this._header = header;
    }}

    if (error_handle_function != null) {{
      this._error_handle_function = error_handle_function;
    }}

    if (function_before_request != null) {{
      this._function_before_request = function_before_request;
    }}

    if (function_after_request != null) {{
      this._function_after_request = function_after_request;
    }}
  }}

  Future<Map<String, dynamic>> _get_reponse_or_error_by_url_path_and_input(
      String sub_url, Map<String, dynamic> input_dict) async {{
    String the_url = "${{this._service_url}}/{identity_name}/${{sub_url}}/";

    var client = HttpClient();
    client.badCertificateCallback =
        ((X509Certificate cert, String host, int port) => true);
    try {{
      var the_url_data = Uri.parse(the_url);

      this._function_before_request();

      HttpClientRequest request = await client.postUrl(the_url_data);
      request.headers.set('content-type', 'application/json');
      _header.forEach((key, value) {{
        request.headers.set(key, value);
      }});

      request.add(utf8.encode(json.encode(input_dict)));

      HttpClientResponse response = await request.close();
      final stringData = await response.transform(utf8.decoder).join();
      final output_dict = json.decode(stringData);

      this._function_after_request();

      return output_dict;
    }} catch (e) {{
      final error_string = e.toString();
      this._error_handle_function(error_string);

      this._function_after_request();

      return {{_special_error_key: error_string}};
    }} finally {{
      client.close();
    }}
  }}

{client_function_list_text}
}}
        """.strip()

        return template_text

    def _convert_yrpc_code_into_typescript_objects_code(self, source_code: str) -> str:
        arguments_dict, _ = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        enum_code_block_list: list[str] = []
        dataclass_code_block_list: list[str] = []
        for class_name, variable_info in arguments_dict.items():
            code_block_type = variable_info["**type**"]
            del variable_info["**type**"]

            if code_block_type == "enum":
                variable_list: list[str] = []
                for index, one in enumerate(variable_info.values()):
                    name = one['name']
                    variable_list.append(f"""
    {name} = "{name}",
                    """.rstrip().lstrip('\n'))
                variable_list_text = "\n".join(variable_list)

                enum_class_text = f"""
export enum {class_name} {{
    // yingshaoxo: I strongly recommend you use enum as a string type in other message data_model
{variable_list_text}
}}
                """.rstrip().lstrip('\n')

                enum_code_block_list.append(enum_class_text)
            else:
                interface_variable_list: list[str] = []
                variable_list: list[str] = []
                property_name_to_its_type_dict_variable_list: list[str] = []
                key_string_dict_list: list[str] = []
                constructor_arguments_list: list[str] = []
                constructor_arguments_inside_code_block_list: list[str] = []

                for index, one in enumerate(variable_info.values()):
                    name = one['name']
                    type = self._yrpc_type_to_typescript_type_dict.get(one['type']) 
                    if type == None:
                        if one['type'] in arguments_dict.keys():
                            type = one['type']
                        else:
                            raise Exception(f"We don't support type of '{one['type']}', have you defined this type in your protocol code?")
                    is_list = one['is_list']
                    is_enum = one['is_enum']
                    is_custom_message_type = one['is_custom_message_type']

                    interface_variable_list.append(f"""
    {name}: {type}{"[]" if is_list else ""} | null;
                    """.rstrip().lstrip('\n'))

                    variable_list.append(f"""
    {name}: {type}{"[]" if is_list else ""} | null = null;
                    """.rstrip().lstrip('\n'))

                    if is_enum or is_custom_message_type:
                        property_name_to_its_type_dict_variable_list.append(f"""
            {name}: {type},
                        """.rstrip().lstrip('\n'))
                    else:
                        property_name_to_its_type_dict_variable_list.append(f"""
            {name}: "{type}",
                        """.rstrip().lstrip('\n'))

                    key_string_dict_list.append(f"""
        {name}: "{name}",
                    """.rstrip().lstrip('\n'))

                    constructor_arguments_list.append(f"""{name}: {type}{"[]" if is_list else ""} | null = null""".rstrip().lstrip('\n'))

                    constructor_arguments_inside_code_block_list.append(f"""
            this.{name} = {name}
                    """.rstrip().lstrip('\n'))

                interface_variable_list_text = "\n".join(interface_variable_list)
                variable_list_text = "\n".join(variable_list)
                property_name_to_its_type_dict_variable_list_text = "\n".join(property_name_to_its_type_dict_variable_list)
                key_string_dict_list_text = "\n".join(key_string_dict_list)
                constructor_arguments_list_text = ", ".join(constructor_arguments_list)
                constructor_arguments_inside_code_block_list_text = "\n".join(constructor_arguments_inside_code_block_list)

                dataclass_text = f"""
export interface _{class_name} {{
{interface_variable_list_text}
}}

export class {class_name} {{
{variable_list_text}

    _property_name_to_its_type_dict = {{
{property_name_to_its_type_dict_variable_list_text}
    }};

    _key_string_dict = {{
{key_string_dict_list_text}
    }};

    /*
    constructor({constructor_arguments_list_text}) {{
{constructor_arguments_inside_code_block_list_text}
    }}
    */

    to_dict(): _{class_name} {{
        return _general_to_dict_function(this);
    }}

    _clone(): {class_name} {{
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }}

    from_dict(item: _{class_name}): {class_name} {{
        let an_item = new {class_name}()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {{
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }}

        return an_item
    }}
}}
                """.rstrip().lstrip('\n')
                dataclass_code_block_list.append(dataclass_text)

        enum_code_block_list_text = "\n\n\n".join(enum_code_block_list)
        dataclass_code_block_list_text = "\n\n\n".join(dataclass_code_block_list)

        template_text = f"""
const _ygrpc_official_types = ["string", "number", "boolean"];

export const clone_object_ = (obj: any) =>  JSON.parse(JSON.stringify(obj));

export const get_secret_alphabet_dict_ = (a_secret_string: string) =>  {{
    const ascii_lowercase = "abcdefghijklmnopqrstuvwxyz".split("")
    const number_0_to_9 = "0123456789".split("")

    var new_key = a_secret_string.replace(" ", "").toLowerCase().split("")
    var character_list: string[] = []
    for (var char of new_key) {{
        if ((/[a-zA-Z]/).test(char)) {{
            if (!character_list.includes(char)) {{
                character_list.push(char)
            }}
        }}
    }}

    if (character_list.length >= 26) {{
        character_list = character_list.slice(0, 26)
    }} else {{
        var characters_that_the_key_didnt_cover: string[] = []
        for (var char of ascii_lowercase) {{
            if (!character_list.includes(char)) {{
                characters_that_the_key_didnt_cover.push(char)
            }}
        }}
        character_list = character_list.concat(characters_that_the_key_didnt_cover) 
    }}

    var final_dict = {{}} as Record<string, string>

    // for alphabet
    for (let [index, char] of ascii_lowercase.entries()) {{
        final_dict[char] = character_list[index]
    }}

    // for numbers
    var original_numbers_in_alphabet_format = ascii_lowercase.slice(0, 10) // 0-9 representations in alphabet format
    var secret_numbers_in_alphabet_format = Object.values(final_dict).slice(0, 10)
    var final_number_list = [] as string[]
    for (var index in number_0_to_9) {{
        var secret_char = secret_numbers_in_alphabet_format[index]
        if (original_numbers_in_alphabet_format.includes(secret_char)) {{
            final_number_list.push(String(original_numbers_in_alphabet_format.findIndex((x) => x===secret_char)))
        }}
    }}
    if (final_number_list.length >= 10) {{
        final_number_list = final_number_list.slice(0, 10)
    }} else {{
        var numbers_that_didnt_get_cover = [] as string[]
        for (var char of number_0_to_9) {{
            if (!final_number_list.includes(char)) {{
                numbers_that_didnt_get_cover.push(char)
            }}
        }}
        final_number_list = final_number_list.concat(numbers_that_didnt_get_cover)
    }}
    for (let [index, char] of final_number_list.entries()) {{
        final_dict[String(index)] = char
    }}

    return final_dict
}};

export const encode_message_ = (a_secret_dict: Record<string, string>, message: string):string => {{
    var new_message = ""
    for (const char of message) {{
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {{
            new_message += char
            continue
        }}
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {{
            new_char = new_char.toUpperCase()
        }}
        new_message += new_char
    }}
    return new_message
}}

export const decode_message_ = (a_secret_dict: Record<string, string>, message: string):string => {{
    var new_secret_dict = {{}} as Record<string, string>
    for (var key of Object.keys(a_secret_dict)) {{
        new_secret_dict[a_secret_dict[key]] = key
    }}
    a_secret_dict = new_secret_dict

    var new_message = ""
    for (const char of message) {{
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {{
            new_message += char
            continue
        }}
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {{
            new_char = new_char.toUpperCase()
        }}
        new_message += new_char
    }}
    return new_message
}}

const _general_to_dict_function = (object: any): any => {{
    let the_type = typeof object
    if (the_type == "object") {{
        if (object == null) {{
            return null
        }} else if (Array.isArray(object)) {{
            let new_list: any[] = []
            for (const one of object) {{
                new_list.push(_general_to_dict_function(one))
            }}
            return new_list
        }} else {{
            let keys = Object.keys(object);
            if (keys.includes("_key_string_dict")) {{
                // custom message type
                let new_dict: any = {{}}
                keys = keys.filter((e) => !["_property_name_to_its_type_dict", "_key_string_dict"].includes(e));
                for (const key of keys) {{
                    new_dict[key] = _general_to_dict_function(object[key])
                    // the enum will become a string in the end, so ignore it
                }}
                return new_dict
            }}
        }}
    }} else {{
        if (_ygrpc_official_types.includes(typeof object)) {{
            return object
        }} else {{
            return null
        }}
    }}
    return null
}};

const _general_from_dict_function = (old_object: any, new_object: any): any => {{
    let the_type = typeof new_object
    if (the_type == "object") {{
        if (Array.isArray(new_object)) {{
            //list
            let new_list: any[] = []
            for (const one of new_object) {{
                new_list.push(structuredClone(_general_from_dict_function(old_object, one)))
            }}
            return new_list
        }} else {{
            // dict or null
            if (new_object == null) {{
                return null
            }} else {{
                let keys = Object.keys(old_object);
                if (keys.includes("_key_string_dict")) {{
                    keys = Object.keys(old_object._property_name_to_its_type_dict)
                    for (const key of keys) {{
                        if (Object.keys(new_object).includes(key)) {{
                            if ((typeof old_object._property_name_to_its_type_dict[key]) == "string") {{
                                // default value type
                                old_object[key] = new_object[key]
                            }} else {{
                                // custom message type || enum
                                if (
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("class") || 
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("function")
                                ) {{
                                    // custom message type || a list of custom type
                                    var reference_object = new (old_object._property_name_to_its_type_dict[key])()
                                    old_object[key] = structuredClone(_general_from_dict_function(reference_object, new_object[key]))
                                }} else {{
                                    // enum
                                    if (Object.keys(new_object).includes(key)) {{
                                        old_object[key] = new_object[key]
                                    }} else {{
                                        old_object[key] = null
                                    }}
                                }}
                            }}
                        }} 
                    }}
                }} else {{
                    return null
                }}
            }}
        }}
    }} 
    return old_object
}}

{enum_code_block_list_text}

{dataclass_code_block_list_text}
        """.strip()

        return template_text

    def _convert_yrpc_code_into_typescript_rpc_code(self, identity_name: str, source_code: str) -> str:
        _, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        client_function_list: list[str] = []
        for function_name, parameter_info in rpc_dict.items():
            input_variable: str = parameter_info["input_variable"]
            output_variable: str = parameter_info["output_variable"]

            if " " in input_variable:
                input_variable = re.split(r"\s+", input_variable)[1]
            if " " in output_variable:
                output_variable = re.split(r"\s+", output_variable)[1]

            client_function_list.append(f"""
    async {function_name}(item: {identity_name}_objects.{input_variable}, ignore_error?: boolean): Promise<{identity_name}_objects.{output_variable} | null> {{
        let result = await this._get_reponse_or_error_by_url_path_and_input("{function_name}", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {{
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {{
                this._error_handle_function(result[this._special_error_key])
            }}
            return null
        }} else {{
            return new {identity_name}_objects.{output_variable}().from_dict(result)
        }}
    }}
            """.rstrip().lstrip('\n'))

        client_function_list_text = "\n\n".join(client_function_list)

        template_text = f"""
import * as {identity_name}_objects from './{identity_name}_objects'

export class Client_{identity_name} {{
  /**
   * @param {{string}} _service_url is something like: "http://127.0.0.1:80" or "https://127.0.0.1"
   * @param {{{{ [key: string]: string }}}} _header  http headers, it's a dictionary, liek {{'content-type', 'application/json'}}
   * @param {{Function}} _error_handle_function will get called when http request got error, you need to give it a function like: (err: String) {{print(err)}}
   * @param {{Function}} _interceptor_function will get called for every response, you need to give it a function like: (data: dict[Any, Any]) {{print(data)}}
   * @param {{Function}} _function_before_request will get called before every request, you need to give it a function like: () {{global_loading_animation = true}}
   * @param {{Function}} _function_after_request will get called after every request, you need to give it a function like: () {{global_loading_animation = false}}
   */
    _service_url: string
    _header: {{ [key: string]: string }} = {{}}
    _error_handle_function: (error: string) => void = (error: string) => {{console.log(error)}}
    _special_error_key: string = "__yingshaoxo's_error__"
    _interceptor_function: (data: any) => void = (data: any) => {{console.log(data)}}
    _function_before_request: () => void = () => {{}}
    _function_after_request: () => void = () => {{}}

    constructor(service_url: string, header?: {{ [key: string]: string }}, error_handle_function?: (error: string) => void, interceptor_function?: (data: any) => void, function_before_request?: () => void, function_after_request?: () => void) {{
        if (service_url.endsWith("/")) {{
            service_url = service_url.slice(0, service_url.length-1);
        }}
        try {{
            if (location.protocol === 'https:') {{
                if (service_url.startsWith("http:")) {{
                    service_url = service_url.replace("http:", "https:")
                }}
            }} else if (location.protocol === 'http:') {{
                if (service_url.startsWith("https:")) {{
                    service_url = service_url.replace("https:", "http:")
                }}
            }}
        }} catch (e) {{
        }}
        this._service_url = service_url
        
        if (header != null) {{
            this._header = header
        }}

        if (error_handle_function != null) {{
            this._error_handle_function = error_handle_function
        }}

        if (interceptor_function != null) {{
            this._interceptor_function = interceptor_function
        }}

        if (function_before_request != null) {{
            this._function_before_request = function_before_request
        }}

        if (function_after_request != null) {{
            this._function_after_request = function_after_request
        }}
    }} 

    async _get_reponse_or_error_by_url_path_and_input(sub_url: string, input_dict: {{ [key: string]: any }}): Promise<any> {{
        let the_url = `${{this._service_url}}/{identity_name}/${{sub_url}}/`
        try {{
            this._function_before_request()
            const response = await fetch(the_url, 
            {{
                method: "POST",
                body: JSON.stringify(input_dict),
                headers: {{
                    "Content-type": "application/json; charset=UTF-8",
                    ...this._header
                }}
            }});
            var json_response = await response.json()
            this._function_after_request()
            this._interceptor_function(json_response)
            return json_response
        }} catch (e) {{
            this._function_after_request()
            return {{[this._special_error_key]: String(e)}};
        }}
    }}

{client_function_list_text}
}}

export default Client_{identity_name}
        """.strip()

        return template_text

    def _convert_yrpc_code_into_javascript_objects_code(self, source_code):
        arguments_dict, _ = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        enum_code_block_list = []
        dataclass_code_block_list = []
        for class_name, variable_info in arguments_dict.items():
            code_block_type = variable_info["**type**"]
            del variable_info["**type**"]

            if code_block_type == "enum":
                variable_list = []
                for index, one in enumerate(variable_info.values()):
                    name = one['name']
                    variable_list.append(f"""
    {name}: "{name}",
                    """.rstrip().lstrip('\n'))
                variable_list_text = "\n".join(variable_list)

                enum_class_text = f"""
export const {class_name} = {{
{variable_list_text}
}}
                """.rstrip().lstrip('\n')

                enum_code_block_list.append(enum_class_text)
            else:
                interface_variable_list = []
                variable_list = []
                property_name_to_its_type_dict_variable_list = []
                key_string_dict_list = []
                constructor_arguments_list = []
                constructor_arguments_inside_code_block_list = []

                for index, one in enumerate(variable_info.values()):
                    name = one['name']
                    type = self._yrpc_type_to_typescript_type_dict.get(one['type'])
                    if type == None:
                        if one['type'] in arguments_dict.keys():
                            type = one['type']
                        else:
                            raise Exception(f"We don't support type of '{one['type']}', have you defined this type in your protocol code?")
                    is_list = one['is_list']
                    is_enum = one['is_enum']
                    is_custom_message_type = one['is_custom_message_type']

                    variable_list.append(f"""
    {name}: {type}{"[]" if is_list else ""} | null = null;
                    """.rstrip().lstrip('\n'))

                    if is_enum or is_custom_message_type:
                        property_name_to_its_type_dict_variable_list.append(f"""
                {name}: {type},
                        """.rstrip().lstrip('\n'))
                    else:
                        property_name_to_its_type_dict_variable_list.append(f"""
                {name}: "{type}",
                        """.rstrip().lstrip('\n'))

                    key_string_dict_list.append(f"""
                {name}: "{name}",
                    """.rstrip().lstrip('\n'))

                    constructor_arguments_list.append(f"""{name}""".rstrip().lstrip('\n'))

                    constructor_arguments_inside_code_block_list.append(f"""
        this.{name} = null;
                    """.rstrip().lstrip('\n'))

                variable_list_text = "\n".join(variable_list)
                property_name_to_its_type_dict_variable_list_text = "\n".join(property_name_to_its_type_dict_variable_list)
                key_string_dict_list_text = "\n".join(key_string_dict_list)
                constructor_arguments_list_text = ", ".join(constructor_arguments_list)
                constructor_arguments_inside_code_block_list_text = "\n".join(constructor_arguments_inside_code_block_list)

                dataclass_text = f"""
export class {class_name} {{
    /*
{variable_list_text}
    */

    constructor() {{
{constructor_arguments_inside_code_block_list_text}

        this._property_name_to_its_type_dict = {{
{property_name_to_its_type_dict_variable_list_text}
        }};

        this._key_string_dict = {{
{key_string_dict_list_text}
        }};

    }}

    to_dict() {{
        return _general_to_dict_function(this);
    }}

    _clone() {{
        var clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this);
        return clone;
    }}

    from_dict(item) {{
        var an_item = new {class_name}();
        var new_dict = _general_from_dict_function(an_item, item);

        for (const key of Object.keys(new_dict)) {{
            var value = new_dict[key];
            //@ts-ignore
            this[key] = value;
            //@ts-ignore
            an_item[key] = value;
        }}

        return an_item;
    }}
}}
                """.rstrip().lstrip('\n')
                dataclass_code_block_list.append(dataclass_text)

        enum_code_block_list_text = "\n\n\n".join(enum_code_block_list)
        dataclass_code_block_list_text = "\n\n\n".join(dataclass_code_block_list)

        template_text = f"""
const _ygrpc_official_types = ["string", "number", "boolean"];

export const clone_object_ = (obj) =>  JSON.parse(JSON.stringify(obj));

export const get_secret_alphabet_dict_ = (a_secret_string) =>  {{
    const ascii_lowercase = "abcdefghijklmnopqrstuvwxyz".split("")
    const number_0_to_9 = "0123456789".split("")

    var new_key = a_secret_string.replace(" ", "").toLowerCase().split("")
    var character_list = []
    for (var char of new_key) {{
        if ((/[a-zA-Z]/).test(char)) {{
            if (!character_list.includes(char)) {{
                character_list.push(char)
            }}
        }}
    }}

    if (character_list.length >= 26) {{
        character_list = character_list.slice(0, 26)
    }} else {{
        var characters_that_the_key_didnt_cover = []
        for (var char of ascii_lowercase) {{
            if (!character_list.includes(char)) {{
                characters_that_the_key_didnt_cover.push(char)
            }}
        }}
        character_list = character_list.concat(characters_that_the_key_didnt_cover)
    }}

    var final_dict = {{}}

    // for alphabet
    for (var [index, char] of ascii_lowercase.entries()) {{
        final_dict[char] = character_list[index]
    }}

    // for numbers
    var original_numbers_in_alphabet_format = ascii_lowercase.slice(0, 10) // 0-9 representations in alphabet format
    var secret_numbers_in_alphabet_format = Object.values(final_dict).slice(0, 10)
    var final_number_list = []
    for (var index in number_0_to_9) {{
        var secret_char = secret_numbers_in_alphabet_format[index]
        if (original_numbers_in_alphabet_format.includes(secret_char)) {{
            final_number_list.push(String(original_numbers_in_alphabet_format.findIndex((x) => x===secret_char)))
        }}
    }}
    if (final_number_list.length >= 10) {{
        final_number_list = final_number_list.slice(0, 10)
    }} else {{
        var numbers_that_didnt_get_cover = []
        for (var char of number_0_to_9) {{
            if (!final_number_list.includes(char)) {{
                numbers_that_didnt_get_cover.push(char)
            }}
        }}
        final_number_list = final_number_list.concat(numbers_that_didnt_get_cover)
    }}
    for (var [index, char] of final_number_list.entries()) {{
        final_dict[String(index)] = char
    }}

    return final_dict
}};

export const encode_message_ = (a_secret_dict, message) => {{
    var new_message = ""
    for (const char of message) {{
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {{
            new_message += char
            continue
        }}
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {{
            new_char = new_char.toUpperCase()
        }}
        new_message += new_char
    }}
    return new_message
}}

export const decode_message_ = (a_secret_dict, message) => {{
    var new_secret_dict = {{}}
    for (var key of Object.keys(a_secret_dict)) {{
        new_secret_dict[a_secret_dict[key]] = key
    }}
    a_secret_dict = new_secret_dict

    var new_message = ""
    for (const char of message) {{
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {{
            new_message += char
            continue
        }}
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {{
            new_char = new_char.toUpperCase()
        }}
        new_message += new_char
    }}
    return new_message
}}

const _general_to_dict_function = (object) => {{
    var the_type = typeof object
    if (the_type == "object") {{
        if (object == null) {{
            return null
        }} else if (Array.isArray(object)) {{
            var new_list = []
            for (const one of object) {{
                new_list.push(_general_to_dict_function(one))
            }}
            return new_list
        }} else {{
            var keys = Object.keys(object);
            if (keys.includes("_key_string_dict")) {{
                // custom message type
                var new_dict = {{}}
                keys = keys.filter((e) => !["_property_name_to_its_type_dict", "_key_string_dict"].includes(e));
                for (const key of keys) {{
                    new_dict[key] = _general_to_dict_function(object[key])
                    // the enum will become a string in the end, so ignore it
                }}
                return new_dict
            }}
        }}
    }} else {{
        if (_ygrpc_official_types.includes(typeof object)) {{
            return object
        }} else {{
            return null
        }}
    }}
    return null
}};

const _general_from_dict_function = (old_object, new_object) => {{
    var the_type = typeof new_object
    if (the_type == "object") {{
        if (Array.isArray(new_object)) {{
            //list
            var new_list = []
            for (const one of new_object) {{
                new_list.push(structuredClone(_general_from_dict_function(old_object, one)))
            }}
            return new_list
        }} else {{
            // dict or null
            if (new_object == null) {{
                return null
            }} else {{
                let keys = Object.keys(old_object);
                if (keys.includes("_key_string_dict")) {{
                    keys = Object.keys(old_object._property_name_to_its_type_dict)
                    for (const key of keys) {{
                        if (Object.keys(new_object).includes(key)) {{
                            if ((typeof old_object._property_name_to_its_type_dict[key]) == "string") {{
                                // default value type
                                old_object[key] = new_object[key]
                            }} else {{
                                // custom message type || enum
                                if (
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("class") ||
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("function")
                                ) {{
                                    // custom message type || a list of custom type
                                    var reference_object = new (old_object._property_name_to_its_type_dict[key])()
                                    old_object[key] = structuredClone(_general_from_dict_function(reference_object, new_object[key]))
                                }} else {{
                                    // enum
                                    if (Object.keys(new_object).includes(key)) {{
                                        old_object[key] = new_object[key]
                                    }} else {{
                                        old_object[key] = null
                                    }}
                                }}
                            }}
                        }}
                    }}
                }} else {{
                    return null
                }}
            }}
        }}
    }}
    return old_object
}}

{enum_code_block_list_text}

{dataclass_code_block_list_text}
        """.strip()

        return template_text

    def _convert_yrpc_code_into_javascript_rpc_code(self, identity_name: str, source_code: str) -> str:
        _, rpc_dict = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        client_function_list: list[str] = []
        for function_name, parameter_info in rpc_dict.items():
            input_variable: str = parameter_info["input_variable"]
            output_variable: str = parameter_info["output_variable"]

            if " " in input_variable:
                input_variable = re.split(r"\s+", input_variable)[1]
            if " " in output_variable:
                output_variable = re.split(r"\s+", output_variable)[1]

            client_function_list.append(f"""
    {function_name}({input_variable}, response_handle_function) {{
        this._get_reponse_or_error_by_url_path_and_input("{function_name}", {input_variable}.to_dict(), response_handle_function)
    }}
            """.rstrip().lstrip('\n'))

        client_function_list_text = "\n\n".join(client_function_list)

        template_text = f"""
import * as {identity_name}_objects from './{identity_name}_objects'

export class Client_{identity_name} {{
  /**
   * @param {{string}} _service_url is something like: "http://127.0.0.1:80" or "https://127.0.0.1"
   * @param {{{{ [key: string]: string }}}} _header  http headers, it's a dictionary, liek {{'content-type', 'application/json'}}
   * @param {{Function}} _error_handle_function will get called when http request got error, you need to give it a function like: (err: String) {{print(err)}}
   * @param {{Function}} _interceptor_function will get called for every response, you need to give it a function like: (data: dict[Any, Any]) {{print(data)}}
   * @param {{Function}} _function_before_request will get called before every request, you need to give it a function like: () {{global_loading_animation = true}}
   * @param {{Function}} _function_after_request will get called after every request, you need to give it a function like: () {{global_loading_animation = false}}
   */

    /*
    service_url: string
    header: {{ [key: string]: string }} = {{}}
    error_handle_function: (error: string) => void = (error: string) => {{console.log(error)}}
    special_error_key: string = "__yingshaoxo's_error__"
    interceptor_function: (data: any) => void = (data: any) => {{console.log(data)}}
    function_before_request: () => void = () => {{}}
    function_after_request: () => void = () => {{}}
    */

    constructor(service_url, header={{}}, error_handle_function=(error) => {{console.log(error)}}, interceptor_function=(data) => {{console.log(data)}}, function_before_request=() => {{}}, function_after_request=() => {{}}) {{
        this._special_error_key = "__yingshaoxo's_error__"

        if (service_url.endsWith("/")) {{
            service_url = service_url.slice(0, service_url.length-1);
        }}
        try {{
            if (location.protocol === 'https:') {{
                if (service_url.startsWith("http:")) {{
                    service_url = service_url.replace("http:", "https:")
                }}
            }} else if (location.protocol === 'http:') {{
                if (service_url.startsWith("https:")) {{
                    service_url = service_url.replace("https:", "http:")
                }}
            }}
        }} catch (e) {{
        }}
        this._service_url = service_url

        if (header != null) {{
            this._header = header
        }}

        if (error_handle_function) {{
            this._error_handle_function = error_handle_function
        }}

        if (interceptor_function) {{
            this._interceptor_function = interceptor_function
        }}

        if (function_before_request) {{
            this._function_before_request = function_before_request
        }}

        if (function_after_request) {{
            this._function_after_request = function_after_request
        }}
    }}

    _get_reponse_or_error_by_url_path_and_input(sub_url, input_dict, handle_response_function) {{
        var the_url = `${{this._service_url}}/{identity_name}/${{sub_url}}/`
        var use_xml_http = false
        if (typeof fetch !== 'undefined') {{
            use_xml_http = false
        }} else {{
            // use less xml_request, it will not give you right error message
            use_xml_http = true
        }}

        var input_json_data = JSON.stringify(input_dict)

        var header = {{'Content-Type': 'application/json; charset=UTF-8'}}
        for (var key in this._header) {{
            var value = this._header[key]
            header[key] = value
        }}

        var special_error_key = this._special_error_key
        var before_function = this._function_before_request
        var after_function = this._function_after_request
        var interceptor_function = this._interceptor_function
        var error_handle_function = this._error_handle_function

        try {{
            if (use_xml_http == false) {{
                // use fetch
                before_function()
                fetch(the_url,
                {{
                    method: "POST",
                    body: input_json_data,
                    headers: header
                }})
                .then((response) => {{
                    response.json().then(
                        (data) => {{
                            interceptor_function(data)
                            handle_response_function(data)
                            after_function()
                        }}
                    ).
                    catch((e) => {{
                        var fake_data = {{[special_error_key]: String(e)}}
                        after_function()
                        error_handle_function(fake_data[special_error_key])
                    }})
                }})
                .catch((e) => {{
                    var fake_data = {{[special_error_key]: String(e)}}
                    after_function()
                    error_handle_function(fake_data[special_error_key])
                }})
            }} else {{
                // use XMLHttpRequest
                before_function()
                var xhr = new XMLHttpRequest();

                xhr.open('POST', the_url, true);
                for (var key in header) {{
                    var value = header[key]
                    xhr.setRequestHeader(key, value);
                }}

                xhr.onreadystatechange = function () {{
                    if (xhr.readyState === XMLHttpRequest.DONE) {{
                        if (xhr.status === 200) {{
                            try {{
                                var data = JSON.parse(xhr.responseText)
                                interceptor_function(data)
                                handle_response_function(data)
                            }}
                            catch (e) {{
                                var fake_data = {{[special_error_key]: "Json parse error" + ": " + String(xhr.statusText)}}
                                error_handle_function(fake_data[special_error_key])
                            }}
                        }} else {{
                            var fake_data = {{[special_error_key]: String(xhr.status)}}
                            error_handle_function(fake_data[special_error_key])
                        }}
                        after_function()
                    }}
                }};

                xhr.onerror = function() {{
                    var fake_data = {{[special_error_key]: String(xhr.status) + ": " + String(xhr.statusText)}}
                    error_handle_function(fake_data[special_error_key])
                    after_function()
                }}

                xhr.send(input_json_data);
            }}
        }} catch (e) {{
            var fake_data = {{[special_error_key]: String(e)}}
            error_handle_function(fake_data[special_error_key])
            after_function()
        }}
    }}

{client_function_list_text}
}}

export default Client_{identity_name}
        """.strip()

        return template_text

    def _convert_yrpc_code_into_golang_objects_code(self, identity_name: str, source_code: str) -> str:
        arguments_dict, _ = self.get_information_from_yrpc_protocol_code(source_code=source_code)

        # enum_code_block_list: list[str] = []
        dataclass_code_block_list: list[str] = []
        for class_name, variable_info in arguments_dict.items():
            capitalized_class_name = self._capitalize_the_first_char_of_a_string(class_name)
            code_block_type = variable_info["**type**"]
            del variable_info["**type**"]

            if code_block_type == "enum":
#                 variable_list: list[str] = []
#                 for index, one in enumerate(variable_info.values()):
#                     name = one['name']
#                     variable_list.append(f"""
#     {name} = "{name}",
#                     """.rstrip().lstrip('\n'))
#                 variable_list_text = "\n".join(variable_list)

#                 enum_class_text = f"""
# enum {class_name} {{
# {variable_list_text}
# }}
#                 """.rstrip().lstrip('\n')

#                 enum_code_block_list.append(enum_class_text)
                print(f"Sorry, because of the stupid syntax of golang, we do not support enum type here: {class_name}")
                exit()
            else:
                variable_list: list[str] = []
                key_to_key_string_dict_variable_list_1: list[str] = []
                key_to_key_string_dict_variable_list_2: list[str] = []
                property_name_to_its_type_dict_variable_list: list[str] = []

                for index, one in enumerate(variable_info.values()):
                    name: str = one['name']
                    capitalized_name = self._capitalize_the_first_char_of_a_string(name)
                    type = self._yrpc_type_to_golang_type_dict.get(one['type']) 
                    if type == None:
                        if one['type'] in arguments_dict.keys():
                            type = one['type']
                        else:
                            raise Exception(f"We don't support type of '{one['type']}', have you defined this type in your protocol code?")
                    is_list = one['is_list']
                    is_enum = one['is_enum']
                    is_custom_message_type = one['is_custom_message_type']

                    if is_list:
                        nullable_type = f"variable_tool.Type_Nullable[[]variable_tool.Type_Nullable[{type}]]"
                    else:
                        nullable_type = f"variable_tool.Type_Nullable[{type}]"

                    variable_list.append(f"""
    {capitalized_name}    {nullable_type}
                    """.rstrip().lstrip('\n'))

                    key_to_key_string_dict_variable_list_1.append(f"""
    {capitalized_name}    string
                    """.rstrip().lstrip('\n'))

                    key_to_key_string_dict_variable_list_2.append(f"""
    {capitalized_name}:    "{name}",
                    """.rstrip().lstrip('\n'))

                    property_name_to_its_type_dict_variable_list.append(f"""
        "{name}":    "{type}",
                    """.rstrip().lstrip('\n'))

                variable_list_text = "\n".join(variable_list)
                key_to_key_string_dict_variable_list_1_text = "\n".join(key_to_key_string_dict_variable_list_1)
                key_to_key_string_dict_variable_list_2_text = "\n".join(key_to_key_string_dict_variable_list_2)
                property_name_to_its_type_dict_variable_list_text = "\n".join(property_name_to_its_type_dict_variable_list)

                dataclass_text = f"""
type {capitalized_class_name} struct {{
{variable_list_text}
}}

var Key_to_key_string_dict_for_{capitalized_class_name}_ = struct {{
{key_to_key_string_dict_variable_list_1_text}
}}{{
{key_to_key_string_dict_variable_list_2_text}
}}

func Get_key_to_value_type_dict_for_{capitalized_class_name}_() map[string]any {{
	return map[string]any{{
{property_name_to_its_type_dict_variable_list_text}
	}}
}}

func (self {capitalized_class_name}) To_dict() map[string]any {{
	return variable_tool.Convert_nullable_struct_into_dict(self, true).(map[string]any)
}}

func (self {capitalized_class_name}) From_dict(a_dict map[string]any) {capitalized_class_name} {{
	variable_tool.Convert_dict_into_nullable_struct(a_dict, &self)
	return self
}}
                """.rstrip().lstrip('\n')
                dataclass_code_block_list.append(dataclass_text)

        # enum_code_block_list_text = "\n\n\n".join(enum_code_block_list)
        dataclass_code_block_list_text = "\n\n\n\n".join(dataclass_code_block_list)

        template_text = f"""
package {identity_name}

import (
	"github.com/yingshaoxo/gopython/variable_tool"
)



{dataclass_code_block_list_text}
        """.strip()

        return template_text

    def _convert_yrpc_code_into_golang_rpc_code(self, identity_name: str, source_code: str) -> str:
        return f"""
package {identity_name}
        """.strip()

    def generate_code(self, which_language: str, input_folder: str, input_files: list[str], output_folder: str = "src/generated_yrpc"):
        """
        which_language: python, dart, typescript, go, kotlin, rust and so on

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

        language_to_file_suffix_dict = {
            "python": ".py",
            "dart": ".dart",
            "typescript": ".ts",
            "javascript": ".js",
            "golang": ".go"
        }

        if which_language not in language_to_file_suffix_dict.keys():
            raise Exception(f"Sorry, we don't support '{which_language}' language. You can @yingshaoxo in social media or send him an email for support.")
        
        if which_language == "python":
            init_file_for_python = disk.join_paths(output_folder, "__init__.py")
            if not disk.exists(init_file_for_python):
                io_.write(init_file_for_python, "")

        for file in files:
            filename,_ = disk.get_stem_and_suffix_of_a_file(file)
            identity_name = filename
            if " " in identity_name:
                print(f"Sorry, protocol filename shoudn't have space inside: '{identity_name}'")
                exit()

            source_code = io_.read(file_path=file)

            objects_code = ""
            rpc_code = ""
            if which_language in ["python", "dart", "typescript", "javascript"]:
                target_objects_file_path = disk.join_paths(output_folder, filename + "_objects" + language_to_file_suffix_dict[which_language])
                target_rpc_file_path = disk.join_paths(output_folder, filename + "_rpc" + language_to_file_suffix_dict[which_language])

                if which_language == "python":
                    objects_code = self._convert_yrpc_code_into_python_objects_code(source_code=source_code)
                    rpc_code = self._convert_yrpc_code_into_python_fastapi_rpc_code(identity_name=identity_name, source_code=source_code)

                    # additonal files for python
                    # pure python rpc server code, single process version
                    pure_python_rpc_code = self._convert_yrpc_code_into_pure_python_rpc_code(identity_name=identity_name, source_code=source_code)
                    target_pure_python_rpc_file_path = disk.join_paths(output_folder, filename + "_pure_python_rpc" + language_to_file_suffix_dict[which_language])
                    io_.write(file_path=target_pure_python_rpc_file_path, content=pure_python_rpc_code)

                    # pure python rpc server code, multiprocess version, could handle a lot of users at the same time
                    auto_everything_based_pure_python_rpc_code = self._convert_yrpc_code_into_auto_everything_based_python_rpc_code(identity_name=identity_name, source_code=source_code)
                    target_auto_everything_based_pure_python_rpc_file_path = disk.join_paths(output_folder, filename + "_auto_everything_based_pure_python_rpc" + language_to_file_suffix_dict[which_language])
                    io_.write(file_path=target_auto_everything_based_pure_python_rpc_file_path, content=auto_everything_based_pure_python_rpc_code)

                    # pure python rpc client
                    pure_python_rpc_client_code = self._convert_yrpc_code_into_pure_python_rpc_client_code(identity_name=identity_name, source_code=source_code)
                    target_pure_python_rpc_client_file_path = disk.join_paths(output_folder, filename + "_pure_python_rpc_client" + language_to_file_suffix_dict[which_language])
                    io_.write(file_path=target_pure_python_rpc_client_file_path, content=pure_python_rpc_client_code)
                elif which_language == "dart":
                    objects_code = self._convert_yrpc_code_into_dart_objects_code(source_code=source_code)
                    rpc_code = self._convert_yrpc_code_into_dart_rpc_code(identity_name=identity_name, source_code=source_code)
                elif which_language == "typescript":
                    objects_code = self._convert_yrpc_code_into_typescript_objects_code(source_code=source_code)
                    rpc_code = self._convert_yrpc_code_into_typescript_rpc_code(identity_name=identity_name, source_code=source_code)
                elif which_language == "javascript":
                    objects_code = self._convert_yrpc_code_into_javascript_objects_code(source_code=source_code)
                    rpc_code = self._convert_yrpc_code_into_javascript_rpc_code(identity_name=identity_name, source_code=source_code)
                io_.write(file_path=target_objects_file_path, content=objects_code)
                io_.write(file_path=target_rpc_file_path, content=rpc_code)
            elif which_language in ["golang"]:
                target_basic_folder = disk.join_paths(output_folder, identity_name)
                disk.create_a_folder(target_basic_folder)
                target_objects_file_path_for_package_based_language = disk.join_paths(target_basic_folder, filename + "_objects" + language_to_file_suffix_dict[which_language])
                target_rpc_file_path_for_package_based_language = disk.join_paths(target_basic_folder, filename + "_rpc" + language_to_file_suffix_dict[which_language])

                if which_language == "golang":
                    objects_code = self._convert_yrpc_code_into_golang_objects_code(identity_name=identity_name, source_code=source_code)
                    rpc_code = self._convert_yrpc_code_into_golang_rpc_code(identity_name=filename, source_code=source_code)
                io_.write(file_path=target_objects_file_path_for_package_based_language, content=objects_code)
                io_.write(file_path=target_rpc_file_path_for_package_based_language, content=rpc_code)


class Develop():
    def __init__(self):
        self.file_modification_dict: dict[str, Any] = {}
        self.folder_modification_dict: dict[str, dict[str, Any]] = {}

    def whether_a_file_has_changed(self, file_path: str):
        last_modification_time = os.path.getmtime(file_path)

        def update_dict():
            self.file_modification_dict.update({
                file_path: last_modification_time
            })

        if file_path in self.file_modification_dict:
            if last_modification_time != self.file_modification_dict[file_path]:
                update_dict()
                return True
            else:
                return False
        else:
            update_dict()
            return False

    def whether_a_folder_has_changed(self, folder_path: str, type_limiter: list[str] = [".py"]):
        if self.folder_modification_dict.get(folder_path) == None:
            self.folder_modification_dict[folder_path] = {}

        files = disk.get_files(folder=folder_path, type_limiter=type_limiter, gitignore_text=".venv/\n\n.node_modules/")
        for file in files:
            changed = False

            last_modification_time = os.path.getmtime(file)

            def update_dict():
                self.folder_modification_dict[folder_path].update({
                    file: last_modification_time
                })

            if file in self.folder_modification_dict[folder_path]:
                if last_modification_time != self.folder_modification_dict[folder_path][file]:
                    update_dict()
                    changed = True
                else:
                    changed = False
            else:
                update_dict()
                changed = False
            
            if changed == True:
                return True
        
        return False


if __name__ == "__main__":
    yrpc = YRPC()

    # result1, result2 = yrpc.get_information_from_yrpc_protocol_code(io_.read("/Users/yingshaoxo/CS/auto_everything/playground/develop/test_protobuff_code.proto"))
    # pprint(result1)

    output_folder = "/home/yingshaoxo/CS/auto_everything/playground/develop/build"

    disk.delete_a_folder(output_folder)

    for language in ["python", "dart", "typescript", "golang"]:
        yrpc.generate_code(
            which_language=language,
            input_folder="/home/yingshaoxo/CS/auto_everything/playground/develop",
            input_files=["simple_protobuff_code.proto"],
            output_folder=output_folder
        )
