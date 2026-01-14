# sudo apt install musl-tools

c_compiler=$(which musl-gcc)
#c_compiler=$(which gcc)

mkdir -p dist/
rm -fr dist/*

$c_compiler -g0 -s -std=c89 -static -D_POSIX_SOURCE -no-pie -o dist/yingshaoxo_dynamic_c.run main.c

echo "./dist/yingshaoxo_dynamic_c.run"


echo -e "\n\n\n"
#echo "The following is the output of test.py:"
#./dist/y_python.run test.py
./dist/yingshaoxo_dynamic_c.run
