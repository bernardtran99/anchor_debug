import fileinput
import os

insert_string = " -pthread"
# print(os.getcwd())

file = "anchor_debug/build/CMakeFiles/normal-node.dir/link.txt"
with open(file, 'r+') as fd:
    contents = fd.readlines()
    print(contents)
    string = contents[0].split()
    string.insert(8, insert_string)
    string = ' '.join(string)
    print(string)
    fd.seek(0)
    fd.writelines(string)
    print("Written to normal-node.dir")

file = "anchor_debug/build/CMakeFiles/normal-node-demo1.dir/link.txt"
with open(file, 'r+') as fd:
    contents = fd.readlines()
    print(contents)
    string = contents[0].split()
    string.insert(8, insert_string)
    string = ' '.join(string)
    print(string)
    fd.seek(0)
    fd.writelines(string)
    print("Written to normal-node-demo1.dir")

file = "anchor_debug/build/CMakeFiles/normal-node-demo2.dir/link.txt"
with open(file, 'r+') as fd:
    contents = fd.readlines()
    print(contents)
    string = contents[0].split()
    string.insert(8, insert_string)
    string = ' '.join(string)
    print(string)
    fd.seek(0)
    fd.writelines(string)
    print("Written to normal-node-demo2.dir")

file = "anchor_debug/build/CMakeFiles/normal-node-demo3.dir/link.txt"
with open(file, 'r+') as fd:
    contents = fd.readlines()
    print(contents)
    string = contents[0].split()
    string.insert(8, insert_string)
    string = ' '.join(string)
    print(string)
    fd.seek(0)
    fd.writelines(string)
    print("Written to normal-node-demo3.dir")

file = "anchor_debug/build/CMakeFiles/normal-node-demo4.dir/link.txt"
with open(file, 'r+') as fd:
    contents = fd.readlines()
    print(contents)
    string = contents[0].split()
    string.insert(8, insert_string)
    string = ' '.join(string)
    print(string)
    fd.seek(0)
    fd.writelines(string)
    print("Written to normal-node-demo4.dir")

file = "anchor_debug/build/CMakeFiles/normal-node-demo5.dir/link.txt"
with open(file, 'r+') as fd:
    contents = fd.readlines()
    print(contents)
    string = contents[0].split()
    string.insert(8, insert_string)
    string = ' '.join(string)
    print(string)
    fd.seek(0)
    fd.writelines(string)
    print("Written to normal-node-demo5.dir")