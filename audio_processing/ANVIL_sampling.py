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
import random
import cv2

video_index = "310"
index_list = []
time_stamps = []
conversation = []
touch = []


def process():
    file_dir = "G:\\My Drive\\PROJECT_VIS_PARADIM\\ANVIL_annotation\\" + video_index + ".anvil"
    # create element tree object
    tree = ET.parse(file_dir)
    # get root element
    root = tree.getroot()
    for attention in root.findall("./body/track[@name='VISGRAINS.attention']/el"):
        start = float(attention.attrib['start'])
        end = float(attention.attrib['end'])
        time_stamps.append((start + end) / 2)
    for t in root.findall("./body/track[@name='VISGRAINS.touch']/el"):
        touch.append({
            "start": float(t.attrib['start']),
            "end": float(t.attrib['end'])
        })
    for c in root.findall("./body/track[@name='VISGRAINS.speech']/el"):
        conversation.append({
            "start": float(c.attrib['start']),
            "end": float(c.attrib['end'])
        })
    return time_stamps


def is_event(time, list):
    for ts in list:
        if ts["start"] < time < ts["end"]:
            return True
    return False


def gen_random():
    random.seed(114)
    for i in range(50):
        r = random.randint(1, len(time_stamps))
        if r not in index_list:
            index_list.append(r)
    index_list.sort()


def capture_video():
    # Read the video from specified path
    cam = cv2.VideoCapture("G:\\My Drive\\PROJECT_VIS_PARADIM\\DATA\\" + video_index + "\\" + video_index + "_side.mp4")
    try:
        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')
            # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')
        # frame
    fps = 30
    for time_index in index_list:
        note = "Conversation:{}, Interaction:{}".format(
            "Yes" if is_event(time_stamps[time_index], conversation) else "No",
            "Yes" if is_event(time_stamps[time_index], touch) else "No"
        )
        print(note)
        frame_no = int(int(time_stamps[time_index]) * fps)
        # The second argument defines the frame number in range 0.0-1.0
        cam.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        # Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
        ret, frame = cam.read()
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, note, (100, 150), font, 2, (0, 0, 0), 2, cv2.LINE_AA)
        time_mark = "Group" + video_index + ',' + str(int(time_stamps[time_index] / 60)) + ':' + str(
            int(time_stamps[time_index]) % 60)
        cv2.putText(frame, time_mark, (100, 60), font, 2, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.waitKey()
        # Store this frame to an image
        name = anvil_capture + video_index + "\\" + video_index + '_' + str(
            int(time_stamps[time_index] / 60)) + '_' + str(
            int(time_stamps[time_index]) % 60) + '.jpg'
        print(name)
        cv2.imwrite(name, frame)
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    process()
    gen_random()
    capture_video()
