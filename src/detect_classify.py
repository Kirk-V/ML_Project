import cv2
import sys

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

def videoToFaces(videoPath, outputPath):
    
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


    framer = FrameExtractor(videoPath, 2)
    framer.store_frames('imagesToDetect')

    # detect faces in imagesToDetect and store in boxedImages
    prediction = detect_object()


    crop(prediction)

    classification = face_recognition()


    classes = filter(classification, celebs)

    #make unique class colours
    class_colours = ((255,0,   0),
                     (0,  255, 0),
                     (0,  0,   255))
    
    #box images
    boxes = box(prediction, classes, class_colours)
    
    fourcc = cv2.VideoWriter_fourcc(*'MPV4') 
    video = cv2.VideoWriter(outputPath, fourcc, 24, (1280, 720))


    for files in os.listdir('./boxedImages/'):
        img = cv2.imread('./boxedImages/'+files)
        video.write(img)

    
    video.release() 
    # for files in glob.glob("./boxedImages/*"):
    #     img = cv2.imread(files)
    #     video.write(img)
    # video.release()
    
    return classes


classes = videoToFaces('./videos/This Is The End - Best Bits_Trim.mp4', "./videos/out.mp4")

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
