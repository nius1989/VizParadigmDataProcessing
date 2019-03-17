import csv
import os
import json
from dateutil import parser
from datetime import datetime
from datetime import timedelta
import math
from global_config import *


def read_file(filename):
    init_time = None
    storage = []
    with open(filename, 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        while line:
            one_action = json.loads(line)
            if init_time is None:
                init_time = parser.parse(one_action['time'])
            min = (parser.parse(one_action['time']) - init_time).total_seconds() / 60
            if min <= 34.0:
                storage.append(line)
            elif min > 36.05:
                new_time = parser.parse(one_action['time']) - timedelta(minutes=2.05)
                one_action['time'] = new_time.strftime("%Y/%m/%d %I:%M:%S %p")
                print(one_action['time'])
                storage.append(json.dumps(one_action) + "\n")
            line = data_file.readline()
    with open(bulk_data + '202.txt', 'w', encoding='utf-8') as the_file:
        for line in storage:
            the_file.write(line)


if __name__ == '__main__':
    read_file(analysis_result + "202_old.txt")
    # save_csv(result)
