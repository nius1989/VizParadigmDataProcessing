import csv
import os
import json
from dateutil import parser
from datetime import datetime
from datetime import timedelta
import math
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy
import csv
from global_config import *

result = {}


def read_file(directory, filename):
    print(filename)
    groupid = filename.split('.')[0]
    counter = 0
    init_time = None
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        while line:
            one_action = json.loads(line)
            if init_time is None and one_action['acttype'] == "START":
                init_time = parser.parse(one_action['time'])
            if one_action["acttype"] == "MOVE_CARD":
                end_point = list(map(float, one_action["data"]["end"].split(',')))
                if one_action["data"]["user"] == "ALEX" and end_point[0] > 640:
                    counter += 1
                if one_action["data"]["user"] == "CHRIS" and end_point[0] < 640:
                    counter += 1
            line = data_file.readline()
    result[groupid] = counter


def save_csv(data):
    with open(final_result_dir + 'card_movement_on_other.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "id", "card movement on other's(cnt)"])
        for group, count in sorted(data.items()):
            overhead_writer.writerow(
                [switcher(str(group)[0]), group, count])


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


# card create by one person and moved by the partner
if __name__ == '__main__':
    process(bulk_data)
    save_csv(result)
