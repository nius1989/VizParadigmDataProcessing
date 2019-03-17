import csv
import os
import json
from dateutil import parser
from datetime import datetime
from datetime import timedelta
from global_config import *

result = {}
total_task_time = {}


def read_file(directory, filename):
    print(filename)
    move_counter = 0
    groupid = filename.split('.')[0]
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        while line:
            one_action = json.loads(line)
            if one_action["acttype"] == "MOVE_CARD":
                move_counter += 1
            line = data_file.readline()
    result[groupid] = move_counter


def save_csv(data):
    with open(final_result_dir + 'total_move_count.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "group ID", "card movement count", "move frequency(cnt/min)"])
        for k, v in sorted(data.items()):
            overhead_writer.writerow([switcher(str(k)[0]), k, v, v / total_task_time[k] * 60])


def switcher(text_code):
    if text_code is '1':
        return "PRL"
    elif text_code is '2':
        return "CON"
    elif text_code is '3':
        return "MEG"


def process(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            read_file(directory, filename)
            continue
        else:
            continue


def load_task_time(csv_file):
    time_data = csv.DictReader(open(csv_file))
    for row in time_data:
        total_task_time[row['group ID']] = float(row['task time(s)'])


if __name__ == '__main__':
    load_task_time(final_result_dir + "total_task_time.csv")
    process(bulk_data)
    save_csv(result)
