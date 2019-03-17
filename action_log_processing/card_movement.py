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

plotly.tools.set_credentials_file(username='shuoniu', api_key='dwCC2CLEvnYrO7gbbwpu')
result = {}


def read_file(directory, filename):
    print(filename)
    groupid = filename.split('.')[0]
    trace = {}
    init_time = None
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        while line:
            one_action = json.loads(line)
            if init_time is None and one_action['acttype'] == "START":
                init_time = parser.parse(one_action['time'])
            if one_action["acttype"] == "MOVE_CARD":
                current_time = str(parser.parse(one_action['time']) - init_time)
                end_point = list(map(float, one_action["data"]["end"].split(',')))
                if one_action["data"]["name"] not in trace:
                    trace[one_action["data"]["name"]] = []
                trace[one_action["data"]["name"]].append(
                    {
                        "name": one_action["data"]["name"],
                        "position": end_point,
                        "time": current_time,
                        "user": one_action["data"]["user"]
                    }
                )
            line = data_file.readline()
    result[groupid] = trace


def save_csv(data):
    with open(analysis_result + 'card_position.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "id", "card name", "user", "time", "x", "y"])
        for group, trace in sorted(data.items()):
            for n, points in trace.items():
                for point in points:
                    overhead_writer.writerow(
                        [switcher(str(group)[0]), group, n, point["user"], point["time"], point["position"][0],
                         point["position"][1]])


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


# generate card moving log
if __name__ == '__main__':
    process(bulk_data)
    save_csv(result)
