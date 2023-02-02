import re

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

    def generate_python_code(self, input_folder: str, output_folder: str = "generated_grpc"):
        if not disk.exists(input_folder):
            raise Exception(f"'{input_folder}' does not exist!")

        if "Error" in t.run_command("python3 -m grpc_tools.protoc --help"):
            raise Exception(
                "You should install grpc_tools by using:\n\npython3 -m pip install grpcio grpcio-tools"
            )

        input_folder = input_folder.rstrip("/")

        t.run(f"""
        pip install --yes "betterproto[compiler]==2.0.0b5"
        """)

        t.run(
            f"""
        mkdir {output_folder}
        python3 -m grpc_tools.protoc --proto_path '{input_folder}' --python_betterproto_out='{output_folder}' '{input_folder}/*'
        """
        #--experimental_allow_proto3_optional
        )

    def generate_golang_code(self, input_folder: str, output_folder: str = "generated_grpc"):
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

        t.run(
            f"""
        mkdir {output_folder}
        protoc --proto_path '{input_folder}' --go_out='{output_folder}' --go-grpc_out='{output_folder}' '{input_folder}/*'
        """
        )

    def generate_dart_code(self, input_folder: str, output_folder: str = "lib/generated_grpc"):
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

        # protoc --dart_out=grpc:lib/src/generated -Iprotos protos/helloworld.proto
        if network.available():
            t.run(
                f"""
            mkdir {output_folder}
            dart pub global activate protoc_plugin
            export PATH="$PATH":"$HOME/.pub-cache/bin"
            protoc --proto_path '{input_folder}' --dart_out=grpc:{output_folder} '{input_folder}/*'
            """
            )
        else:
            t.run(
                f"""
            mkdir {output_folder}
            export PATH="$PATH":"$HOME/.pub-cache/bin"
            protoc --proto_path '{input_folder}' --dart_out=grpc:{output_folder} '{input_folder}/*'
            """
            )
    
    def _get_data_from_proto_file(self, proto_file_path: str):
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
        
        return data
    
    def generate_key_string_map_from_protocols(self, for_which_language:str , input_folder: str, output_folder: str|None = "grpc_key_string_maps"):
        #your name
        """
        for_which_language: 'rust', 'python', 'kotlin'...
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

        if for_which_language == "rust":
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

                io_.write(target_file_path, kotlin_code)
        else:
            raise Exception(f"We don't support '{for_which_language}' language.")

if __name__ == "__main__":
    grpc = GRPC()
    grpc.generate_python_code(
        input_folder="/tmp/hi/protos/", output_folder="/tmp/hi/py_grpc"
    )
    grpc.generate_golang_code(
        input_folder="/tmp/hi/protos/", output_folder="/tmp/hi/go_grpc"
    )
    grpc.generate_dart_code(
        input_folder="/tmp/hi/protos/", output_folder="/tmp/hi/dart_grpc"
    )
