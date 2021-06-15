from auto_everything.terminal import Terminal
from auto_everything.io import IO
import os

t = Terminal(debug=True)
io_ = IO()

class GRPC():
    def __init__(self):
        pass

    def generate_python_code(self, input_folder, output_folder="py_protos"):
        if "Error" in t.run_command("python3 -m grpc_tools.protoc --help"):
            raise Exception("You should install grpc_tools by using:\n\npip install grpcio-tools")

        #input_folder = os.path.abspath(input_folder)
        #output_folder = os.path.abspath(output_folder)

        #python3 -m grpc_tools.protoc -I protos/  --python_out=py_protos --grpc_python_out=py_protos hi.proto
        t.run(f"""
        mkdir {output_folder}
        python3 -m grpc_tools.protoc --proto_path {input_folder}  --python_out={output_folder} --grpc_python_out={output_folder} {input_folder}/*
        """)

        init_file = f"{output_folder}/__init__.py"
        t.run(f"""
        rm {init_file}
        echo 
        """)
        io_.write(init_file, """
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
        """)

if __name__ == "__main__":
    grpc = GRPC()
    grpc.generate_python_code(input_folder="/tmp/hi/protos/",output_folder="/tmp/hi/my_grpc")
