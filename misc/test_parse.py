import socket
import asyncio
import sys
import time
from datetime import datetime
import os
import pprint
import re
from decimal import Decimal

#time_entry = time_struct(10, 12, 23, 132771)
#SHA encoding has bitstream output, if we convert bitstream to base64 then base64 does not include "_" char
#throughput and latency are factors for table

#lat_dict[foo][0] is the the time that data1 is generated

data1string = "1:18.6.5.134013_test1 2:18.6.5.314977_test1 2:18.7.10.777123_test2"
data2string = "2:18.7.10.315132_test2 1:18.7.10.115612_test2 2:18.6.5.885130_test1"
data3string = "1:0.0.10.10000_test3 2:0.0.10.110000_test3"

lat_dict = {}

def split_chars(word):
    return list(word)

def pop_lat(string_input):
    global lat_dict
    strings = string_input.split()
    for i in range(len(strings)):
        if "1:" in strings[i]:
            result = (re.search("1:(.*)_",strings[i])).group(1).split(".")
            # print(result)
            time_entry = time_struct(int(result[0]),int(result[1]),int(result[2]),int(result[3]))
            data = (re.search("_(.*)",strings[i])).group(1)
            # print(data)
            if data not in lat_dict:
                lat_dict[data] = [time_entry]
            else:
                lat_dict[data][0] = time_entry
            # print(lat_dict[data])
        
        if "2:" in strings[i]:
            result = (re.search("2:(.*)_",strings[i])).group(1).split(".")
            # print(result)
            time_entry = time_struct(int(result[0]),int(result[1]),int(result[2]),int(result[3]))
            data = (re.search("_(.*)",strings[i])).group(1)
            # print(data)
            if data not in lat_dict:
                lat_dict[data] = [0]
            lat_dict[data].append(time_entry)
            # print(lat_dict[data])

def calc_average():
    overall_avg = 0

    for i in lat_dict:
        total_hour = total_minute = total_sec = total_milsec = 0

        for j in (lat_dict[i])[1:]:
            total_hour += j.hour - lat_dict[i][0].hour
            total_minute += j.minute - lat_dict[i][0].minute
            total_sec += j.sec - lat_dict[i][0].sec
            total_milsec += j.milsec - lat_dict[i][0].milsec

        avg_hour = (total_hour / (len(lat_dict[i]) - 1)) * 3600
        avg_minute = (total_minute / (len(lat_dict[i]) - 1)) * 60
        avg_sec = (total_sec / (len(lat_dict[i]) - 1))
        avg_milsec = (total_milsec / (len(lat_dict[i]) - 1)) * (0.000001)

        total_avg = avg_hour + avg_minute + avg_sec + avg_milsec
        overall_avg += total_avg
        print(i + ":" , lat_dict[i], str(round(total_avg,6)) + " seconds")

    print("Overall Average:", round((overall_avg/len(lat_dict)),6))

class time_struct:
    def __init__(self, hour, minute, sec, milsec):
        self.hour = hour
        self.minute = minute
        self.sec = sec
        self.milsec = milsec

    def __repr__(self):
        return str(self.hour) + "." + str(self.minute) + "." + str(self.sec) + "." + str(self.milsec)

pop_lat(data1string)
pop_lat(data2string)
pop_lat(data3string)

calc_average()