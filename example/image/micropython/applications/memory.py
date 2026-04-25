#terminal_arguments, input_=input, print_=print

from gc import mem_free
print_("current memory: " + str(mem_free()/1024) + "kb.")
