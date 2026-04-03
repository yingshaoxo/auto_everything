#file_path = "./utf8_test.txt"
#with open(file_path, "w", encoding="utf-8") as f:
#    f.write("操z你")
#
#with open(file_path, "rb") as f:
#    data = f.read()

data = "操z你".encode("utf-8")
print(data)
#b'\xe6\x93\x8dz\xe4\xbd\xa0'

index = 0
while True:
    one = data[index]
    if type(one) != int:
        one = ord(one)

    if one <= 0x7F:
        print("en:", one)
        index += 1
    elif 0xE0 <= one <= 0xEF:
        # for utf-8
        print("cn:", data[index:index+3])
        index += 3
    elif one >= 0x80:
        # for gbk(gb2312)
        print("cn:", data[index:index+2])
        index += 2
    else:
        index += 1

    if index >= len(data):
        break

#b'\xe6\x93\x8dz\xe4\xbd\xa0'
#cn: b'\xe6\x93\x8d'
#en: 122
#cn: b'\xe4\xbd\xa0'
