import numpy as np
import json
import copy
import csv
import os

result = {}


def read_file(dir, file):
    with open(os.path.join(dir, file)) as json_file:
        data = json.load(json_file)
        cum_time = 0
        for sen in data["result"]["results"]:
            for word in sen["alternatives"][0]["timestamps"]:
                start = word[1]
                end = word[2]
                cum_time += end - start
        if file[0:3] not in result:
            result[file[0:3]] = cum_time
        else:
            result[file[0:3]] += cum_time


def process(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            read_file(directory, filename)
            continue
        else:
            continue


if __name__ == '__main__':
    process("D:\\video_transcript")
    # process("D:\\test")
    with open('D:\\video_speech.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["group", "id", "time"])
        for k in result:
            print(k, result[k])
            overhead_writer.writerow([k[0], k, result[k]])
