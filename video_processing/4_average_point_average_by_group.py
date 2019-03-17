import numpy as np
import cv2
import copy
import csv
import os

matrix1 = [[0] * 85 for i in range(48)]
matrix2 = [[0] * 85 for i in range(48)]
matrix3 = [[0] * 85 for i in range(48)]


def read_file(dir, file, matrix):
    with open(os.path.join(dir, file)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_counter = 0
        for row in csv_reader:
            parse_row = [float(c) for c in row]
            col_count = 0
            for col in parse_row:
                matrix[line_counter][col_count] += col
                col_count += 1
            line_counter += 1
    # print(matrix[1])


def process(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            print(filename)
            if filename[26] is '1':
                read_file(directory, filename, matrix1)
            elif filename[26] is '2':
                read_file(directory, filename, matrix2)
            elif filename[26] is '3':
                read_file(directory, filename, matrix3)
            continue
        else:
            continue


def save_csv(matrix, index):
    with open('D:\\viz_data_8\\final_result\\heat_map\\matrix' + index + '.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        for r in range(48):
            overhead_writer.writerow(matrix[r])


if __name__ == '__main__':
    process("D:\\viz_data_8\\normal_accum\\")
    save_csv(matrix1, '_PRL')
    save_csv(matrix2, '_CON')
    save_csv(matrix3, '_MEG')
