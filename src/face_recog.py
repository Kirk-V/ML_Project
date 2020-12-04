import cv2
import sys

from frame_extractor import FrameExtractor
from boxes import BoxMaker
from detect import detect_object, crop





# useful links 
# Captureing frames from vid: https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1

"""
	This file shows the usage of frameExtractor, and detection. 
    This file simply brings other objects in to perform two main steps:
    	1) Frame capture on a video file using Frame extractor 
    	2) Detection of faces within the folder 'imagesToDetect'
    	3) Storage of images with bounding boxes in detectedImages
    	4) Print out the image name followed by the minx, miny, maxx, maxy, class, confidence
    		--the class is always 0 as we are only detecting human faces


    The purpose is to show how to gather images from a video and extract faces. 
    This does not include cropping of images yet. 

    Should be run from src with 'python face_recog.py' for relative imports

"""

# #make frame extractor object
framer = FrameExtractor('../videos/The King of Staten Island.mp4', 5000)

# extract and store frames in imagesToDetect
framer.store_frames('imagesToDetect')

print("video frames stored")

# detect faces in imagesToDetect/
prediction = detect_object()

# show boxes and confidence for each image
print(prediction)

#testing cropper
crop(prediction, './detectedImages',)