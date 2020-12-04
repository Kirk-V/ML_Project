import os
import shutil

# pwd
pwd = os.path.abspath(os.getcwd())
print(pwd)

# rootdir = '../images'
collection = './images'

# labels from widerface
annotations = 'wider_face_train_bbx_gt.txt'

# get image names
imageNames = []
for file in os.listdir(collection):
    imageNames.append(file)

yoloPath = '<pathToYoloTrainData>'
newAnnotations = []  #store the new annotations
# iterate over image names
for image in imageNames:
    #open label file for reading
    fp = open(annotations, 'r')
    # iterate over labels until a match is found for the image name
    for x in fp:
        if image in x:
            numOfBoxes = int(fp.readline()) 
            annotationLine = '' # found match, start new string to add to converted labels file
            for box in range(numOfBoxes):
                dims = fp.readline()
                dims = dims.split()
                x = int(dims[0])
                y = int(dims[1])
                w = int(dims[2])
                h = int(dims[3])
                minx = int(x)
                miny = int(y)
                maxx = int(x+w)
                maxy = int(y+h)
                newdims = ' {x1},{y1},{x2},{y2},0'.format(x1=minx, y1=miny, x2=maxx, y2=maxy)
                annotationLine += newdims
            #add label string to new file
            newAnnotations.append(yoloPath + '/' + image + ' ' +annotationLine)
            break


with open('./data_train.txt', "w") as outfile:
    outfile.write("\n".join(newAnnotations))