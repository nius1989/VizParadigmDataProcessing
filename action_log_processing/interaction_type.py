import csv
import os
import json
from dateutil import parser
from datetime import datetime
from datetime import timedelta
from global_config import *

result = {}
total_task_time = {}
interval = 5


def read_file(directory, filename):
    print(filename)
    move_counter = 0
    groupid = filename.split('.')[0]
    init_time = None
    buffer = []
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        buffer = {}
        while line:
            one_action = json.loads(line)
            if init_time is None and one_action['acttype'] == "START":
                init_time = parser.parse(one_action['time'])
            if one_action["acttype"] != "ERROR" and one_action["acttype"] != "NOTIF_VIZ" and one_action[
                "acttype"] != "START" and one_action["acttype"] != "END" and one_action["acttype"] != "SHOW_BOX":
                time = parser.parse(one_action["time"])
                bin_num = int((time - init_time).total_seconds() / interval)
                if bin_num not in buffer:
                    buffer[bin_num] = []
                buffer[bin_num].append(one_action)
            line = data_file.readline()
    non_interact = 0
    one_interact = 0
    two_interact = 0
    max_index = max(buffer.keys())
    rg = [i for i in range(max_index + 1)]
    for i in rg:
        if i not in buffer:
            non_interact += 1
            continue
        a_interact = list(filter(lambda x: x["user"] == "ALEX", buffer[i]))
        c_interact = list(filter(lambda x: x["user"] == "CHRIS", buffer[i]))
        if len(a_interact) != 0 and len(c_interact) != 0:
            two_interact += 1
        else:
            one_interact += 1

    result[groupid] = {
        "non": non_interact / (max_index + 1),
        "one": one_interact / (max_index + 1),
        "two": two_interact / (max_index + 1)
    }


def save_csv(data):
    with open(final_result_dir + 'sim_seq_pattern.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "group ID", "two interact", "one interact", "no interact"])
        for k, v in sorted(data.items()):
            overhead_writer.writerow([switcher(str(k)[0]), k, v["two"], v["one"], v["non"]])


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
