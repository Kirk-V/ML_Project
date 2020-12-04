
from keras_yolo3.yolo import YOLO, detect_video, detect_webcam
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
import cv2


def detect_object(imageFolder='imagesToDetect/', postfix=""):
    """
    Calls the YOLO face detector on a folder and saves results to detectedImages folder

    Args:
      imageFolder: string
          folder where the images to detect are stored

      postfix: string 
          appends string to filenames
    Returns:
      detections: a list of bounding boxes in format [filename,[(xmin,ymin,xmax,ymax,class_id,confidence]]

    """
    save_img = True #always save the images for now

    #keeping the output folder static for time being
    save_img_path = 'detectedImages/'

    #get detection output folder from params
    detect_path = imageFolder

    #make the yolo model
    yolo = YOLO()

    # list for min 
    # images = []
    detections = []
    
    #iterate over all images in detect folder, try to open image and detect
    for img_path in os.listdir('imagesToDetect'):
      try:
          image = Image.open(detect_path+img_path)
          if image.mode != "RGB":
              image = image.convert("RGB")
          image_array = np.array(image)
      # thrown if file can't be opened, return None if this is the case
      except:
          print("File Open Error! Try again!")
          return None

      # make Prediction using yolo network 
      prediction, new_image = yolo.detect_image(image)

      # add faces detected to be returned
      detections.append([img_path, prediction])

      # save image in output folder
      img_out = postfix.join(os.path.splitext(os.path.basename(img_path)))
      if save_img:
          new_image.save(os.path.join(save_img_path, img_out))

    return detections


def crop(boxList, directory='detectedImages'):
    """
    Crops images within a folder based on the passed list of bounding boxes for
    the faces on each image. 

    Args:
      directory: string
          folder where the images to crop are

      boxList: list 
          2D list of [['imageName', 'minx, miny, maxx, maxy']

    Returns:
    """
    for img in boxList:
        imgName = img[0]
        if len(img[1]) > 0:
            image = Image.open(directory+'/'+imgName)
            saveCount = 0
            for box in img[1]:
                left = box[0]
                top = box[1]
                right = box[2]
                bottom = box[3]
                cropped = image.crop((left, top, right, bottom))
                saveDir = directory+'/'+str(saveCount)+imgName
                cropped.save(saveDir)
                saveCount += 1
        os.remove(directory+'/'+imgName)

