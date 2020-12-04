This folder contians the tools to convert the wider face labels to yolo friendly
box labels:

1) Put images from wider dataset with original names into images folder. 
2) run convert.py
3) converted boxes are stored in 'data_train.txt'

* This will only convert the labels that are in the data set. For example, if
only a subset of the total widerImage dataset is include, only a subset of the 
labels will be generated and stored. 
