sudo gcc myx11.cpp -g -Og -lstdc++ -lX11 -lXmu -o go.so
#&& ./go.so
valgrind --leak-check=full --show-leak-kinds=all ./go.so
