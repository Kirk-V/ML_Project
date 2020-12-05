import numpy as np

def filter(classification_data):
    classesFound = []
    for image in classification_data:
        print(image)
        name = image[0]
        classes = image[1]
        bestValue = max(classes[0])
        bestIndex = np.argmax(classes[0])
        if (bestValue>.4):
            classesFound.append([name, bestIndex, bestValue])
    return classesFound