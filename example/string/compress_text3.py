# just a demo

string_1 = "Have you eat today?"
string_2 = "Have you sleep today?"

compressing_dict = {
    "Have you": "1",
    "eat": "2",
    "sleep": "3",
    "today": "4",
    "?": "5",
    " ": "0",
}
uncompressing_dict = {}
for key,value in compressing_dict.items():
    uncompressing_dict[value] = key

compressed_string_1 = "1_2_4_5"
compressed_string_2 = "1_2_3_5"

# question? how do you handle number and _ in raw string?
def encode_unknown_string(a_stange_string):
    # a_stange_string can be '!@#$^@%^&**&^()\n'
    return "h" + a_stange_string.encode("utf-8").hex()

def decode_unknown_string(h_start_hex_string):
    hex_string = h_start_hex_string[1:]
    return (bytes.fromhex(hex_string)).decode("utf-8")

def compressing_method(input_string):
    output_list = []
    while len(input_string) > 0:
        found = False
        for key, value in compressing_dict.items():
            if input_string.startswith(key):
                output_list.append(value)
                input_string = input_string[len(key):]
                found = True
                break
        if found == False:
            unknown_char = input_string[0]
            input_string = input_string[1:]
            output_list.append(encode_unknown_string(unknown_char))
    output_string = ""
    index = 0
    while index < len(output_list):
        a_string = output_list[index]
        if not a_string.startswith("h"):
            output_string += a_string + "_"
        else:
            output_string += a_string
            next_index = index + 1
            while next_index < len(output_list):
                a_value = output_list[next_index]
                if a_value.startswith("h"):
                    output_string += a_value[1:]
                else:
                    index = next_index
                    break
                next_index += 1
            output_string += "_"
        index += 1
    output_string = output_string[:-1]
    output_string = output_string.replace("_0_", "_")
    return output_string

def uncompressing_method(input_string):
    """
{'Have you': '1', 'eat': '2', 'sleep': '3', 'today': '4', '?': '5', ' ': '0'}
Have you Have you eat and sleep today??? Can you !@#%^&@$%!#$ ?
1_1_2_h616e64_3_4_5_5_5_h43616e_h796f75_h214023255e26402425212324_5
    """
    input_list = input_string.split("_")
    output_string = ""
    for one in input_list:
        if one.startswith("h"):
            output_string += decode_unknown_string(one) + " "
        else:
            output_string += uncompressing_dict[one] + " "
    return output_string

test_string = "Have you Have you eat and sleep today??? Can you !@#%^&@$%!#$ ?"
output_string = compressing_method(test_string)

print("the dict:               ", compressing_dict)
print("the raw input:          ", test_string)
print("the compressed output:  ", output_string)
print("the uncompressed output:", uncompressing_method(output_string))

# Actually you can use it to translate most languages, it can at least make sure the meaning group or long sub sentence get well translated.
