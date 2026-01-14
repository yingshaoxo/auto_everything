# sudo apt install musl-tools

c_compiler=$(which musl-gcc)

mkdir -p dist/
rm -fr dist/*

$c_compiler -g0 -s -std=c99 -static -D_POSIX_SOURCE -no-pie -o dist/test.run _test.c
#$c_compiler -std=c99 -static -o dist/test.run _test.c

echo "./dist/test.run"
./dist/test.run
