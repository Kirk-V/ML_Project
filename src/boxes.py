import cv2
import sys
import os


class BoxMaker:
    """
    A class to create boxes around faces on all images within a directory
    ...

    Attributes
    ----------
    imageDirectory : str
        Where the video is located

    drawBoxes : bool
        set if boxes should be drawn on images

    Methods
    -------
    make_box()
        Makes a directory at passed location

    store_frames(directory='Frames')
        Stores frames from video in the passed directory

    """
    def __init__(self, imageDirectory, drawBoxes=True):
        """
        Parameters
        ----------
        imageDirectory : str
            Where the video is located

        drawBoxes : bool, optional, default=True
            Controls whether the images in folder are drawn over with the green bounding boxes
        """
        self.directory = imageDirectory
        self.drawBoxes = drawBoxes

    def make_box(self):
        """Iterates over every file within a folder and finds the bounding boxes 
        for faces. If a face is found, a box is defined with (x,y,w,h). 
        Optionally, the boxes are drawn on the images.

        """
        dimOut = [] #holder for (x,y,w,h) of each image

        for filename in os.listdir(self.directory):
            frame = cv2.imread(self.directory + '/' + filename)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=3,
                minSize=(30, 30)
            )

            for (x, y, w, h) in faces:
                if (self.drawBoxes):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    status = cv2.imwrite(self.directory + '/' + filename, frame)
                dims = filename + ' ' +str(x)+ ' ' +str(y)+ ' ' +str(w)+ ' ' +str(h)
                dimOut.append(dims)


        #write dimensions of box to txt file
        with open(self.directory + '/locations.txt', 'w') as f:
            for item in dimOut:
                f.write(item + '\n')