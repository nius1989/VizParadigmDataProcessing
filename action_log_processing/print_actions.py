import csv
import os
import json
from dateutil import parser
from datetime import datetime
from datetime import timedelta
import math
from global_config import *

result = {}
work_sheet_answers = {}


def read_file(directory, filename):
    groupid = filename.split('.')[0]
    init_time = None
    target = {
        "name": "map",
        "x": 0,
        "y": 0

    }
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        # while line:
        for i in range(20):
            one_action = json.loads(line)
            if init_time is None:
                init_time = parser.parse(one_action['time'])
            print("time:{}, type:{}".format(one_action['time'], one_action['acttype']))
            # if one_action["acttype"] == "MOVE_CARD":
            #     coord = [float(c) for c in one_action['data']['end'].split(',')]
            #     if one_action['data']['name'] == target["name"]:
            #         target['x'] = coord[0]
            #         target['y'] = coord[1]
            #     time_stamp = (parser.parse(one_action['time']) - init_time).total_seconds() / 60
            #     dist = math.sqrt((target['x'] - coord[0]) ** 2 + (target['y'] - coord[1]) ** 2)
            #     # if dist < 400:
            #     print("card:{}, time:{}, dist:{}".format(one_action['data']['name'], time_stamp,
            #                                              str(dist)))
            line = data_file.readline()
    result[groupid] = 1


def process(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            if filename == "101.txt":
                read_file(directory, filename)
            continue
        else:
            continue


if __name__ == '__main__':
    process(bulk_data)
    # save_csv(result)
