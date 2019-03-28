import numpy as np
import cv2
import copy
import csv
import os
from global_config import *


def read_file(dir, file):
    counter = [0] * (48 * 85)
    with open(os.path.join(dir, file)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            for col in range(len(row)):
                counter[col] += float(row[col])
            line_count += 1
    with open('D:\\viz_data\\accum\\accum_' + file, mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        for r in range(48):
            overhead_writer.writerow(counter[r * 85:(r * 85 + 85)])


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
