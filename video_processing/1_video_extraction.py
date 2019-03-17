'''
Copyright (c) 2017 Intel Corporation.
Licensed under the MIT license. See LICENSE file in the project root for full license information.
'''

import numpy as np
import cv2
import copy
import csv
import os


def process(file):
    filename_w_ext = os.path.basename(file)
    file_name, file_extension = os.path.splitext(filename_w_ext)
    dir = os.path.dirname(os.path.realpath(file))
    cap = cv2.VideoCapture(file)
    # pip install opencv-contrib-python
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    # number of frames is a variable for development purposes, you can change the for loop to a while(cap.isOpened()) instead to go through the whole video
    num_frames = 500

    first_iteration_indicator = 1
    frame_counter = 0
    with open(dir + file_name + '_overhead_data.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        # for i in range(0, num_frames):
        while cap.isOpened():
            '''
            There are some important reasons this if statement exists:
                -in the first run there is no previous frame, so this accounts for that
                -the first frame is saved to be used for the overlay after the accumulation has occurred
                -the height and width of the video are used to create an empty image for accumulation (accum_image)
            '''
            frame_counter += 1
            if first_iteration_indicator == 1:
                ret, frame = cap.read()
                first_frame = copy.deepcopy(frame)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                height, width = gray.shape[:2]
                accum_image = np.zeros((height, width), np.uint8)
                first_iteration_indicator = 0
            else:
                ret, frame = cap.read()  # read a frame
                if frame is None:
                    break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale

                fgmask = fgbg.apply(gray)  # remove the background

                # for testing purposes, show the result of the background subtraction
                cv2.imshow('diff-bkgnd-frame', fgmask)

                # apply a binary threshold only keeping pixels above thresh and setting the result to maxValue.  If you want
                # motion to be picked up more, increase the value of maxValue.  To pick up the least amount of motion over time, set maxValue = 1
                thresh = 3
                maxValue = 1
                ret, th1 = cv2.threshold(fgmask, thresh, maxValue, cv2.THRESH_BINARY)

                # gen stored data
                data = [0] * (48 * 85)
                for r in range(48):
                    for c in range(85):
                        if th1[r * 10 + 5, c * 10 + 1] > 0:
                            data[r * 85 + c] = 1
                overhead_writer.writerow(data)
                # for testing purposes, show the threshold image
                # cv2.imwrite('diff-th1.jpg', th1)

                # add to the accumulated image
                # accum_image = cv2.add(accum_image, th1)
                # for testing purposes, show the accumulated image
                # cv2.imwrite(dir + file_name + '_accum.jpg', accum_image)

                # for testing purposes, control frame by frame
                # raw_input("press any key to continue")

                # for testing purposes, show the current frame
                # cv2.imshow('frame', gray)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # apply a color map
    # COLORMAP_PINK also works well, COLORMAP_BONE is acceptable if the background is dark
    # color_image = im_color = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)
    # for testing purposes, show the colorMap image
    # cv2.imwrite('diff-color.jpg', color_image)

    # overlay the color mapped image to the first frame
    # result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)

    # save the final overlay image
    # cv2.imwrite(dir + file_name + '_overlay.jpg', result_overlay)

    # cleanup
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    process("D:\\video process\\101_cut.mp4")
    process("D:\\video process\\102_cut.mp4")
    process("D:\\video process\\103_cut.mp4")
    process("D:\\video process\\104_cut.mp4")
    process("D:\\video process\\105_cut.mp4")
    process("D:\\video process\\109_cut.mp4")
    process("D:\\video process\\110_cut.mp4")
    process("D:\\video process\\111_cut.mp4")
    process("D:\\video process\\112_cut.mp4")
    process("D:\\video process\\202_cut.mp4")
    process("D:\\video process\\203_cut.mp4")
    process("D:\\video process\\205_cut.mp4")
    process("D:\\video process\\206_cut.mp4")
    process("D:\\video process\\207_cut.mp4")
    process("D:\\video process\\209_cut.mp4")
    process("D:\\video process\\210_cut.mp4")
    process("D:\\video process\\211_cut.mp4")
    process("D:\\video process\\212_cut.mp4")
    process("D:\\video process\\301_cut.mp4")
    process("D:\\video process\\302_cut.mp4")
    process("D:\\video process\\303_cut.mp4")
    process("D:\\video process\\304_cut.mp4")
    process("D:\\video process\\305_cut.mp4")
    process("D:\\video process\\309_cut.mp4")
    process("D:\\video process\\310_cut.mp4")
    process("D:\\video process\\311_cut.mp4")
    process("D:\\video process\\312_cut.mp4")
