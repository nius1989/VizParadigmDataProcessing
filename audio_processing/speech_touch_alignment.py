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

videos = {}

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
    file_parts = filename.split('-')
    groupid = file_parts[0]
    sub = file_parts[1] is '2'
    if groupid not in videos:
        videos[groupid] = []
    with open(os.path.join(directory, filename)) as srt:
        line = srt.readline()
        while line:
            if re.match('\d{2}:\d{2}:\d{2},\d{3} \-\-> \d{2}:\d{2}:\d{2},\d{3}', line):
                times = re.findall('\d{2}:\d{2}:\d{2},\d{3}', line)
                start = parser.parse(times[0])
                end = parser.parse(times[1])
                if sub:
                    start += timedelta(seconds=1790)
                    end += timedelta(seconds=1790)
                videos[groupid].append(
                    {
                        "start_time": start,
                        "end_time": end
                    })
            line = srt.readline()


def adjust_time():
    zero_time = datetime.now().replace(hour=0, minute=0, second=0)
    for groupid in videos:
        for stamp in videos[groupid]:
            stamp["start_time"] -= timedelta(seconds=starting_time_adjustment[groupid])
            stamp["end_time"] -= timedelta(seconds=starting_time_adjustment[groupid])
        videos[groupid] = list(filter(lambda x: x['start_time'] > zero_time, videos[groupid]))
        with open(processed_script_json + "\\" + groupid + '.csv', mode='w', newline='') as overhead_data:
            overhead_writer = csv.writer(overhead_data, lineterminator='\n')
            overhead_writer.writerow(["start", "end"])
            for stamp in videos[groupid]:
                overhead_writer.writerow([(stamp["start_time"] - zero_time).total_seconds(),
                                          (stamp["end_time"] - zero_time).total_seconds()])


def process(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".srt"):
            read_file(directory, filename)
            continue
        else:
            continue


def switcher(text_code):
    if text_code is '1':
        return "PRL"
    elif text_code is '2':
        return "CON"
    elif text_code is '3':
        return "MEG"


if __name__ == '__main__':
    process(processed_script)
    adjust_time()
    # save_csv(videos)
