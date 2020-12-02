import cv2
import sys

from frame_extractor import FrameExtractor
from boxes import BoxMaker

# useful links 
# Captureing frames from vid: https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1



"""
    This file simply brings other objects in to perform two main steps:
    1) a frame capture on a video file using Frame extractor 
    2) A BoxMaker to put bounding boxes around the faces on the frams from step 1

    The purpose is to show how to gather images from a video and extract faces. 
    This does not include cropping of images. 

    consult classes for more documentation on their procedures

    ***IMPORTANT***
    Running this code will create a directory ./Test to store the frames in. This must not exist before execution

    Should be run from src with 'python face_recog.py'

"""

framer = FrameExtractor('..\\videos\Silicon Valley S02E02.mp4', 9000)
framer.store_frames('Test')
bxmkr = BoxMaker('Test')
bxmkr.make_box()
