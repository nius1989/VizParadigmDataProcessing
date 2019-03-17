import csv
import os
import json
from dateutil import parser
from datetime import datetime
from datetime import timedelta
from global_config import *

result = {}


def read_file(directory, filename):
    print(filename)
    start_time = None
    search_end_time = datetime.now()
    end_time = datetime.now()
    groupid = filename.split('.')[0]
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        while line:
            one_action = json.loads(line)
            if one_action["acttype"] == "ADD_CARD" and start_time is None:
                start_time = parser.parse(one_action["time"])
            if one_action["acttype"] == "MOVE_CARD":
                end_time = parser.parse(one_action["time"])
            if one_action["acttype"] == "ADD_CARD":
                if one_action["data"]["name"] == "warm coat" or one_action["data"]["name"] == "tent":
                    search_end_time = parser.parse(one_action["time"])
            line = data_file.readline()
    result[groupid] = {}
    result[groupid]["total time"] = (end_time - start_time).total_seconds()
    result[groupid]["search time"] = (search_end_time - start_time).total_seconds()
    result[groupid]["answer time"] = (end_time - search_end_time).total_seconds()


def save_csv(data):
    with open(final_result_dir + 'total_task_time.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "group ID", "task time(s)", "search time(s)", "answer time(s)"])
        for k, v in sorted(data.items()):
            overhead_writer.writerow([switcher(str(k)[0]), k, v["total time"], v["search time"], v["answer time"]])


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


if __name__ == '__main__':
    process(bulk_data)
    save_csv(result)
