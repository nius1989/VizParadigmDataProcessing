import csv
import os
import json
from dateutil import parser
from datetime import datetime
from datetime import timedelta
from collections import Counter
from heapq import nlargest
from global_config import *

questions = {
    'hiking boots': {},
    'parka': {},
    'tarp': {},
    'flashlight': {},
    'guidebook': {},
    'energy drink mix': {},
    'top 5 electronics': {},
    'top 5 overnight': {}
}

keys = {
    'hiking boots': [],
    'parka': [],
    'tarp': [],
    'flashlight': [],
    'guidebook': [],
    'energy drink mix': [],
    'top 5 electronics': [],
    'top 5 overnight': []
}


def gen_correct_answer(csv_file):
    work_sheet = csv.DictReader(open(csv_file))
    for row in work_sheet:
        for k in questions:
            answers = [str(c).strip().lower() for c in row[k].split(',')]
            for ans in answers:
                if ans not in questions[k]:
                    questions[k][ans] = 1
                else:
                    questions[k][ans] += 1
    for k in keys:
        print("***********  " + k + "  ******************")
        largest = nlargest(4, questions[k], key=questions[k].get)
        if k == "top 5 electronics" or k == "top 5 overnight":
            largest = nlargest(5, questions[k], key=questions[k].get)
        for t in largest:
            keys[k].append(t)
        for l in keys[k]:
            print("largest:{}, num:{}".format(l, questions[k][l]))


def check_answer(csv_file):
    work_sheet = csv.DictReader(open(csv_file))
    with open(final_result_dir + 'worksheet_answer.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "group ID"] + list(map(str, keys.keys())) + ["total missed answers"])
        for row in work_sheet:
            print(row["Group code"], end=',')
            correct_output = []
            total_correct = 0
            for k in keys:
                answers = [str(c).strip().lower() for c in row[k].split(',')]
                wrong_count = 0
                for key in keys[k]:
                    if key not in answers:
                        wrong_count += 1
                total_correct += wrong_count
                correct_output.append(wrong_count)
                print(wrong_count, end=',')
            print(total_correct)
            correct_output.append(total_correct)
            overhead_writer.writerow(
                [switcher(row["Group code"][0]), row["Group code"]] + list(map(str, correct_output)))


def switcher(text_code):
    if text_code is '1':
        return "PRL"
    elif text_code is '2':
        return "CON"
    elif text_code is '3':
        return "MEG"


if __name__ == '__main__':
    gen_correct_answer(analysis_result + "study_worsheet_question_list.csv")
    check_answer(analysis_result + "study_worsheet_question_list.csv")
