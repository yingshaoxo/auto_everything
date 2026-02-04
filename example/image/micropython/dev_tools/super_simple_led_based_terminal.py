from auto_everything import IO
io_ = IO()

while True:
    input_data = input(">")
    bytes_data = input_data.encode("ascii")
    print(bytes_data)

    int_data = io_.bytes_list_to_int_list(bytes_data)
    print(int_data)

    binary_0_and_1_data = io_.bytes_to_binary_zero_and_one(bytes_data)
    print(binary_0_and_1_data)

    print()
    final_led_text = ""
    for i in range(8):
        for one in binary_0_and_1_data:
            final_led_text += one[i] + " "
        final_led_text += "\n"
    print(final_led_text)
    print()
