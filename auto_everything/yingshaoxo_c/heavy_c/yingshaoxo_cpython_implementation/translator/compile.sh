# sudo apt install musl-tools

c_compiler=$(which musl-gcc)
#c_compiler=$(which gcc)

mkdir -p dist/
rm -fr dist/*

$c_compiler -g0 -s -std=c99 -static -D_POSIX_SOURCE -no-pie -o dist/y_python.run y_python.c

echo "./dist/y_python"


echo -e "\n\n\n"
echo "The following is the output of test.py:"
./dist/y_python.run test.py
