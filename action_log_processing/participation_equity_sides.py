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

# plotly.tools.set_credentials_file(username='shuoniu', api_key='dwCC2CLEvnYrO7gbbwpu')
result = {}


def read_file(directory, filename):
    print(filename)
    groupid = filename.split('.')[0]
    actions = {
        "card_move_A": 0,
        "card_move_B": 0,
        "move_A": 0,
        "move_B": 0,
    }
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        while line:
            one_action = json.loads(line)
            if one_action["user"] == "ALEX":
                actions["move_A"] += 1
            if one_action["user"] == "CHRIS":
                actions["move_B"] += 1
            if one_action["acttype"] == "MOVE_CARD":
                end_point = list(map(float, one_action["data"]["end"].split(',')))
                if end_point[0] < 640:
                    actions["card_move_A"] += 1
                if end_point[0] > 640:
                    actions["card_move_B"] += 1
            line = data_file.readline()
    result[groupid] = actions


def save_csv(data):
    with open(final_result_dir + 'participation_equity_sdies.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(
            ["paradigm", "id", "card movement A", "card movement B", "card movement standard deviation",
             "action A", "action B", "action standard deviation"])
        for group, actions in sorted(data.items()):
            c_move_a = actions["card_move_A"] / (actions["card_move_A"] + actions["card_move_B"])
            c_move_b = actions["card_move_B"] / (actions["card_move_A"] + actions["card_move_B"])
            move_a = actions["move_A"] / (actions["move_A"] + actions["move_B"])
            move_b = actions["move_B"] / (actions["move_A"] + actions["move_B"])
            overhead_writer.writerow(
                [switcher(str(group)[0]), group,
                 c_move_a, c_move_b, numpy.std([c_move_a, c_move_b]),
                 move_a, move_b, numpy.std([move_a, move_b])])


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
