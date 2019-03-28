import numpy as np
import cv2
import copy
import csv
import os
from global_config import *


def read_file(dir, file):
    matrix = [[0] * 85 for i in range(48)]
    sum_points = 0
    with open(os.path.join(dir, file)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_counter = 0
        for row in csv_reader:
            parse_row = [float(c) for c in row]
            sum_points += sum(parse_row)
            matrix[line_counter] = parse_row
            line_counter += 1
        print(sum_points)
    for rdex in range(len(matrix)):
        matrix[rdex] = [c / sum_points * 1000 for c in matrix[rdex]]
    with open('D:\\viz_data_8\\normal_accum\\normal_' + file, mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        for r in range(48):
            overhead_writer.writerow(matrix[r])


def process(directory):
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith(".csv"):
            read_file(directory, filename)
            continue
        else:
            continue


if __name__ == '__main__':
    process(root + "accum\\")
