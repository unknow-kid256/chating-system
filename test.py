string = "4omer"
index = 0
str_num = ""
while string[index].isnumeric():
    str_num = string[index]
    index += 1
name = string[index:int(str_num)+1]
print(name)