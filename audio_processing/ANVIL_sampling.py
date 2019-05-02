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

video_index = "105"


def process():
    file_dir = "G:\\My Drive\\PROJECT_VIS_PARADIM\\ANVIL_annotation\\" + video_index + ".anvil"
    # create element tree object
    tree = ET.parse(file_dir)
    # get root element
    root = tree.getroot()
    time_stamps = []
    for attention in root.findall("./body/track[@name='VISGRAINS.attention']/el"):
        start = float(attention.attrib['start'])
        end = float(attention.attrib['end'])
        time_stamps.append((start + end) / 2)
    return time_stamps


def gen_random(size):
    index_list = []
    for i in range(50):
        r = random.randint(0, len(size))
        if r not in index_list:
            index_list.append(r)
    index_list.sort()
    return index_list


def capture_video(index):
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
    currentframe = 0
    while (True):
        # reading from frame
        ret, frame = cam.read()
        if ret:
            # if video is still left continue creating images
            name = './data/frame' + str(currentframe) + '.jpg'
            print('Creating...' + name)
            # writing the extracted images
            cv2.imwrite(name, frame)
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break
    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    time_stamps = process()
    select_index = gen_random(time_stamps)
    capture_video(select_index)
