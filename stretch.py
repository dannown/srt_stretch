import re
from parse import parse

VIDEO_FPS = 23.967
SUBS_FPS = 25

FILE = open("/tmp/a.sub", "r")


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


# read in the whole file as a string:
lines = FILE.read()
sub_lines = re.findall("\d+\n.+ --> .+\n.*\n(?:.*\n)\n", lines.strip())
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
FILE = open("/tmp/out.sub", "w")
FILE.write(good_lines)
FILE.close()