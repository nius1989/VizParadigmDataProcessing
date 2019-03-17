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
total_task_time = {}

starting_time = {
    "101": 15
}


def read_file(directory, filename):
    file_parts = filename.split('-')
    print("read file: " + filename)
    if file_parts[0] not in videos:
        videos[file_parts[0]] = []
    sub = file_parts[1] is '2'
    with open(os.path.join(directory, filename)) as srt:
        counter = 0
        line = srt.readline()
        while line:
            if re.match('\d{2}:\d{2}:\d{2},\d{3} \-\-> \d{2}:\d{2}:\d{2},\d{3}', line):
                times = re.findall('\d{2}:\d{2}:\d{2},\d{3}', line)
                start = parser.parse(times[0])
                end = parser.parse(times[1])
                if sub:
                    start += timedelta(minutes=30)
                    end += timedelta(minutes=30)
                # print("{} --> {}".format(start.strftime('%H:%M:%S.%f'), end.strftime('%H:%M:%S.%f')))
                videos[file_parts[0]].append((end - start).total_seconds())
                counter += 1
            line = srt.readline()


def process(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".srt"):
            read_file(directory, filename)
            continue
        else:
            continue


def save_csv(data):
    with open(final_result_dir + 'video_speech_p.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(
            ["group", "id", "speech time(s)", "no speech time(s)", "total_speech_cnt", "speech time ratio"])
        for k, v in sorted(data.items()):
            overhead_writer.writerow(
                [switcher(str(k)[0]), k, sum(v), total_task_time[k] - sum(v), len(v), sum(v) / total_task_time[k]])


def switcher(text_code):
    if text_code is '1':
        return "PRL"
    elif text_code is '2':
        return "CON"
    elif text_code is '3':
        return "MEG"


def load_task_time(csv_file):
    time_data = csv.DictReader(open(csv_file))
    for row in time_data:
        total_task_time[row['group ID']] = float(row['task time(s)'])


if __name__ == '__main__':
    load_task_time(final_result_dir + "total_task_time.csv")
    process(processed_script)
    save_csv(videos)
