
from keras_yolo3.yolo import YOLO, detect_video, detect_webcam
from PIL import Image, ImageFont, ImageDraw
import tensorflow as tf
import numpy as np
import os
import cv2


def detect_object(imageFolder='imagesToDetect/', postfix=""):
    gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)
    session = tf.compat.v1.InteractiveSession(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))

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
    save_img_path = 'boxedImages/'

    #get detection output folder from params
    detect_path = imageFolder

    #make the yolo model
    yolo = YOLO()

    # list for min 
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

    session.close()
    return detections


def crop(boxList, directory='./boxedImages'):
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
                saveDir = './croppedImages'+'/'+str(saveCount)+imgName
                cropped.save(saveDir)
                saveCount += 1


def box(boxList, classes, class_col, indirectory='boxedImages'):
    """
    Updates the detected faces to include coloured boxes for classified faces.
    This also write the label on the image 

    Args:
      Boxlist: list
          A list of all bounding boxes from face detection

      classes: list 
          a list of all classified faces

      Class_col: Dict{string:(r,g,b)}
          A dictionary of {Label: colour} for the class
        
      indirectory: String
          The string of the directory contianing face detected images

    Returns:
    """
    for img in classes:
        imgName = img[0][1:]
        boxNum = int(img[0][0])
        label = img[1]
        for boxes in boxList:
            if boxes[0] == imgName:
                # found image
                box = boxes[1][boxNum]
                left = box[0]
                top = box[1]
                right = box[2]
                bottom = box[3]
                image = cv2.imread(indirectory+'/'+imgName)
                boxed = cv2.rectangle(image, (left, top), (right, bottom), class_col.get(label), 3)
                boxed = cv2.putText(boxed, label, (left, bottom), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                saveDir = indirectory+'/'+imgName
                cv2.imwrite(saveDir, boxed)

