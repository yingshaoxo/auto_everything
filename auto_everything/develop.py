from auto_everything.terminal import Terminal
from auto_everything.io import IO
from auto_everything.disk import Disk
from auto_everything.network import Network
import os

t = Terminal(debug=True)
disk = Disk()
io_ = IO()
network = Network()


class GRPC:
    def __init__(self):
        pass

    def generate_python_code(self, input_folder: str, output_folder: str = "py_api"):
        if not disk.exists(input_folder):
            raise Exception(f"'{input_folder}' does not exist!")

        if "Error" in t.run_command("python3 -m grpc_tools.protoc --help"):
            raise Exception(
                "You should install grpc_tools by using:\n\npip install grpcio-tools"
            )

        input_folder = input_folder.rstrip("/")

        # python3 -m grpc_tools.protoc -I protos/  --python_out=py_protos --grpc_python_out=py_protos hi.proto
        t.run(
            f"""
        mkdir {output_folder}
        python3 -m grpc_tools.protoc --proto_path {input_folder}  --python_out={output_folder} --grpc_python_out={output_folder} {input_folder}/* --experimental_allow_proto3_optional
        """
        )

        init_file = f"{output_folder}/__init__.py"
        t.run(
            f"""
        rm {init_file}
        echo 
        """
        )
        io_.write(
            init_file,
            """
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
        """,
        )

    def generate_golang_code(self, input_folder: str, output_folder: str = "go_api"):
        if not disk.exists(input_folder):
            raise Exception(f"'{input_folder}' does not exist!")

        if "not found" in t.run_command("protoc --version"):
            raise Exception(
                "You should install protobuf-compiler by using:\n\nsudo apt install -y protobuf-compiler"
            )

        input_folder = input_folder.rstrip("/")

        t.run(
            f"""
        mkdir {output_folder}
        protoc --proto_path {input_folder} --go_out={output_folder} --go_opt=paths=source_relative --go-grpc_out={output_folder} --go-grpc_opt=paths=source_relative {input_folder}/* --experimental_allow_proto3_optional
        """
        )

    def generate_dart_code(self, input_folder: str, output_folder: str = "dart_api"):
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
            protoc --proto_path {input_folder} --dart_out=grpc:{output_folder} {input_folder}/* --experimental_allow_proto3_optional
            """
            )
        else:
            t.run(
                f"""
            mkdir {output_folder}
            export PATH="$PATH":"$HOME/.pub-cache/bin"
            protoc --proto_path {input_folder} --dart_out=grpc:{output_folder} {input_folder}/* --experimental_allow_proto3_optional
            """
            )


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
