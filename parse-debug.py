import fileinput
import os

inputFile = "/home/debug/Documents/anchor_debug/build/debug-output.txt"
outputFile = "/home/debug/Documents/anchor_debug/build/parsed-debug.txt"
onInterest = ""
nodeStart = ""
isAnchor = ""
with open(inputFile, 'r+') as fd:
    for line in fd:
        print(line)
        strings = line.strip()
        print(strings)
        