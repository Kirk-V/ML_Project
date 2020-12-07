import cv2
import sys
import random
from frame_extractor import FrameExtractor
from boxes import BoxMaker
from detect import detect_object, crop, box
from classification import face_recognition
from filter_classification import filter
import os
import glob
from pathlib import Path
from shutil import rmtree



""" This file contains the main function to bring together the processing pipeline:"""



#Globals for classes/colours of boxes
celebs = ['Craig Robinson', 'Danny McBride', 'James Franco', 'Jay Baruchel', 
        'Jonah Hill', 'Seth Rogan']


colors = [(255,0,0), (0,255,0),  (0, 0, 255), (255,225,25), (145, 30, 180), 
        (240,50,230), (170, 110, 40)]




def videoToFaces(videoPath, outputPath):
    """
    Given a pathh to a video, the frames are extracted and faces are detected and classified.

    Args:
      videoPath: string
          folder where the video is located

      outputPath: string
          path where detected video can be put

    Returns:
        classes: list
            all the classified frames names and associeted class
        
        returnList: list
            A list of all actors/actresses their label colour on the video
            and the max confidence detected.
    """
    print("Deleting old images")
    

    # Delete old files in image folders
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

    # create dicts for each class
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

    # Extract the frames 
    print("Extracting Frames")
    framer = FrameExtractor(videoPath, 1)
    framer.store_frames('imagesToDetect')

    # detect faces in imagesToDetect and store in boxedImages
    print("Detecting and cropping Faces")    
    prediction = detect_object()
    crop(prediction)

    #classify
    print('Classifying faces')
    classification = face_recognition()


    # Filter out the poor quality classifications
    classes = filter(classification, celebs)
    for classified in classes:
        value = classified[2]
        person = classified[1]
        for i in returnList:
            if i.get('name') == person:
                currentMax = i.get('max')
                if value > currentMax:
                    i.update({'max': value})
         
    # add the classified face boxes
    print('Adding boxes')
    boxes = box(prediction, classes, class_colours)
    
    # Write the classified frames back to a video
    fourcc = cv2.VideoWriter_fourcc(*'MPV4') 
    video = cv2.VideoWriter(outputPath, fourcc, 30, (1280, 720))
    files = os.listdir('./boxedImages/')
    files.sort()
    for f in files:
        img = cv2.imread('./boxedImages/'+f)
        video.write(img)
    video.release() 


    return classes, returnList


classes, returnl = videoToFaces('./videos/This Is The End - Best Bits_Trim.mp4', "./videos/out.mp4")

