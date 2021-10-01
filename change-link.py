import fileinput
import os

file = "/home/pi/Documents/anchor_debug/build/CMakeFiles/normal-node.dir/link.txt"
match_string = ".o  "
insert_string = "-pthread "
print(os.getcwd())

with open(file, 'r+') as fd:
    contents = fd.readlines()
    print(contents)
    string = contents[0].split()
    string.insert(8, " -pthread")
    string = ' '.join(string)
    print(string)
    # fd.seek(0)
    # fd.writelines(contents)
