import cv2
import sys
import os

class FrameExtractor:
    """
    A class used to extract and save the frames from a video
    ...

    Attributes
    ----------
    path : str
        Where the video is located
    rate : int
        The rate at which to capture frames. Will save 1 of every <rate> 
        frames

    Methods
    -------
    make_dir(directory)
        Makes a directory at passed location

    store_frames(directory='Frames')
        Stores frames from video in the passed directory
    """

    def __init__(self, videoPath, rate, showFrames=False):
        """
        Parameters
        ----------
        path : str
            Where the video is located
        rate : int
            The rate at which to capture frames. Will save 1 of every <rate> 
            frames

        showFrames : bool, optional, defaul=False
            Controls whether frames are displayed as they are recorded
                - this will cause a new window to open
        """
        self.path = videoPath
        self.rate = rate
        self.showFrames = showFrames

    def make_dir(self, directory):
        """ Assures the directory passed exists. If not, one is
        created. 

        Parameters
        ----------
        directory : str
            name of the directory to create

        """
        path = directory
        # Make new directory or Empty old one

        if os.path.isdir(path): 
            files_in_dir = os.listdir(path)  # get list of files in the directory
            for file in files_in_dir:        # loop to delete each file in folder
                os.remove(f'{path}/{file}')
        else:
            try:
                os.mkdir(path, 777)
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                print ("Successfully created the directory %s " % path)


    def store_frames(self, directory='imagesToDetect'):
        """ Stores the frames from the video (passed to constructor) at the
        location provided by param: directory

        Parameters
        ----------
        directory : str
            name of the directory to create where frames will be stored

        """
        self.make_dir(directory)
        count = 0
        video = cv2.VideoCapture(self.path)

        if (video.isOpened()== False): 
            print("Error opening video file")
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        while(video.isOpened()):
            ret, frame = video.read()

            if ret:
                if (self.showFrames):
                    cv2.imshow('Frame',frame)

                cv2.imwrite( directory + "/%05dframe.jpg" % count, frame) 
                count += self.rate
                if (count > length):
                    break
                #set the VideoCapture obj to increase by 'count' frames
                video.set(1, count)
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            # Break the loop if no more frames could be retrieved 
            else: 
                break

        video.release()
