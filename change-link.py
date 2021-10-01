import fileinput
import os

file = "/home/pi/Documents/anchor_debug/build/CMakeFiles/normal-node.dir/link.txt"
match_string = ".o  "
insert_string = "-pthread "
print(os.getcwd())

with open(file, 'r+') as fd:
    contents = fd.readlines()
    print(contents[0])
    print(enumerate(contents))
#     if match_string in contents[-1]:  # Handle last line to prevent IndexError
#         contents.append(insert_string)
#     else:
#         for index, line in enumerate(contents):
#             if match_string in line and insert_string not in contents[index + 1]:
#                 contents.insert(index + 1, insert_string)
#                 break
#     fd.seek(0)
#     fd.writelines(contents)