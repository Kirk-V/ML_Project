import cv2
import sys
import random

from frame_extractor import FrameExtractor
from boxes import BoxMaker
from detect import detect_object, crop, box
from vgg_face_testing import face_recognition
from filter_classification import filter
import os
import glob
from pathlib import Path
from shutil import rmtree

# useful links 
# Captureing frames from vid: https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1

celebs = ['Craig Robinson', 'Danny McBride', 'Jay Baruchel', 'Jonah Hill', 'Seth Rogan']
colors = [(255,0,0), (0,255,0),  (0, 0, 255), (255,225,25), (145, 30, 180), (240,50,230), (170, 110, 40)]

def videoToFaces(videoPath, outputPath):
    print("Deleting old images")
    
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
    for path in Path('./croppedImages').glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
    for path in Path('./boxedImages').glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
    
    returnList = []
    # Make a new dict of name, colour, maxConf, for each celeb.

    class_colours = {}
    count = 0
    for celeb in celebs:
        r = int(random.random() * 256) 
        g = int(random.random() * 256) 
        b = int(random.random() * 256)
        celebDict = {
            'name': celeb,
            'color': colors[count],
            'max': 0
        }
        count+=1
        class_colours[celeb] = colors[count]
        returnList.append(celebDict)

    print("Extracting Frames")    
    framer = FrameExtractor(videoPath, 1)
    framer.store_frames('imagesToDetect')

    # detect faces in imagesToDetect and store in boxedImages
    print("Detecting and cropping Faces")    
    prediction = detect_object()
    crop(prediction)

    print('Classifying faces')
    classification = face_recognition()



    classes = filter(classification, celebs)
    for classified in classes:
        value = classified[2]
        person = classified[1]
        for i in returnList:
            if i.get('name') == person:
                currentMax = i.get('max')
                if value > currentMax:
                    i.update({'max': value})
         
    print('Adding boxes')
    #box images
    boxes = box(prediction, classes, class_colours)
    
    fourcc = cv2.VideoWriter_fourcc(*'MPV4') 
    video = cv2.VideoWriter(outputPath, fourcc, 30, (1280, 720))


    for files in os.listdir('./boxedImages/'):
        img = cv2.imread('./boxedImages/'+files)
        video.write(img)

    video.release() 
    
    return classes


# classes = videoToFaces('./videos/This Is The End - Best Bits_Trim.mp4', "./videos/out.mp4")

# outputPath = './videos/out.mp4'


# fourcc = cv2.VideoWriter_fourcc(*'MP4V')
# print("here") 

# video = cv2.VideoWriter(outputPath, fourcc, 24, (1280, 720))
# print("here")

# # for files in glob.glob("./boxedImages/*"):
# #     img = cv2.imread(files)
# #     video.write(img)
# # video.release()

# for files in os.listdir('./boxedImages/'):
#     print(files)
#     img = cv2.imread('./boxedImages/'+files)
#     print('files')
#     video.write(img)

# video.release()

#for aclass in classes:
#    print(aclass)
