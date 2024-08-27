from auto_everything.io import File_IO
import os

file_io = File_IO(os.path.expanduser("~/Downloads/io_test.txt"))
print(file_io.get_size(), "b")

file_io.seek_from_end(0)
file_io.write(b"line 1\n")
file_io.write(b"line 2\n")

file_io.seek_from_end(-7)
print(file_io.read(6))

file_io.seek_from_end(0)
file_io.write(b"line 3\n")

file_io.seek_from_end(-7)
print(file_io.read(6))

file_io.close()

"""
# micropython version

file_io = File_IO("./io_test.txt")
print(file_io.get_size(), "b")

file_io.seek(0)
file_io.write(b"line 1\n")
file_io.write(b"line 2\n")

file_io.seek(7)
print(file_io.read(6))

file_io.seek(0)
print(file_io.read(6))

file_io.close()
"""
