import numpy as np
import cv2
import copy
import csv
import os
from global_config import *
import numpy

result = {}


def read_file(dir, file):
    groupid = file.split('.')[0]
    with open(os.path.join(dir, file)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        left_frame = 0
        right_frame = 0
        for line in csv_reader:
            left_counter = 0
            right_counter = 0
            for row in range(48):
                for col in range(85):
                    val = line[row * 85 + col]
                    if val == '1':
                        if 15 <= col <= 41:
                            left_counter += 1
                        elif 69 >= col >= 43:
                            right_counter += 1
            # if left_counter > right_counter:
            #     left_frame += 1
            # elif left_counter < right_counter:
            #     right_frame += 1
            left_frame += left_counter
            right_frame += right_counter
        result[groupid] = {
            "frame_A": left_frame,
            "frame_B": right_frame
        }


def save_csv(data):
    with open(final_result_dir + 'video_equity_sdies2.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(
            ["paradigm", "id", "Frame A", "Frame B", "Frame A percentage",
             "Frame B percentage", "action standard deviation"])
        for group, actions in sorted(data.items()):
            c_move_a = actions["frame_A"] / (actions["frame_A"] + actions["frame_B"])
            c_move_b = actions["frame_B"] / (actions["frame_A"] + actions["frame_B"])
            overhead_writer.writerow(
                [switcher(str(group)[0]), group, actions["frame_A"], actions["frame_B"],
                 c_move_a, c_move_b, numpy.std([c_move_a, c_move_b])])


def switcher(text_code):
    if text_code is '1':
        return "PRL"
    elif text_code is '2':
        return "CON"
    elif text_code is '3':
        return "MEG"


def process(directory):
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith(".csv"):
            read_file(directory, filename)
            continue
        else:
            continue


if __name__ == '__main__':
    process(root + "video_process_csv_data\\")
    save_csv(result)
