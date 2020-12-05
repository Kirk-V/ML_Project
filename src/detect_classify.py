import cv2
import sys

from frame_extractor import FrameExtractor
from boxes import BoxMaker
from detect import detect_object, crop
from vgg_face_testing import face_recognition
from filter_classification import filter
import os
import glob
from pathlib import Path
from shutil import rmtree

# useful links 
# Captureing frames from vid: https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1


def videoToFaces(videoPath):
    for path in Path("./imagesToDetect").glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
    for path in Path('./detectedImages').glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

    framer = FrameExtractor(videoPath, 100)
    framer.store_frames('imagesToDetect')
    # detect faces in imagesToDetect
    prediction = detect_object()
    crop(prediction, './detectedImages')
    classification = face_recognition()
    classes = filter(classification)
    return classes


classes = videoToFaces('./videos/THIS IS THE END - Official Redband Trailer - In Theaters 6_12.mp4')

print(classes)