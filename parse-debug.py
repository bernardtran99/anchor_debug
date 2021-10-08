import fileinput
import time
import os

inputFile = "/home/debug/Documents/anchor_debug/build/debug-output.txt"
outputFile = "/home/debug/Documents/anchor_debug/build/parsed-debug.txt"
onInterest = ""
nodeStart = ""
isAnchor = ""

ipDict = {
  "1": "155.246.44.142",
  "2": "155.246.215.101",
  "3": "155.246.202.145",
  "4": "155.246.216.113",
  "5": "155.246.203.173",
  "6": "155.246.216.33",
  "7": "155.246.202.111",
  "8": "155.246.212.111",
  "9": "155.246.213.83",
  "10": "155.246.210.98",
}

while True:
    fd = open(inputFile, 'r+')

    for line in fd:
        print(line)
    fd.close()
    time.sleep(0.003)


# with open(inputFile, 'r+') as fd:
#     for line in fd:
#         print(line)
#         if "" in line:
#             strings = line.split()
#             del strings[5]
#             #print(type(strings))
#             print(strings)
        