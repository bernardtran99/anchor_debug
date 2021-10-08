import fileinput
import os

inputFile = "/home/debug/Documents/anchor_debug/build/debug-output.txt"
with open(inputFile, 'r+') as fd:
    contents = fd.readlines()
    print(contents)
