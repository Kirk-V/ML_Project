import numpy as np

def filter(classification_data, classesAvailable):
    """
    A function to filter out all the uncessary classification data.  

    Args:
      classification_data: list
          data from the classifier for each face detected

      classesAvailable: [string]
          list of celebs available to classify
          

    Returns:
      classesFound: list
        The classified frame, label, and highest confidence
    """
    classesFound = []
    for image in classification_data:
        name = image[0]
        classes = image[1]
        bestValue = max(classes[0])
        bestIndex = np.argmax(classes[0])
        if (bestValue>.4):
            classesFound.append([name, classesAvailable[bestIndex], bestValue])
    return classesFound