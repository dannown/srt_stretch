#!/usr/bin/env python3

import re
from parse import parse
from regex import regex
import sys
import shutil
import chardet

VIDEO_FPS = 23.967
# VIDEO_FPS = 24.0
SUBS_FPS = 25

def timecode_to_millis(timecode):
    (hours,minutes,seconds,milliseconds) = parse("{:d}:{:d}:{:d},{:d}", timecode)
    millis = ((hours*60+minutes)*60+seconds)*1000 + milliseconds
    return millis


def millis_to_timecode(millis):
    millis = int(millis)
    hours = millis//(60*60*1000)
    minutes = millis%(60*60*1000)//(60*1000)
    seconds = millis%(60*1000)//1000
    milliseconds = millis%1000
    return "{}:{}:{},{}".format(hours, minutes, seconds, milliseconds)


def usage():
    print ("usage: {} filename".format(sys.argv[0]))
    exit(0)


def get_encoding(filename):
    DETFILE = open(filename, "rb")
    filetype = chardet.detect(DETFILE.read())
    DETFILE.close()
    return filetype['encoding']
    


if len(sys.argv) != 2:
    usage()
filename = sys.argv[1]
# make a backup
shutil.copy(filename, filename + ".bak")
encoding = get_encoding(filename)
FILE = open(filename, "r", encoding=encoding)
# read in the whole file as a string:
lines = FILE.read()
FILE.close();
sub_lines = regex.findall(pattern="\d+\n.+ --> .+\n(?:.+\n)+\n",
                          string=lines.strip(),
                          flags=regex.MULTILINE)
subs = list(map(
    lambda x: parse("{num:d}\n{start_time} --> {end_time}\n{lines}\n\n", x).named,
    sub_lines))

good_lines = ""
for sub in subs:
    start_time = millis_to_timecode(SUBS_FPS / VIDEO_FPS * timecode_to_millis(sub['start_time']))
    end_time = millis_to_timecode(SUBS_FPS / VIDEO_FPS * timecode_to_millis(sub['end_time']))
    good_lines += "{}\n{} --> {}\n{}\n\n".format(
                        sub['num'],
                        start_time, end_time,
                        sub['lines'])
FILE = open(filename, "w")
FILE.write(good_lines)
FILE.close()
