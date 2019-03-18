import csv
import os
import json
from dateutil import parser
from datetime import datetime
from datetime import timedelta
from global_config import *

result = {}
total_task_time = {}
total_speech_time = {}
interval = 6.76


def read_file(directory, filename):
    print(filename)
    groupid = filename.split('.')[0]
    init_time = None
    buffer = {}
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
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
    max_index = max(buffer.keys())
    rg = [i for i in range(max_index + 1)]
    action_pattern = {}
    for i in rg:
        if check_speech(groupid, i):
            action_pattern[i] = "C"
        else:
            action_pattern[i] = "L"
        if i not in buffer:
            action_pattern[i] += "N"
            continue
        a_interact = list(filter(lambda x: x["user"] == "ALEX", buffer[i]))
        c_interact = list(filter(lambda x: x["user"] == "CHRIS", buffer[i]))
        if len(a_interact) != 0 and len(c_interact) != 0:
            action_pattern[i] += "B"
        else:
            action_pattern[i] += "O"
    pattern_count = {
        "LN": 0,
        "LO": 0,
        "LB": 0,
        "CN": 0,
        "CO": 0,
        "CB": 0
    }
    for k, v in action_pattern.items():
        pattern_count[v] += 1
    result[groupid] = pattern_count
    print(pattern_count)


def load_speech(directory, filename):
    groupid = filename.split('.')[0]
    work_sheet = csv.DictReader(open(os.path.join(directory, filename)))
    speech_time = []
    for row in work_sheet:
        speech_time.append({"start": float(row['start']), "end": float(row['end'])})
    total_speech_time[groupid] = speech_time


def check_speech(groupid, time_stamp):
    for time in total_speech_time[groupid]:
        if time['start'] < time_stamp * interval and time['end'] > (time_stamp + 1) * interval:
            return True
        elif time['start'] > time_stamp * interval and time['end'] < (time_stamp + 1) * interval:
            return True
        elif time['start'] < time_stamp * interval < time['end']:
            return True
        elif time['start'] < (time_stamp + 1) * interval < time['end']:
            return True
    return False


def save_csv(data):
    with open(final_result_dir + 'speech_action_matching.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "group ID", "CB", "CO", "CN", "LB", "LO", "LN"])
        for k, v in sorted(data.items()):
            overhead_writer.writerow([switcher(str(k)[0]), k, v["CB"], v["CO"], v["CN"], v["LB"], v["LO"], v["LN"]])


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


def process2(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            load_speech(directory, filename)
            continue
        else:
            continue


if __name__ == '__main__':
    process2(processed_script_json)
    process(bulk_data)
    save_csv(result)
