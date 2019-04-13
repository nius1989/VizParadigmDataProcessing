import numpy as np
import json
import copy
import csv
import os
import re
from dateutil import parser
from datetime import datetime
from datetime import timedelta
from global_config import *
from string import Template

videos = {}
total_task_time = {}

starting_time_adjustment = {
    "101": 1,
    "102": 5,
    "103": 5,
    "104": 1,
    "105": 9,
    "109": 8,
    "110": 9,
    "111": 7,
    "112": 9,
    "202": 9,
    "203": 6,
    "205": 6,
    "206": 3,
    "207": 6,
    "209": 11,
    "210": 7,
    "211": 6,
    "212": 8,
    "301": 4,
    "302": 6,
    "303": 38,
    "304": 7,
    "305": 3,
    "309": 8,
    "310": 9,
    "311": 36,
    "312": 36,
}


def read_file(directory, filename):
    print(filename)
    file_parts = filename.split('.')
    groupid = file_parts[0]
    if groupid not in videos:
        videos[groupid] = []
    with open(os.path.join(directory, filename)) as srt:
        line = srt.readline()
        while line:
            if re.match('\d{2}:\d{2}:\d{2},\d{3} \-\-> \d{2}:\d{2}:\d{2},\d{3}', line):
                times = re.findall('\d{2}:\d{2}:\d{2},\d{3}', line)
                start = datetime.strptime(times[0], "%H:%M:%S,%f")
                end = datetime.strptime(times[1], "%H:%M:%S,%f")
                print(start)
            line = srt.readline()


def save_csv():
    for groupid in videos:
        with open(script + "\\" + groupid + '.srt', mode='w') as data_writer:
            for stamp in videos[groupid]:
                # print(stamp)
                data_writer.write(str(stamp["index"]) + "\n")
                start_time = stamp["start_time"]
                end_time = stamp["end_time"]
                data_writer.write(
                    start_time.strftime("%H:%M:%S,%f")[:-3] + " --> " + end_time.strftime("%H:%M:%S,%f")[:-3] + "\n")
                data_writer.write(stamp["content"] + "\n")


def switcher(text_code):
    if text_code is '1':
        return "PRL"
    elif text_code is '2':
        return "CON"
    elif text_code is '3':
        return "MEG"


def process_act(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            print(filename)
            # read_file(directory, filename)
            continue
        else:
            continue


def process_srt(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".srt"):
            print(filename)
            read_file(directory, filename)
            continue
        else:
            continue


if __name__ == '__main__':
    process_srt(script)
    process_act(bulk_data)
    save_csv()
