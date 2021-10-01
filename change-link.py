import fileinput
import os

file = "/home/pi/Documents/anchor_debug/build/CMakeFiles/normal-node.dir/link.txt"
match_string = ".o  "
insert_string = "-pthread "
print(os.getcwd())

with open(file, 'r+') as fd:
    contents = fd.readlines()
    print(contents[0])
    if match_string in contents[0]:
        contents.insert(contents[0], insert_string)
    print(contents[0])
    # fd.seek(0)
    # fd.writelines(contents)
