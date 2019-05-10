import numpy as np
import json
import copy
import csv
import os
import re
from dateutil import parser
from datetime import datetime, date, time, timedelta
from global_config import *
import xml.etree.ElementTree as ET
from lxml import etree

starting_time_adjustment = {
    "101": 2.2,
    "102": 5,
    "103": 5,
    "104": 7.8,
    "105": 9,
    "109": 9.4,
    "110": 9,
    "111": 7,
    "112": 9,
    "202": 9,
    "203": 6,
    "205": 6,
    "206": 3,
    "207": 6,
    "209": 11,
    "210": 7,
    "211": 6,
    "212": 8,
    "301": 4,
    "302": 6,
    "303": 38,
    "304": 7,
    "305": 3,
    "309": 8,
    "310": 9,
    "311": 36,
    "312": 43,
}

ticks = {}
conversation = {}
touch = {}


def read_srt_file(directory, filename):
    print(filename)
    file_parts = filename.split('.')
    groupid = file_parts[0]
    ticks[groupid] = []
    conversation[groupid] = []
    with open(os.path.join(directory, filename)) as srt:
        line = srt.readline()
        while line:
            if re.match('\d{2}:\d{2}:\d{2},\d{3} \-\-> \d{2}:\d{2}:\d{2},\d{3}', line):
                times = re.findall('\d{2}:\d{2}:\d{2},\d{3}', line)
                start = datetime.strptime(times[0], "%H:%M:%S,%f")
                end = datetime.strptime(times[1], "%H:%M:%S,%f")
                ticks[groupid].append(start)
                ticks[groupid].append(end)
                conversation[groupid].append({
                    "start": start,
                    "end": end
                })
            line = srt.readline()


def read_act_file(directory, filename):
    print(filename)
    groupid = filename.split('.')[0]
    init_time = None
    time_tracker = None
    time_stamp_pre = None
    time_gap = 5
    touch[groupid] = []
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as data_file:
        line = data_file.readline()
        while line:
            one_action = json.loads(line)
            if init_time is None:
                init_time = parser.parse(one_action['time'])
                time_tracker = parser.parse(one_action['time'])
                time_stamp_pre = parser.parse(one_action['time'])
            time_stamp = parser.parse(one_action["time"])
            if (time_stamp - time_stamp_pre).seconds > time_gap:
                start = datetime.strptime(str(time_tracker - init_time), "%H:%M:%S") + timedelta(
                    seconds=starting_time_adjustment[groupid])
                end = datetime.strptime(str(time_stamp_pre - init_time), "%H:%M:%S") + timedelta(
                    seconds=starting_time_adjustment[groupid])
                ticks[groupid].append(start)
                ticks[groupid].append(end)
                time_tracker = time_stamp
                touch[groupid].append({
                    "start": start,
                    "end": end
                })
            time_stamp_pre = time_stamp
            line = data_file.readline()


def sort_data():
    for file in ticks:
        ticks[file].sort()
        print(len(ticks[file]))
        i = 0
        while i < len(ticks[file]) - 1:
            if (ticks[file][i + 1] - ticks[file][i]).seconds < 1:
                new_time = ticks[file][i] + (ticks[file][i + 1] - ticks[file][i]) / 2
                ticks[file].pop(i + 1)
                ticks[file].pop(i)
                ticks[file].insert(i, new_time)
            else:
                i += 1
        print(len(ticks[file]))


def save_anvil():
    for groupid in ticks:
        root = ET.Element("annotation")
        head = ET.SubElement(root, "head")
        ET.SubElement(head, "specification", src="../anvil_specification.xml")
        ET.SubElement(head, "video",
                      src="../DATA/" + groupid + "/" + groupid + "_side.mp4",
                      master="true")
        ET.SubElement(head, "info", key="coder", type="String").text = "Lindah"
        ET.SubElement(head, "info", key="encoding", type="String").text = "UTF-16"
        body = ET.SubElement(root, "body")
        # track1
        track = ET.SubElement(body, "track", name="VISGRAINS.attention", type="primary")
        for i in range(len(ticks[groupid]) - 1):
            start_mark = ticks[groupid][i] - datetime(1900, 1, 1)
            end_mark = ticks[groupid][i + 1] - datetime(1900, 1, 1)
            ET.SubElement(track, "el", index=str(i),
                          start=str(start_mark.total_seconds()), end=str(end_mark.total_seconds()))
        # track2
        track = ET.SubElement(body, "track", name="VISGRAINS.conversation", type="primary")
        for i in range(len(ticks[groupid]) - 1):
            start_mark = ticks[groupid][i] - datetime(1900, 1, 1)
            end_mark = ticks[groupid][i + 1] - datetime(1900, 1, 1)
            ET.SubElement(track, "el", index=str(i),
                          start=str(start_mark.total_seconds()), end=str(end_mark.total_seconds()))
        # track3
        track = ET.SubElement(body, "track", name="VISGRAINS.touch", type="primary")
        for i in range(len(touch[groupid])):
            start_mark = touch[groupid][i]["start"] - datetime(1900, 1, 1)
            end_mark = touch[groupid][i]["end"] - datetime(1900, 1, 1)
            el = ET.SubElement(track, "el", index=str(i),
                               start=str(start_mark.total_seconds()), end=str(end_mark.total_seconds()))
            ET.SubElement(el, "attribute", name="touch").text = "Touch"
        # track4
        track = ET.SubElement(body, "track", name="VISGRAINS.ref_conversation", type="primary")
        for i in range(len(conversation[groupid])):
            start_mark = conversation[groupid][i]["start"] - datetime(1900, 1, 1)
            end_mark = conversation[groupid][i]["end"] - datetime(1900, 1, 1)
            el = ET.SubElement(track, "el", index=str(i),
                               start=str(start_mark.total_seconds()), end=str(end_mark.total_seconds()))
            ET.SubElement(el, "attribute", name="ref_conversation").text = "Talk"
        xmlstr = ET.tostring(root, encoding='utf8', method='xml')
        dom = etree.fromstring(xmlstr)
        with open(anvil + "\\" + groupid + ".anvil", encoding="utf-8", mode="w") as data_file:
            data_file.write(etree.tostring(dom, pretty_print=True, xml_declaration=True, encoding="utf-8").decode())


def switcher(text_code):
    if text_code is '1':
        return "PRL"
    elif text_code is '2':
        return "CON"
    elif text_code is '3':
        return "MEG"


def process_act(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            read_act_file(directory, filename)
            continue
        else:
            continue


def process_srt(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".srt"):
            read_srt_file(directory, filename)
            continue
        else:
            continue


if __name__ == '__main__':
    process_srt(script)
    process_act(bulk_data)
    sort_data()
    save_anvil()
