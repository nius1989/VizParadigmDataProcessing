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
    groupid = filename.split('.')[0]
    exc_a = {}
    exc_b = {}
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        while line:
            one_action = json.loads(line)
            if one_action["acttype"] == "MOVE_CARD":
                end = str(one_action["data"]["end"]).split(",")
                end_x = float(end[0])
                if one_action["data"]["user"] == "ALEX" and end_x > 640:
                    exc_a[one_action["data"]["name"]] = 1
                if one_action["data"]["user"] == "CHRIS" and end_x < 640:
                    exc_b[one_action["data"]["name"]] = 1
            line = data_file.readline()
    result[groupid] = len(exc_a) + len(exc_b)


def save_csv(data):
    with open(final_result_dir + 'total_exchange_count.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "id", "card exchange count"])
        for k, v in sorted(data.items()):
            overhead_writer.writerow([switcher(str(k)[0]), k, v])


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


# how many cards have been passed to the partner
if __name__ == '__main__':
    process(bulk_data)
    save_csv(result)
